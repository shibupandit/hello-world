# Horizon Launcher

A redesigned home screen for Android. It replaces your phone's home screen and app drawer.
You don't need root, nothing gets wiped, and you can switch back to your old launcher any time.

## Features

- Big clock with the date and a greeting, shown over your own wallpaper
- A dock with up to 5 pinned apps and an accent-coloured app drawer button
- Full-screen app drawer: swipe up from the home screen, search as you type, press Go to open the top result
- Hold any app for **Pin to dock / App info / Uninstall**
- Hold an empty spot on the home screen for settings: accent colour (6 choices), 24-hour clock, drawer columns (3–6), wallpaper, default home app
- Pressing Home always brings you back to the home page; Back closes the drawer

## Video wallpaper

Use your own videos as a moving wallpaper on the home screen and lock screen.
Open it from Horizon's settings (hold the home screen, then tap **Video wallpaper**). Then:

1. Tap **Add videos** and pick one or more videos. MP4 loops under a minute are best for battery.
2. Adjust the settings (listed below). Changes apply straight away.
3. Tap **Set as wallpaper**, then choose **Home screen and lock screen**.

Settings:

- **Playback:** speed from 0.25× to 2×, start and stop points, mute
- **Order and timing:** loop one video, play all in order, or switch every 1–60 minutes; shuffle
- **Transitions:** fade between videos, 0.2–3 s
- **Look:** fill the screen (crop) or fit the whole video; dim up to 80 %
- **When to play:** on the lock screen, pause while the app drawer is open, pause in battery saver, or freeze 5/10/30 s after unlocking
- **Idle screen:** the same videos as Android's screen saver while the phone charges (Settings › Display › Screen saver › Horizon Video)

The video always pauses while an app is open or the screen is off, so it doesn't drain the battery in the background.
Android doesn't let apps change the boot animation or the unlock animation without root.

## Install on your phone

1. On your phone, open this repository's **Releases** page on GitHub and pick the newest *Horizon Launcher (build N)*.
2. Tap **Horizon-Launcher.apk** to download it, then open the file.
3. If Android asks, allow your browser or file manager to **install unknown apps**, then tap **Install**.
4. Press the **Home** button. When Android asks which app to use, choose **Horizon** and tap **Always**.
   If it doesn't ask, go to *Settings → Apps → Default apps → Home app* and pick **Horizon**.

Every push builds a new APK through GitHub Actions (`.github/workflows/build-apk.yml`).
Builds are signed with the same key each time, so a newer build installs over an older one.

### Switching back

Go to *Settings → Apps → Default apps → Home app* and pick your previous launcher.
Or uninstall Horizon and Android goes back to its own launcher.

## Building locally

You need Android Studio, or JDK 17 plus the Android SDK (platform 35). Then run:

```
./gradlew assembleRelease
```

The APK is written to `app/build/outputs/apk/release/app-release.apk`.

## Code map

| File | What it does |
|---|---|
| `app/src/main/AndroidManifest.xml` | Registers the app as a HOME launcher |
| `MainActivity.kt` | Entry point; refreshes the app list on resume |
| `AppRepository.kt` | Reads installed apps and their icons |
| `LauncherViewModel.kt` | State and saved settings (dock, accent, clock, columns) |
| `ui/HomeScreen.kt` | Clock, greeting, dock, gestures |
| `ui/AppDrawer.kt` | Searchable app grid and the app long-press menu |
| `ui/SettingsSheet.kt` | Settings panel |
| `ui/Theme.kt` | Colours and the text style used over the wallpaper |
| `wallpaper/VideoWallpaperService.kt` | The live wallpaper Android runs |
| `wallpaper/VideoRenderer.kt` | Video playback (Media3 ExoPlayer) and OpenGL drawing: fit/fill, dim, fades |
| `wallpaper/VideoDreamService.kt` | The screen saver |
| `wallpaper/VideoWallpaperActivity.kt` | Video wallpaper settings screen |
| `wallpaper/VideoSettings.kt` | Saved video wallpaper settings |
