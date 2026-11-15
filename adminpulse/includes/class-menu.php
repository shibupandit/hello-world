<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Admin menu editor: hide, rename, reorder top-level items. */
class AdminPulse_Menu {
	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'apply' ), 9999 );
		add_filter( 'custom_menu_order', '__return_true' );
		add_filter( 'menu_order', array( __CLASS__, 'order' ), 9999 );
	}

	/** Hidden/renamed apply to everyone except when editing settings (so you can't lock yourself out). */
	public static function apply() {
		global $menu;
		if ( ! is_array( $menu ) ) {
			return;
		}
		$hidden  = (array) AdminPulse_Settings::get( 'menu_hidden' );
		$renamed = (array) AdminPulse_Settings::get( 'menu_renamed' );
		foreach ( $menu as $i => $item ) {
			$slug = $item[2];
			if ( 'adminpulse' === $slug || 'adminpulse-settings' === $slug ) {
				continue;
			}
			if ( in_array( $slug, $hidden, true ) ) {
				remove_menu_page( $slug );
				continue;
			}
			if ( ! empty( $renamed[ $slug ] ) ) {
				// Preserve notification bubbles after the label.
				$bubble = preg_match( '/<span class="(?:update|awaiting)-plugins?.*<\/span>/s', $item[0], $m ) ? ' ' . $m[0] : '';
				$menu[ $i ][0] = esc_html( $renamed[ $slug ] ) . $bubble;
			}
		}
	}

	public static function order( $order ) {
		$saved = (array) AdminPulse_Settings::get( 'menu_order' );
		if ( ! $saved ) {
			return $order;
		}
		$known = array_values( array_intersect( $saved, $order ) );
		$rest  = array_values( array_diff( $order, $known ) );
		return array_merge( $known, $rest );
	}

	/** Items for the settings screen (label stripped of markup). */
	public static function items() {
		global $menu;
		$out = array();
		foreach ( (array) $menu as $item ) {
			if ( '' === $item[0] || false !== strpos( (string) $item[4], 'wp-menu-separator' ) ) {
				continue;
			}
			$out[] = array(
				'slug'  => $item[2],
				'label' => trim( wp_strip_all_tags( preg_replace( '/<span.*?<\/span>/s', '', $item[0] ) ) ),
			);
		}
		return $out;
	}
}
