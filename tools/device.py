"""Read-only discovery and explicitly requested install/recovery operations over ADB."""
import json
from pathlib import Path
import re
import subprocess
from build import PACKAGE

HOME_ARGS = ('cmd', 'package', 'resolve-activity', '--brief', '--user', '0', '-a',
             'android.intent.action.MAIN', '-c', 'android.intent.category.HOME')
COMPONENT = re.compile(r'[\w.]+/[\w.$]+')
AD_PACKAGES = (
    'com.miui.tv.analytics', 'com.xiaomi.statistic', 'tv.alphonso.alphonso_eula',
    'com.google.android.feedback', 'com.google.android.tv.bugreportsender',
    'com.android.tv.feedbackconsent', 'com.mitv.tvhome.oemtab', 'com.mitv.tvhome.michannel',
    'com.xm.webcontent', 'android.autoinstalls.config.xioami.mibox3',
    'android.autoinstalls.config.soc.amlogic',
)
APP_NAMES = dict(zip(
    ['com.google.android.youtube.tv', 'com.netflix.ninja', 'com.truedmp.idtv', 'com.iqiyi.i18n.tv',
     'com.amazon.amazonvideo.livingroom', 'in.startv.hotstar.dplus.tv', 'com.disney.disneyplus',
     'com.wbd.stream', 'com.wbd.hbomax', 'com.tencent.qqlivei18n'],
    ['YouTube', 'Netflix', 'TrueID TV', 'iQIYI', 'Prime Video', 'Disney+ Hotstar', 'Disney+', 'Max', 'HBO Max', 'WeTV']))


def choose_device(output, requested=None):
    devices = {}
    for line in output.splitlines():
        bits = line.split()
        if len(bits) >= 2 and bits[1] in ('device', 'offline', 'unauthorized'):
            devices[bits[0]] = bits[1]
    if requested:
        if devices.get(requested) != 'device':
            raise ValueError('Requested device is missing, offline, or unauthorized. Accept the TV debugging prompt first.')
        return requested
    ready = [key for key, value in devices.items() if value == 'device']
    if len(ready) != 1 or any(state != 'device' for state in devices.values()):
        raise ValueError('Need exactly one authorized TV. Use --device SERIAL when multiple devices are connected.')
    return ready[0]


def select_apps(answer, choices):
    try:
        indices = list(dict.fromkeys(int(part.strip()) - 1 for part in answer.split(',')))
    except ValueError:
        raise ValueError('Choose comma-separated app numbers, such as 1,3,5.') from None
    if not indices or any(index < 0 or index >= len(choices) for index in indices):
        raise ValueError('Choose at least one valid installed app number.')
    return [choices[index][0] for index in indices]


class Adb:
    def __init__(self, executable, serial=None):
        self.executable, self.serial = str(executable), serial

    def command(self, *args, timeout=60):
        command = [self.executable] + (['-s', self.serial] if self.serial else []) + list(map(str, args))
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace',
                                timeout=timeout, shell=False)
        output = result.stdout + result.stderr
        if result.returncode or re.search(r'(?im)^(Error:|Failure|java\.lang\..*Exception|adb: error)', output):
            raise RuntimeError('ADB operation failed: ' + output.strip()[:800])
        return output.strip()

    def shell(self, *args):
        return self.command('shell', *args)


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def identity(adb):
    serial = adb.shell('getprop', 'ro.serialno') or adb.shell('getprop', 'ro.boot.serialno')
    if not serial:
        serial = adb.shell('settings', 'get', 'secure', 'android_id')
    if not serial or serial == 'null':
        raise ValueError('Cannot identify this TV safely; no recovery snapshot can be bound to it.')
    return {'serial': serial, 'fingerprint': adb.shell('getprop', 'ro.build.fingerprint')}


def check_identity(saved, current):
    if saved.get('serial') != current.get('serial') or saved.get('fingerprint') != current.get('fingerprint'):
        raise ValueError('This backup belongs to another device or firmware. Review it manually before restoring.')


def home_component(adb):
    for line in reversed(adb.shell(*HOME_ARGS).splitlines()):
        if COMPONENT.fullmatch(line.strip()): return line.strip()
    raise ValueError('Cannot resolve the current Home; choose a default Home on the TV before continuing.')


def package_state(adb, package):
    if not PACKAGE.fullmatch(package): raise ValueError('Invalid package ID.')
    match = re.search(r'User 0:.*?\benabled=(\d)', adb.shell('dumpsys', 'package', package))
    if not match or int(match[1]) not in range(5):
        raise ValueError('Cannot read package enabled state for ' + package)
    return int(match[1])


def launchable_apps(adb):
    output = adb.shell('cmd', 'package', 'query-activities', '--brief', '--user', '0', '-a',
                       'android.intent.action.MAIN', '-c', 'android.intent.category.LEANBACK_LAUNCHER')
    packages = sorted(set(line.strip().split('/')[0] for line in output.splitlines()
                          if COMPONENT.fullmatch(line.strip()) and not line.startswith('io.freemytv/')))
    return [(pkg, APP_NAMES.get(pkg, pkg)) for pkg in packages]


def snapshot(adb):
    result = {'identity': identity(adb), 'home': home_component(adb),
              'dream': adb.shell('settings', 'get', 'secure', 'screensaver_components'),
              'model': adb.shell('getprop', 'ro.product.model'),
              'sdk': adb.shell('getprop', 'ro.build.version.sdk')}
    present = set(line.removeprefix('package:').strip() for line in adb.shell('pm', 'list', 'packages').splitlines())
    candidates = set(AD_PACKAGES) | {result['home'].split('/')[0], 'com.google.android.tungsten.setupwraith',
                                    'com.google.android.tvrecommendations'}
    for component in result['dream'].split(','):
        if COMPONENT.fullmatch(component): candidates.add(component.split('/')[0])
    result['packages'] = {pkg: package_state(adb, pkg) for pkg in sorted(candidates & present)}
    return result


def restore_packages(adb, journal, progress=None):
    states = {0: 'default-state', 1: 'enable', 2: 'disable', 3: 'disable-user', 4: 'disable-until-used'}
    pending = list(journal.get('restore_pending', journal['packages']))
    for pkg in list(pending):
        state = journal['packages'][pkg]
        if not PACKAGE.fullmatch(pkg) or state not in states: raise ValueError('Invalid recovery package/state.')
        try:
            adb.shell('pm', states[state], '--user', '0', pkg)
            if package_state(adb, pkg) == state: pending.remove(pkg)
        except (RuntimeError, ValueError, subprocess.TimeoutExpired):
            pass
        journal['restore_pending'] = list(pending)
        if progress: progress(journal)
    return pending


def restore(adb, path):
    journal = json.loads(Path(path).read_text(encoding='utf-8'))
    check_identity(journal['identity'], identity(adb))
    remaining = restore_packages(adb, journal, lambda data: atomic_json(path, data))
    if remaining: raise RuntimeError('Recovery incomplete; backup retained. Reconnect and repeat --restore.')
    if not COMPONENT.fullmatch(journal['home']): raise ValueError('Invalid Home in backup.')
    adb.shell('cmd', 'package', 'set-home-activity', '--user', '0', journal['home'])
    dream = journal['dream']
    if dream in ('', 'null'):
        adb.shell('settings', 'delete', 'secure', 'screensaver_components')
    elif all(COMPONENT.fullmatch(component) for component in dream.split(',')):
        adb.shell('settings', 'put', 'secure', 'screensaver_components', dream)
    else: raise ValueError('Invalid screensaver in backup.')
    if home_component(adb) != journal['home']:
        raise RuntimeError('Home did not restore. Backup retained for manual recovery.')
    actual_dream = adb.shell('settings', 'get', 'secure', 'screensaver_components')
    if (actual_dream or 'null') != (dream or 'null'):
        raise RuntimeError('Screensaver did not restore. Backup retained; repeat --restore after resolving the error.')
    journal['restored'] = True
    atomic_json(path, journal)
    adb.shell('am', 'start', '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.HOME')
    print('Restored recorded package states, Home, and screensaver. Backup retained.')
