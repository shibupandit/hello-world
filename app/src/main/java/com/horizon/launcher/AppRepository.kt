package com.horizon.launcher

import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.content.pm.ResolveInfo
import android.os.Build
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.core.graphics.drawable.toBitmap

/** Reads the list of launchable apps from the system, caching icons between refreshes. */
object AppRepository {

    private const val ICON_PX = 144
    private val iconCache = HashMap<String, ImageBitmap>()

    @Synchronized
    fun load(context: Context): List<AppInfo> {
        val pm = context.packageManager
        val intent = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        val resolved: List<ResolveInfo> = if (Build.VERSION.SDK_INT >= 33) {
            pm.queryIntentActivities(intent, PackageManager.ResolveInfoFlags.of(0))
        } else {
            @Suppress("DEPRECATION")
            pm.queryIntentActivities(intent, 0)
        }

        val apps = resolved
            .filter { it.activityInfo.packageName != context.packageName }
            .map { ri ->
                val component = ComponentName(ri.activityInfo.packageName, ri.activityInfo.name)
                val key = component.flattenToString()
                val icon = iconCache.getOrPut(key) {
                    ri.loadIcon(pm).toBitmap(ICON_PX, ICON_PX).asImageBitmap()
                }
                AppInfo(ri.loadLabel(pm).toString(), component, icon)
            }
            .sortedBy { it.label.lowercase() }

        // Forget icons of uninstalled apps.
        val live = apps.mapTo(HashSet()) { it.key }
        iconCache.keys.retainAll(live)
        return apps
    }
}
