<?php
/**
 * Plugin Name: PNW Trenchless – revision cap
 * Description: Keeps at most 2 revisions per page/post/template, so the database stays light (user, 2026-11-10).
 */
defined( 'ABSPATH' ) || exit;

add_filter( 'wp_revisions_to_keep', static function () {
	return 2;
}, 99 );
