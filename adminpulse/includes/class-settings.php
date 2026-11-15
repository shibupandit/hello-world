<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class AdminPulse_Settings {
	const OPTION = 'adminpulse_settings';

	public static function defaults() {
		return array(
			'accent'          => '#4f46e5',
			'brand_name'      => '',
			'brand_logo'      => '',
			'hide_wp_logo'    => 0,
			'footer_text'     => '',
			'hide_wp_version' => 0,
			'dark_default'    => 'auto', // off|on|auto
			'dashboard_on'    => 1,
			'login_on'        => 0,
			'login_bg'        => '#0f172a',
			'login_logo'      => '',
			'login_logo_url'  => '',
			'menu_hidden'     => array(),
			'menu_renamed'    => array(),
			'menu_order'      => array(),
			'activity_on'     => 1,
			'activity_keep'   => 90,
		);
	}

	public static function all() {
		$saved = get_option( self::OPTION, array() );
		return wp_parse_args( is_array( $saved ) ? $saved : array(), self::defaults() );
	}

	public static function get( $key ) {
		$all = self::all();
		return isset( $all[ $key ] ) ? $all[ $key ] : null;
	}
}
