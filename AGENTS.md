# Instructions for coding/installing assistants

Read README.md, INSTALL.md, PROMPT.md, docs/MI_BOX_ADS.md and docs/RECOVERY.md. Ask the installation questions before device changes. Do not replace this app with another launcher.

- This repository must contain **no personal TMDB credential**. config.example.properties stays empty at tmdb_key. Never print the user's config, generated Config.java or secret-bearing APK contents. Use hidden local key entry; no chat credential requests.
- Never commit .local, personal config, signing keys, ADB keys, backups, device addresses/identifiers, or APKs. Check staged files before every public push. Do not use a previous owner's key or signing material.
- Windows x64 tools are actual files in tools/bundles. Verify hashes and use setup.cmd; no global tools are required. Preserve licenses/notices. Do not put a file above 100 MB in Git.
- Use exact intended ADB serial. Ambiguous, offline or unauthorized devices are stop conditions for TV changes. Do not reboot during viewing without authorization.
- Do not uninstall or clear data, disable Play Protect, remove Wi-Fi/account settings, or mutate unrelated display/audio/network options. Stop on signature mismatch.
- Do not disable Wi-Fi owners. Only exact present Xiaomi ad IDs from AdPackages may be part of optional cleanup. Keep updates, Chromecast, phone remote, Bluetooth, pairing, DRM, accessibility, Play services and chosen apps. Home/setup disabling required for activation is distinct from ad cleanup and needs its own recovery journal.
- Write recovery state before mutations. Preserve pre-disabled packages and numeric enabled/default states. Keep partial failures pending. Original restores app-owned changes; emergency computer backups are private and device-bound.
- Preserve io.freemytv, minSdk 28, targetSdk 34, Thai/English UI, Noto Sans Thai/OFL and Inter/OFL notices, Windows raw-ZIP normalization, legacy GPU/RenderNode/screensaver fallbacks, and watchdog. Current version is 2.0 / code 2.
- Keep the credit beneath the settings version: Thai `แปลไทยโดย FB : Kiw Kiattisak`, English `Thai translation by FB : Kiw Kiattisak`.
- User selects the dock; never hardcode the author's seven apps as installation defaults. Keep arbitrary counts reachable through seven-tile pages, including accessibility bounds and D-pad transitions.
- Use subprocess argument arrays, validated package/component IDs, UTF-8 files, and escaped generated Java strings. No shell interpolation of user input or credentials.
- Run setup.cmd --build-only and setup.cmd --self-test. Inspect signatures, raw APK asset paths and UI screenshots when a device is available. Label untested hardware honestly; a successful build is not a hardware test.
- Public installation/AI documentation is English. Keep upstream MIT copyright and third-party notices intact.
