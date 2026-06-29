# M4Aファイルのタイトルメタデータをファイル名にしてコピーするスクリプト
###
# 必要なインポート
# pip install mutagen
###

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from mutagen.mp4 import MP4

INVALID_WINDOWS_CHARS = r'<>:"/\\|?*\0'
INVALID_CHAR_RE = re.compile(r"[" + re.escape(INVALID_WINDOWS_CHARS) + r"]+")

def sanitize_filename(value: str, default: str = "untitled") -> str:
    value = value.strip()
    value = INVALID_CHAR_RE.sub("_", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or default

def get_title(path: Path) -> str | None:
    tags = MP4(str(path))
    if tags.tags is None:
        return None

    title_keys = ["\xa9nam", "©nam", "title"]
    for key in title_keys:
        if key in tags.tags:
            value = tags.tags[key]
            if isinstance(value, list):
                value = value[0] if value else None
            if isinstance(value, bytes):
                value = value.decode(errors="ignore")
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None

def get_album(path: Path) -> str | None:
    tags = MP4(str(path))
    if tags.tags is None:
        return None

    album_keys = ["\xa9alb", "©alb", "album"]
    for key in album_keys:
        if key in tags.tags:
            value = tags.tags[key]
            if isinstance(value, list):
                value = value[0] if value else None
            if isinstance(value, bytes):
                value = value.decode(errors="ignore")
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None

def choose_target_name(title: str, extension: str, target_dir: Path) -> Path:
    base = sanitize_filename(title)
    candidate = target_dir / f"{base}{extension}"
    counter = 1
    while candidate.exists():
        candidate = target_dir / f"{base} ({counter}){extension}"
        counter += 1
    return candidate

def copy_with_title(origin_dir: Path, result_dir: Path) -> int:
    result_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    allowed_exts = {".m4a", ".mp4"}
    for path in sorted(origin_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in allowed_exts:
            continue

        try:
            title = get_title(path)
        except Exception as exc:
            print(f"[error] {path.name} - failed to read metadata: {exc}")
            continue

        if not title:
            print(f"[skip] {path.name} - title metadata not found")
            continue

        target = choose_target_name(title, path.suffix, result_dir)
        try:
            shutil.copy2(path, target)
            path.unlink()
            print(f"[moved] {path.name} -> {target.name}")
            count += 1
        except Exception as exc:
            print(f"[error] {path.name} - failed to copy: {exc}")
            if target.exists():
                try:
                    target.unlink()
                except Exception:
                    pass
    return count

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy M4A/MP4 files from origin to result using title metadata as the file name."
    )
    parser.add_argument("--origin", default="origin", help="Source directory containing .m4a and .mp4 files")
    parser.add_argument("--result", default="result", help="Destination directory")
    args = parser.parse_args()

    origin_dir = Path(args.origin)
    result_dir = Path(args.result)

    if not origin_dir.exists():
        print(f"Source directory not found: {origin_dir}")
        return 1

    copied = copy_with_title(origin_dir, result_dir)
    print(f"Processed {copied} file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
