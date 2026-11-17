package com.horizon.launcher

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.Settings
import android.widget.Toast

private fun Context.safeStart(intent: Intent) {
    try {
        startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
    } catch (e: ActivityNotFoundException) {
        Toast.makeText(this, "Couldn't open that", Toast.LENGTH_SHORT).show()
    } catch (e: SecurityException) {
        Toast.makeText(this, "Couldn't open that", Toast.LENGTH_SHORT).show()
    }
}

fun Context.launchApp(app: AppInfo) = safeStart(
    Intent(Intent.ACTION_MAIN)
        .addCategory(Intent.CATEGORY_LAUNCHER)
        .setComponent(app.component)
        .addFlags(Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED)
)

fun Context.openAppInfo(app: AppInfo) = safeStart(
    Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", app.packageName, null))
)

@Suppress("DEPRECATION")
fun Context.uninstallApp(app: AppInfo) = safeStart(
    Intent(Intent.ACTION_DELETE, Uri.fromParts("package", app.packageName, null))
)

fun Context.openWallpaperPicker() = safeStart(
    Intent.createChooser(Intent(Intent.ACTION_SET_WALLPAPER), "Choose wallpaper")
)

fun Context.openDefaultHomeSettings() = safeStart(Intent(Settings.ACTION_HOME_SETTINGS))
