"""ユーティリティ関数"""

import re
from pathlib import Path

INVALID_WINDOWS_CHARS = r'<>:"/\\|?*\0'
INVALID_CHAR_RE = re.compile(r"[" + re.escape(INVALID_WINDOWS_CHARS) + r"]+")


def sanitize_filename(value: str, default: str = "untitled") -> str:
    """ファイル名に使用できない文字を削除または置換"""
    value = value.strip()
    value = INVALID_CHAR_RE.sub("_", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or default


def choose_target_name(title: str, extension: str, target_dir: Path) -> Path:
    """ターゲットファイル名を決定（既存ファイルがある場合は番号を付与）"""
    base = sanitize_filename(title)
    candidate = target_dir / f"{base}{extension}"
    counter = 1
    while candidate.exists():
        candidate = target_dir / f"{base} ({counter}){extension}"
        counter += 1
    return candidate
