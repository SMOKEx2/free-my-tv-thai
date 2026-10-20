# Optional Xiaomi advertising/analytics cleanup

This project uses only a conservative ad/telemetry subset researched from these cleanyourtv profiles:

- [Mi Box S / Android TV 9](https://github.com/Gathin23/cleanyourtv/blob/main/examples/xiaomi-mi-box-s/debloat.txt)
- [Mi Box S 2nd Gen / Google TV 11](https://github.com/Gathin23/cleanyourtv/blob/main/examples/xiaomi-mi-box-s-2nd-gen/debloat.txt)
- [TV Box S 3rd Gen / MiTV-AFMU0](https://github.com/Gathin23/cleanyourtv/blob/main/examples/xiaomi-mitv-afmu0/debloat.txt)

The other launchers, broad app removals, personal choices and system changes in those lists are not imported. Package availability differs by firmware. A name in this table does not prove that a specific box has it.

| Exact package | Purpose identified in the reference profiles |
| --- | --- |
| com.miui.tv.analytics | Xiaomi usage analytics |
| com.xiaomi.statistic | Xiaomi statistics uploader |
| tv.alphonso.alphonso_eula | Alphonso advertising/usage tracking |
| com.google.android.feedback | Feedback uploader |
| com.google.android.tv.bugreportsender | TV bug-report sender |
| com.android.tv.feedbackconsent | TV feedback consent component |
| com.mitv.tvhome.oemtab | Xiaomi promotional row |
| com.mitv.tvhome.michannel | Xiaomi content/recommendation rows |
| com.xm.webcontent | Xiaomi web promotions |
| android.autoinstalls.config.xioami.mibox3 | Partner auto-install configuration; spelling follows the package ID |
| android.autoinstalls.config.soc.amlogic | Amlogic partner auto-install configuration on applicable firmware |

Cleanup defaults to **off**. It is enabled only through the user's local clean_ads=true choice. Xiaomi-specific candidates are used only when Android reports Xiaomi as manufacturer or brand. The app checks that a package is present, not protected, not a saved-Wi-Fi owner and not a selected dock app before disabling it. Unknown packages are left alone.

The following are deliberately kept: Xiaomi/Google firmware updates, quick settings (including the ambiguous com.xiaomi.tvqs.overseas.y24), partnercustomizer/remote pairing, mitv.service, Bluetooth/Amlogic components, Assistant/microphone, Chromecast, phone remote, Mi sharing/mirroring, accessibility, Play services/store, DRM, streaming apps, PatchWall and Xiaomi TV+ as general content apps unless they are the actual stock Home being replaced.

Activation separately replaces the current stock Home/screensaver and, when applicable, Google TV's setup recovery Home. Classic Android TV recommendations may be disabled alongside its stock launcher. These are Home-switch operations, not an excuse to run the entire reference debloat list. setupwraith can own Wi-Fi and remote pairing; the app blocks unsafe Wi-Fi-owner changes, and recovery must precede re-pairing or a factory reset.

Every operation uses pm disable-user --user 0. No package is uninstalled or its data cleared. Version 2.0 records original numeric enabled states before changing them and journals pending ownership before pm runs. Packages already disabled by the owner are left alone. Original restores the app-owned changes; the emergency snapshot provides a second recovery route. Firmware that rejects a command is reported rather than treated as success.

This removes selected system promotional/telemetry components. It does not remove advertisements inside YouTube, streaming services or other apps, and it is not a network-wide ad blocker.
