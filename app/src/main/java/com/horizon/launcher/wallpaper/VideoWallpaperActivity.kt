package com.horizon.launcher.wallpaper

import android.app.WallpaperManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import android.provider.Settings
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Button
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.horizon.launcher.AccentColors
import com.horizon.launcher.ui.HorizonTheme
import java.util.Locale

/** Settings screen for the video wallpaper. Opened from Horizon's settings or Android's wallpaper picker. */
class VideoWallpaperActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val accentIndex = getSharedPreferences("horizon_prefs", MODE_PRIVATE)
            .getInt("accent", 0).coerceIn(AccentColors.indices)
        setContent {
            HorizonTheme(accent = AccentColors[accentIndex]) {
                VideoWallpaperScreen(onClose = { finish() })
            }
        }
    }
}

@Composable
private fun VideoWallpaperScreen(onClose: () -> Unit) {
    val context = LocalContext.current
    var s by remember { mutableStateOf(VideoPrefs.load(context)) }
    fun update(next: VideoSettings) {
        s = next
        VideoPrefs.save(context, next)
    }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenMultipleDocuments()) { uris ->
        val added = uris.map { uri ->
            // Keep access to the file after the phone restarts.
            runCatching {
                context.contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            uri.toString()
        }
        if (added.isNotEmpty()) update(s.copy(videos = (s.videos + added).distinct()))
    }

    Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        Column(
            Modifier
                .fillMaxSize()
                .systemBarsPadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp),
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Video wallpaper", style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
                IconButton(onClick = onClose) { Icon(Icons.Default.Close, contentDescription = "Close") }
            }

            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Button(onClick = { setAsWallpaper(context) }, modifier = Modifier.fillMaxWidth(), enabled = s.videos.isNotEmpty()) {
                    Text("Set as wallpaper")
                }
                Text(
                    if (s.videos.isEmpty()) "Add at least one video first."
                    else "When Android asks, choose “Home screen and lock screen”.",
                    style = MaterialTheme.typography.bodySmall,
                )
            }

            Section("Videos") {
                s.videos.forEachIndexed { i, uri ->
                    val name = remember(uri) { displayName(context, uri) }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("${i + 1}.  $name", maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f))
                        IconButton(onClick = { update(s.copy(videos = s.videos - uri)) }) {
                            Icon(Icons.Default.Close, contentDescription = "Remove $name")
                        }
                    }
                }
                OutlinedButton(onClick = { picker.launch(arrayOf("video/*")) }, modifier = Modifier.fillMaxWidth()) {
                    Text("Add videos")
                }
            }

            Section("Playback") {
                SliderRow("Speed", String.format(Locale.US, "%.2f×", s.speed), s.speed, 0.25f..2f, steps = 6) {
                    update(s.copy(speed = it))
                }
                SliderRow("Start at", "${s.trimStartSec} s", s.trimStartSec.toFloat(), 0f..60f, steps = 59) {
                    update(s.copy(trimStartSec = it.toInt()))
                }
                SliderRow(
                    "Stop at", if (s.trimEndSec == 0) "End of video" else "${s.trimEndSec} s",
                    s.trimEndSec.toFloat(), 0f..120f, steps = 119,
                ) { update(s.copy(trimEndSec = it.toInt())) }
                SwitchRow("Mute sound", s.muted) { update(s.copy(muted = it)) }
            }

            Section("Order and timing") {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ModeChip("Loop one", s.mode == PlayMode.LOOP_ONE) { update(s.copy(mode = PlayMode.LOOP_ONE)) }
                    ModeChip("Play all", s.mode == PlayMode.PLAYLIST) { update(s.copy(mode = PlayMode.PLAYLIST)) }
                    ModeChip("Switch every…", s.mode == PlayMode.INTERVAL) { update(s.copy(mode = PlayMode.INTERVAL)) }
                }
                if (s.mode == PlayMode.INTERVAL) {
                    SliderRow("Switch video every", "${s.intervalMin} min", s.intervalMin.toFloat(), 1f..60f, steps = 58) {
                        update(s.copy(intervalMin = it.toInt()))
                    }
                }
                if (s.mode != PlayMode.LOOP_ONE) {
                    SwitchRow("Shuffle", s.shuffle) { update(s.copy(shuffle = it)) }
                }
            }

            Section("Transitions") {
                SwitchRow("Fade between videos", s.fade) { update(s.copy(fade = it)) }
                if (s.fade) {
                    SliderRow("Fade length", "${s.fadeMs} ms", s.fadeMs.toFloat(), 200f..3000f, steps = 27) {
                        update(s.copy(fadeMs = (it / 100).toInt() * 100))
                    }
                }
            }

            Section("Look") {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ModeChip("Fill screen", s.fill) { update(s.copy(fill = true)) }
                    ModeChip("Fit whole video", !s.fill) { update(s.copy(fill = false)) }
                }
                SliderRow("Dim", "${(s.dim * 100).toInt()} %", s.dim, 0f..0.8f, steps = 15) {
                    update(s.copy(dim = it))
                }
            }

            Section("When to play") {
                SwitchRow("Play on lock screen", s.playOnLock) { update(s.copy(playOnLock = it)) }
                SwitchRow("Pause while app drawer is open", s.pauseInDrawer) { update(s.copy(pauseInDrawer = it)) }
                SwitchRow("Pause in battery saver", s.pauseOnBatterySaver) { update(s.copy(pauseOnBatterySaver = it)) }
                Text("After unlocking, play for", style = MaterialTheme.typography.bodyMedium)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf(0 to "Always", 5 to "5 s", 10 to "10 s", 30 to "30 s").forEach { (sec, label) ->
                        ModeChip(label, s.playSecondsAfterShow == sec) { update(s.copy(playSecondsAfterShow = sec)) }
                    }
                }
                Text(
                    "The video always pauses while an app is open or the screen is off.",
                    style = MaterialTheme.typography.bodySmall,
                )
            }

            Section("Idle screen") {
                Text(
                    "Use the same videos as Android's screen saver, shown while the phone is charging or docked.",
                    style = MaterialTheme.typography.bodyMedium,
                )
                OutlinedButton(onClick = { openScreensaverSettings(context) }, modifier = Modifier.fillMaxWidth()) {
                    Text("Open screen saver settings")
                }
                Text("Choose “Horizon Video” there.", style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}

@Composable
private fun Section(title: String, content: @Composable ColumnScope.() -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        HorizontalDivider()
        Text(title, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
        content()
    }
}

@Composable
private fun SliderRow(
    label: String,
    valueText: String,
    value: Float,
    range: ClosedFloatingPointRange<Float>,
    steps: Int,
    onChange: (Float) -> Unit,
) {
    Column {
        Row {
            Text(label, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
            Text(valueText, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
        }
        Slider(value = value.coerceIn(range), onValueChange = onChange, valueRange = range, steps = steps)
    }
}

@Composable
private fun SwitchRow(label: String, checked: Boolean, onChange: (Boolean) -> Unit) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text(label, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
        Switch(checked = checked, onCheckedChange = onChange)
    }
}

@Composable
private fun ModeChip(label: String, selected: Boolean, onClick: () -> Unit) {
    FilterChip(selected = selected, onClick = onClick, label = { Text(label) })
}

private fun displayName(context: Context, uri: String): String = runCatching {
    context.contentResolver.query(Uri.parse(uri), arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)
        ?.use { c -> if (c.moveToFirst()) c.getString(0) else null }
}.getOrNull() ?: uri.substringAfterLast('/')

fun setAsWallpaper(context: Context) {
    val intent = Intent(WallpaperManager.ACTION_CHANGE_LIVE_WALLPAPER)
        .putExtra(
            WallpaperManager.EXTRA_LIVE_WALLPAPER_COMPONENT,
            ComponentName(context, VideoWallpaperService::class.java),
        )
    val fallback = Intent(WallpaperManager.ACTION_LIVE_WALLPAPER_CHOOSER)
    for (i in listOf(intent, fallback)) {
        try {
            context.startActivity(i)
            return
        } catch (_: Exception) {
        }
    }
    Toast.makeText(context, "Couldn't open the wallpaper picker", Toast.LENGTH_SHORT).show()
}

private fun openScreensaverSettings(context: Context) {
    try {
        context.startActivity(Intent(Settings.ACTION_DREAM_SETTINGS))
    } catch (_: Exception) {
        Toast.makeText(context, "Open Settings › Display › Screen saver", Toast.LENGTH_LONG).show()
    }
}
