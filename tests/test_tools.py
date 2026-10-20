import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build
import device
import tv_setup


class BuildTests(unittest.TestCase):
    def test_config_keeps_unicode_and_quotes_without_code_injection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'settings with spaces.properties'
            path.write_text('language=th\ncity=ลำพูน "city" \\ station\nshelf_packages=app.one,app.two,app.one\n', encoding='utf-8')
            config = build.read_config(path)
            generated = build.config_java(config)
            self.assertIn('ลำพูน \\"city\\" \\\\ station', generated)
            self.assertEqual(config['shelf_packages'], 'app.one,app.two')
            self.assertEqual(config['tmdb_key'], '')

    def test_invalid_config_rejected_before_build(self):
        for line in ['latitude=91', 'longitude=-181', 'language=xyz',
                     'shelf_packages=app.good;rm -rf /', 'clean_ads=sure']:
            with self.subTest(line=line), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'config.properties'
                path.write_text(line, encoding='utf-8')
                with self.assertRaises(ValueError):
                    build.read_config(path)


class DeviceTests(unittest.TestCase):
    def test_multiple_unauthorized_and_offline_devices_never_auto_selected(self):
        for output in ['a\tdevice\nb\tdevice', 'a\tunauthorized', 'a\toffline', '']:
            with self.subTest(output=output), self.assertRaises(ValueError):
                device.choose_device(output)
        self.assertEqual(device.choose_device('List of devices attached\nbox:5555\tdevice'), 'box:5555')

    def test_user_selects_any_count_in_their_order(self):
        choices = [('pkg.app' + str(i), 'App ' + str(i)) for i in range(15)]
        picked = device.select_apps('15,1,8,1,2,3,4,5,6,7', choices)
        self.assertEqual(picked[0], 'pkg.app14')
        self.assertEqual(len(picked), 9)
        for bad in ['', '0', '16', '1; reboot']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                device.select_apps(bad, choices)

    def test_restore_uses_exact_prior_state_and_retains_failed_changes(self):
        class Fake:
            def __init__(self): self.commands = []
            def shell(self, *args):
                self.commands.append(args)
                if args[-1] == 'pkg.fail': raise RuntimeError('offline')
                if args[0] == 'dumpsys':
                    state = {'pkg.default': 0, 'pkg.enabled': 1, 'pkg.disabled': 3}[args[-1]]
                    return 'User 0: installed=true enabled=' + str(state)
                return 'ok'
        fake = Fake()
        journal = {'packages': {'pkg.default': 0, 'pkg.enabled': 1, 'pkg.disabled': 3, 'pkg.fail': 0}}
        remaining = device.restore_packages(fake, journal)
        self.assertIn(('pm', 'default-state', '--user', '0', 'pkg.default'), fake.commands)
        self.assertIn(('pm', 'disable-user', '--user', '0', 'pkg.disabled'), fake.commands)
        self.assertEqual(remaining, ['pkg.fail'])

    def test_restore_detects_silent_package_manager_failure(self):
        class Fake:
            def shell(self, *args):
                return 'User 0: installed=true enabled=3' if args[0] == 'dumpsys' else 'ok'
        self.assertEqual(device.restore_packages(Fake(), {'packages': {'pkg.default': 0}}), ['pkg.default'])

    def test_recovery_refuses_another_device(self):
        with self.assertRaises(ValueError):
            device.check_identity({'serial': 'A', 'fingerprint': 'same'}, {'serial': 'B', 'fingerprint': 'same'})

    def test_recovery_retains_backup_when_screensaver_write_silently_fails(self):
        class Fake:
            def shell(self, *args):
                if args == ('getprop', 'ro.serialno'): return 'TEST'
                if args == ('getprop', 'ro.build.fingerprint'): return 'TEST-FIRMWARE'
                if args == device.HOME_ARGS: return 'pkg.home/.Home'
                if args == ('settings', 'get', 'secure', 'screensaver_components'): return 'io.freemytv/.Screensaver'
                return 'ok'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'backup.json'
            path.write_text(json.dumps({'identity': {'serial': 'TEST', 'fingerprint': 'TEST-FIRMWARE'},
                                       'packages': {}, 'home': 'pkg.home/.Home', 'dream': 'pkg.dream/.Dream'}))
            with self.assertRaises(RuntimeError): device.restore(Fake(), path)
            self.assertFalse(json.loads(path.read_text()).get('restored', False))

    def test_verify_rejects_incomplete_screensaver_activation(self):
        class Fake:
            def shell(self, *args):
                if args == device.HOME_ARGS: return 'io.freemytv/.HomeActivity'
                return 'pkg.dream/.Dream'
        with self.assertRaises(RuntimeError): tv_setup.verify(Fake())


if __name__ == '__main__':
    unittest.main()
