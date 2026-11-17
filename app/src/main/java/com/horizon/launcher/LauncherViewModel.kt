package com.horizon.launcher

import android.app.Application
import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

val AccentColors = listOf(
    Color(0xFF7AB8FF), // sky
    Color(0xFF5EE2B0), // mint
    Color(0xFFFF8A65), // sunset
    Color(0xFFB39DFF), // violet
    Color(0xFFFF6FA3), // rose
    Color(0xFFFFC857), // gold
)

const val MAX_DOCK = 5

class LauncherViewModel(app: Application) : AndroidViewModel(app) {

    private val prefs = app.getSharedPreferences("horizon_prefs", Context.MODE_PRIVATE)

    var apps by mutableStateOf<List<AppInfo>>(emptyList())
        private set

    var dock by mutableStateOf(
        prefs.getString(KEY_DOCK, "").orEmpty().split('|').filter { it.isNotBlank() }
    )
        private set

    var accentIndex by mutableIntStateOf(prefs.getInt(KEY_ACCENT, 0).coerceIn(AccentColors.indices))
        private set

    var use24h by mutableStateOf(prefs.getBoolean(KEY_24H, true))
        private set

    var columns by mutableIntStateOf(prefs.getInt(KEY_COLUMNS, 4))
        private set

    var drawerOpen by mutableStateOf(false)
    var settingsOpen by mutableStateOf(false)

    val accent: Color get() = AccentColors[accentIndex]

    val dockApps: List<AppInfo>
        get() = dock.mapNotNull { key -> apps.firstOrNull { it.key == key } }

    fun refresh() {
        viewModelScope.launch {
            apps = withContext(Dispatchers.Default) { AppRepository.load(getApplication()) }
        }
    }

    fun isInDock(app: AppInfo) = app.key in dock

    /** Adds or removes an app from the dock. Returns false if the dock is already full. */
    fun toggleDock(app: AppInfo): Boolean {
        val next = if (isInDock(app)) {
            dock - app.key
        } else {
            // Drop entries for apps that were uninstalled before checking the limit.
            val live = dock.filter { key -> apps.any { it.key == key } }
            if (live.size >= MAX_DOCK) return false
            live + app.key
        }
        dock = next
        prefs.edit().putString(KEY_DOCK, next.joinToString("|")).apply()
        return true
    }

    fun updateAccent(index: Int) {
        accentIndex = index
        prefs.edit().putInt(KEY_ACCENT, index).apply()
    }

    fun updateUse24h(value: Boolean) {
        use24h = value
        prefs.edit().putBoolean(KEY_24H, value).apply()
    }

    fun updateColumns(value: Int) {
        columns = value
        prefs.edit().putInt(KEY_COLUMNS, value).apply()
    }

    private companion object {
        const val KEY_DOCK = "dock"
        const val KEY_ACCENT = "accent"
        const val KEY_24H = "use24h"
        const val KEY_COLUMNS = "columns"
    }
}
