package com.horizon.launcher.wallpaper

import android.os.Bundle
import android.service.wallpaper.WallpaperService
import android.view.SurfaceHolder

/** The live wallpaper Android shows behind the home screen and (if chosen) the lock screen. */
class VideoWallpaperService : WallpaperService() {

    override fun onCreateEngine(): Engine = VideoEngine()

    inner class VideoEngine : Engine() {
        private val renderer = VideoRenderer(applicationContext, isScreensaver = false)

        override fun onCreate(surfaceHolder: SurfaceHolder) {
            super.onCreate(surfaceHolder)
            setTouchEventsEnabled(false)
        }

        override fun onSurfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
            super.onSurfaceChanged(holder, format, width, height)
            renderer.attach(holder.surface, width, height)
        }

        override fun onSurfaceDestroyed(holder: SurfaceHolder) {
            renderer.detach()
            super.onSurfaceDestroyed(holder)
        }

        override fun onVisibilityChanged(visible: Boolean) {
            renderer.setVisible(visible)
        }

        override fun onCommand(
            action: String?, x: Int, y: Int, z: Int, extras: Bundle?, resultRequested: Boolean,
        ): Bundle? {
            when (action) {
                WallpaperCommands.DRAWER_OPEN -> renderer.setDrawerOpen(true)
                WallpaperCommands.DRAWER_CLOSED -> renderer.setDrawerOpen(false)
            }
            return super.onCommand(action, x, y, z, extras, resultRequested)
        }

        override fun onDestroy() {
            renderer.release()
            super.onDestroy()
        }
    }
}
