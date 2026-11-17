package com.horizon.launcher.ui

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.horizon.launcher.LauncherViewModel

@Composable
fun LauncherScreen(vm: LauncherViewModel) {
    // A launcher never closes itself on Back; Back only closes the drawer.
    BackHandler(enabled = true) {
        vm.drawerOpen = false
    }

    Box(Modifier.fillMaxSize()) {
        HomeScreen(vm)

        AnimatedVisibility(
            visible = vm.drawerOpen,
            enter = slideInVertically { it / 3 } + fadeIn(),
            exit = slideOutVertically { it / 3 } + fadeOut(),
        ) {
            AppDrawer(vm, onClose = { vm.drawerOpen = false })
        }
    }

    if (vm.settingsOpen) {
        SettingsSheet(vm, onDismiss = { vm.settingsOpen = false })
    }
}
