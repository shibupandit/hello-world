<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class AdminPulse_Settings_Page {
	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'register' ) );
		add_action( 'admin_init', array( __CLASS__, 'register_setting' ) );
		add_action( 'admin_enqueue_scripts', array( __CLASS__, 'assets' ) );
		add_action( 'admin_post_adminpulse_clear_log', array( __CLASS__, 'clear_log' ) );
	}

	public static function register() {
		add_submenu_page( 'options-general.php', 'AdminPulse', 'AdminPulse', 'manage_options', 'adminpulse-settings', array( __CLASS__, 'render' ) );
	}

	public static function register_setting() {
		register_setting( 'adminpulse', AdminPulse_Settings::OPTION, array( 'sanitize_callback' => array( __CLASS__, 'sanitize' ) ) );
	}

	public static function assets( $hook ) {
		if ( false === strpos( $hook, 'adminpulse-settings' ) ) {
			return;
		}
		wp_enqueue_media();
		wp_enqueue_style( 'wp-color-picker' );
		wp_enqueue_script( 'adminpulse-settings', ADMINPULSE_URL . 'assets/settings.js', array( 'jquery', 'jquery-ui-sortable', 'wp-color-picker' ), ADMINPULSE_VERSION, true );
	}

	/** Only the tab being saved is updated; other tabs keep their stored values. */
	public static function sanitize( $in ) {
		$out = AdminPulse_Settings::all();
		$tab = isset( $in['_tab'] ) ? $in['_tab'] : '';
		$hex = function ( $v, $d ) { return sanitize_hex_color( $v ) ?: $d; };

		if ( 'general' === $tab ) {
			$out['accent']          = $hex( $in['accent'] ?? '', '#4f46e5' );
			$out['brand_name']      = sanitize_text_field( $in['brand_name'] ?? '' );
			$out['brand_logo']      = esc_url_raw( $in['brand_logo'] ?? '' );
			$out['footer_text']     = wp_kses_post( $in['footer_text'] ?? '' );
			$out['hide_wp_logo']    = empty( $in['hide_wp_logo'] ) ? 0 : 1;
			$out['hide_wp_version'] = empty( $in['hide_wp_version'] ) ? 0 : 1;
			$out['dashboard_on']    = empty( $in['dashboard_on'] ) ? 0 : 1;
			$out['dark_default']    = in_array( $in['dark_default'] ?? '', array( 'off', 'on', 'auto' ), true ) ? $in['dark_default'] : 'auto';
		} elseif ( 'login' === $tab ) {
			$out['login_on']       = empty( $in['login_on'] ) ? 0 : 1;
			$out['login_bg']       = $hex( $in['login_bg'] ?? '', '#0f172a' );
			$out['login_logo']     = esc_url_raw( $in['login_logo'] ?? '' );
			$out['login_logo_url'] = esc_url_raw( $in['login_logo_url'] ?? '' );
		} elseif ( 'menu' === $tab ) {
			$slugs = isset( $in['menu_order'] ) ? array_map( 'wp_unslash', (array) $in['menu_order'] ) : array();
			$out['menu_order']   = array_values( array_filter( array_map( 'sanitize_text_field', $slugs ) ) );
			$out['menu_hidden']  = array_values( array_map( 'sanitize_text_field', array_map( 'wp_unslash', (array) ( $in['menu_hidden'] ?? array() ) ) ) );
			$ren = array();
			foreach ( (array) ( $in['menu_renamed'] ?? array() ) as $slug => $label ) {
				$label = sanitize_text_field( wp_unslash( $label ) );
				if ( '' !== $label ) {
					$ren[ sanitize_text_field( $slug ) ] = $label;
				}
			}
			$out['menu_renamed'] = $ren;
			if ( ! empty( $in['menu_reset'] ) ) {
				$out['menu_order'] = $out['menu_hidden'] = $out['menu_renamed'] = array();
			}
		} elseif ( 'activity' === $tab ) {
			$out['activity_on']   = empty( $in['activity_on'] ) ? 0 : 1;
			$out['activity_keep'] = max( 1, min( 3650, (int) ( $in['activity_keep'] ?? 90 ) ) );
		}
		return $out;
	}

	public static function clear_log() {
		check_admin_referer( 'adminpulse_clear_log' );
		if ( current_user_can( 'manage_options' ) ) {
			global $wpdb;
			$wpdb->query( 'TRUNCATE TABLE ' . AdminPulse_Activity::table() );
		}
		wp_safe_redirect( admin_url( 'options-general.php?page=adminpulse-settings&tab=activity' ) );
		exit;
	}

	private static function media_field( $name, $value ) {
		printf(
			'<div class="ap-media"><input type="url" class="regular-text" name="%1$s[%2$s]" value="%3$s"> <button type="button" class="button ap-pick">%4$s</button></div>',
			esc_attr( AdminPulse_Settings::OPTION ), esc_attr( $name ), esc_attr( $value ), esc_html__( 'Choose image', 'adminpulse' )
		);
	}

	public static function render() {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$tabs = array(
			'general'  => __( 'General & Branding', 'adminpulse' ),
			'login'    => __( 'Login page', 'adminpulse' ),
			'menu'     => __( 'Menu editor', 'adminpulse' ),
			'activity' => __( 'Activity log', 'adminpulse' ),
		);
		$tab = isset( $_GET['tab'] ) && isset( $tabs[ $_GET['tab'] ] ) ? sanitize_key( $_GET['tab'] ) : 'general'; // phpcs:ignore WordPress.Security.NonceVerification
		$s   = AdminPulse_Settings::all();
		$o   = AdminPulse_Settings::OPTION;
		echo '<div class="wrap"><h1>AdminPulse</h1><nav class="nav-tab-wrapper">';
		foreach ( $tabs as $k => $label ) {
			printf( '<a class="nav-tab %s" href="%s">%s</a>', $k === $tab ? 'nav-tab-active' : '', esc_url( admin_url( 'options-general.php?page=adminpulse-settings&tab=' . $k ) ), esc_html( $label ) );
		}
		echo '</nav>';

		if ( 'activity' === $tab ) {
			self::tab_activity( $s );
			echo '</div>';
			return;
		}

		echo '<form method="post" action="options.php">';
		settings_fields( 'adminpulse' );
		printf( '<input type="hidden" name="%s[_tab]" value="%s">', esc_attr( $o ), esc_attr( $tab ) );
		echo '<table class="form-table" role="presentation">';

		if ( 'general' === $tab ) {
			?>
			<tr><th>Accent colour</th><td><input type="text" class="ap-color" name="<?php echo esc_attr( $o ); ?>[accent]" value="<?php echo esc_attr( $s['accent'] ); ?>"></td></tr>
			<tr><th>Custom dashboard</th><td><label><input type="checkbox" name="<?php echo esc_attr( $o ); ?>[dashboard_on]" value="1" <?php checked( $s['dashboard_on'] ); ?>> Replace the default WordPress dashboard with Pulse</label></td></tr>
			<tr><th>Dark mode default</th><td><select name="<?php echo esc_attr( $o ); ?>[dark_default]">
				<?php foreach ( array( 'auto' => 'Follow system', 'on' => 'Always dark', 'off' => 'Always light' ) as $v => $l ) { printf( '<option value="%s" %s>%s</option>', esc_attr( $v ), selected( $s['dark_default'], $v, false ), esc_html( $l ) ); } ?>
			</select><p class="description">Each user can override this with the toggle in the admin bar.</p></td></tr>
			<tr><th>Brand name</th><td><input type="text" class="regular-text" name="<?php echo esc_attr( $o ); ?>[brand_name]" value="<?php echo esc_attr( $s['brand_name'] ); ?>"><p class="description">Shown in the admin bar, window titles and on the login page.</p></td></tr>
			<tr><th>Brand logo</th><td><?php self::media_field( 'brand_logo', $s['brand_logo'] ); ?></td></tr>
			<tr><th>Footer text</th><td><input type="text" class="large-text" name="<?php echo esc_attr( $o ); ?>[footer_text]" value="<?php echo esc_attr( $s['footer_text'] ); ?>"></td></tr>
			<tr><th>White label</th><td>
				<label><input type="checkbox" name="<?php echo esc_attr( $o ); ?>[hide_wp_logo]" value="1" <?php checked( $s['hide_wp_logo'] ); ?>> Hide the WordPress logo menu</label><br>
				<label><input type="checkbox" name="<?php echo esc_attr( $o ); ?>[hide_wp_version]" value="1" <?php checked( $s['hide_wp_version'] ); ?>> Hide the WordPress version in the footer</label></td></tr>
			<?php
		} elseif ( 'login' === $tab ) {
			?>
			<tr><th>Custom login page</th><td><label><input type="checkbox" name="<?php echo esc_attr( $o ); ?>[login_on]" value="1" <?php checked( $s['login_on'] ); ?>> Enable</label></td></tr>
			<tr><th>Background colour</th><td><input type="text" class="ap-color" name="<?php echo esc_attr( $o ); ?>[login_bg]" value="<?php echo esc_attr( $s['login_bg'] ); ?>"></td></tr>
			<tr><th>Logo</th><td><?php self::media_field( 'login_logo', $s['login_logo'] ); ?></td></tr>
			<tr><th>Logo link</th><td><input type="url" class="regular-text" name="<?php echo esc_attr( $o ); ?>[login_logo_url]" value="<?php echo esc_attr( $s['login_logo_url'] ); ?>" placeholder="<?php echo esc_attr( home_url( '/' ) ); ?>"></td></tr>
			<?php
		} elseif ( 'menu' === $tab ) {
			$items  = AdminPulse_Menu::items();
			$order  = (array) $s['menu_order'];
			usort( $items, function ( $a, $b ) use ( $order ) {
				$ia = array_search( $a['slug'], $order, true );
				$ib = array_search( $b['slug'], $order, true );
				return ( false === $ia ? 999 : $ia ) <=> ( false === $ib ? 999 : $ib );
			} );
			echo '<tr><td colspan="2"><p>Drag to reorder. Untick to hide. Type a new label to rename. Hidden items remain reachable by direct URL; this is cosmetic, not a permissions control.</p><ul id="ap-menu-list">';
			foreach ( $items as $it ) {
				$slug = $it['slug'];
				printf(
					'<li><span class="dashicons dashicons-menu"></span><input type="hidden" name="%1$s[menu_order][]" value="%2$s"><label><input type="checkbox" name="%1$s[menu_hidden][]" value="%2$s" %3$s> %4$s</label><input type="text" name="%1$s[menu_renamed][%2$s]" value="%5$s" placeholder="%6$s"></li>',
					esc_attr( $o ), esc_attr( $slug ), checked( in_array( $slug, (array) $s['menu_hidden'], true ), true, false ),
					esc_html__( 'Hide', 'adminpulse' ), esc_attr( $s['menu_renamed'][ $slug ] ?? '' ), esc_attr( $it['label'] )
				);
			}
			echo '</ul><label><input type="checkbox" name="' . esc_attr( $o ) . '[menu_reset]" value="1"> Reset menu to default on save</label></td></tr>';
		}
		echo '</table>';
		submit_button();
		echo '</form></div>';
	}

	private static function tab_activity( $s ) {
		$o     = AdminPulse_Settings::OPTION;
		$page  = max( 1, (int) ( $_GET['paged'] ?? 1 ) ); // phpcs:ignore WordPress.Security.NonceVerification
		$per   = 30;
		$total = AdminPulse_Activity::count();
		echo '<form method="post" action="options.php" style="margin:16px 0">';
		settings_fields( 'adminpulse' );
		printf( '<input type="hidden" name="%s[_tab]" value="activity">', esc_attr( $o ) );
		printf( '<label><input type="checkbox" name="%s[activity_on]" value="1" %s> Record activity</label> &nbsp; Keep for <input type="number" min="1" style="width:70px" name="%s[activity_keep]" value="%d"> days ', esc_attr( $o ), checked( $s['activity_on'], 1, false ), esc_attr( $o ), (int) $s['activity_keep'] );
		submit_button( 'Save', 'secondary', 'submit', false );
		echo '</form>';
		AdminPulse_Dashboard::activity_table( AdminPulse_Activity::recent( $per, ( $page - 1 ) * $per ) );
		echo '<div class="tablenav"><div class="tablenav-pages">' . wp_kses_post( paginate_links( array(
			'base'    => add_query_arg( 'paged', '%#%' ),
			'format'  => '',
			'current' => $page,
			'total'   => max( 1, (int) ceil( $total / $per ) ),
		) ) ) . '</div></div>';
		if ( $total ) {
			printf( '<form method="post" action="%s" onsubmit="return confirm(\'Delete all log entries?\')">', esc_url( admin_url( 'admin-post.php' ) ) );
			echo '<input type="hidden" name="action" value="adminpulse_clear_log">';
			wp_nonce_field( 'adminpulse_clear_log' );
			submit_button( 'Clear log', 'delete', 'submit', false );
			echo '</form>';
		}
	}
}
