"""Free My TV Thai 2.0: guided setup, read-only discovery, build, install, verify and recovery."""
import argparse
from datetime import datetime
import getpass
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.parse
import urllib.request

import build
import device

ROOT = build.ROOT
TOOLS = ROOT / '.local/toolchain'


def ask(prompt, default=''):
    answer = input(prompt + (f' [{default}]' if default else '') + ': ').strip()
    return answer or default


def geocode(city):
    query = urllib.parse.urlencode({'name': city, 'count': 5, 'language': 'en', 'format': 'json'})
    try:
        with urllib.request.urlopen('https://geocoding-api.open-meteo.com/v1/search?' + query, timeout=15) as response:
            return json.load(response).get('results', [])
    except (OSError, ValueError):
        return []


def guided_config(adb, choices, config_path):
    config = build.read_config(config_path)
    print('\nChoose your own settings. Nothing has been changed on the TV.')
    config['language'] = ask('Interface language: th, en, or auto', config['language'])
    city = ask('City for weather and sunrise/sunset (Enter to use coordinates)', config['city'])
    results = geocode(city) if city else []
    selected = None
    if results:
        for index, result in enumerate(results, 1):
            print(f"{index}. {result['name']}, {result.get('admin1', '')}, {result.get('country', '')}")
        option = ask('Choose location number, or 0 to enter coordinates', '1')
        if option.isdigit() and 1 <= int(option) <= len(results): selected = results[int(option) - 1]
    config['city'] = city
    if selected:
        config.update(latitude=str(selected['latitude']), longitude=str(selected['longitude']),
                      tmdb_region=selected.get('country_code', config['tmdb_region']))
    else:
        config['latitude'] = ask('Latitude (-90 to 90)', config['latitude'])
        config['longitude'] = ask('Longitude (-180 to 180)', config['longitude'])
    config['tmdb_region'] = ask('Streaming country, two-letter code', config['tmdb_region']).upper()
    config['temperature'] = ask('Temperature: C, F, or auto', config['temperature'])
    print('Optional TMDB API key: create YOUR OWN at https://www.themoviedb.org/settings/api.')
    print('Enter it here privately, never in the chat. Enter keeps a saved key, or skips recommendations if none exists.')
    key = getpass.getpass('Your TMDB API key (hidden): ').strip()
    if key: config['tmdb_key'] = key
    print('\nInstalled TV apps:')
    for index, (pkg, name) in enumerate(choices, 1): print(f'{index:2}. {name} ({pkg})')
    config['shelf_packages'] = ','.join(device.select_apps(ask('App numbers in dock order; choose 1, 7, or any count'), choices))
    maker = adb.shell('getprop', 'ro.product.manufacturer')
    brand = adb.shell('getprop', 'ro.product.brand')
    xiaomi = maker.lower() == 'xiaomi' or brand.lower() == 'xiaomi'
    if xiaomi:
        present = {line.removeprefix('package:').strip() for line in adb.shell('pm', 'list', 'packages').splitlines()}
        selected_apps = set(config['shelf_packages'].split(','))
        candidates = [pkg for pkg in device.AD_PACKAGES if pkg in present and pkg not in selected_apps]
        print('\nPresent Xiaomi ad/analytics candidates (saved-Wi-Fi owners are additionally protected by the app):')
        print('\n'.join('  ' + pkg for pkg in candidates) or '  None on this firmware.')
        config['clean_ads'] = 'true' if candidates and ask('Disable these ads/analytics when Free My TV is activated? yes/no', 'no').lower() == 'yes' else 'false'
    else:
        config['clean_ads'] = 'false'
    config['disable_assistant'] = 'false'
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text('# Private configuration. Never commit or share this file.\n' +
                           '\n'.join(key + '=' + value for key, value in config.items()) + '\n', encoding='utf-8')
    build.read_config(config_path)  # validate all values before any device mutation
    return config


def connect(args, executable):
    host = device.Adb(executable)
    if args.pair:
        if not re.fullmatch(r'[A-Za-z0-9_.:\[\]-]+', args.pair): raise ValueError('Invalid pairing endpoint.')
        code = getpass.getpass('Wireless debugging pairing code (hidden): ').strip()
        host.command('pair', args.pair, code, timeout=30)
    if args.connect:
        if not re.fullmatch(r'[A-Za-z0-9_.:\[\]-]+', args.connect): raise ValueError('Invalid connection endpoint.')
        print(host.command('connect', args.connect, timeout=25))
    output = host.command('devices')
    try:
        serial = device.choose_device(output, args.device)
    except ValueError:
        guided = not any((args.probe, args.install, args.verify, args.restore))
        if not guided or args.connect or args.device or re.search(r'(?m)^\S+\s+(device|offline|unauthorized)\b', output): raise
        endpoint = ask('TV debugging address from TV Settings (IP:port, usually IP:5555)')
        if not re.fullmatch(r'[A-Za-z0-9_.:\[\]-]+', endpoint): raise ValueError('Invalid connection endpoint.')
        print(host.command('connect', endpoint, timeout=25))
        serial = device.choose_device(host.command('devices'))
    return device.Adb(executable, serial)


def verify(adb):
    current = device.home_component(adb)
    dream = adb.shell('settings', 'get', 'secure', 'screensaver_components')
    print('Home:', current)
    print('Screensaver:', dream)
    if not current.startswith('io.freemytv/'):
        raise RuntimeError('Free My TV is not the active Home. Open its settings and activate it on the TV.')
    if not any(component.startswith('io.freemytv/') for component in dream.split(',')):
        raise RuntimeError('Free My TV is not the active screensaver. Inspect activation/recovery on the TV.')
    png = ROOT / '.local/verification/home.png'
    png.parent.mkdir(parents=True, exist_ok=True)
    adb.command('shell', 'screencap', '-p', '/data/local/tmp/freemytv-verification.png')
    adb.command('pull', '/data/local/tmp/freemytv-verification.png', png)
    print('Saved local screenshot to .local/verification/home.png. Inspect it before claiming visual success.')


def install(adb, config_path, config):
    if not config['shelf_packages']:
        raise ValueError('Choose the user\'s dock apps first. Run setup.cmd interactively, or fill shelf_packages in local config.')
    choices = dict(device.launchable_apps(adb))
    if any(pkg not in choices for pkg in config['shelf_packages'].split(',')):
        raise ValueError('A selected app is unavailable. Re-run --probe and ask the user to choose installed apps.')
    apk = build.build_apk(config_path)
    baseline = device.snapshot(adb)
    if int(baseline['sdk']) < 28: raise ValueError('This app requires Android TV 9 / API 28 or newer.')
    if baseline['home'].startswith('io.freemytv/'):
        print('Updating an existing Free My TV. Keep its original signing key and earlier recovery backup.')
    backup = ROOT / '.local/backups' / (datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.json')
    device.atomic_json(backup, baseline)
    print('Saved private emergency backup:', backup.relative_to(ROOT))
    result = adb.command('install', '-r', str(apk), timeout=180)
    if 'Success' not in result:
        raise RuntimeError('Installation did not report Success. Do not uninstall or clear data; check the existing signing key.')
    adb.shell('am', 'start', '-n', 'io.freemytv/.SettingsActivity')
    print('\nInstalled 2.0. On the TV: Home Screen -> Free My TV. Authorize its debugging prompt if shown.')
    print('This changes Home/screensaver and disables its recorded stock Home components. Optional ad cleanup follows your choice.')
    print('If setup owns the saved Wi-Fi, the app stops: forget/rejoin that network in TV Settings before trying again.')
    print('Then run setup.cmd --verify --device YOUR_DEVICE and inspect the screenshot.')
    print('To undo: select Original in the app. Emergency recovery: setup.cmd --restore ' + str(backup.relative_to(ROOT)))


def self_test():
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-v'], cwd=ROOT)
    if result.returncode: raise RuntimeError('Python tests failed.')
    tools = build.tool_paths()
    classes = ROOT / '.local/policy-tests'
    classes.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'app/src/io/freemytv'
    build.run([tools['javac'], '-encoding', 'UTF-8', '--release', '8', '-d', classes, ROOT / 'tests/PolicyTest.java',
               source / 'ShelfPolicy.java', source / 'AdPackages.java', source / 'PackageState.java', source / 'RecoveryFile.java', source / 'Thai.java'])
    print(build.run([tools['java'], '-cp', classes, 'io.freemytv.PolicyTest']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    for action in ('build-only', 'probe', 'install', 'verify', 'self-test', 'bundle-info'):
        actions.add_argument('--' + action, action='store_true')
    actions.add_argument('--restore', type=Path, metavar='BACKUP_JSON')
    parser.add_argument('--device', help='Explicit ADB serial when more than one device is connected')
    parser.add_argument('--connect', metavar='IP:PORT')
    parser.add_argument('--pair', metavar='IP:PAIRING_PORT')
    parser.add_argument('--config', type=Path, default=ROOT / 'config.properties')
    args = parser.parse_args()
    if args.bundle_info:
        print(json.dumps(json.loads((ROOT / 'tools/bundles/windows-x64.json').read_text())['components'], indent=2))
        return
    if args.self_test: return self_test()
    if args.build_only: return build.build_apk(args.config)
    executable = TOOLS / ('platform-tools/adb.exe' if os.name == 'nt' else 'platform-tools/adb')
    adb = connect(args, executable)
    if args.restore: return device.restore(adb, args.restore.resolve())
    if args.verify: return verify(adb)
    model = adb.shell('getprop', 'ro.product.model')
    sdk = adb.shell('getprop', 'ro.build.version.sdk')
    print('Connected TV:', model, '| Android API', sdk)
    if not sdk.isdigit() or int(sdk) < 28: raise ValueError('Android TV 9 or newer is required.')
    choices = device.launchable_apps(adb)
    if args.probe:
        print(json.dumps({'model': model, 'sdk': sdk, 'apps': choices}, ensure_ascii=False, indent=2))
        return
    if not choices: raise ValueError('No launchable TV apps were found. Stop and inspect the TV firmware.')
    config = build.read_config(args.config) if args.install else guided_config(adb, choices, args.config)
    install(adb, args.config, config)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print('Stopped safely:', error, file=sys.stderr)
        raise SystemExit(1)
    except (KeyboardInterrupt, EOFError):
        print('\nCancelled. Existing backups and signing keys are retained.', file=sys.stderr)
        raise SystemExit(130)
