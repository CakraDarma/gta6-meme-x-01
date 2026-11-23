#!/usr/bin/env python3
"""Finish the gta6-meme-x-01 meme: brand-seal the eviction-notice artwork.

assets/eviction-base.png is the base artwork (a Vice City Housing Court
"notice to vacate" served on GTA V after its 13-year tenancy). This pass
sizes it to the 1200x1200 submission format and stamps the official
make.fun mark on the document as the seal on the "paid by my AI agent on
make.fun" charge line, so the mascot sits inside the scene's fiction.

Run:  python3 make_meme_final.py   (needs Pillow)
"""
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
BASE = HERE / "assets" / "eviction-base.png"
MARK = HERE / "assets" / "mark-1024.png"
OUT = HERE / "meme.png"

W = H = 1200

img = Image.open(BASE).convert("RGB").resize((W, H), Image.LANCZOS)

# the make.fun mark as the document's second official stamp, on the empty
# margin under the "13 YEARS LATE!" stamp and above the Vice City polaroid
mark = Image.open(MARK).convert("RGBA").resize((140, 140), Image.LANCZOS)
img.paste(mark, (1025, 385), mark)

img.save(OUT)
print(f"saved {OUT}")
