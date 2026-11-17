package com.horizon.launcher

import android.content.ComponentName
import androidx.compose.ui.graphics.ImageBitmap

data class AppInfo(
    val label: String,
    val component: ComponentName,
    val icon: ImageBitmap,
) {
    val key: String get() = component.flattenToString()
    val packageName: String get() = component.packageName
}
