#!/usr/bin/env python3
"""Rewrite Windows-style backslashes in APK asset ZIP entry names to Android's required `/`."""

from pathlib import Path
import sys
import zipfile


def normalize(apk_path: Path) -> int:
    temp_path = apk_path.with_name(apk_path.name + ".normalized")
    renamed = 0
    seen = set()
    try:
        with zipfile.ZipFile(apk_path, "r") as source, zipfile.ZipFile(temp_path, "w") as target:
            for original in source.infolist():
                raw_name = original.orig_filename
                name = raw_name.replace("\\", "/")
                if name in seen:
                    raise ValueError(f"normalizing ZIP entry creates a duplicate: {name}")
                seen.add(name)
                item = zipfile.ZipInfo(name, original.date_time)
                item.compress_type = original.compress_type
                item.comment = original.comment
                item.extra = original.extra
                item.create_system = original.create_system
                item.external_attr = original.external_attr
                item.internal_attr = original.internal_attr
                item.flag_bits = original.flag_bits
                target.writestr(item, source.read(original), compress_type=original.compress_type)
                renamed += name != raw_name
        temp_path.replace(apk_path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    print(f"Normalized APK asset paths ({renamed} ZIP entries).")
    return renamed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: normalize_apk_asset_paths.py APK")
    normalize(Path(sys.argv[1]))
