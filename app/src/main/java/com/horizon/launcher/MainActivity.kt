package com.horizon.launcher

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import com.horizon.launcher.ui.HorizonTheme
import com.horizon.launcher.ui.LauncherScreen

class MainActivity : ComponentActivity() {

    private val vm: LauncherViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
        )
        setContent {
            HorizonTheme(accent = vm.accent) {
                LauncherScreen(vm)
            }
        }
    }

    override fun onResume() {
        super.onResume()
        // Picks up apps installed or removed while we were in the background.
        vm.refresh()
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        // Home button pressed while the launcher is already showing: go back to the home page.
        vm.drawerOpen = false
        vm.settingsOpen = false
    }
}
