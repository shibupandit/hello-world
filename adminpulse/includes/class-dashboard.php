<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class AdminPulse_Dashboard {
	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'register' ) );
		add_action( 'admin_init', array( __CLASS__, 'redirect' ) );
	}

	public static function register() {
		if ( ! AdminPulse_Settings::get( 'dashboard_on' ) ) {
			return;
		}
		add_menu_page( __( 'Pulse', 'adminpulse' ), __( 'Pulse', 'adminpulse' ), 'read', 'adminpulse', array( __CLASS__, 'render' ), 'dashicons-chart-area', 2 );
	}

	/** Send the default Dashboard screen to ours. */
	public static function redirect() {
		global $pagenow;
		if ( 'index.php' === $pagenow && AdminPulse_Settings::get( 'dashboard_on' ) && ! wp_doing_ajax() && empty( $_GET['adminpulse_skip'] ) ) {
			wp_safe_redirect( admin_url( 'admin.php?page=adminpulse' ) );
			exit;
		}
	}

	private static function counts() {
		$out = array();
		foreach ( array( 'post', 'page' ) as $t ) {
			$c = wp_count_posts( $t );
			$out[ $t ] = array( 'publish' => (int) $c->publish, 'draft' => (int) $c->draft );
		}
		$out['users']    = (int) count_users()['total_users'];
		$out['comments'] = (int) wp_count_comments()->moderated;
		return $out;
	}

	/** Posts published per day for last 14 days. */
	private static function series() {
		global $wpdb;
		$rows = $wpdb->get_results( $wpdb->prepare(
			"SELECT DATE(post_date) d, COUNT(*) n FROM {$wpdb->posts} WHERE post_status='publish' AND post_type IN ('post','page') AND post_date >= %s GROUP BY d",
			gmdate( 'Y-m-d', current_time( 'timestamp' ) - 13 * DAY_IN_SECONDS )
		), OBJECT_K );
		$s = array();
		for ( $i = 13; $i >= 0; $i-- ) {
			$d   = gmdate( 'Y-m-d', current_time( 'timestamp' ) - $i * DAY_IN_SECONDS );
			$s[] = isset( $rows[ $d ] ) ? (int) $rows[ $d ]->n : 0;
		}
		return $s;
	}

	private static function sparkline( $s ) {
		$max = max( 1, max( $s ) );
		$w = 280; $h = 60; $n = count( $s );
		$pts = array();
		foreach ( $s as $i => $v ) {
			$pts[] = round( $i * $w / ( $n - 1 ), 1 ) . ',' . round( $h - 4 - ( $v / $max ) * ( $h - 8 ), 1 );
		}
		$line = implode( ' ', $pts );
		return '<svg viewBox="0 0 ' . $w . ' ' . $h . '" class="ap-spark" preserveAspectRatio="none" role="img" aria-label="' . esc_attr__( 'Content published, last 14 days', 'adminpulse' ) . '"><polygon points="0,' . $h . ' ' . $line . ' ' . $w . ',' . $h . '" class="ap-spark-fill"/><polyline points="' . $line . '" class="ap-spark-line"/></svg>';
	}

	public static function render() {
		$c      = self::counts();
		$series = self::series();
		$user   = wp_get_current_user();
		$recent = get_posts( array( 'numberposts' => 6, 'post_status' => array( 'publish', 'draft', 'pending' ), 'post_type' => array( 'post', 'page' ) ) );
		$h      = (int) current_time( 'G' );
		$greet  = $h < 12 ? __( 'Good morning', 'adminpulse' ) : ( $h < 18 ? __( 'Good afternoon', 'adminpulse' ) : __( 'Good evening', 'adminpulse' ) );
		$upd    = function_exists( 'wp_get_update_data' ) ? wp_get_update_data() : array( 'counts' => array( 'total' => 0 ) );
		?>
		<div class="wrap ap-dash">
			<h1 class="screen-reader-text"><?php esc_html_e( 'Dashboard', 'adminpulse' ); ?></h1>
			<header class="ap-hero">
				<div>
					<h2><?php echo esc_html( $greet . ', ' . $user->display_name ); ?> 👋</h2>
					<p><?php echo esc_html( sprintf( /* translators: %s site name */ __( 'Here is what is happening on %s.', 'adminpulse' ), get_bloginfo( 'name' ) ) ); ?></p>
				</div>
				<div class="ap-actions">
					<?php if ( current_user_can( 'edit_posts' ) ) : ?><a class="button button-primary" href="<?php echo esc_url( admin_url( 'post-new.php' ) ); ?>"><?php esc_html_e( 'New post', 'adminpulse' ); ?></a><?php endif; ?>
					<?php if ( current_user_can( 'edit_pages' ) ) : ?><a class="button" href="<?php echo esc_url( admin_url( 'post-new.php?post_type=page' ) ); ?>"><?php esc_html_e( 'New page', 'adminpulse' ); ?></a><?php endif; ?>
					<a class="button" href="<?php echo esc_url( home_url( '/' ) ); ?>" target="_blank" rel="noopener"><?php esc_html_e( 'View site', 'adminpulse' ); ?></a>
				</div>
			</header>

			<div class="ap-grid ap-stats">
				<?php
				$cards = array(
					array( __( 'Posts', 'adminpulse' ), $c['post']['publish'], sprintf( _n( '%d draft', '%d drafts', $c['post']['draft'], 'adminpulse' ), $c['post']['draft'] ), admin_url( 'edit.php' ) ),
					array( __( 'Pages', 'adminpulse' ), $c['page']['publish'], sprintf( _n( '%d draft', '%d drafts', $c['page']['draft'], 'adminpulse' ), $c['page']['draft'] ), admin_url( 'edit.php?post_type=page' ) ),
					array( __( 'Users', 'adminpulse' ), $c['users'], '', admin_url( 'users.php' ) ),
					array( __( 'Pending comments', 'adminpulse' ), $c['comments'], '', admin_url( 'edit-comments.php?comment_status=moderated' ) ),
					array( __( 'Updates', 'adminpulse' ), (int) $upd['counts']['total'], '', admin_url( 'update-core.php' ) ),
				);
				foreach ( $cards as $card ) {
					printf( '<a class="ap-card ap-stat" href="%s"><span class="ap-label">%s</span><strong>%s</strong><em>%s</em></a>', esc_url( $card[3] ), esc_html( $card[0] ), esc_html( number_format_i18n( $card[1] ) ), esc_html( $card[2] ) );
				}
				?>
			</div>

			<div class="ap-grid ap-two">
				<section class="ap-card">
					<h3><?php esc_html_e( 'Publishing — last 14 days', 'adminpulse' ); ?></h3>
					<?php echo self::sparkline( $series ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
					<p class="ap-muted"><?php echo esc_html( sprintf( _n( '%d item published', '%d items published', array_sum( $series ), 'adminpulse' ), array_sum( $series ) ) ); ?></p>
				</section>
				<section class="ap-card">
					<h3><?php esc_html_e( 'Recent content', 'adminpulse' ); ?></h3>
					<ul class="ap-list">
						<?php foreach ( $recent as $p ) : ?>
							<li><a href="<?php echo esc_url( get_edit_post_link( $p->ID ) ); ?>"><?php echo esc_html( $p->post_title ?: __( '(no title)', 'adminpulse' ) ); ?></a>
							<span class="ap-pill ap-<?php echo esc_attr( $p->post_status ); ?>"><?php echo esc_html( $p->post_status ); ?></span></li>
						<?php endforeach; ?>
						<?php if ( ! $recent ) : ?><li class="ap-muted"><?php esc_html_e( 'Nothing yet.', 'adminpulse' ); ?></li><?php endif; ?>
					</ul>
				</section>
			</div>

			<?php if ( current_user_can( 'manage_options' ) && AdminPulse_Settings::get( 'activity_on' ) ) : ?>
			<section class="ap-card">
				<h3><?php esc_html_e( 'Recent activity', 'adminpulse' ); ?> <a class="ap-more" href="<?php echo esc_url( admin_url( 'admin.php?page=adminpulse-settings&tab=activity' ) ); ?>"><?php esc_html_e( 'View all', 'adminpulse' ); ?></a></h3>
				<?php self::activity_table( AdminPulse_Activity::recent( 8 ) ); ?>
			</section>
			<?php endif; ?>

			<p class="ap-muted"><a href="<?php echo esc_url( admin_url( 'index.php?adminpulse_skip=1' ) ); ?>"><?php esc_html_e( 'Open classic WordPress dashboard', 'adminpulse' ); ?></a></p>
		</div>
		<?php
	}

	public static function activity_table( $rows ) {
		if ( ! $rows ) {
			echo '<p class="ap-muted">' . esc_html__( 'No activity recorded yet.', 'adminpulse' ) . '</p>';
			return;
		}
		echo '<table class="widefat striped ap-table"><thead><tr><th>' . esc_html__( 'When', 'adminpulse' ) . '</th><th>' . esc_html__( 'User', 'adminpulse' ) . '</th><th>' . esc_html__( 'Action', 'adminpulse' ) . '</th><th>' . esc_html__( 'Detail', 'adminpulse' ) . '</th><th>IP</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			$u = $r->user_id ? get_userdata( $r->user_id ) : false;
			printf(
				'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>',
				esc_html( human_time_diff( strtotime( $r->created ), current_time( 'timestamp' ) ) . ' ' . __( 'ago', 'adminpulse' ) ),
				esc_html( $u ? $u->display_name : '—' ),
				esc_html( str_replace( '_', ' ', $r->action ) . ' ' . $r->object_type ),
				esc_html( $r->detail ),
				esc_html( $r->ip )
			);
		}
		echo '</tbody></table>';
	}
}
