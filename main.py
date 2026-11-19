"""One-day world-news image entry for make.fun's news-image-20261119 bounty.

The repository holds entry.png: a 1024x1024 front-page poster summarising the
world's news of Thursday 19 November 2026 (the Trump-Xi-Putin APEC trilateral,
the Crimea bridge strike, the ICJ Rohingya judgment, Anthropic's record IPO
debut, Nvidia after Huang, GTA VI's launch and Cyclone Akvan). The program
copies that image to /output/entry.png, byte for byte, with no network and no
randomness, so both graded runs produce identical output.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

MAX_BYTES = 1048576  # the gate: at most 1 MiB
MAX_SIDE = 1024  # the gate: at most 1024 by 1024 pixels
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_image(path: Path) -> None:
    """Fail fast if the shipped image would not pass the contest gate."""
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        sys.exit(f"{path.name}: not a PNG (bad signature)")
    if len(data) > MAX_BYTES:
        sys.exit(f"{path.name}: {len(data)} bytes exceeds the 1 MiB cap")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        sys.exit(f"{path.name}: {width}x{height} exceeds 1024x1024")


def main() -> None:
    source = HERE / "entry.png"
    check_image(source)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, OUTPUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
