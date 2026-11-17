package com.horizon.launcher.ui

import android.widget.Toast
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.horizon.launcher.AppInfo
import com.horizon.launcher.LauncherViewModel
import com.horizon.launcher.MAX_DOCK
import com.horizon.launcher.launchApp
import com.horizon.launcher.openAppInfo
import com.horizon.launcher.uninstallApp

@Composable
fun AppDrawer(vm: LauncherViewModel, onClose: () -> Unit) {
    val context = LocalContext.current
    var query by rememberSaveable { mutableStateOf("") }
    val apps = vm.apps
    val filtered = remember(query, apps) {
        val q = query.trim()
        if (q.isEmpty()) apps else apps.filter { it.label.contains(q, ignoreCase = true) }
    }

    fun open(app: AppInfo) {
        context.launchApp(app)
        onClose()
    }

    Column(
        Modifier
            .fillMaxSize()
            .background(Color(0xEB101014))
            .systemBarsPadding()
            .imePadding()
            .padding(horizontal = 16.dp, vertical = 12.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("Search ${apps.size} apps") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                singleLine = true,
                shape = RoundedCornerShape(28.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedBorderColor = Color.White.copy(alpha = 0.2f),
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                ),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Go),
                keyboardActions = KeyboardActions(onGo = { filtered.firstOrNull()?.let(::open) }),
            )
            IconButton(onClick = onClose) {
                Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White)
            }
        }

        if (filtered.isEmpty()) {
            Text(
                if (apps.isEmpty()) "Loading apps…" else "No apps match \"$query\"",
                color = Color.White.copy(alpha = 0.7f),
                modifier = Modifier.fillMaxWidth().padding(top = 48.dp),
                textAlign = TextAlign.Center,
            )
        }

        LazyVerticalGrid(
            columns = GridCells.Fixed(vm.columns),
            modifier = Modifier.fillMaxSize().padding(top = 12.dp),
        ) {
            items(filtered, key = { it.key }) { app ->
                DrawerItem(
                    app = app,
                    inDock = vm.isInDock(app),
                    onOpen = { open(app) },
                    onToggleDock = {
                        val wasInDock = vm.isInDock(app)
                        val msg = when {
                            !vm.toggleDock(app) -> "Dock is full ($MAX_DOCK apps). Remove one first."
                            wasInDock -> "Removed ${app.label} from dock"
                            else -> "Pinned ${app.label} to dock"
                        }
                        Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
                    },
                    onInfo = { context.openAppInfo(app) },
                    onUninstall = { context.uninstallApp(app) },
                )
            }
        }
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun DrawerItem(
    app: AppInfo,
    inDock: Boolean,
    onOpen: () -> Unit,
    onToggleDock: () -> Unit,
    onInfo: () -> Unit,
    onUninstall: () -> Unit,
) {
    var menuOpen by remember { mutableStateOf(false) }
    Box {
        Column(
            Modifier
                .fillMaxWidth()
                .combinedClickable(onClick = onOpen, onLongClick = { menuOpen = true })
                .padding(vertical = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Image(bitmap = app.icon, contentDescription = null, modifier = Modifier.size(52.dp))
            Text(
                app.label,
                color = Color.White,
                fontSize = 12.sp,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(top = 6.dp, start = 4.dp, end = 4.dp),
            )
        }
        DropdownMenu(expanded = menuOpen, onDismissRequest = { menuOpen = false }) {
            DropdownMenuItem(
                text = { Text(if (inDock) "Remove from dock" else "Pin to dock") },
                onClick = { menuOpen = false; onToggleDock() },
            )
            DropdownMenuItem(text = { Text("App info") }, onClick = { menuOpen = false; onInfo() })
            DropdownMenuItem(text = { Text("Uninstall") }, onClick = { menuOpen = false; onUninstall() })
        }
    }
}
