<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Global admin styling, dark mode, white-label branding. */
class AdminPulse_Theme {
	public static function init() {
		add_action( 'admin_enqueue_scripts', array( __CLASS__, 'enqueue' ) );
		add_action( 'admin_head', array( __CLASS__, 'inline_vars' ), 1 );
		add_filter( 'admin_body_class', array( __CLASS__, 'body_class' ) );
		add_filter( 'admin_footer_text', array( __CLASS__, 'footer_text' ) );
		add_filter( 'update_footer', array( __CLASS__, 'hide_version' ), 99 );
		add_action( 'admin_bar_menu', array( __CLASS__, 'admin_bar' ), 1 );
		add_action( 'admin_bar_menu', array( __CLASS__, 'dark_toggle' ), 100 );
		add_action( 'wp_ajax_adminpulse_dark', array( __CLASS__, 'ajax_dark' ) );
		add_filter( 'admin_title', array( __CLASS__, 'admin_title' ) );
	}

	/** Returns 'on', 'off' or 'auto' for the current user. */
	public static function mode() {
		$m = get_user_meta( get_current_user_id(), 'adminpulse_dark', true );
		return in_array( $m, array( 'on', 'off', 'auto' ), true ) ? $m : AdminPulse_Settings::get( 'dark_default' );
	}

	public static function enqueue() {
		wp_enqueue_style( 'adminpulse', ADMINPULSE_URL . 'assets/admin.css', array(), ADMINPULSE_VERSION );
		wp_enqueue_script( 'adminpulse', ADMINPULSE_URL . 'assets/admin.js', array(), ADMINPULSE_VERSION, true );
		wp_localize_script( 'adminpulse', 'AdminPulse', array(
			'ajax'      => admin_url( 'admin-ajax.php' ),
			'nonce'     => wp_create_nonce( 'adminpulse' ),
			'rest'      => esc_url_raw( rest_url( 'adminpulse/v1/' ) ),
			'restNonce' => wp_create_nonce( 'wp_rest' ),
			'mode'      => self::mode(),
			'i18n'      => array(
				'placeholder' => __( 'Search posts, users, admin pages…', 'adminpulse' ),
				'none'        => __( 'No results', 'adminpulse' ),
			),
		) );
	}

	public static function inline_vars() {
		$accent = sanitize_hex_color( AdminPulse_Settings::get( 'accent' ) ) ?: '#4f46e5';
		echo '<style id="adminpulse-vars">:root{--ap-accent:' . esc_html( $accent ) . ';}</style>';
		// Prevent flash of light theme: resolve mode before paint.
		echo '<script>(function(){var m="' . esc_js( self::mode() ) . '",d=m==="on"||(m==="auto"&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches);document.documentElement.classList.toggle("ap-dark",d);})();</script>';
	}

	public static function body_class( $classes ) {
		return $classes . ' adminpulse';
	}

	public static function admin_bar( $bar ) {
		if ( AdminPulse_Settings::get( 'hide_wp_logo' ) ) {
			$bar->remove_node( 'wp-logo' );
		}
		$name = AdminPulse_Settings::get( 'brand_name' );
		$logo = AdminPulse_Settings::get( 'brand_logo' );
		if ( $name || $logo ) {
			$html = $logo ? '<img src="' . esc_url( $logo ) . '" alt="" style="height:20px;vertical-align:middle;margin-right:6px">' : '';
			$bar->add_node( array(
				'id'    => 'adminpulse-brand',
				'title' => $html . esc_html( $name ),
				'href'  => admin_url(),
			) );
		}
	}

	public static function dark_toggle( $bar ) {
		$bar->add_node( array(
			'id'     => 'adminpulse-dark',
			'parent' => 'top-secondary',
			'title'  => '<span class="ab-icon dashicons dashicons-admin-appearance" style="margin-top:2px"></span><span class="screen-reader-text">' . esc_html__( 'Toggle dark mode', 'adminpulse' ) . '</span>',
			'href'   => '#',
			'meta'   => array( 'title' => __( 'Toggle dark mode', 'adminpulse' ), 'class' => 'adminpulse-dark-toggle' ),
		) );
		$bar->add_node( array(
			'id'     => 'adminpulse-search',
			'parent' => 'top-secondary',
			'title'  => '<span class="ab-icon dashicons dashicons-search" style="margin-top:2px"></span><span class="screen-reader-text">' . esc_html__( 'Search', 'adminpulse' ) . '</span>',
			'href'   => '#',
			'meta'   => array( 'title' => __( 'Search (Ctrl/Cmd+K)', 'adminpulse' ), 'class' => 'adminpulse-search-open' ),
		) );
	}

	public static function ajax_dark() {
		check_ajax_referer( 'adminpulse', 'nonce' );
		$m = isset( $_POST['mode'] ) ? sanitize_key( wp_unslash( $_POST['mode'] ) ) : 'auto';
		if ( in_array( $m, array( 'on', 'off', 'auto' ), true ) ) {
			update_user_meta( get_current_user_id(), 'adminpulse_dark', $m );
			wp_send_json_success();
		}
		wp_send_json_error();
	}

	public static function footer_text( $text ) {
		$custom = AdminPulse_Settings::get( 'footer_text' );
		return '' !== $custom ? wp_kses_post( $custom ) : $text;
	}

	public static function hide_version( $text ) {
		return AdminPulse_Settings::get( 'hide_wp_version' ) ? '' : $text;
	}

	public static function admin_title( $title ) {
		$name = AdminPulse_Settings::get( 'brand_name' );
		return $name ? str_replace( 'WordPress', $name, $title ) : $title;
	}
}
