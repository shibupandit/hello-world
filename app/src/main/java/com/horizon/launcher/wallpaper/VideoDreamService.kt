package com.horizon.launcher.wallpaper

import android.service.dreams.DreamService
import android.view.SurfaceHolder
import android.view.SurfaceView

/** Android "Screen saver": plays the same videos while the phone is charging or docked. */
class VideoDreamService : DreamService() {

    private var renderer: VideoRenderer? = null

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        isInteractive = false
        isFullscreen = true
        val r = VideoRenderer(this, isScreensaver = true)
        renderer = r
        val view = SurfaceView(this)
        view.holder.addCallback(object : SurfaceHolder.Callback {
            override fun surfaceCreated(holder: SurfaceHolder) = Unit
            override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
                r.attach(holder.surface, width, height)
            }
            override fun surfaceDestroyed(holder: SurfaceHolder) {
                r.detach()
            }
        })
        setContentView(view)
    }

    override fun onDreamingStarted() {
        super.onDreamingStarted()
        renderer?.setVisible(true)
    }

    override fun onDreamingStopped() {
        renderer?.setVisible(false)
        super.onDreamingStopped()
    }

    override fun onDetachedFromWindow() {
        renderer?.release()
        renderer = null
        super.onDetachedFromWindow()
    }
}
