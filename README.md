# Free My TV Thai 2.0

A Thai and English adaptation of [Free My TV](https://github.com/simbasjungles/free-my-tv), focused on Xiaomi Mi Box / TV Box S. A native Android TV Home and screensaver, with readable Thai typography, optional movie recommendations, and reversible advertising/analytics cleanup.

**Thai translation by FB : Kiw Kiattisak**

Thai UI credit: **แปลไทยโดย FB : Kiw Kiattisak**

This is an independent adaptation, not an official Xiaomi, Google, Apple, or upstream Free My TV release. The original MIT license and third-party notices are preserved.

## Start here

**Windows 10/11 x64:** download this repository using **Code → Download ZIP**, extract the entire folder, then double-click **`setup.cmd`**. The actual portable ADB, Python, Java compiler/runtime, and Android build files are included in [`tools/bundles/`](tools/bundles/README.md). The script checks their SHA-256 hashes and extracts them locally. No separate tool downloads, Android Studio, WSL, Git Bash, Gradle, pip, or administrator access are required.

Your computer and TV must be on the same local network. Enable USB/network debugging on the TV and authorize your computer. The installer asks for your language, city, country, temperature units, optional **own** TMDB key, dock apps and their order, and optional Xiaomi ad cleanup. Choose one, seven, or any number of installed TV apps; the dock shows seven per page.

- [Detailed installation, upgrades, and troubleshooting](INSTALL.md)
- [Copy-paste prompt for an AI assistant](PROMPT.md) — includes the questions it must ask first
- [Compatibility and actual test coverage](docs/COMPATIBILITY.md)
- [Recovery instructions](docs/RECOVERY.md)
- [What the optional Xiaomi cleanup changes](docs/MI_BOX_ADS.md)
- [Version 2.0 changes](CHANGELOG.md)
- [Tool/font licenses and corresponding source](THIRD_PARTY_NOTICES.md)

## What changed in 2.0

- Thai and English UI, Noto Sans Thai typography, Thai weather/status text, and `th-TH` TMDB recommendations when Thai is selected.
- Translation credit beneath the version in the settings screen, matching the selected language.
- User-selected dock apps, ordered and paged instead of a fixed personal seven-app configuration.
- Native Windows setup/build using the included tool files; Windows APK asset-path normalization fixes missing icons/fonts.
- Optional conservative Xiaomi ad/analytics cleanup. No system apps are uninstalled. Pre-existing disabled states and recovery records are preserved.

## TMDB and privacy

**This repository contains no TMDB API key.** A key is optional; the launcher and app dock work without recommendations. Create your own at [TMDB API settings](https://www.themoviedb.org/settings/api), then enter it privately in the installer or local `config.properties`. Do not paste it into an AI chat. The public example leaves `tmdb_key=` empty.

An APK built with your key contains that key: keep it private. Your configuration, generated source, APKs, signing keys, ADB authorization, TV identifiers and recovery snapshots stay in ignored local paths. Keep `.local/signing/` and `.local/backups/` for upgrades and recovery; never publish them.

## Compatibility in brief

Android TV / Google TV **9 or newer** (minSdk 28, targetSdk 34). Xiaomi TV Box S 3rd Gen / MiTV-AFMU0 on Android 14 is the main target. Android 9–11 keep the upstream rendering and screensaver fallbacks for older Mi Box hardware. A Mi Box 3 still on Android 6/8 cannot install this build. See the compatibility document for what was actually tested; a clean build is not evidence that every firmware was hardware-tested.

For an existing SDK/JDK on another build host, see [source builds](INSTALL.md#source-builds-on-other-hosts). The included ready-to-run binaries are **Windows x64 only**.

## Development

```powershell
.\setup.cmd --build-only
.\setup.cmd --self-test
```

The default build intentionally has no key and no chosen apps; an unconfigured on-TV Home opens the shelf picker. For installation, run the guided setup or supply your own ignored configuration first. App package: `io.freemytv`; version: **2.0**, versionCode **2**.
