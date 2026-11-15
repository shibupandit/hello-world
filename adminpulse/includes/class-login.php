<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class AdminPulse_Login {
	public static function init() {
		add_action( 'login_enqueue_scripts', array( __CLASS__, 'styles' ) );
		add_filter( 'login_headerurl', function ( $url ) {
			$custom = AdminPulse_Settings::get( 'login_on' ) ? AdminPulse_Settings::get( 'login_logo_url' ) : '';
			return $custom ? esc_url( $custom ) : home_url( '/' );
		} );
		add_filter( 'login_headertext', function ( $t ) {
			$n = AdminPulse_Settings::get( 'brand_name' );
			return $n ? esc_html( $n ) : $t;
		} );
	}

	public static function styles() {
		if ( ! AdminPulse_Settings::get( 'login_on' ) ) {
			return;
		}
		$bg     = sanitize_hex_color( AdminPulse_Settings::get( 'login_bg' ) ) ?: '#0f172a';
		$accent = sanitize_hex_color( AdminPulse_Settings::get( 'accent' ) ) ?: '#4f46e5';
		$logo   = esc_url( AdminPulse_Settings::get( 'login_logo' ) );
		$css    = "body.login{background:$bg;display:flex;align-items:center;justify-content:center;min-height:100vh}
#login{width:380px;padding:0}
.login form{background:#fff;border:0;border-radius:16px;padding:28px;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.login label{font-weight:600}
.login input[type=text],.login input[type=password]{border-radius:10px;padding:8px 12px;border-color:#e2e8f0}
.login input:focus{border-color:$accent;box-shadow:0 0 0 3px {$accent}33}
.wp-core-ui .button-primary{background:$accent;border-color:$accent;border-radius:10px;height:42px;width:100%;font-weight:600;text-shadow:none;box-shadow:none}
.login #nav a,.login #backtoblog a,.login .privacy-policy-page-link a{color:#cbd5e1}
.login h1 a{" . ( $logo ? "background-image:url($logo);background-size:contain;width:100%;height:80px;" : '' ) . "}";
		echo '<style>' . $css . '</style>'; // phpcs:ignore WordPress.Security.EscapeOutput
	}
}
