"""M4A/MP4 ファイルのメタデータ取得関数"""

from pathlib import Path
from mutagen.mp4 import MP4


def get_title(path: Path) -> str | None:
    """M4A/MP4ファイルのタイトルメタデータを取得"""
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
    """M4A/MP4ファイルのアルバムメタデータを取得"""
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


def get_disc(path: Path) -> str | None:
    """M4A/MP4ファイルのディスク番号メタデータを取得"""
    tags = MP4(str(path))
    if tags.tags is None:
        return None

    disc_keys = ["\xa9dsk", "©dsk", "disk", "disc"]
    for key in disc_keys:
        if key in tags.tags:
            value = tags.tags[key]

            while isinstance(value, (list, tuple)) and value:
                value = value[0]

            if isinstance(value, bytes):
                value = value.decode(errors="ignore")
            if isinstance(value, tuple) and value:
                value = value[0]
            if isinstance(value, int):
                return str(value)

            # Extract just the disc number (e.g., "1/1" -> "1")
            if isinstance(value, str) and value.strip():
                disc_num = value.split('/')[0].strip()
                if disc_num:
                    return disc_num
    return None
