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
