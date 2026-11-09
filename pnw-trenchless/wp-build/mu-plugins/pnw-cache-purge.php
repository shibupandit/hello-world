<?php
/**
 * Plugin Name: PNW Trenchless – purge page cache on site-wide edits
 * Description: StackCache only purges a post's own URL when it is edited. Website Settings
 *              (ACF options page), testimonials and services appear on many pages, so saving
 *              any of them purges the whole cache and the change shows on every page at once.
 * Version:     1.1.0
 *
 * Source: pnw-trenchless/wp-build/mu-plugins/pnw-cache-purge.php (deployed to wp-content/mu-plugins).
 */

defined( 'ABSPATH' ) || exit;

/**
 * Full purge through StackCache's own purge endpoint (the same request its admin-bar
 * "Purge all" button sends). Runs once, at the end of the request.
 */
function pnw_purge_all_cache() {
	static $done = false;
	if ( $done || ! class_exists( 'WPStackCache', false ) || ! defined( 'WPStackCache::PURGE_URL' ) ) {
		return;
	}
	$done = true;
	$url  = add_query_arg( [ 'q' => 'all', 'iam' => get_current_user() ], WPStackCache::PURGE_URL );
	wp_remote_get( $url, [ 'timeout' => 3, 'redirection' => 0, 'user-agent' => 'StackCache Plugin Purger' ] );
}

add_action(
	'acf/save_post',
	function ( $post_id ) {
		$sitewide = ( 'options' === $post_id || 'option' === $post_id )
			|| ( is_numeric( $post_id ) && in_array( get_post_type( (int) $post_id ), [ 'testimonial', 'service' ], true ) );
		if ( $sitewide ) {
			add_action( 'shutdown', 'pnw_purge_all_cache' );
		}
	},
	20
);

// Testimonials and services that are trashed, restored or deleted also change other pages.
foreach ( [ 'trashed_post', 'untrashed_post', 'deleted_post' ] as $pnw_hook ) {
	add_action(
		$pnw_hook,
		function ( $post_id ) {
			if ( in_array( get_post_type( (int) $post_id ), [ 'testimonial', 'service' ], true ) ) {
				add_action( 'shutdown', 'pnw_purge_all_cache' );
			}
		}
	);
}
