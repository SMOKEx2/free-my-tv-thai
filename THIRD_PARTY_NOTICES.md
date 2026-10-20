# Attribution, licenses and corresponding source

The app adaptation and new setup scripts are distributed under the [MIT license](LICENSE). Third-party components retain their own licenses; the MIT license does not replace those terms.

## Original app and research

- [Free My TV](https://github.com/simbasjungles/free-my-tv), MIT, Copyright (c) 2026 Free My TV contributors. This repository retains that copyright/license and adapts its native Java launcher/screensaver/settings. This is an independent adaptation.
- Thai adaptation and translation credit: **FB : Kiw Kiattisak**. The app displays the credit in Thai/English below its version.
- [cleanyourtv Mi Box profiles](docs/MI_BOX_ADS.md) were consulted only for package identities, ad/analytics purposes, Wi-Fi and recovery caveats. Its other launcher/features/general debloat are not included.

## Fonts and symbols

- Inter variable font, SIL Open Font License 1.1. License: app/assets/fonts/OFL.txt. [Upstream](https://github.com/rsms/inter).
- Noto Sans Thai variable font, SIL Open Font License 1.1. License: app/assets/fonts/NotoSansThai-OFL.txt. [Upstream source and metadata](https://github.com/google/fonts/tree/main/ofl/notosansthai).
- Material Symbols Rounded rendered PNGs, Apache License 2.0. Notice: app/assets/symbols/LICENSE-material-symbols.txt. [Upstream](https://github.com/google/material-design-icons).

No Apple proprietary typeface is bundled. The visual style is inspired by TV/iOS typography and glass interfaces.

## Included Windows tool archive

The version/hash manifest is tools/bundles/windows-x64.json. Notices below are included as actual files inside windows-x64.zip and extracted beside their components.

### Eclipse Temurin / OpenJDK

Version **17.0.20.1+1**, Windows x64, compact jlink runtime with the Java compiler and signing/jar tools. OpenJDK is distributed under **GPL version 2 with the Classpath Exception**, with per-module additional notices. All selected-module legal/ files and release metadata are retained inside java/.

Exact official binary release: [Adoptium jdk-17.0.20.1+1](https://github.com/adoptium/temurin17-binaries/releases/tag/jdk-17.0.20.1%2B1).

**Complete corresponding source for the bundled OpenJDK version is also provided as an unmodified archive with this project's v2.0 release:** [OpenJDK17U-jdk-sources_17.0.20.1_1.tar.gz](https://github.com/SMOKEx2/free-my-tv-thai/releases/download/v2.0/OpenJDK17U-jdk-sources_17.0.20.1_1.tar.gz). The [official upstream source archive](https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.20.1%2B1/OpenJDK17U-jdk-sources_17.0.20.1_1.tar.gz) is an additional source mirror. tools/package_toolchain.py contains the exact jlink module/options used to assemble the subset. Keep access to the corresponding source and these notices when redistributing the tool archive.

### CPython

Official **CPython 3.14.8** Windows x64 embeddable package from [python.org](https://www.python.org/ftp/python/3.14.8/python-3.14.8-embed-amd64.zip). Python's PSF license and bundled third-party notices remain in python/LICENSE.txt. The only configuration change is a relative tools/ entry added to python314._pth so the local scripts can import each other. [CPython source](https://www.python.org/ftp/python/3.14.8/Python-3.14.8.tar.xz).

### Android Open Source Project tools and API stubs

Selected open-source AOSP components from Android build-tools **34.0.0**, platform **android-34**, and platform-tools **37.0.1**: aapt2, D8/R8, apksigner, zipalign, ADB, support DLLs and compile-time android.jar. Their full distribution NOTICE.txt files are retained under sdk/build-tools/34.0.0, sdk/platforms/android-34, and platform-tools. These include Apache 2.0 and component-specific third-party notices.

Sources: [AAPT2](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/tools/aapt2/), [R8/D8](https://r8.googlesource.com/r8/), [apksigner](https://android.googlesource.com/platform/tools/apksig/), [zipalign](https://android.googlesource.com/platform/build/+/refs/heads/main/tools/zipalign/), [ADB](https://android.googlesource.com/platform/packages/modules/adb/), [Android framework](https://android.googlesource.com/platform/frameworks/base/). Official distribution source: [Google Android repository](https://dl.google.com/android/repository/repository2-1.xml).

Only the open-source tools/API stubs needed here are redistributed, with notices. The full Android Studio/SDK manager package, proprietary Google API add-ons, emulator/system images and platform signing keys are not bundled. Android's [SDK terms](https://developer.android.com/studio/terms) distinguish open-source components governed by their own licenses (section 3.5). Preserve all component notices when sharing the bundle.

## Online services

The app can use TMDB for recommendations and Open-Meteo for weather/geocoding. They are external services with their own terms and availability; no account, entitlement or credential is supplied by this repository. App TMDB attribution is retained. This product uses the TMDB API but is not endorsed or certified by TMDB.
