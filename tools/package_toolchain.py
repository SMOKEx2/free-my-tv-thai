"""Maintainer-only: create the redistributable Windows bundle from official local tools."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MODULES = 'java.base,java.compiler,jdk.compiler,jdk.jartool,java.logging,java.xml,java.naming,jdk.crypto.ec,jdk.zipfs,jdk.unsupported'


def package(jdk, sdk, adb, python_zip):
    output = ROOT / 'tools/bundles'
    output.mkdir(parents=True, exist_ok=True)
    (ROOT / '.local').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bundle-', dir=ROOT / '.local') as temp:
        stage = Path(temp)
        subprocess.run([str(jdk / 'bin/jlink.exe'), '--add-modules', MODULES, '--strip-debug', '--no-header-files',
                        '--no-man-pages', '--compress=2', '--output', str(stage / 'java')], check=True)
        bt = stage / 'sdk/build-tools/34.0.0'
        bt.mkdir(parents=True)
        for filename in ('aapt2.exe', 'zipalign.exe', 'NOTICE.txt', 'lib/d8.jar', 'lib/apksigner.jar'):
            target = bt / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sdk / 'build-tools/34.0.0' / filename, target)
        # LLVM/Clang DLLs belong to RenderScript tools, which this project does not use.
        for dll in (sdk / 'build-tools/34.0.0').glob('libwinpthread*.dll'): shutil.copy2(dll, bt / dll.name)
        platform = stage / 'sdk/platforms/android-34'
        platform.mkdir(parents=True)
        shutil.copy2(sdk / 'platforms/android-34/android.jar', platform / 'android.jar')
        for notice in (sdk / 'platforms/android-34').rglob('*NOTICE*'):
            if notice.is_file(): shutil.copy2(notice, platform / notice.name)
        dest_adb = stage / 'platform-tools'
        dest_adb.mkdir()
        for filename in ('adb.exe', 'AdbWinApi.dll', 'AdbWinUsbApi.dll', 'NOTICE.txt', 'source.properties'):
            shutil.copy2(adb / filename, dest_adb / filename)
        with zipfile.ZipFile(python_zip) as archive: archive.extractall(stage / 'python')
        pth = next((stage / 'python').glob('python*._pth'))
        pth.write_text(pth.read_text(encoding='utf-8') + '\n../../../tools\n', encoding='utf-8')
        files = {file.relative_to(stage).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
                 for file in sorted(stage.rglob('*')) if file.is_file()}
        archive_path = output / 'windows-x64.zip'
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name in files: archive.write(stage / name, name)
        if archive_path.stat().st_size >= 100_000_000:
            raise ValueError('Bundle exceeds the repository single-file size limit.')
        manifest = dict(platform='windows-x64', archive=archive_path.name,
                        sha256=hashlib.sha256(archive_path.read_bytes()).hexdigest(), files=files,
                        components={'java': 'Eclipse Temurin 17.0.20.1+1 (jlink subset)', 'python': 'CPython 3.14.8 embeddable',
                                    'android_build_tools': '34.0.0 (AOSP subset)', 'android_api': '34 (AOSP stubs)',
                                    'adb': (adb / 'source.properties').read_text(encoding='utf-8').strip()},
                        sources=['https://api.adoptium.net/v3/assets/latest/17/hotspot?architecture=x64&image_type=jdk&os=windows',
                                 'https://github.com/adoptium/temurin17-binaries/releases/tag/jdk-17.0.20.1%2B1',
                                 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.20.1%2B1/OpenJDK17U-jdk-sources_17.0.20.1_1.tar.gz',
                                 'https://www.python.org/ftp/python/3.14.8/python-3.14.8-embed-amd64.zip',
                                 'https://dl.google.com/android/repository/', 'https://source.android.com/'])
        (output / 'windows-x64.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        print('Bundled', len(files), 'files;', archive_path.stat().st_size, 'bytes. No credentials or user config included.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('jdk', 'sdk', 'adb', 'python-zip'): parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    package(args.jdk, args.sdk, args.adb, args.python_zip)
