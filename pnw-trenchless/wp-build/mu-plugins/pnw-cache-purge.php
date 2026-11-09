<?php
/**
 * Plugin Name: PNW Trenchless – purge page cache on site-wide edits
 * Description: StackCache only purges a post's own URL when it is edited. Website Settings
 *              (ACF options page) and testimonials appear on many pages, so saving either
 *              purges the whole cache, so the change shows up on every page straight away.
 * Version:     1.0.0
 *
 * Source: pnw-trenchless/wp-build/mu-plugins/pnw-cache-purge.php (deployed to wp-content/mu-plugins).
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'acf/save_post',
	function ( $post_id ) {
		$sitewide = ( 'options' === $post_id || 'option' === $post_id )
			|| ( is_numeric( $post_id ) && in_array( get_post_type( (int) $post_id ), [ 'testimonial', 'service' ], true ) );
		if ( ! $sitewide ) {
			return;
		}
		// StackCache hooks its "purge everything" routine to this action.
		do_action( 'autoptimize_action_cachepurged' );
	},
	20
);
