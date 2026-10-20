# Installation guide

This guide is for Windows 10/11 x64. All required build/install tool files are already inside the repository. Internet is needed to download the repository, obtain your own optional TMDB key, and use online recommendations/weather. Building from the downloaded repository works without a separate tool download.

## 1. Ask the owner before touching the TV

An AI assistant must collect these answers first. Do not assume the author's apps, city, key, or preferences apply to someone else.

1. What is the exact TV/box model and Android version? Is this a Mi Box 3, Box S first/second generation, or TV Box S third generation?
2. Which language should the UI use: Thai, English, or the TV's language automatically?
3. Which city/country should weather, sunrise/sunset, and available streaming services use? Which temperature units?
4. Do you want TMDB recommendations? If yes, create your own key and enter it **locally and privately**. If no, leave it empty.
5. After reading the installed-app list, which apps should appear in the dock, and in what order? Choose **one, seven, or any number**. Do not choose apps that are not installed.
6. Do you want the optional Xiaomi ad/analytics cleanup? Show the exact candidate packages and explain that it uses reversible disable operations. Default is no.
7. Confirm Assistant/microphone, Chromecast, phone remote, Bluetooth pairing, firmware updates, accessibility and streaming apps should remain available. This project keeps them by default.
8. Is another Free My TV already installed? Preserve its signing key and original recovery backup. Do not uninstall it to resolve a signature mismatch.

Ask about an unanswered item once, then continue work that does not depend on it. Do not claim the owner accepted a choice merely because they did not reply.

## 2. Get the repository

1. Open [SMOKEx2/free-my-tv-thai](https://github.com/SMOKEx2/free-my-tv-thai).
2. Choose **Code → Download ZIP** and extract the whole archive to a writable folder, such as `Documents\FreeMyTVThai`.
3. Keep the `app`, `tools`, tests and scripts together. Do not run from inside the ZIP or a protected Program Files directory.
4. The included `tools/bundles/windows-x64.zip` is a real binary tool archive, not a Git LFS pointer or a download shortcut. Keep it and its JSON checksum manifest together.

Alternatively, an existing Git client can clone the repository. Git itself is not needed to use the downloaded ZIP.

## 3. Prepare the TV

1. Connect the computer and box to the same trusted local network. Guest Wi-Fi/client isolation may prevent ADB connections.
2. On Xiaomi/Google TV: **Settings → System / Device Preferences → About**.
3. Select **Android TV OS build / Build** and press OK about seven times until developer mode is enabled.
4. Go back to **Developer options** and enable **USB debugging**. If your firmware offers **Network debugging / ADB debugging**, enable it too.
5. Find the TV's IP address in **Network & Internet → connected network**. Keep the TV awake.
6. Many Mi Box versions expose ADB at `TV_IP:5555` when USB debugging is enabled. This varies by firmware; do not expose port 5555 on the internet or configure router port forwarding.
7. Accept **Allow USB debugging?** on the TV and select **Always allow from this computer** if you trust this computer.

If your firmware uses **Wireless debugging → Pair device with pairing code**, the pairing port and connection port are different. Pair first, then connect to the connection address shown by the TV:

```powershell
.\setup.cmd --probe --pair TV_IP:PAIRING_PORT --connect TV_IP:CONNECTION_PORT
```

The code is requested privately. For the classic Mi Box connection:

```powershell
.\setup.cmd --probe --connect TV_IP:5555
```

Replace placeholders with the owner's values. Never guess an unrelated LAN device. If more than one ADB device is present, add `--device EXACT_ADB_SERIAL` to every device command.

## 4. Run the guided setup

Double-click `setup.cmd`, or open PowerShell in the extracted directory:

```powershell
.\setup.cmd --connect TV_IP:5555
```

The launcher runs PowerShell for this process, validates the included archive, extracts tools into `.local/toolchain`, verifies each extracted file, and starts the bundled Python installer. It does not change your global execution policy, PATH, or install system-wide software. If local policy blocks the wrapper, use your organization's approved way to run the included script; do not disable security software globally.

If no TV is connected yet, a double-click run asks for the debugging address from TV Settings. Offline or unauthorized devices still stop safely.

Follow the prompts:

- **Language:** enter `th`, `en`, or `auto`.
- **City:** the installer queries Open-Meteo geocoding and asks you to select the matching location. If unavailable, enter latitude and longitude manually.
- **Country:** use a two-letter country code, for example `TH`, `US`, or `GB`. This controls streaming availability.
- **Temperature:** choose `C`, `F`, or `auto`.
- **TMDB:** enter your own optional API key using the hidden local prompt. Input is not echoed. Enter without a saved key skips recommendations.
- **Dock:** read the installed TV app list and enter app numbers in the desired order, such as `3,1,6,2`. The installer removes duplicate selections. More than seven apps are split into dock pages, reached by continuing Left/Right on the remote.
- **Ads:** on detected Xiaomi hardware, choose whether to disable the listed ad/analytics candidates. Review [the package policy](docs/MI_BOX_ADS.md). Default is no.

The installer saves private `config.properties`, builds and verifies your APK, saves an emergency backup, installs it, and opens Free My TV settings. No uninstall or data clear is performed.

### Entering your own TMDB key

Create an account at [TMDB](https://www.themoviedb.org/), open **Settings → API**, follow TMDB's current application process and terms, and obtain an API key. Use the API key field in the hidden installer prompt. Keep the key out of chat messages, screenshots, terminal history, commits, issues and shared APKs.

If you prefer editing a file, copy `config.example.properties` to ignored `config.properties` and fill `tmdb_key=` locally. Do not run a command that prints the file. Do not ask an AI assistant to include the key in generated documentation. No key belonging to this repository's owner is included or needed.

## 5. Activate on the TV

1. In Free My TV settings, choose **Home Screen → Free My TV**. In Thai, use **หน้าโฮม → Free My TV**.
2. The app asks to authorize its own local debugging connection. Accept the TV prompt if you intend to activate it. Computer authorization and app authorization are separate.
3. The app switches Home and screensaver, and records the package states it changes. If optional cleanup was selected, eligible advertising/analytics packages are disabled too.
4. On Google TV, setupwraith's recovery Home can otherwise take over after disabling launcherx. The app handles this and checks Wi-Fi ownership first.
5. If it says the initial setup saved the Wi-Fi, it stops before changing packages. In TV **Network & Internet**, forget and rejoin that network so it is saved by Settings, then retry. Never disable a package that owns a saved Wi-Fi network: Android can delete those networks immediately. Do not have AI erase saved networks without the owner's specific consent.
6. When complete, press Home. Open each chosen dock app, test the remote, Wi-Fi, audio, Bluetooth, casting and standby/wake. If the box uses a startup prompt, select Free My TV as the default Home.

Changing Home requires a legitimate TV authorization; the installer does not bypass Android's prompts. Do not disable Play Protect to force an installation. Investigate any warning or failed signature instead.

## 6. Verify and test reboot persistence

```powershell
.\setup.cmd --verify --device EXACT_ADB_SERIAL
```

This checks the resolved Home and selected screensaver, then saves a local screenshot in `.local/verification/home.png`. Inspect it for icons, Thai/English text, dock order, clipping, and poster loading. ADB reporting success alone is not a visual test. Recommendation images may take some time on the first run, and require a working own TMDB key.

Ask the owner before interrupting their viewing with a reboot. After the box restarts, reconnect if its IP changed, press Home and verify again. Distinguish standby/wake from a full power-cycle. Do not claim reboot persistence was tested if you only checked the default Home setting.

## 7. AI-assisted / noninteractive steps

After the owner answers the checklist, an assistant can perform these concrete steps:

```powershell
.\setup.cmd --probe --connect TV_IP:5555
# Create ignored config.properties from the owner's answers; the owner enters the key locally.
.\setup.cmd --build-only
.\setup.cmd --self-test
.\setup.cmd --install --device EXACT_ADB_SERIAL --config config.properties
# Guide on-TV activation, then:
.\setup.cmd --verify --device EXACT_ADB_SERIAL
```

The `--install` action requires chosen, installed shelf packages. It saves a fresh private backup before installation. The assistant must not replace the user's choices with the author's seven apps. Never commit the local config, generated Config.java, `.local`, APK, ADB keys, or backup JSON.

## 8. Upgrades and signing keys

Each local install generates its own `.local/signing/freemytv.keystore`. Back up this directory privately. Android only accepts in-place updates signed with the same key. Keep the same folder/config when building a later version.

If updating an earlier personal build, place its existing compatible `freemytv.keystore` at `.local/signing/freemytv.keystore` **before building**. The original build uses alias/password `freemytv`; custom keys may require adapting the signing invocation locally. This repository never includes the author's signing key.

For `INSTALL_FAILED_UPDATE_INCOMPATIBLE`, stop. Locate the earlier key or explain the mismatch. Do not automatically uninstall the app, clear its data, or overwrite the only recovery/signing backup. Existing on-TV shelf preferences take priority over new compiled defaults; edit **Shelf / แถบแอป** on the TV to change them after an upgrade.

## 9. Undo and troubleshoot

Use **Home Screen → Original** in the app to restore its recorded Home/screensaver/package states. Keep Free My TV installed until recovery completes. For an emergency, see [RECOVERY.md](docs/RECOVERY.md).

| Problem | Next step |
| --- | --- |
| No devices / connection refused | Check TV IP/port, debugging, shared network and awake state. Do not scan internet addresses. |
| Unauthorized | Accept the TV's debugging dialog; reconnect. |
| Several devices | Supply `--device` with the intended TV's exact ADB serial. |
| No network after Home switch | The app should block Wi-Fi-owner disables. Recover from the TV settings; do not repeat disabling setup blindly. |
| Tool checksum mismatch | Re-extract the repository or included bundle. Do not run an unverified executable. |
| Missing icons/fonts | Build with included tooling; tests check raw APK ZIP asset names for Windows backslashes. |
| No posters | Verify the owner's local TMDB key/country and network; the dock still works without it. |
| Android below API 28 | This build is unsupported. Update through official firmware if available; do not bypass minSdk. |
| Old Mi Box USB port stops powering a drive | Some firmware switches USB mode when debugging is on. See the compatibility notes; keep recovery implications in mind before turning debugging off. |

## Source builds on other hosts

The bundled binaries and guided bootstrap support **Windows x64 only**. macOS/Linux users with Python 3.10+, JDK 17 and Android SDK platform/build-tools 34 installed can build using:

```bash
python3 tools/build.py --sdk-root "$ANDROID_HOME" --java-home "$JAVA_HOME"
```

This is a source-build route, not a claim of bundled macOS/Linux tooling or hardware testing. Preserve all local signing/config/recovery files, and follow the same questions and TV authorization steps.
