package com.horizon.launcher.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.text.TextStyle

@Composable
fun HorizonTheme(accent: Color, content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = accent,
            secondary = accent,
            onPrimary = Color(0xFF101014),
            surface = Color(0xFF1A1C24),
            background = Color(0xFF101014),
        ),
        content = content,
    )
}

/** White text with a soft shadow so it stays readable on any wallpaper. */
val OnWallpaper = TextStyle(
    color = Color.White,
    shadow = Shadow(color = Color.Black.copy(alpha = 0.55f), offset = Offset(0f, 2f), blurRadius = 10f),
)
