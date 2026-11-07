<p align="center">
  <img src="app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png" width="120" alt="ThugTV app icon">
</p>

<h1 align="center">ThugTV for Android</h1>

<p align="center">
  An Android app for <a href="https://thugtv.online/">thugtv.online</a>: open the site full-screen on your phone, with fullscreen video and downloads.
</p>

<p align="center">
  <a href="https://github.com/shibupandit/hello-world/actions/workflows/build-apk.yml">
    <img src="https://github.com/shibupandit/hello-world/actions/workflows/build-apk.yml/badge.svg" alt="Build status">
  </a>
  <img src="https://img.shields.io/badge/Android-5.0%2B-3DDC84?logo=android&logoColor=white" alt="Android 5.0+">
  <img src="https://img.shields.io/badge/version-1.1-E50914" alt="Version 1.1">
</p>

---

## Features

- **Always up to date:** the app loads the live website, so new movies, shows and site updates appear instantly with no app update needed.
- **Fullscreen video:** tap fullscreen on any player and the app switches to landscape and keeps your screen awake.
- **Stays signed in:** logins and cookies are kept between launches.
- **Downloads:** files save to your phone's **Downloads** folder, with a notification when they finish.
- **Fewer pop-ups:** pop-up windows you didn't tap are blocked.
- **Back button:** goes back through pages, just like a browser.
- **Offline screen:** a friendly "Can't connect" page with a **Retry** button when you lose internet.
- **Opens links:** thugtv.online links shared from other apps open directly in ThugTV.
- **Small:** the APK is only about 60 KB.

## Download & install

1. Go to the [**latest successful build**](https://github.com/shibupandit/hello-world/actions/workflows/build-apk.yml?query=is%3Asuccess) and open the top run.
2. Scroll down to **Artifacts** and download **ThugTV-apk** (you must be signed in to GitHub).
3. Unzip the download to get `ThugTV.apk`.
4. Open the APK on your Android phone. If asked, allow installing apps from this source, then tap **Install**.

> Already have the app? Installing a newer APK updates it in place and keeps you signed in.

## Requirements

- Android 5.0 (Lollipop) or newer
- An internet connection

## Build it yourself

Every push to the app code builds a signed APK automatically with GitHub Actions ([`.github/workflows/build-apk.yml`](.github/workflows/build-apk.yml)). You can also start a build manually from the **Actions** tab with **Run workflow**.

To build on your own computer you need JDK 17, the Android SDK, and Gradle 8.9 or newer:

```bash
gradle assembleRelease
# APK: app/build/outputs/apk/release/app-release.apk
```

Or open the project folder in **Android Studio** and choose **Build → Build APK(s)**.

## Project structure

```
app/
├── build.gradle                     # App config: package name, version, signing
├── release.keystore                 # Signing key for release builds
└── src/main/
    ├── AndroidManifest.xml          # Permissions, launcher activity, link handling
    ├── java/online/thugtv/app/
    │   └── MainActivity.java        # The WebView app
    └── res/                         # Icons, theme, strings
.github/workflows/build-apk.yml      # Automatic APK build
```

## Customizing

| What | Where |
| --- | --- |
| Website address | `HOME_URL` in `MainActivity.java` |
| App name | `app/src/main/res/values/strings.xml` |
| App icon | `app/src/main/res/mipmap-*/ic_launcher*.png` |
| Version | `versionCode` / `versionName` in `app/build.gradle` |

Increase `versionCode` every time you release a new APK so phones accept it as an update.

## A note on signing

Release builds are signed with `app/release.keystore`, and its password is in `app/build.gradle`. Keeping the same key lets new versions install over old ones. Because the key is in the repository, anyone with access to it can sign apps as ThugTV. Before publishing to the Google Play Store, create a new private key and store it in [GitHub Actions secrets](https://docs.github.com/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) instead.

---

<p align="center">Made for <a href="https://thugtv.online/">thugtv.online</a></p>
