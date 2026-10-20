# Give this prompt to your AI assistant

Copy the following into an assistant that can read files and run local commands. Use a local coding assistant, not a chat-only bot. Start from this repository. Do not paste credentials into the prompt.

---

Help me install **Free My TV Thai 2.0** from https://github.com/SMOKEx2/free-my-tv-thai on my own Android TV / Mi Box. Read `README.md`, `INSTALL.md`, `AGENTS.md`, `docs/MI_BOX_ADS.md`, and `docs/RECOVERY.md` first. Build this repository's latest source; do not substitute another launcher. Preserve Thai/English support and the Kiw Kiattisak translation credit.

### Ask these questions before device mutations

1. What exact box/TV model and Android version do I have? Ask me to keep it awake and tell you the IP/debugging address if discovery is insufficient.
2. Should the interface be **Thai**, **English**, or **automatic**?
3. Which **city, country and temperature units** should weather/sunset and streaming availability use? Confirm the location if several cities match.
4. Do I want recommendations? Explain that I must obtain **my own optional TMDB API key**. Tell me how to enter it in the local hidden installer prompt or ignored config file. **Do not ask me to paste the key in chat, echo it, or print config.properties.** No recommendations is a valid choice.
5. After a read-only inventory, show the actual installed TV apps. Ask: **Which apps, in which order, should appear on your Home dock? You can choose one, seven, or any number.** Do not assume the repository author's favorite apps. More than seven are paged, not discarded.
6. Ask whether I want the optional **Xiaomi ad/analytics cleanup**. Show exact present candidates from the documented conservative profile. Default to no. Keep Assistant/microphone, Chromecast/phone remote, Bluetooth pairing, Wi-Fi, firmware updates, DRM, accessibility and streaming apps.
7. Ask whether Free My TV is already installed. Find and preserve its existing signing key and original recovery backup before attempting an update. A signature mismatch is a stop condition, not permission to uninstall.

### Prepare and install

- The Windows x64 tool files are already in `tools/bundles/windows-x64.zip`; this is an actual binary archive with a SHA-256 manifest. Use `setup.cmd` / `setup.ps1` to verify and extract them. Do not tell me to download Java, Python, adb, Android Studio, WSL, Gradle or pip separately.
- First run `setup.cmd --probe --connect TV_IP:PORT`. Handle unauthorized/offline/multiple devices explicitly; use `--device EXACT_ADB_SERIAL`. If the TV uses wireless pairing, use `--pair` with its pairing address, then connect to its separate connection address. Guide me through the TV authorization dialog.
- Collect my answers. Use the interactive installer or populate **ignored local** `config.properties`; let me enter my key privately. Do not overwrite my existing config or signing material without understanding it.
- Build with `setup.cmd --build-only`; test with `setup.cmd --self-test`. The native build handles UTF-8 Java, Windows paths and raw ZIP asset names. It signs with my private local key.
- Run `setup.cmd --install --device EXACT_ADB_SERIAL --config config.properties`. Keep the generated emergency snapshot. The installer never uninstalls apps or clears their data.
- Explain the on-TV activation action, then guide me to **Home Screen → Free My TV** and its own local debugging authorization. Do not bypass authorization or disable security software to get it working.
- Never disable a package that owns a saved Wi-Fi network. If setupwraith owns Wi-Fi, stop and guide me to forget/rejoin that network in TV Settings before retrying. Obtain explicit consent before removing any saved network, especially one not currently visible.
- Disable only exact, present, unprotected, user-approved ad candidates through the app's journaled mode switch. Do not copy the broad optional removals from other debloat lists. Never uninstall, clear system app data, remove account/network/display settings, or disable updates/casting/pairing.

### Verify honestly

Run `setup.cmd --verify --device EXACT_ADB_SERIAL` and **inspect the local screenshot**. Check version 2.0 and the Thai/English translation credit in settings. Check all selected dock apps, Left/Right across pages, Up/Down, settings, icons, Thai vowel/tonemark rendering, posters when a key is provided, screensaver, Wi-Fi, audio, remote shortcuts, Bluetooth and casting. Ask me before rebooting or interrupting playback. After an authorized reboot, verify again. Keep older untested Mi Box firmware explicitly marked untested.

If the TV is unreachable, continue local build/tests/docs but say that hardware validation could not be completed. Never report a command as successful merely because a process launched. Do not repeatedly mutate settings while disconnected.

### Recovery and final report

Prefer **Home Screen → Original** while the app remains installed. Emergency restore is `setup.cmd --restore PATH_TO_MY_BACKUP.json --device EXACT_ADB_SERIAL`; it refuses a different device/firmware. Preserve pending failures and backups. Do not uninstall Free My TV before undoing its changes.

Finish with what was installed, my selected language/apps, what cleanup actually changed, the verification performed, any untested behavior, and the private paths I must back up. Keep my TMDB key, APK containing it, signing key, ADB authorization, device IDs and recovery snapshots out of public commits/issues/messages.

---
