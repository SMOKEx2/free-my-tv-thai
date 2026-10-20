# Recovery

Keep Free My TV installed until its changes are undone. Removing the app first does not re-enable packages it disabled.

## Normal recovery

Open Free My TV settings, choose Home Screen → Original, and let the operation finish. Version 2.0 restores recorded package enabled/default states, Home and screensaver. It does not re-enable packages that were already disabled before a fresh 2.0 activation. Earlier versions did not record every numeric baseline; upgraded legacy records use their previous enable-on-restore behavior when that baseline is unavailable.

If the operation is partial, keep the app and retry Original after reconnecting. An interrupted activation can also be restored even when its mode never reached Free. If a killed process left a busy indicator, wait three minutes for it to expire. Pending failures are retained. Journal write failures stop package mutations. Restored states and screensaver settings are read back before their recovery records are cleared. A watchdog also attempts to give Home back to the original launcher after three repeated launcher crashes; this is a safety net, not a replacement for a backup.

## Emergency recovery from the computer

Before installation, the installer saves an ignored .local/backups/TIMESTAMP.json. It contains the TV identity, firmware, original Home/screensaver and enabled states for relevant candidates. Treat this file as private. For an upgrade from an already active Free My TV, preserve the earlier original-mode backup: the new snapshot records the current state and cannot invent a lost original baseline.

1. Turn on the TV, connect it to the trusted local network, and authorize debugging if required.
2. Use the same extracted repository/tool files. Reconnect with the current connection address if its IP changed.
3. Select the correct original-mode backup and intended ADB serial:

```powershell
.\setup.cmd --restore .local/backups/YOUR_TIMESTAMP.json --connect TV_IP:PORT --device EXACT_ADB_SERIAL
```

4. The script refuses a different device or changed firmware fingerprint. Do not edit identifiers simply to force a restore. After a firmware change, inspect the saved/current package inventory with the owner and use reviewed commands for that firmware instead.
5. Package states are restored and read back. Failed packages remain in restore_pending; the backup is retained. Reconnect and repeat the same command to retry pending work.
6. Home and screensaver are restored after package recovery. Confirm Home resolves correctly, press Home, and test network/remote/audio. Only then consider removing Free My TV.

## Manual last resort

Use the included ADB at .local/toolchain/platform-tools/adb.exe. Read the private backup locally; do not upload it. For each recorded changed package, restore its prior enabled state with the intended serial and user 0:

| Recorded state | pm action |
| --- | --- |
| 0 | default-state |
| 1 | enable |
| 2 | disable |
| 3 | disable-user |
| 4 | disable-until-used |

Example form: adb -s SERIAL shell pm default-state --user 0 PACKAGE. Then restore the recorded Home component using cmd package set-home-activity --user 0 COMPONENT, and restore screensaver_components to its recorded value (delete the setting only when the original value was null/empty).

Never run a blanket “enable every disabled package” command. Never guess an original Home for a different model. Re-enable setup/pairing components as required before re-pairing a remote or resetting the TV. If Wi-Fi disappeared because an app-owned saved network was deleted, reconnect from TV Settings; re-enabling the package cannot reconstruct a deleted network/password.

## Private files worth keeping

- config.properties: personal location, chosen apps and optional TMDB key.
- .local/signing/freemytv.keystore: necessary for future in-place app updates.
- .local/backups/: device-bound emergency records.
- The app's own internal mode journal while it is installed.

Do not publish any of these, or a personalized APK containing a TMDB key.
