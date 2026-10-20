# Compatibility and test evidence

## Supported design

- Native Java Android app, package io.freemytv. Version 2.0 / code 2, minSdk 28 (Android 9), targetSdk 34.
- No app-native ABI dependencies: ARM/ARM64 boxes use the Android runtime. The bundled Windows x64 build tools run on the computer, not on the box.
- Android 9–11 retain the upstream Ui.LEGACY drawing path: avoid expensive hardware layers, use cached shadows/bitmap rounding, and use the legacy Recording fallback rather than unguarded RenderNode calls.
- Android 9–12 retain non-AGSL backgrounds. Android 11 keeps its separate screensaver process variant. Thai fonts and symbols are stored at normalized forward-slash asset paths.
- Stock Home/setup/saved-Wi-Fi handling, remote shortcuts and ADB permissions vary by firmware. The dedicated shortcut interception inherited from upstream is TCL-specific; do not promise it remaps Xiaomi shortcut buttons.
- Streaming boxes have HDMI output, not necessarily HDMI input or a tuner. Input/Live TV availability depends on installed TV services.

## Hardware status

| Device | Status |
| --- | --- |
| Xiaomi TV Box S 3rd Gen, MiTV-AFMU0, Android 14 | Main target. The preceding customized 1.0 build was observed on hardware with Thai Home/settings, recommendations, seven dock apps and icons. 2.0 adds new setup/recovery/pagination behavior and needs its own fresh firmware-level test. |
| Xiaomi Mi Box S 2nd Gen, Android 11 | Upstream-style legacy/screensaver paths retained; not hardware-tested here with 2.0. |
| Xiaomi Mi Box S / Mi Box 3 with Android 9 | API floor and older GPU fallbacks retained; not hardware-tested here with 2.0. |
| Mi Box 3 still running Android 6/8 | Unsupported by minSdk 28. Do not bypass Android's minimum version check or flash unofficial firmware as part of this installer. |
| Other Android TV / Google TV 9+ | Source may run; Xiaomi-specific cleanup is gated off on other manufacturers. No blanket compatibility claim. |
| Samsung Tizen / LG webOS / Fire TV | Not supported by this installer. |

At packaging time the previously used box was unreachable over ADB. Version 2.0 was built and tested locally with the included portable tools; no fresh 2.0 on-device or controlled reboot test is claimed. Public cleanyourtv model notes are research inputs, not this project's hardware test results.

## Checks shipped with this repository

setup.cmd --self-test exercises config escaping/validation, no-key defaults, installed-app selection/order/count, ambiguous/offline devices, device-bound recovery, exact enabled-state restoration and partial failures, raw APK ZIP paths, Thai/English/version/credit configuration, and pure Java shelf/ad/recovery policies. setup.cmd --build-only compiles against API 34 and verifies the APK signature using the included tools.

## Hardware acceptance checklist

For each exact model/firmware, record the Android API, selected language, and before/after results privately. Test: first-run selection; 1/7/8/15-app page navigation; back/up/down and accessibility; Thai marks; all app launches; day/night styling; weather and no-key mode; own-key recommendations; icons; screen saver start/exit; Wi-Fi; Bluetooth pairing; Assistant/mic; phone remote; casting; audio/HDR/video playback; standby/wake; authorized full reboot; and Original recovery preserving pre-disabled packages. Do not publish credentials or unique device IDs with a report.

Some older Mi Box S firmware changes the USB port into debugging/device mode while USB debugging is enabled, which can cut power to attached drives/speakers. Disabling debugging may also remove the app's local ADB ability to switch/restore modes. Plan recovery first and test the specific firmware rather than assuming all Mi Box generations behave the same.
