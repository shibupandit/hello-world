package com.horizon.launcher.ui

import android.widget.Toast
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.horizon.launcher.AppInfo
import com.horizon.launcher.LauncherViewModel
import com.horizon.launcher.launchApp
import kotlinx.coroutines.delay
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun HomeScreen(vm: LauncherViewModel) {
    Box(
        Modifier
            .fillMaxSize()
            .pointerInput(Unit) {
                detectVerticalDragGestures { _, dragAmount ->
                    if (dragAmount < -20f) vm.drawerOpen = true
                }
            }
            .combinedClickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = {},
                onLongClick = { vm.settingsOpen = true },
            )
            .systemBarsPadding()
            .padding(horizontal = 24.dp)
    ) {
        Column(Modifier.fillMaxSize()) {
            Spacer(Modifier.height(56.dp))
            ClockBlock(vm.use24h)
            Spacer(Modifier.weight(1f))
            Text(
                "Swipe up for apps  ·  Hold for settings",
                style = OnWallpaper,
                fontSize = 12.sp,
                color = Color.White.copy(alpha = 0.7f),
                modifier = Modifier
                    .align(Alignment.CenterHorizontally)
                    .padding(bottom = 12.dp),
            )
            Dock(vm)
            Spacer(Modifier.height(16.dp))
        }
    }
}

@Composable
private fun ClockBlock(use24h: Boolean) {
    var now by remember { mutableStateOf(LocalDateTime.now()) }
    LaunchedEffect(Unit) {
        while (true) {
            now = LocalDateTime.now()
            delay(1000L - System.currentTimeMillis() % 1000L)
        }
    }

    val time = now.format(DateTimeFormatter.ofPattern(if (use24h) "HH:mm" else "h:mm"))
    val date = now.format(DateTimeFormatter.ofPattern("EEEE, d MMMM"))
    val greeting = when (now.hour) {
        in 5..11 -> "Good morning"
        in 12..16 -> "Good afternoon"
        in 17..21 -> "Good evening"
        else -> "Good night"
    }

    Text(time, style = OnWallpaper, fontSize = 96.sp, fontWeight = FontWeight.Thin, lineHeight = 100.sp)
    Text(date, style = OnWallpaper, fontSize = 20.sp, fontWeight = FontWeight.Medium)
    Text(
        greeting,
        style = OnWallpaper,
        fontSize = 16.sp,
        color = MaterialTheme.colorScheme.primary,
        modifier = Modifier.padding(top = 4.dp),
    )
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun Dock(vm: LauncherViewModel) {
    val context = LocalContext.current
    val dockApps = vm.dockApps

    Row(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(32.dp))
            .background(Color.White.copy(alpha = 0.16f))
            .padding(horizontal = 14.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceEvenly,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        if (dockApps.isEmpty()) {
            Text(
                "Hold any app in the drawer to pin it here",
                style = OnWallpaper,
                fontSize = 13.sp,
                modifier = Modifier.weight(1f).padding(start = 6.dp),
            )
        }
        dockApps.forEach { app ->
            DockIcon(
                app,
                onClick = { context.launchApp(app) },
                onLongClick = {
                    vm.toggleDock(app)
                    Toast.makeText(context, "Removed ${app.label} from dock", Toast.LENGTH_SHORT).show()
                },
            )
        }
        AppsButton(onClick = { vm.drawerOpen = true })
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun DockIcon(app: AppInfo, onClick: () -> Unit, onLongClick: () -> Unit) {
    Image(
        bitmap = app.icon,
        contentDescription = app.label,
        modifier = Modifier
            .size(52.dp)
            .clip(CircleShape)
            .combinedClickable(onClick = onClick, onLongClick = onLongClick),
    )
}

/** Round accent-coloured button with a 3×3 dot grid that opens the app drawer. */
@Composable
private fun AppsButton(onClick: () -> Unit) {
    val accent = MaterialTheme.colorScheme.primary
    Box(
        Modifier
            .size(52.dp)
            .clip(CircleShape)
            .background(accent)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center,
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            repeat(3) {
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    repeat(3) {
                        Box(
                            Modifier
                                .size(5.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.onPrimary)
                        )
                    }
                }
            }
        }
    }
}
