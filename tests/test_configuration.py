from pathlib import Path
import json
import re
import struct
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APK = ROOT / "dist/FreeMyTV-2.0.apk"


def english_ui_strings():
    pattern = re.compile(r'Ui\.tr\(\s*"(?:\\.|[^"\\])*"\s*,\s*"((?:\\.|[^"\\])*)"')
    values = set()
    for path in (ROOT / "app/src/io/freemytv").glob("*.java"):
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            values.add(json.loads('"' + match.group(1) + '"'))
    return values


def test_apk_assets_use_assetmanager_paths():
    if not APK.exists(): raise unittest.SkipTest("Build the APK to verify its packaged assets")
    with zipfile.ZipFile(APK) as apk:
        names = set(apk.namelist())
    assert "assets/symbols/live_tv.png" in names
    assert "assets/symbols/hdmi.png" in names
    assert "assets/symbols/settings.png" in names
    assert "assets/fonts/InterVariable.ttf" in names
    assert "assets/fonts/NotoSansThai.ttf" in names
    raw_names = raw_zip_names(APK.read_bytes())
    assert not any("\\" in name for name in raw_names if name.startswith("assets/"))


def raw_zip_names(data):
    end = data.rfind(b"PK\x05\x06")
    assert end >= 0, "APK has no ZIP end-of-central-directory record"
    entries = struct.unpack_from("<H", data, end + 10)[0]
    offset = struct.unpack_from("<I", data, end + 16)[0]
    names = []
    for _ in range(entries):
        assert data[offset:offset + 4] == b"PK\x01\x02", "invalid ZIP central directory"
        name_len, extra_len, comment_len = struct.unpack_from("<HHH", data, offset + 28)
        raw = data[offset + 46:offset + 46 + name_len]
        names.append(raw.decode("utf-8"))
        offset += 46 + name_len + extra_len + comment_len
    return names


def test_configurable_shelf_and_version_credit():
    source = (ROOT / "app/src/io/freemytv/HomeApps.java").read_text(encoding="utf-8")
    assert 'ShelfPolicy.packages(Config.SHELF_PACKAGES)' in source
    manifest = (ROOT / 'app/AndroidManifest.xml').read_text(encoding='utf-8')
    assert 'android:versionName="2.0"' in manifest and 'android:versionCode="2"' in manifest
    settings = (ROOT / 'app/src/io/freemytv/SettingsActivity.java').read_text(encoding='utf-8')
    assert 'แปลไทยโดย FB : Kiw Kiattisak' in settings
    assert 'Thai translation by FB : Kiw Kiattisak' in settings


def test_thai_locale_and_core_translation_are_available():
    prefs = (ROOT / "app/src/io/freemytv/Prefs.java").read_text(encoding="utf-8")
    ui = (ROOT / "app/src/io/freemytv/Ui.java").read_text(encoding="utf-8")
    settings = (ROOT / "app/src/io/freemytv/SettingsActivity.java").read_text(encoding="utf-8")
    thai = (ROOT / "app/src/io/freemytv/Thai.java").read_text(encoding="utf-8")
    recs = (ROOT / "app/src/io/freemytv/Recs.java").read_text(encoding="utf-8")
    assert 'v.startsWith("th") ? "th"' in prefs
    assert '"auto", "pt", "en", "es", "th"' in settings
    assert '"th".equals(lang)' in ui
    translations = dict((json.loads('"' + k + '"'), json.loads('"' + v + '"'))
                        for k, v in re.findall(r'm\("((?:\\.|[^"\\])*)",\s*"((?:\\.|[^"\\])*)"\);', thai))
    assert translations.get("Settings") == "การตั้งค่า"
    assert 'กด OK เพื่อเพิ่มหรือนำแอปออก' in settings
    assert 'if (Ui.th) return "th-TH";' in recs
    assert '!listLanguage.equals(languageCacheKey())' in recs
    assert 'parts.add(seasons + " ซีซัน")' in recs
    assert not (english_ui_strings() - translations.keys())


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(unittest.FunctionTestCase(test) for test in
            [test_apk_assets_use_assetmanager_paths, test_configurable_shelf_and_version_credit,
             test_thai_locale_and_core_translation_are_available])


if __name__ == "__main__": unittest.main()
