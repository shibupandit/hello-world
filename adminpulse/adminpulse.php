<?php
/**
 * Plugin Name: AdminPulse
 * Description: A modern WordPress admin experience: custom dashboard, dark mode, command-palette search, menu editor, white-label branding, custom login page and activity log.
 * Version:     1.0.0
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Author:      Shibu Pandit
 * License:     GPL-2.0-or-later
 * Text Domain: adminpulse
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'ADMINPULSE_VERSION', '1.0.0' );
define( 'ADMINPULSE_FILE', __FILE__ );
define( 'ADMINPULSE_DIR', plugin_dir_path( __FILE__ ) );
define( 'ADMINPULSE_URL', plugin_dir_url( __FILE__ ) );

require_once ADMINPULSE_DIR . 'includes/class-settings.php';
require_once ADMINPULSE_DIR . 'includes/class-activity.php';
require_once ADMINPULSE_DIR . 'includes/class-theme.php';
require_once ADMINPULSE_DIR . 'includes/class-menu.php';
require_once ADMINPULSE_DIR . 'includes/class-login.php';
require_once ADMINPULSE_DIR . 'includes/class-search.php';
require_once ADMINPULSE_DIR . 'includes/class-dashboard.php';
require_once ADMINPULSE_DIR . 'includes/class-settings-page.php';

register_activation_hook( __FILE__, array( 'AdminPulse_Activity', 'install' ) );

add_action( 'plugins_loaded', function () {
	AdminPulse_Activity::init();
	AdminPulse_Theme::init();
	AdminPulse_Menu::init();
	AdminPulse_Login::init();
	AdminPulse_Search::init();
	AdminPulse_Dashboard::init();
	AdminPulse_Settings_Page::init();
} );
