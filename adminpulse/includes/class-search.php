<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Global command-palette search (REST endpoint; UI in assets/admin.js). */
class AdminPulse_Search {
	public static function init() {
		add_action( 'rest_api_init', function () {
			register_rest_route( 'adminpulse/v1', '/search', array(
				'methods'             => 'GET',
				'permission_callback' => function () { return current_user_can( 'edit_posts' ); },
				'args'                => array( 'q' => array( 'type' => 'string', 'required' => true, 'sanitize_callback' => 'sanitize_text_field' ) ),
				'callback'            => array( __CLASS__, 'handle' ),
			) );
		} );
	}

	public static function handle( WP_REST_Request $req ) {
		$q       = trim( $req['q'] );
		$results = array();
		if ( mb_strlen( $q ) < 2 ) {
			return $results;
		}

		// Admin pages.
		global $menu, $submenu;
		foreach ( self::menu_links() as $l ) {
			if ( false !== stripos( $l['title'], $q ) ) {
				$results[] = $l + array( 'type' => 'Page' );
			}
		}

		// Content.
		$posts = get_posts( array(
			's'              => $q,
			'post_type'      => 'any',
			'post_status'    => array( 'publish', 'draft', 'pending', 'future', 'private' ),
			'posts_per_page' => 8,
		) );
		foreach ( $posts as $p ) {
			if ( ! current_user_can( 'edit_post', $p->ID ) ) {
				continue;
			}
			$results[] = array(
				'title' => $p->post_title ?: __( '(no title)', 'adminpulse' ),
				'url'   => get_edit_post_link( $p->ID, 'raw' ),
				'type'  => get_post_type_object( $p->post_type )->labels->singular_name . ' · ' . $p->post_status,
			);
		}

		// Users.
		if ( current_user_can( 'list_users' ) ) {
			foreach ( get_users( array( 'search' => '*' . $q . '*', 'number' => 5, 'search_columns' => array( 'user_login', 'user_email', 'display_name' ) ) ) as $u ) {
				$results[] = array(
					'title' => $u->display_name . ' (' . $u->user_login . ')',
					'url'   => get_edit_user_link( $u->ID, 'raw' ),
					'type'  => 'User',
				);
			}
		}
		return array_slice( $results, 0, 20 );
	}

	private static function menu_links() {
		global $menu, $submenu;
		$links = array();
		foreach ( (array) $menu as $item ) {
			if ( '' === $item[0] || ! current_user_can( $item[1] ) ) {
				continue;
			}
			$label = trim( wp_strip_all_tags( preg_replace( '/<span.*?<\/span>/s', '', $item[0] ) ) );
			$links[] = array( 'title' => $label, 'url' => self::url( $item[2] ) );
			foreach ( (array) ( $submenu[ $item[2] ] ?? array() ) as $sub ) {
				if ( current_user_can( $sub[1] ) ) {
					$links[] = array( 'title' => $label . ' → ' . trim( wp_strip_all_tags( preg_replace( '/<span.*?<\/span>/s', '', $sub[0] ) ) ), 'url' => self::url( $sub[2], $item[2] ) );
				}
			}
		}
		return $links;
	}

	private static function url( $slug, $parent = '' ) {
		if ( preg_match( '/\.php/', $slug ) ) {
			return admin_url( $slug );
		}
		$base = ( $parent && preg_match( '/\.php/', $parent ) ) ? $parent : 'admin.php';
		return admin_url( $base . '?page=' . $slug );
	}
}
