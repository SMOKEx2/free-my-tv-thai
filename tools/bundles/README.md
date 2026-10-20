# Included Windows x64 tools

windows-x64.zip contains actual executable/runtime/tool files. It is committed directly to Git, not Git LFS, and is below GitHub's single-file limit. windows-x64.json records archive SHA-256, per-file SHA-256, versions and upstream sources. setup.ps1 verifies the archive, extracts it into ignored .local/toolchain, then verifies every extracted file before invoking it.

| Folder inside archive | Contents |
| --- | --- |
| python/ | Official CPython 3.14.8 Windows x64 embeddable distribution, standard library and license |
| java/ | Eclipse Temurin OpenJDK 17.0.20.1+1 jlink subset with javac, keytool, jar, runtime, release metadata and module legal notices |
| sdk/build-tools/34.0.0/ | AOSP aapt2, D8, apksigner, zipalign and required support files; notices retained |
| sdk/platforms/android-34/ | Android API 34 compile-time stubs and notices |
| platform-tools/ | ADB 37.0.1, Windows DLLs and notices |

No author credential, APK, signing key, ADB authorization, user config or device backup is in the bundle. No global PATH changes or separate tool downloads are required on Windows x64. The app itself runs on supported Android TV hardware, independently of the computer's x64 architecture.

For licenses, corresponding source and provenance, read [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). A maintainer can reproduce the archive from official local distributions with tools/package_toolchain.py; the script does not fetch or include any user data. Only the open-source AOSP tools/stubs are selected, not Android Studio, the complete SDK manager distribution, proprietary Google APIs or emulator images.
