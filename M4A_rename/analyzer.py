"""ファイル構造の分析関数"""

from pathlib import Path
from metadata import get_album, get_disc


def count_files_by_album(origin_dir: Path) -> dict[str, int]:
    """各アルバムのファイル数をカウント"""
    album_counts = {}
    allowed_exts = {".m4a", ".mp4"}
    
    for path in origin_dir.iterdir():
        if not path.is_file() or path.suffix.lower() not in allowed_exts:
            continue
        
        try:
            album = get_album(path) or "Unknown Album"
        except Exception:
            album = "Unknown Album"
        
        album_counts[album] = album_counts.get(album, 0) + 1
    
    return album_counts


def count_discs_by_album(origin_dir: Path) -> dict[str, set[str]]:
    """各アルバム内のディスク数をカウント"""
    album_discs = {}
    allowed_exts = {".m4a", ".mp4"}
    
    for path in origin_dir.iterdir():
        if not path.is_file() or path.suffix.lower() not in allowed_exts:
            continue
        
        try:
            album = get_album(path) or "Unknown Album"
            disc = get_disc(path) or "1"
        except Exception:
            album = "Unknown Album"
            disc = "1"
        
        if album not in album_discs:
            album_discs[album] = set()
        album_discs[album].add(disc)
    
    return album_discs
