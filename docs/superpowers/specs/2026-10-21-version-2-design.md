# Free My TV Thai 2.0

## Purpose and requirements

Publish the latest working Thai adaptation of Free My TV as `SMOKEx2/free-my-tv-thai`, a public MIT repository that another person can hand to an AI assistant. Keep upstream attribution. All installation documentation and AI instructions are in English. Never distribute the owner's TMDB credential, signing key, private config, device address, ADB authorization, or recovery backup.

The Android package remains `io.freemytv`, minSdk 28, targetSdk 34. Set versionName to 2.0 and versionCode to 2. Under the version text on the settings screen, show `แปลไทยโดย FB : Kiw Kiattisak` in Thai and `Thai translation by FB : Kiw Kiattisak` in English. Preserve Thai fonts, translated recommendations, PNG path correction, the existing rendering fallbacks, screensavers, and watchdog.

## Installer and bundled tools

Builder decision: Windows x64 is the supported ready-to-run host, matching the development machine. Commit actual portable tool files as a checksum-verified archive under `tools/bundles/`, including a compact OpenJDK 17 runtime with javac/keytool/jar, AOSP Android build tools/API stubs, ADB, embedded Python, and their notices. Keep every Git object below GitHub's 100 MB limit. No manual tool downloads, global PATH changes, admin rights, WSL, Git Bash, Android Studio, Gradle, pip, or paid services are required. Source builders on other hosts can use an existing SDK/JDK through explicit options; do not claim bundled support there.

Use PowerShell/CMD entrypoints and standard-library Python for native builds and interactive installation. Before TV mutations, ask language, city/coordinates, country, units, the user's own optional TMDB key, which installed apps and order to place in the dock, and whether optional Xiaomi ad/analytics cleanup should run. Secure key entry stays local. Prompt for network debugging authorization/pairing only as required by the TV. Never clear app data or uninstall on signature mismatch.

Support any count of unique, installed TV apps, including more than seven, with seven visible per dock page and D-pad navigation across pages. A missing configuration opens the shelf picker. Existing on-TV shelf preferences win over compiled defaults.

## Xiaomi cleanup and recovery

Use only the ad/analytics parts of cleanyourtv's Mi Box profiles as research. Do not copy its unrelated app removals or launcher. Gate Xiaomi-specific packages on detected manufacturer/brand, use exact package IDs, skip absent/protected/selected apps and Wi-Fi owners, and leave Assistant, casting, Bluetooth, pairing, settings, updates, DRM, Play services, streaming apps, and accessibility enabled. The stock launcher/setup handling already required for Home is distinct from optional ad cleanup. Do not disable Xiaomi quick settings based on an unverified telemetry label.

Every disable is reversible (`pm disable-user --user 0`, never uninstall). Preserve packages already disabled before setup. Journal each successful mutation immediately. Restore the recorded enabled/default states, Home, and screensaver; retain recovery records on partial failure. The app's Original action restores app-owned changes. The computer installer also creates an ignored emergency recovery snapshot before installation/activation.

## Validation and scope

Test installer selection validation, subprocess isolation, missing/unauthorized devices, device-specific restore safeguards, Wi-Fi ownership protection, protected packages, interrupted/partial restore, build input escaping, API-key hygiene, raw ZIP path names, paged dock boundaries, version/credit, and Thai/English configuration. Build and verify a public APK with an empty TMDB key. Inspect the committed tree and binary archive for secrets. Record hardware evidence separately: the latest predecessor was tested on MiTV-AFMU0/Android 14; 2.0 must not be called hardware-tested without a fresh device run. Mi Box 3/Android 9 and Box S generations retain API and rendering fallbacks but require firmware-specific testing.

The owner selected the public repository name. Routine implementation decisions and source packaging are authorized by the request. Keep the old personalized installation and its private files outside this repository.
