package com.horizon.launcher.wallpaper

import android.app.KeyguardManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.SharedPreferences
import android.graphics.SurfaceTexture
import android.net.Uri
import android.opengl.EGL14
import android.opengl.EGLConfig
import android.opengl.EGLContext
import android.opengl.EGLDisplay
import android.opengl.EGLSurface
import android.opengl.GLES11Ext
import android.opengl.GLES20
import android.os.Handler
import android.os.HandlerThread
import android.os.Looper
import android.os.PowerManager
import android.os.SystemClock
import android.util.Log
import android.view.Surface
import androidx.core.content.ContextCompat
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.PlaybackParameters
import androidx.media3.common.Player
import androidx.media3.common.VideoSize
import androidx.media3.exoplayer.ExoPlayer
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.FloatBuffer
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import kotlin.random.Random

/**
 * Plays the user's videos onto a Surface (the wallpaper or the screensaver).
 *
 * Frames are decoded into a SurfaceTexture and drawn with OpenGL so we can
 * fit/fill, dim and fade between videos. Everything runs on one background thread.
 */
class VideoRenderer(context: Context, private val isScreensaver: Boolean) {

    private val appContext = context.applicationContext
    private val thread = HandlerThread("HorizonVideo").apply { start() }
    private val handler = Handler(thread.looper)

    private var settings = VideoPrefs.load(appContext)

    // EGL / GL state
    private var eglDisplay: EGLDisplay = EGL14.EGL_NO_DISPLAY
    private var eglContext: EGLContext = EGL14.EGL_NO_CONTEXT
    private var eglSurface: EGLSurface = EGL14.EGL_NO_SURFACE
    private var attachedSurface: Surface? = null
    private var program = 0
    private var textureId = 0
    private var surfaceTexture: SurfaceTexture? = null
    private var decoderSurface: Surface? = null
    private val texMatrix = FloatArray(16)
    private var frameAvailable = false
    private var hasFrame = false
    private var surfaceW = 0
    private var surfaceH = 0
    private var videoW = 0f
    private var videoH = 0f

    // Playback state
    private var player: ExoPlayer? = null
    private var index = 0
    private var itemStartedAt = 0L
    private var visible = false
    private var visibleSince = 0L
    private var drawerOpen = false
    private var frozenAfterShow = false

    // Fade: level 0 = black, 1 = full picture. dir: 1 fading in, -1 fading out, 0 idle.
    private var fadeLevel = 1f
    private var fadeDir = 0
    private var fadeStart = 0L

    private val drawRunnable = Runnable { draw() }
    private val tickRunnable = object : Runnable {
        override fun run() {
            tick()
            handler.postDelayed(this, 250)
        }
    }

    private val prefsListener = SharedPreferences.OnSharedPreferenceChangeListener { _, _ ->
        val fresh = VideoPrefs.load(appContext)
        handler.post { applySettings(fresh) }
    }

    private val systemReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            handler.post {
                if (intent.action == Intent.ACTION_USER_PRESENT) {
                    // Unlocked: the wallpaper is now the home screen; restart the "play for N seconds" timer.
                    visibleSince = SystemClock.elapsedRealtime()
                    frozenAfterShow = false
                }
                updatePlayState()
            }
        }
    }

    init {
        VideoPrefs.prefs(appContext).registerOnSharedPreferenceChangeListener(prefsListener)
        val filter = IntentFilter().apply {
            addAction(Intent.ACTION_USER_PRESENT)
            addAction(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED)
        }
        ContextCompat.registerReceiver(appContext, systemReceiver, filter, ContextCompat.RECEIVER_EXPORTED)
    }

    // ---------------------------------------------------------------- public API

    fun attach(surface: Surface, width: Int, height: Int) = runSync {
        if (attachedSurface === surface && eglSurface != EGL14.EGL_NO_SURFACE) {
            surfaceW = width
            surfaceH = height
            requestDraw()
            return@runSync
        }
        teardownGl()
        surfaceW = width
        surfaceH = height
        try {
            setupGl(surface)
        } catch (e: RuntimeException) {
            Log.e(TAG, "GL setup failed", e)
            teardownGl()
            return@runSync
        }
        val p = player ?: createPlayer().also { player = it }
        p.setVideoSurface(decoderSurface)
        if (p.mediaItemCount == 0) playIndex(index) else updatePlayState()
        handler.removeCallbacks(tickRunnable)
        handler.post(tickRunnable)
        requestDraw()
    }

    fun detach() = runSync {
        handler.removeCallbacks(tickRunnable)
        player?.let {
            it.playWhenReady = false
            it.clearVideoSurface()
        }
        teardownGl()
    }

    fun setVisible(isVisible: Boolean) = handler.post {
        if (isVisible && !visible) {
            visibleSince = SystemClock.elapsedRealtime()
            frozenAfterShow = false
        }
        visible = isVisible
        updatePlayState()
        requestDraw()
    }

    fun setDrawerOpen(open: Boolean) = handler.post {
        drawerOpen = open
        updatePlayState()
    }

    fun release() {
        runSync {
            handler.removeCallbacksAndMessages(null)
            player?.release()
            player = null
            teardownGl()
        }
        VideoPrefs.prefs(appContext).unregisterOnSharedPreferenceChangeListener(prefsListener)
        runCatching { appContext.unregisterReceiver(systemReceiver) }
        thread.quitSafely()
    }

    // ---------------------------------------------------------------- playback

    private fun createPlayer(): ExoPlayer {
        val p = ExoPlayer.Builder(appContext).setLooper(thread.looper).build()
        p.addListener(object : Player.Listener {
            override fun onVideoSizeChanged(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    videoW = videoSize.width * videoSize.pixelWidthHeightRatio
                    videoH = videoSize.height.toFloat()
                    requestDraw()
                }
            }

            override fun onRenderedFirstFrame() {
                if (settings.fade && fadeLevel < 1f && fadeDir == 0) {
                    fadeDir = 1
                    fadeStart = SystemClock.uptimeMillis()
                }
                requestDraw()
            }

            override fun onPlaybackStateChanged(state: Int) {
                if (state == Player.STATE_ENDED && fadeDir != -1) advance()
            }

            override fun onPlayerError(error: PlaybackException) {
                Log.w(TAG, "Can't play video ${settings.videos.getOrNull(index)}", error)
                if (settings.videos.size > 1) handler.postDelayed({ advance() }, 1000)
            }
        })
        applyPlayerParams(p)
        return p
    }

    private fun applyPlayerParams(p: ExoPlayer) {
        p.volume = if (settings.muted) 0f else 1f
        p.playbackParameters = PlaybackParameters(settings.speed.coerceIn(0.25f, 2f))
        p.repeatMode = if (settings.mode == PlayMode.PLAYLIST) Player.REPEAT_MODE_OFF else Player.REPEAT_MODE_ONE
    }

    private fun playIndex(i: Int) {
        val p = player ?: return
        val videos = settings.videos
        if (videos.isEmpty()) {
            p.stop()
            p.clearMediaItems()
            hasFrame = false
            requestDraw()
            return
        }
        index = i.mod(videos.size)
        val item = MediaItem.Builder().setUri(Uri.parse(videos[index]))
        val startMs = settings.trimStartSec * 1000L
        val endMs = settings.trimEndSec * 1000L
        if (startMs > 0 || endMs > startMs) {
            val clip = MediaItem.ClippingConfiguration.Builder().setStartPositionMs(startMs)
            if (endMs > startMs) clip.setEndPositionMs(endMs)
            item.setClippingConfiguration(clip.build())
        }
        p.setMediaItem(item.build())
        applyPlayerParams(p)
        p.prepare()
        fadeDir = 0
        fadeLevel = if (settings.fade && hasFrame) 0f else 1f
        itemStartedAt = SystemClock.elapsedRealtime()
        updatePlayState()
    }

    private fun nextIndex(): Int {
        val n = settings.videos.size
        if (n <= 1) return 0
        if (!settings.shuffle) return (index + 1) % n
        var next: Int
        do { next = Random.nextInt(n) } while (next == index)
        return next
    }

    private fun advance() {
        if (settings.mode == PlayMode.LOOP_ONE) {
            // Never leave the screen faded out if the mode changed mid-transition.
            fadeDir = 0
            fadeLevel = 1f
            requestDraw()
            return
        }
        playIndex(nextIndex())
    }

    /** Fade to black (if enabled and visible), then switch video. */
    private fun transitionToNext() {
        if (settings.fade && visible && hasFrame) {
            if (fadeDir == -1) return
            fadeDir = -1
            fadeStart = SystemClock.uptimeMillis()
            requestDraw()
        } else {
            advance()
        }
    }

    private fun shouldPlay(): Boolean {
        if (!visible || settings.videos.isEmpty() || eglSurface == EGL14.EGL_NO_SURFACE) return false
        if (settings.pauseInDrawer && drawerOpen) return false
        val power = appContext.getSystemService(PowerManager::class.java)
        if (settings.pauseOnBatterySaver && power?.isPowerSaveMode == true) return false
        if (!isScreensaver) {
            val keyguard = appContext.getSystemService(KeyguardManager::class.java)
            if (!settings.playOnLock && keyguard?.isKeyguardLocked == true) return false
            if (frozenAfterShow) return false
        }
        return true
    }

    private fun updatePlayState() {
        player?.playWhenReady = shouldPlay()
    }

    private fun tick() {
        val p = player ?: return
        if (!p.playWhenReady) return
        val now = SystemClock.elapsedRealtime()

        if (!isScreensaver && settings.playSecondsAfterShow > 0 &&
            now - visibleSince >= settings.playSecondsAfterShow * 1000L
        ) {
            frozenAfterShow = true
            updatePlayState()
            return
        }

        when (settings.mode) {
            PlayMode.PLAYLIST -> {
                val duration = p.duration
                if (settings.fade && duration != C.TIME_UNSET && fadeDir == 0) {
                    val remainingMs = (duration - p.currentPosition) / settings.speed
                    if (remainingMs <= settings.fadeMs / 2f && remainingMs > 0) transitionToNext()
                }
            }
            PlayMode.INTERVAL -> {
                if (now - itemStartedAt >= settings.intervalMin * 60_000L) {
                    itemStartedAt = now
                    transitionToNext()
                }
            }
            PlayMode.LOOP_ONE -> Unit
        }
    }

    private fun applySettings(fresh: VideoSettings) {
        val old = settings
        settings = fresh
        val needsReload = old.videos != fresh.videos ||
            old.trimStartSec != fresh.trimStartSec || old.trimEndSec != fresh.trimEndSec
        player?.let { p ->
            if (needsReload) {
                val current = old.videos.getOrNull(index)
                val keep = fresh.videos.indexOf(current)
                playIndex(if (keep >= 0) keep else 0)
            } else {
                applyPlayerParams(p)
            }
        }
        if (!fresh.fade) { fadeDir = 0; fadeLevel = 1f }
        updatePlayState()
        requestDraw()
    }

    // ---------------------------------------------------------------- drawing

    private fun requestDraw(delayMs: Long = 0) {
        handler.removeCallbacks(drawRunnable)
        if (delayMs > 0) handler.postDelayed(drawRunnable, delayMs) else handler.post(drawRunnable)
    }

    private fun draw() {
        if (eglSurface == EGL14.EGL_NO_SURFACE) return
        val st = surfaceTexture ?: return
        if (frameAvailable) {
            frameAvailable = false
            st.updateTexImage()
            st.getTransformMatrix(texMatrix)
            hasFrame = true
        }

        val half = (settings.fadeMs / 2).coerceAtLeast(1)
        if (fadeDir != 0) {
            val t = ((SystemClock.uptimeMillis() - fadeStart).toFloat() / half).coerceIn(0f, 1f)
            fadeLevel = if (fadeDir > 0) t else 1f - t
            if (t >= 1f) {
                val wasFadingOut = fadeDir < 0
                fadeDir = 0
                if (wasFadingOut) advance()
            }
        }

        GLES20.glViewport(0, 0, surfaceW, surfaceH)
        GLES20.glClearColor(0f, 0f, 0f, 1f)
        GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT)

        if (hasFrame && program != 0) {
            GLES20.glUseProgram(program)
            val (sx, sy) = scale()
            GLES20.glUniform2f(GLES20.glGetUniformLocation(program, "uScale"), sx, sy)
            GLES20.glUniformMatrix4fv(GLES20.glGetUniformLocation(program, "uTexM"), 1, false, texMatrix, 0)
            val brightness = (1f - settings.dim.coerceIn(0f, 0.9f)) * fadeLevel
            GLES20.glUniform1f(GLES20.glGetUniformLocation(program, "uBright"), brightness)

            val aPos = GLES20.glGetAttribLocation(program, "aPos")
            val aTex = GLES20.glGetAttribLocation(program, "aTex")
            GLES20.glEnableVertexAttribArray(aPos)
            GLES20.glVertexAttribPointer(aPos, 2, GLES20.GL_FLOAT, false, 0, QUAD_POS)
            GLES20.glEnableVertexAttribArray(aTex)
            GLES20.glVertexAttribPointer(aTex, 2, GLES20.GL_FLOAT, false, 0, QUAD_TEX)

            GLES20.glActiveTexture(GLES20.GL_TEXTURE0)
            GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, textureId)
            GLES20.glUniform1i(GLES20.glGetUniformLocation(program, "uTex"), 0)
            GLES20.glDrawArrays(GLES20.GL_TRIANGLE_STRIP, 0, 4)

            GLES20.glDisableVertexAttribArray(aPos)
            GLES20.glDisableVertexAttribArray(aTex)
        }

        EGL14.eglSwapBuffers(eglDisplay, eglSurface)

        // Keep animating while a fade is running.
        if (fadeDir != 0) requestDraw(16)
    }

    /** How much to stretch the unit quad so the video fills (crops) or fits (letterboxes) the screen. */
    private fun scale(): Pair<Float, Float> {
        if (videoW <= 0f || videoH <= 0f || surfaceW <= 0 || surfaceH <= 0) return 1f to 1f
        val videoAspect = videoW / videoH
        val screenAspect = surfaceW.toFloat() / surfaceH
        val videoIsWider = videoAspect > screenAspect
        return if (settings.fill) {
            if (videoIsWider) (videoAspect / screenAspect) to 1f else 1f to (screenAspect / videoAspect)
        } else {
            if (videoIsWider) 1f to (screenAspect / videoAspect) else (videoAspect / screenAspect) to 1f
        }
    }

    private fun setupGl(surface: Surface) {
        eglDisplay = EGL14.eglGetDisplay(EGL14.EGL_DEFAULT_DISPLAY)
        val version = IntArray(2)
        check(EGL14.eglInitialize(eglDisplay, version, 0, version, 1)) { "eglInitialize failed" }

        val configAttribs = intArrayOf(
            EGL14.EGL_RED_SIZE, 8, EGL14.EGL_GREEN_SIZE, 8, EGL14.EGL_BLUE_SIZE, 8,
            EGL14.EGL_RENDERABLE_TYPE, EGL14.EGL_OPENGL_ES2_BIT,
            EGL14.EGL_NONE,
        )
        val configs = arrayOfNulls<EGLConfig>(1)
        val count = IntArray(1)
        check(EGL14.eglChooseConfig(eglDisplay, configAttribs, 0, configs, 0, 1, count, 0) && count[0] > 0) {
            "No EGL config"
        }
        val config = configs[0]!!
        eglContext = EGL14.eglCreateContext(
            eglDisplay, config, EGL14.EGL_NO_CONTEXT,
            intArrayOf(EGL14.EGL_CONTEXT_CLIENT_VERSION, 2, EGL14.EGL_NONE), 0,
        )
        eglSurface = EGL14.eglCreateWindowSurface(eglDisplay, config, surface, intArrayOf(EGL14.EGL_NONE), 0)
        check(eglSurface != EGL14.EGL_NO_SURFACE) { "eglCreateWindowSurface failed" }
        check(EGL14.eglMakeCurrent(eglDisplay, eglSurface, eglSurface, eglContext)) { "eglMakeCurrent failed" }
        attachedSurface = surface

        program = buildProgram()
        val tex = IntArray(1)
        GLES20.glGenTextures(1, tex, 0)
        textureId = tex[0]
        GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, textureId)
        GLES20.glTexParameteri(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_LINEAR)
        GLES20.glTexParameteri(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR)
        GLES20.glTexParameteri(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE)
        GLES20.glTexParameteri(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE)

        val st = SurfaceTexture(textureId)
        st.setOnFrameAvailableListener({
            frameAvailable = true
            requestDraw()
        }, handler)
        surfaceTexture = st
        decoderSurface = Surface(st)
        hasFrame = false
        android.opengl.Matrix.setIdentityM(texMatrix, 0)
    }

    private fun teardownGl() {
        decoderSurface?.release()
        decoderSurface = null
        surfaceTexture?.release()
        surfaceTexture = null
        if (eglDisplay != EGL14.EGL_NO_DISPLAY) {
            if (program != 0) GLES20.glDeleteProgram(program)
            if (textureId != 0) GLES20.glDeleteTextures(1, intArrayOf(textureId), 0)
            EGL14.eglMakeCurrent(eglDisplay, EGL14.EGL_NO_SURFACE, EGL14.EGL_NO_SURFACE, EGL14.EGL_NO_CONTEXT)
            if (eglSurface != EGL14.EGL_NO_SURFACE) EGL14.eglDestroySurface(eglDisplay, eglSurface)
            if (eglContext != EGL14.EGL_NO_CONTEXT) EGL14.eglDestroyContext(eglDisplay, eglContext)
            EGL14.eglReleaseThread()
        }
        program = 0
        textureId = 0
        eglSurface = EGL14.EGL_NO_SURFACE
        eglContext = EGL14.EGL_NO_CONTEXT
        attachedSurface = null
        hasFrame = false
    }

    private fun buildProgram(): Int {
        fun compile(type: Int, src: String): Int {
            val shader = GLES20.glCreateShader(type)
            GLES20.glShaderSource(shader, src)
            GLES20.glCompileShader(shader)
            val ok = IntArray(1)
            GLES20.glGetShaderiv(shader, GLES20.GL_COMPILE_STATUS, ok, 0)
            check(ok[0] != 0) { "Shader error: " + GLES20.glGetShaderInfoLog(shader) }
            return shader
        }
        val vs = compile(GLES20.GL_VERTEX_SHADER, VERTEX_SHADER)
        val fs = compile(GLES20.GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
        val prog = GLES20.glCreateProgram()
        GLES20.glAttachShader(prog, vs)
        GLES20.glAttachShader(prog, fs)
        GLES20.glLinkProgram(prog)
        val ok = IntArray(1)
        GLES20.glGetProgramiv(prog, GLES20.GL_LINK_STATUS, ok, 0)
        check(ok[0] != 0) { "Link error: " + GLES20.glGetProgramInfoLog(prog) }
        GLES20.glDeleteShader(vs)
        GLES20.glDeleteShader(fs)
        return prog
    }

    /** Runs [block] on the render thread and waits for it (needed when the surface is going away). */
    private fun runSync(block: () -> Unit) {
        if (Looper.myLooper() == thread.looper) {
            block()
            return
        }
        if (!thread.isAlive) return
        val latch = CountDownLatch(1)
        handler.post {
            try { block() } finally { latch.countDown() }
        }
        latch.await(3, TimeUnit.SECONDS)
    }

    private companion object {
        const val TAG = "HorizonVideo"

        const val VERTEX_SHADER = """
            attribute vec4 aPos;
            attribute vec4 aTex;
            uniform mat4 uTexM;
            uniform vec2 uScale;
            varying vec2 vTex;
            void main() {
                gl_Position = vec4(aPos.xy * uScale, 0.0, 1.0);
                vTex = (uTexM * aTex).xy;
            }
        """

        const val FRAGMENT_SHADER = """
            #extension GL_OES_EGL_image_external : require
            precision mediump float;
            varying vec2 vTex;
            uniform samplerExternalOES uTex;
            uniform float uBright;
            void main() {
                vec4 c = texture2D(uTex, vTex);
                gl_FragColor = vec4(c.rgb * uBright, 1.0);
            }
        """

        val QUAD_POS: FloatBuffer = floatBuffer(-1f, -1f, 1f, -1f, -1f, 1f, 1f, 1f)
        val QUAD_TEX: FloatBuffer = floatBuffer(0f, 0f, 1f, 0f, 0f, 1f, 1f, 1f)

        fun floatBuffer(vararg v: Float): FloatBuffer =
            ByteBuffer.allocateDirect(v.size * 4).order(ByteOrder.nativeOrder()).asFloatBuffer().apply {
                put(v)
                position(0)
            }
    }
}
