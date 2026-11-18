package com.horizon.launcher.wallpaper

import android.content.Context
import android.content.SharedPreferences

enum class PlayMode { LOOP_ONE, PLAYLIST, INTERVAL }

/** Everything the user can tune for the video wallpaper and screensaver. */
data class VideoSettings(
    val videos: List<String> = emptyList(),
    val speed: Float = 1f,
    val trimStartSec: Int = 0,
    /** 0 means "play to the end". */
    val trimEndSec: Int = 0,
    val mode: PlayMode = PlayMode.LOOP_ONE,
    val intervalMin: Int = 10,
    val shuffle: Boolean = false,
    val fade: Boolean = true,
    val fadeMs: Int = 800,
    val fill: Boolean = true,
    val dim: Float = 0f,
    val muted: Boolean = true,
    val playOnLock: Boolean = true,
    val pauseInDrawer: Boolean = true,
    val pauseOnBatterySaver: Boolean = true,
    /** 0 means keep playing; otherwise freeze this many seconds after the wallpaper becomes visible. */
    val playSecondsAfterShow: Int = 0,
)

object VideoPrefs {
    const val NAME = "video_wallpaper"

    fun prefs(context: Context): SharedPreferences =
        context.getSharedPreferences(NAME, Context.MODE_PRIVATE)

    fun load(context: Context): VideoSettings {
        val p = prefs(context)
        val d = VideoSettings()
        return VideoSettings(
            videos = p.getString("videos", "").orEmpty().split('\n').filter { it.isNotBlank() },
            speed = p.getFloat("speed", d.speed),
            trimStartSec = p.getInt("trimStart", d.trimStartSec),
            trimEndSec = p.getInt("trimEnd", d.trimEndSec),
            mode = runCatching { PlayMode.valueOf(p.getString("mode", d.mode.name)!!) }.getOrDefault(d.mode),
            intervalMin = p.getInt("intervalMin", d.intervalMin),
            shuffle = p.getBoolean("shuffle", d.shuffle),
            fade = p.getBoolean("fade", d.fade),
            fadeMs = p.getInt("fadeMs", d.fadeMs),
            fill = p.getBoolean("fill", d.fill),
            dim = p.getFloat("dim", d.dim),
            muted = p.getBoolean("muted", d.muted),
            playOnLock = p.getBoolean("playOnLock", d.playOnLock),
            pauseInDrawer = p.getBoolean("pauseInDrawer", d.pauseInDrawer),
            pauseOnBatterySaver = p.getBoolean("pauseOnSaver", d.pauseOnBatterySaver),
            playSecondsAfterShow = p.getInt("playSeconds", d.playSecondsAfterShow),
        )
    }

    fun save(context: Context, s: VideoSettings) {
        prefs(context).edit()
            .putString("videos", s.videos.joinToString("\n"))
            .putFloat("speed", s.speed)
            .putInt("trimStart", s.trimStartSec)
            .putInt("trimEnd", s.trimEndSec)
            .putString("mode", s.mode.name)
            .putInt("intervalMin", s.intervalMin)
            .putBoolean("shuffle", s.shuffle)
            .putBoolean("fade", s.fade)
            .putInt("fadeMs", s.fadeMs)
            .putBoolean("fill", s.fill)
            .putFloat("dim", s.dim)
            .putBoolean("muted", s.muted)
            .putBoolean("playOnLock", s.playOnLock)
            .putBoolean("pauseInDrawer", s.pauseInDrawer)
            .putBoolean("pauseOnSaver", s.pauseOnBatterySaver)
            .putInt("playSeconds", s.playSecondsAfterShow)
            .apply()
    }
}

/** Messages the launcher sends to the running wallpaper. */
object WallpaperCommands {
    const val DRAWER_OPEN = "com.horizon.launcher.DRAWER_OPEN"
    const val DRAWER_CLOSED = "com.horizon.launcher.DRAWER_CLOSED"
}
