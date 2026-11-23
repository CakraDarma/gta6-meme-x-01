#!/usr/bin/env python3
"""Compose the meme.png for the gta6-meme-x-01 entry (1200x1200).

The make.fun ghost grinds bounties on a laptop on a Vice City beach while the
whole world waited 13 years for GTA 6. Brand assets come from the official
press kit at https://make.fun/press/ (mark-1024.png and the
ghost-laptop-recording illustration, kept in ./assets).

Run:  python3 make_meme.py   (needs Pillow)
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "meme.png"

W = H = 1200
INK = (25, 20, 25)
MAGENTA = (196, 28, 131)
WHITE = (255, 255, 255)

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---- sky: Vice City sunset gradient ------------------------------------
top = (43, 13, 74)
mid = MAGENTA
low = (255, 122, 61)
horizon = 800

for y in range(horizon):
    if y < horizon * 0.55:
        c = lerp(top, mid, y / (horizon * 0.55))
    else:
        c = lerp(mid, low, (y - horizon * 0.55) / (horizon * 0.45))
    d.line([(0, y), (W, y)], fill=c)

# ---- retro sun ----------------------------------------------------------
sun_cx, sun_cy, sun_r = 600, 770, 290
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
sd.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
           fill=(255, 209, 102, 255))
y = sun_cy - 20
gap = 8
while y < sun_cy + sun_r:
    sd.rectangle([sun_cx - sun_r, y, sun_cx + sun_r, y + gap], fill=(0, 0, 0, 0))
    y += gap + 30
    gap += 7
img.paste(sun, (0, 0), sun)
d = ImageDraw.Draw(img)

# ---- sea ------------------------------------------------------------------
for y in range(horizon, H):
    c = lerp((94, 18, 74), INK, (y - horizon) / (H - horizon))
    d.line([(0, y), (W, y)], fill=c)
refl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(refl)
y = horizon + 10
wid = 180
while y < H - 60:
    rd.line([(sun_cx - wid // 2, y), (sun_cx + wid // 2, y)],
            fill=(255, 170, 90, 150), width=5)
    y += 28
    wid = int(wid * 1.1)
img.paste(refl, (0, 0), refl)
d = ImageDraw.Draw(img)

# ---- skyline silhouette ----------------------------------------------------
sky = Image.new("RGBA", (W, H), (0, 0, 0, 0))
kd = ImageDraw.Draw(sky)
random.seed(6)
x = 0
while x < W:
    bw = random.randint(38, 90)
    bh = random.randint(30, 140)
    kd.rectangle([x, horizon - bh, x + bw, horizon + 4], fill=INK + (255,))
    if random.random() < 0.3:
        kd.line([(x + bw // 2, horizon - bh), (x + bw // 2, horizon - bh - 24)],
                fill=INK + (255,), width=4)
    x += bw + random.randint(6, 26)
img.paste(sky, (0, 0), sky)
d = ImageDraw.Draw(img)


# ---- palms -------------------------------------------------------------------
def frond(pd, tx, ty, angle_deg, length, width, droop):
    """One palm frond: a curved tapered sliver from (tx, ty)."""
    a = math.radians(angle_deg)
    tipx = tx + math.cos(a) * length
    tipy = ty + math.sin(a) * length + droop
    cx = tx + math.cos(a) * length * 0.55
    cy = ty + math.sin(a) * length * 0.55 - droop * 0.9
    pts = []
    for i in range(13):
        t = i / 12
        px = (1 - t) ** 2 * tx + 2 * (1 - t) * t * cx + t * t * tipx
        py = (1 - t) ** 2 * ty + 2 * (1 - t) * t * cy + t * t * tipy
        pts.append((px, py, t))
    upper, lower = [], []
    for i, (px, py, t) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - px, pts[1][1] - py
        elif i == len(pts) - 1:
            dx, dy = px - pts[i - 1][0], py - pts[i - 1][1]
        else:
            dx = pts[i + 1][0] - pts[i - 1][0]
            dy = pts[i + 1][1] - pts[i - 1][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = width * (1 - t * 0.85)
        upper.append((px + nx * w, py + ny * w))
        lower.append((px - nx * w, py - ny * w))
    pd.polygon(upper + lower[::-1], fill=INK + (255,))


def palm(base_x, base_y, height, flip=1):
    p = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p)
    lean = flip * 110
    steps = 26
    tx, ty = base_x + lean, base_y - height
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        x0 = base_x + lean * t0 * t0
        y0 = base_y - height * t0
        x1 = base_x + lean * t1 * t1
        y1 = base_y - height * t1
        pd.line([(x0, y0), (x1, y1)], fill=INK + (255,),
                width=int(20 - 10 * t0))
    if flip == 1:
        angles = [(-8, 240, 16, 70), (-38, 265, 17, 85), (-68, 255, 16, 90),
                  (-100, 240, 15, 70), (-132, 250, 16, 95), (-163, 235, 15, 80),
                  (12, 210, 14, 95)]
    else:
        angles = [(188, 240, 16, 70), (218, 265, 17, 85), (248, 255, 16, 90),
                  (280, 240, 15, 70), (312, 250, 16, 95), (343, 235, 15, 80),
                  (168, 210, 14, 95)]
    for ang, ln, wd, dr in angles:
        frond(pd, tx, ty, ang, ln, wd, dr)
    pd.ellipse([tx - 16, ty - 4, tx + 6, ty + 18], fill=INK + (255,))
    pd.ellipse([tx + 2, ty - 8, tx + 22, ty + 12], fill=INK + (255,))
    return p


p1 = palm(80, H - 40, 560, flip=1)
img.paste(p1, (0, 0), p1)
p2 = palm(W - 70, H - 60, 490, flip=-1)
img.paste(p2, (0, 0), p2)
d = ImageDraw.Draw(img)

# ---- the make.fun ghost at its laptop ---------------------------------------
ghost = Image.open(ASSETS / "ghost-laptop-recording.png").convert("RGBA")
gw, gh = ghost.size
# erase the illustration's "recording" badge and sparkles top-right so the
# scene reads as work, not streaming; the laptop's top corner sits lower
px = ghost.load()
for yy in range(0, 285):
    for xx in range(430, gw):
        px[xx, yy] = (0, 0, 0, 0)
# tail of the sparkle below the block: clear only light pixels so the laptop's
# ink outline and magenta corner survive
for yy in range(275, 330):
    for xx in range(615, gw):
        r, g, b, a = px[xx, yy]
        if min(r, g, b) > 150:
            px[xx, yy] = (0, 0, 0, 0)
ghost = ghost.resize((560, int(560 * gh / gw)), Image.LANCZOS)
img.paste(ghost, (330, 520), ghost)
d = ImageDraw.Draw(img)


# ---- bounty coins the agent won ----------------------------------------------
def coin(cx, cy, r):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(c)
    cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA + (255,),
               outline=INK + (255,), width=max(3, r // 8))
    sr = r * 0.5
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = sr if i % 2 == 0 else sr * 0.45
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    cd.polygon(pts, fill=WHITE + (255,))
    return c


for cx, cy, r in [(950, 905, 46), (1030, 965, 40), (975, 1015, 36),
                  (880, 990, 30), (1065, 885, 30), (190, 965, 38),
                  (245, 1025, 30), (140, 1015, 26)]:
    cimg = coin(cx, cy, r)
    img.paste(cimg, (0, 0), cimg)

# the biggest coin is the real make.fun mark
mark = Image.open(ASSETS / "mark-1024.png").convert("RGBA").resize(
    (150, 150), Image.LANCZOS)
img.paste(mark, (960, 760), mark)
d = ImageDraw.Draw(img)

# ---- captions -----------------------------------------------------------------
FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"


def caption(text, y, size):
    f = ImageFont.truetype(FONT, size)
    bbox = d.textbbox((0, 0), text, font=f, stroke_width=0)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) / 2, y), text, font=f, fill=WHITE, stroke_width=10,
           stroke_fill=INK)


caption("WAITED 13 YEARS FOR GTA 6", 42, 96)
caption("MY AI AGENT SPENT THEM", 1005, 82)
caption("EARNING REAL MONEY ON make.fun", 1095, 82)

img.save(OUT)
print(f"saved {OUT}")
