# M4Aファイルのタイトルメタデータをファイル名にしてコピーするスクリプト
###
# 必要なインポート
# pip install mutagen
###

from __future__ import annotations

import argparse
from pathlib import Path
from processor import copy_with_title


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
