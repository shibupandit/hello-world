package com.horizon.launcher.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.horizon.launcher.AccentColors
import com.horizon.launcher.LauncherViewModel
import com.horizon.launcher.openDefaultHomeSettings
import com.horizon.launcher.openWallpaperPicker

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsSheet(vm: LauncherViewModel, onDismiss: () -> Unit) {
    val context = LocalContext.current

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp),
        ) {
            Text("Horizon settings", style = MaterialTheme.typography.titleLarge)

            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Accent colour", style = MaterialTheme.typography.labelLarge)
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    AccentColors.forEachIndexed { index, color ->
                        val selected = index == vm.accentIndex
                        Box(
                            Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .background(color)
                                .border(
                                    width = if (selected) 3.dp else 0.dp,
                                    color = if (selected) Color.White else Color.Transparent,
                                    shape = CircleShape,
                                )
                                .clickable { vm.updateAccent(index) },
                            contentAlignment = Alignment.Center,
                        ) {
                            if (selected) {
                                Icon(Icons.Default.Check, contentDescription = "Selected", tint = Color(0xFF101014))
                            }
                        }
                    }
                }
            }

            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("24-hour clock", modifier = Modifier.weight(1f))
                Switch(checked = vm.use24h, onCheckedChange = vm::updateUse24h)
            }

            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("App drawer columns", style = MaterialTheme.typography.labelLarge)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf(3, 4, 5, 6).forEach { n ->
                        FilterChip(
                            selected = vm.columns == n,
                            onClick = { vm.updateColumns(n) },
                            label = { Text("$n") },
                        )
                    }
                }
            }

            Spacer(Modifier.height(4.dp))
            FilledTonalButton(onClick = { context.openWallpaperPicker() }, modifier = Modifier.fillMaxWidth()) {
                Text("Change wallpaper")
            }
            FilledTonalButton(onClick = { context.openDefaultHomeSettings() }, modifier = Modifier.fillMaxWidth()) {
                Text("Choose default home app")
            }
        }
    }
}
