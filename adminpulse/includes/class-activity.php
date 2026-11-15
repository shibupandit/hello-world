<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class AdminPulse_Activity {
	public static function table() {
		global $wpdb;
		return $wpdb->prefix . 'adminpulse_activity';
	}

	public static function install() {
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		$charset = $wpdb->get_charset_collate();
		dbDelta( 'CREATE TABLE ' . self::table() . " (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			created DATETIME NOT NULL,
			user_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			action VARCHAR(40) NOT NULL,
			object_type VARCHAR(40) NOT NULL DEFAULT '',
			object_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			detail VARCHAR(255) NOT NULL DEFAULT '',
			ip VARCHAR(45) NOT NULL DEFAULT '',
			PRIMARY KEY  (id),
			KEY created (created)
		) $charset;" );
		if ( ! wp_next_scheduled( 'adminpulse_prune' ) ) {
			wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'adminpulse_prune' );
		}
	}

	public static function init() {
		add_action( 'adminpulse_prune', array( __CLASS__, 'prune' ) );
		if ( ! AdminPulse_Settings::get( 'activity_on' ) ) {
			return;
		}
		add_action( 'save_post', function ( $id, $post, $update ) {
			if ( wp_is_post_revision( $id ) || wp_is_post_autosave( $id ) || 'auto-draft' === $post->post_status ) {
				return;
			}
			self::log( $update ? 'updated' : 'created', $post->post_type, $id, $post->post_title );
		}, 10, 3 );
		add_action( 'before_delete_post', function ( $id ) {
			$p = get_post( $id );
			if ( $p && 'revision' !== $p->post_type ) {
				self::log( 'deleted', $p->post_type, $id, $p->post_title );
			}
		} );
		add_action( 'wp_login', function ( $login, $user ) {
			self::log( 'login', 'user', $user->ID, $login, $user->ID );
		}, 10, 2 );
		add_action( 'wp_login_failed', function ( $login ) {
			self::log( 'login_failed', 'user', 0, $login, 0 );
		} );
		add_action( 'user_register', function ( $id ) {
			self::log( 'created', 'user', $id, (string) get_userdata( $id )->user_login );
		} );
		add_action( 'delete_user', function ( $id ) {
			$u = get_userdata( $id );
			self::log( 'deleted', 'user', $id, $u ? $u->user_login : '' );
		} );
		add_action( 'activated_plugin', function ( $p ) { self::log( 'activated', 'plugin', 0, $p ); } );
		add_action( 'deactivated_plugin', function ( $p ) { self::log( 'deactivated', 'plugin', 0, $p ); } );
		add_action( 'switch_theme', function ( $name ) { self::log( 'switched', 'theme', 0, $name ); } );
	}

	public static function log( $action, $type, $object_id, $detail = '', $user_id = null ) {
		global $wpdb;
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
		$wpdb->insert( self::table(), array(
			'created'     => current_time( 'mysql' ),
			'user_id'     => null === $user_id ? get_current_user_id() : (int) $user_id,
			'action'      => substr( $action, 0, 40 ),
			'object_type' => substr( $type, 0, 40 ),
			'object_id'   => (int) $object_id,
			'detail'      => mb_substr( wp_strip_all_tags( (string) $detail ), 0, 255 ),
			'ip'          => substr( $ip, 0, 45 ),
		) );
	}

	public static function recent( $limit = 20, $offset = 0 ) {
		global $wpdb;
		return $wpdb->get_results( $wpdb->prepare(
			'SELECT * FROM ' . self::table() . ' ORDER BY id DESC LIMIT %d OFFSET %d',
			$limit,
			$offset
		) );
	}

	public static function count() {
		global $wpdb;
		return (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . self::table() );
	}

	public static function prune() {
		global $wpdb;
		$days = max( 1, (int) AdminPulse_Settings::get( 'activity_keep' ) );
		$wpdb->query( $wpdb->prepare(
			'DELETE FROM ' . self::table() . ' WHERE created < %s',
			gmdate( 'Y-m-d H:i:s', current_time( 'timestamp' ) - $days * DAY_IN_SECONDS )
		) );
	}
}
