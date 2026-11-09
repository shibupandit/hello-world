<?php
/**
 * PNW Trenchless: sync wp-build/classes.json + elements.json into the Bricks site.
 * Run through Novamira execute-php with $sha set to a pushed commit. Uses only the
 * Novamira Bricks abilities (create/edit/delete global class, create-template,
 * set-content, insert-content), never raw option writes.
 */
$sha  = $sha ?? get_option( 'pnw_build_sha' );
$base = "https://raw.githubusercontent.com/shibupandit/hello-world/$sha/pnw-trenchless/wp-build/";
$get  = function ( $f ) use ( $base ) {
	return json_decode( wp_remote_retrieve_body( wp_remote_get( $base . $f, [ 'timeout' => 30 ] ) ), true );
};
$classes = $get( 'classes.json' );
$els     = $get( 'elements.json' );
if ( ! $classes || ! $els ) {
	return 'fetch fail';
}
update_option( 'pnw_build_sha', $sha, false );
$out = [];

// 1. Classes: create / update, then delete PNW classes no longer in the generator.
$create = wp_get_ability( 'novamira/bricks-create-global-class' );
$edit   = wp_get_ability( 'novamira/bricks-edit-global-class' );
$del    = wp_get_ability( 'novamira/bricks-delete-global-class' );
$ex     = [];
foreach ( (array) get_option( 'bricks_global_classes', [] ) as $c ) {
	$ex[ $c['name'] ] = $c;
}
$want_names = [];
$made = $upd = 0;
foreach ( $classes as $x ) {
	$want_names[] = $x['name'];
	$s = [ '_cssCustom' => $x['css'] ];
	if ( isset( $ex[ $x['name'] ] ) ) {
		$cur = $ex[ $x['name'] ];
		if ( 0 === strpos( $cur['id'], 'acss_' ) ) {
			continue;
		}
		if ( ( $cur['settings']['_cssCustom'] ?? '' ) === str_replace( '%root%', '.' . $x['name'], $x['css'] ) ) {
			continue;
		}
		$edit->execute( [ 'id' => $cur['id'], 'settings' => $s, 'replace' => true ] );
		$upd++;
	} else {
		$create->execute( [ 'name' => $x['name'], 'category' => 'PNW', 'settings' => $s ] );
		$made++;
	}
}
$pnw_cat = null;
foreach ( (array) get_option( 'bricks_global_classes_categories', [] ) as $cat ) {
	if ( 'PNW' === $cat['name'] ) {
		$pnw_cat = $cat['id'];
	}
}
$removed = [];
foreach ( $ex as $name => $c ) {
	if ( $pnw_cat && ( $c['category'] ?? '' ) === $pnw_cat && ! in_array( $name, $want_names, true ) ) {
		$r = $del->execute( [ 'id' => $c['id'] ] );
		$removed[] = $name . ( is_wp_error( $r ) ? ' (error: ' . $r->get_error_message() . ')' : '' );
	}
}
$out['classes'] = [ 'created' => $made, 'updated' => $upd, 'removed' => $removed ];

// 2. Resolve class names and media placeholders.
$cmap = [];
foreach ( (array) get_option( 'bricks_global_classes', [] ) as $c ) {
	$cmap[ $c['name'] ] = $c['id'];
}
$media = [];
foreach ( get_option( 'pnw_media_ids' ) as $k => $id ) {
	$media[ $k ] = [ 'id' => $id, 'url' => wp_get_attachment_url( $id ) ];
}
$missing = [];
$resolve = function ( $v ) use ( &$resolve, $cmap, $media, &$missing ) {
	if ( ! is_array( $v ) ) {
		return $v;
	}
	if ( isset( $v['__media'] ) ) {
		$m = $media[ $v['__media'] ] ?? null;
		if ( ! $m ) {
			$missing[] = $v['__media'];
		}
		$o = $v;
		unset( $o['__media'] );
		return array_merge( (array) $m, $o );
	}
	$o = [];
	foreach ( $v as $k => $x ) {
		if ( '_cls' === $k ) {
			$ids = [];
			foreach ( $x as $n ) {
				if ( isset( $cmap[ $n ] ) ) {
					$ids[] = $cmap[ $n ];
				} else {
					$missing[] = 'class:' . $n;
				}
			}
			if ( $ids ) {
				$o['_cssGlobalClasses'] = $ids;
			}
			continue;
		}
		$o[ $k ] = $resolve( $x );
	}
	return $o;
};
// Empty settings must be an array: Bricks crashes on stdClass settings.
$prep = function ( $list ) use ( $resolve ) {
	return array_map( function ( $e ) use ( $resolve ) {
		$e['settings'] = $resolve( $e['settings'] ) ?: [];
		return $e;
	}, $list );
};

// 3. Header / footer templates.
$set  = wp_get_ability( 'novamira/bricks-set-content' );
$ins  = wp_get_ability( 'novamira/bricks-insert-content' );
$tpls = get_option( 'pnw_template_ids', [] );
foreach ( [ 'header', 'footer' ] as $area ) {
	$r = $set->execute( [ 'post_id' => (int) $tpls[ $area ], 'area' => $area, 'elements' => $prep( $els[ $area ] ) ] );
	$out[ $area ] = is_wp_error( $r ) ? $r->get_error_message() : ( $r['verified'] ? 'ok' : 'mismatch' );
}

// 4. Home page, one insert per section.
$post = (int) get_option( 'page_on_front' );
$set->execute( [ 'post_id' => $post, 'area' => 'content', 'elements' => [] ] );
foreach ( $els['sections'] as $s ) {
	$r = $ins->execute( [ 'post_id' => $post, 'area' => 'content', 'elements' => $prep( $s['elements'] ) ] );
	$out['page'][ $s['key'] ] = is_wp_error( $r ) ? $r->get_error_message() : ( $r['verified'] ? 'ok' : 'mismatch' );
}

// 4b. Other pages (e.g. service posts), found or created by slug + post type.
$out['pages'] = [];
foreach ( (array) ( $els['pages'] ?? [] ) as $pg ) {
	$p = get_page_by_path( $pg['slug'], OBJECT, $pg['post_type'] );
	$pid = $p ? (int) $p->ID : (int) wp_insert_post( [
		'post_type'   => $pg['post_type'],
		'post_title'  => $pg['title'],
		'post_name'   => $pg['slug'],
		'post_status' => 'publish',
		'post_excerpt' => $pg['excerpt'] ?? '',
	] );
	if ( $p && isset( $pg['excerpt'] ) ) {
		wp_update_post( [ 'ID' => $pid, 'post_excerpt' => $pg['excerpt'], 'post_title' => $pg['title'] ] );
	}
	update_post_meta( $pid, '_bricks_editor_mode', 'bricks' );
	$set->execute( [ 'post_id' => $pid, 'area' => 'content', 'elements' => [] ] );
	$res = [ 'id' => $pid ];
	foreach ( $pg['sections'] as $s ) {
		$r = $ins->execute( [ 'post_id' => $pid, 'area' => 'content', 'elements' => $prep( $s['elements'] ) ] );
		$res[ $s['key'] ] = is_wp_error( $r ) ? $r->get_error_message() : ( $r['verified'] ? 'ok' : 'mismatch' );
	}
	$res['url'] = get_permalink( $pid );
	$out['pages'][ $pg['key'] ] = $res;
}
if ( ! empty( $els['pages'] ) ) {
	flush_rewrite_rules( false );
}

// 5. In-process render test.
$test = function ( $elements ) {
	try {
		ob_start();
		$h = \Bricks\Frontend::render_data( $elements );
		ob_end_clean();
		return 'ok ' . strlen( (string) $h );
	} catch ( \Throwable $e ) {
		ob_end_clean();
		return $e->getMessage();
	}
};
$out['render'] = [
	'header' => $test( get_post_meta( (int) $tpls['header'], BRICKS_DB_PAGE_HEADER, true ) ),
	'footer' => $test( get_post_meta( (int) $tpls['footer'], BRICKS_DB_PAGE_FOOTER, true ) ),
	'page'   => $test( get_post_meta( $post, BRICKS_DB_PAGE_CONTENT, true ) ),
];
foreach ( $out['pages'] as $k => $res ) {
	$out['render'][ $k ] = $test( get_post_meta( $res['id'], BRICKS_DB_PAGE_CONTENT, true ) );
}
$out['missing'] = array_values( array_unique( $missing ) );
return $out;
