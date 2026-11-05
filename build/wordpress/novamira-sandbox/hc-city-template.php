<?php
/**
 * Hartwell & Crane: one Bricks template ("Areas We Serve Single") for every city page (post type cities, /dallas/)
 * and every city service page (post types city-<slug>, /dallas/truck-accidents/).
 *
 * Dynamic tags (group "Hartwell & Crane"): {hc_city_name} {hc_city_url} {hc_heading} {hc_lede} {hc_intro}
 * {hc_breadcrumb} {hc_services_heading} {hc_why_heading}
 * Query loops: the elements listed in the option hc_city_tpl_loops are pointed at this city's
 * service pages ("services") and at the other cities ("cities").
 * The template conditions are kept in sync with all city-* post types automatically.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function hc_city_of( $post = null ) {
	$post = $post ? get_post( $post ) : get_queried_object();
	if ( ! $post instanceof WP_Post ) {
		return null;
	}
	if ( $post->post_type === 'cities' ) {
		return $post;
	}
	if ( strpos( $post->post_type, 'city-' ) === 0 ) {
		return get_page_by_path( substr( $post->post_type, 5 ), OBJECT, 'cities' );
	}
	return null;
}

function hc_city_tag( $name ) {
	$post = get_queried_object();
	if ( ! $post instanceof WP_Post ) {
		return '';
	}
	$city    = hc_city_of( $post );
	$c       = $city ? $city->post_title : '';
	$is_svc  = $city && $post->ID !== $city->ID;
	$service = $is_svc ? $post->post_title : '';
	switch ( $name ) {
		case 'hc_city_name':
			return esc_html( $c );
		case 'hc_city_url':
			return $city ? get_permalink( $city ) : '';
		case 'hc_heading':
			return esc_html( $is_svc ? $service . ' Lawyer in ' . $c : $c . ' Trial Lawyers' );
		case 'hc_lede':
			return esc_html( $is_svc
				? 'Hurt, wronged or facing charges in ' . $c . '? Our ' . strtolower( $service ) . ' attorneys prepare every case for trial, and your first consultation is free.'
				: 'Hartwell & Crane represents people, families and businesses across ' . $c . ' and the surrounding area. A partner leads every case, and your first consultation is free.' );
		case 'hc_services_heading':
			return esc_html( $is_svc ? 'More practice areas in ' . $c : 'How we help clients in ' . $c );
		case 'hc_why_heading':
			return esc_html( 'Why ' . $c . ' clients choose Hartwell & Crane' );
		case 'hc_intro':
			$content = trim( $post->post_content );
			if ( $content !== '' ) {
				return apply_filters( 'the_content', $content );
			}
			if ( $is_svc ) {
				return '<p class="prose__lead">' . esc_html( $service ) . ' cases move fast, and the other side starts building its defense right away. Our ' . esc_html( $c ) . ' team moves faster.</p>'
					. '<p>Hartwell &amp; Crane has represented clients in ' . esc_html( $c ) . ' for more than three decades. A named partner leads every matter, we investigate before evidence disappears, and we prepare every case as if a jury will decide it. That preparation is what produces fair results.</p>'
					. '<p>Tell us what happened. We will review your situation for free and explain your options in plain English.</p>';
			}
			return '<p class="prose__lead">From our Texas offices, Hartwell &amp; Crane serves clients throughout ' . esc_html( $c ) . ' and the surrounding communities.</p>'
				. '<p>Whether you were injured, treated unfairly at work, are facing a family law matter or have been charged with a crime, a partner will review your case personally. We meet in person, by phone or by video, whichever is easier for you.</p>'
				. '<p>Explore the practice areas below, or request a free case review and we will respond within one business day.</p>';
		case 'hc_breadcrumb':
			$items = '<li><a href="' . esc_url( home_url( '/' ) ) . '">Home</a></li><li>Areas We Serve</li>';
			if ( $is_svc ) {
				$items .= '<li><a href="' . esc_url( get_permalink( $city ) ) . '">' . esc_html( $c ) . '</a></li><li aria-current="page">' . esc_html( $service ) . '</li>';
			} else {
				$items .= '<li aria-current="page">' . esc_html( $c ) . '</li>';
			}
			return '<ol role="list">' . $items . '</ol>';
	}
	return '';
}

function hc_city_tag_names() {
	return array( 'hc_city_name', 'hc_city_url', 'hc_heading', 'hc_lede', 'hc_intro', 'hc_breadcrumb', 'hc_services_heading', 'hc_why_heading' );
}

add_filter( 'bricks/dynamic_tags_list', function ( $tags ) {
	foreach ( hc_city_tag_names() as $n ) {
		$tags[] = array( 'name' => '{' . $n . '}', 'label' => $n, 'group' => 'Hartwell & Crane' );
	}
	return $tags;
} );

add_filter( 'bricks/dynamic_data/render_tag', function ( $tag, $post, $context = 'text' ) {
	if ( ! is_string( $tag ) ) {
		return $tag;
	}
	$clean = trim( $tag, '{}' );
	return in_array( $clean, hc_city_tag_names(), true ) ? hc_city_tag( $clean ) : $tag;
}, 20, 3 );

$hc_city_render_content = function ( $content ) {
	if ( ! is_string( $content ) || strpos( $content, '{hc_' ) === false ) {
		return $content;
	}
	foreach ( hc_city_tag_names() as $n ) {
		if ( strpos( $content, '{' . $n . '}' ) !== false ) {
			$content = str_replace( '{' . $n . '}', hc_city_tag( $n ), $content );
		}
	}
	return $content;
};
add_filter( 'bricks/dynamic_data/render_content', $hc_city_render_content, 20 );
add_filter( 'bricks/frontend/render_data', $hc_city_render_content, 20 );

add_filter( 'bricks/posts/query_vars', function ( $vars, $settings, $element_id ) {
	$loops = get_option( 'hc_city_tpl_loops', array() );
	if ( empty( $loops ) || ! in_array( $element_id, $loops, true ) ) {
		return $vars;
	}
	$current = get_queried_object();
	$city    = hc_city_of( $current );
	if ( ! $city ) {
		return $vars;
	}
	if ( $element_id === ( $loops['services'] ?? '' ) ) {
		$vars['post_type']      = array( 'city-' . $city->post_name );
		$vars['posts_per_page'] = 12;
		$vars['orderby']        = 'menu_order';
		$vars['order']          = 'ASC';
		$vars['post__not_in']   = array( (int) $current->ID );
	}
	// Sidebar "Recent in {city}": latest pages of the same city (max 5), current page excluded.
	if ( $element_id === ( $loops['recent'] ?? '' ) ) {
		$vars['post_type']           = array( 'city-' . $city->post_name );
		$vars['posts_per_page']      = 5;
		$vars['orderby']             = 'date';
		$vars['order']               = 'DESC';
		$vars['ignore_sticky_posts'] = true;
		$vars['no_found_rows']       = true;
		$vars['post__not_in']        = array( (int) $current->ID );
	}
	if ( $element_id === ( $loops['cities'] ?? '' ) ) {
		$vars['post_type']      = array( 'cities' );
		$vars['posts_per_page'] = -1;
		$vars['orderby']        = 'menu_order';
		$vars['order']          = 'ASC';
		$vars['post__not_in']   = array( (int) $city->ID );
	}
	return $vars;
}, 20, 3 );

// Keep the template assigned to every city post type (new cities included).
add_action( 'admin_init', function () {
	$tid = (int) get_option( 'hc_city_tpl_id' );
	if ( ! $tid || ! defined( 'BRICKS_DB_TEMPLATE_SETTINGS' ) ) {
		return;
	}
	$types = array_values( array_filter( array_keys( get_post_types() ), function ( $t ) {
		return $t === 'cities' || strpos( $t, 'city-' ) === 0;
	} ) );
	sort( $types );
	$s   = get_post_meta( $tid, BRICKS_DB_TEMPLATE_SETTINGS, true );
	$cur = $s['templateConditions'][0]['postType'] ?? array();
	sort( $cur );
	if ( $cur !== $types ) {
		$s['templateConditions'] = array( array( 'id' => 'hccity', 'main' => 'postType', 'postType' => $types ) );
		update_post_meta( $tid, BRICKS_DB_TEMPLATE_SETTINGS, $s );
	}
} );