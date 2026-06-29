"""ファイル処理関数"""

import shutil
from pathlib import Path
from metadata import get_title, get_album, get_disc
from utils import sanitize_filename, choose_target_name
from analyzer import count_files_by_album, count_discs_by_album


def copy_with_title(origin_dir: Path, result_dir: Path) -> int:
    """タイトルメタデータをファイル名にしてコピー（アルバム・ディスク別に整理）"""
    result_dir.mkdir(parents=True, exist_ok=True)
    
    # Count files by album and discs by album first
    album_counts = count_files_by_album(origin_dir)
    album_discs = count_discs_by_album(origin_dir)
    
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

        # Get album name, default to "Unknown Album" if not found
        try:
            album = get_album(path) or "Unknown Album"
        except Exception as exc:
            print(f"[warn] {path.name} - failed to read album metadata: {exc}")
            album = "Unknown Album"

        # Get disc number, default to "1" if not found
        try:
            disc = get_disc(path) or "1"
        except Exception as exc:
            print(f"[warn] {path.name} - failed to read disc metadata: {exc}")
            disc = "1"

        # Determine target directory based on album and disc structure
        if album_counts.get(album, 1) > 1:
            # Multiple files in album - create album directory
            album_dir = result_dir / sanitize_filename(album)
            album_dir.mkdir(parents=True, exist_ok=True)
            
            # If there are multiple discs in this album, create disc subdirectory
            if len(album_discs.get(album, {"1"})) > 1:
                target_dir = album_dir / f"DISC{disc}"
                target_dir.mkdir(parents=True, exist_ok=True)
                output_msg = f"[moved] {path.name} -> {album}/DISC{disc}/{title}{path.suffix}"
            else:
                target_dir = album_dir
                output_msg = f"[moved] {path.name} -> {album}/{title}{path.suffix}"
        else:
            # Single file album - place directly in result
            target_dir = result_dir
            output_msg = f"[moved] {path.name} -> {title}{path.suffix}"

        target = choose_target_name(title, path.suffix, target_dir)
        try:
            shutil.copy2(path, target)
            path.unlink()
            print(output_msg)
            count += 1
        except Exception as exc:
            print(f"[error] {path.name} - failed to copy: {exc}")
            if target.exists():
                try:
                    target.unlink()
                except Exception:
                    pass
    return count
