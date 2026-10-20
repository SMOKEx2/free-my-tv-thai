"""Native, dependency-free Android build. Credentials are read only from ignored local config."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+')
DEFAULTS = dict(tmdb_key='', tmdb_region='US', latitude='0', longitude='0', city='', language='auto',
                currency='USD', temperature='auto', show_crypto='false', disable_assistant='false',
                clean_ads='false', shelf_packages='')


def read_config(path):
    values = dict(DEFAULTS)
    if Path(path).exists():
        for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            key, sep, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if not sep or key not in values:
                raise ValueError('Unknown or malformed config key (see config.example.properties).')
            if any(ord(ch) < 32 for ch in value):
                raise ValueError('Control characters are not allowed in config values.')
            values[key] = value
    for key, limit in [('latitude', 90), ('longitude', 180)]:
        value = float(values[key])
        if not -limit <= value <= limit:
            raise ValueError('Invalid ' + key)
    for key in ['clean_ads', 'disable_assistant', 'show_crypto']:
        if values[key] not in ('true', 'false'):
            raise ValueError(key + ' must be true or false.')
    if values['language'] not in ('auto', 'th', 'en', 'pt', 'es'):
        raise ValueError('Unsupported language.')
    if values['temperature'] not in ('auto', 'C', 'F'):
        raise ValueError('temperature must be auto, C, or F.')
    if not re.fullmatch('[A-Z]{2}', values['tmdb_region']) or not re.fullmatch('[A-Z]{3}', values['currency']):
        raise ValueError('Use a two-letter country and three-letter currency code.')
    packages = list(dict.fromkeys(p.strip() for p in values['shelf_packages'].split(',') if p.strip()))
    if any(not PACKAGE.fullmatch(pkg) for pkg in packages):
        raise ValueError('Invalid shelf package ID.')
    values['shelf_packages'] = ','.join(packages)
    return values


def config_java(config):
    fields = []
    for key, value in config.items():
        boolean = key in ('clean_ads', 'disable_assistant', 'show_crypto')
        fields.append('    static final %s %s = %s;' %
                      ('boolean' if boolean else 'String', key.upper(), value if boolean else json.dumps(value, ensure_ascii=False)))
    return 'package io.freemytv;\nfinal class Config {\n' + '\n'.join(fields) + '\n}\n'


def run(args, cwd=ROOT):
    result = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', shell=False)
    if result.returncode:
        log = ROOT / '.local' / 'build-error.log'
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(result.stdout + result.stderr, encoding='utf-8')
        raise RuntimeError('Build tool failed: ' + Path(args[0]).name + '. Details in ignored .local/build-error.log.')
    return result.stdout


def tool_paths(toolchain=None, sdk_root=None, java_home=None):
    root = Path(toolchain or ROOT / '.local/toolchain').resolve()
    sdk = Path(sdk_root or root / 'sdk').resolve()
    java = Path(java_home or root / 'java').resolve()
    suffix = '.exe' if os.name == 'nt' else ''
    paths = dict(java=java / ('bin/java' + suffix), javac=java / ('bin/javac' + suffix),
                 keytool=java / ('bin/keytool' + suffix), aapt2=sdk / ('build-tools/34.0.0/aapt2' + suffix),
                 zipalign=sdk / ('build-tools/34.0.0/zipalign' + suffix), android=sdk / 'platforms/android-34/android.jar',
                 d8=sdk / 'build-tools/34.0.0/lib/d8.jar', signer=sdk / 'build-tools/34.0.0/lib/apksigner.jar',
                 adb=root / ('platform-tools/adb' + suffix))
    for key, value in paths.items():
        if key != 'adb' and not value.is_file():
            raise FileNotFoundError('Missing build tool ' + key + '. Run setup.cmd to extract the bundled tools.')
    return paths


def build_apk(config_path=None, toolchain=None, sdk_root=None, java_home=None, output_dir=None, keystore=None):
    config = read_config(config_path or ROOT / 'config.properties')
    tools = tool_paths(toolchain, sdk_root, java_home)
    out = Path(output_dir or ROOT / '.local/build').resolve()
    # Only clean generated build directories, never the repository or a user-supplied parent.
    out.mkdir(parents=True, exist_ok=True)
    for child in ('gen', 'classes'):
        target = out / child
        if target.exists(): shutil.rmtree(target)
        target.mkdir(parents=True)
    generated = out / 'gen/io/freemytv/Config.java'
    generated.parent.mkdir(parents=True, exist_ok=True)
    generated.write_text(config_java(config), encoding='utf-8')
    run([tools['aapt2'], 'compile', '--dir', ROOT / 'app/res', '-o', out / 'res.zip'])
    run([tools['aapt2'], 'link', '-o', out / 'base.apk', '-I', tools['android'], '--manifest', ROOT / 'app/AndroidManifest.xml',
         '--java', out / 'gen', out / 'res.zip', '--min-sdk-version', '28', '--target-sdk-version', '34',
         '-A', ROOT / 'app/assets', '-0', 'ttf'])
    sources = sorted((ROOT / 'app/src').rglob('*.java')) + sorted((out / 'gen').rglob('*.java'))
    argfile = out / 'sources.txt'
    argfile.write_text('\n'.join('"' + p.as_posix() + '"' for p in sources), encoding='utf-8')
    run([tools['javac'], '-encoding', 'UTF-8', '--release', '8', '-classpath', tools['android'], '-d', out / 'classes', '@' + str(argfile)])
    with zipfile.ZipFile(out / 'classes.jar', 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((out / 'classes').rglob('*.class')):
            archive.write(file, file.relative_to(out / 'classes').as_posix())
    run([tools['java'], '-cp', tools['d8'], 'com.android.tools.r8.D8', '--release', '--min-api', '28', '--lib',
         tools['android'], '--output', out, out / 'classes.jar'])
    # Rewrite raw Windows ZIP names; Python's ZipInfo.filename hides these backslashes on Windows.
    with zipfile.ZipFile(out / 'base.apk') as source, zipfile.ZipFile(out / 'packed.apk', 'w') as target:
        for original in source.infolist():
            item = zipfile.ZipInfo(original.orig_filename.replace('\\', '/'), original.date_time)
            item.compress_type = original.compress_type
            target.writestr(item, source.read(original))
        target.write(out / 'classes.dex', 'classes.dex', compress_type=zipfile.ZIP_DEFLATED)
    run([tools['zipalign'], '-f', '-p', '4', out / 'packed.apk', out / 'aligned.apk'])
    key = Path(keystore or ROOT / '.local/signing/freemytv.keystore').resolve()
    key.parent.mkdir(parents=True, exist_ok=True)
    if not key.exists():
        run([tools['keytool'], '-genkeypair', '-keystore', key, '-alias', 'freemytv', '-keyalg', 'RSA', '-keysize', '2048',
             '-validity', '20000', '-storepass', 'freemytv', '-keypass', 'freemytv', '-dname', 'CN=Free My TV Thai'])
    apk = ROOT / 'dist/FreeMyTV-2.0.apk'
    apk.parent.mkdir(parents=True, exist_ok=True)
    run([tools['java'], '-jar', tools['signer'], 'sign', '--ks', key, '--ks-pass', 'pass:freemytv', '--key-pass',
         'pass:freemytv', '--out', apk, out / 'aligned.apk'])
    run([tools['java'], '-jar', tools['signer'], 'verify', '--verbose', apk])
    print('Built and verified dist/FreeMyTV-2.0.apk. Keep your private .local/signing folder for future updates.')
    return apk


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ('config', 'toolchain', 'sdk-root', 'java-home', 'output-dir', 'keystore'):
        parser.add_argument('--' + option)
    args = parser.parse_args()
    build_apk(args.config, args.toolchain, args.sdk_root, args.java_home, args.output_dir, args.keystore)
