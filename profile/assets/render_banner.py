#!/usr/bin/env python3
"""Render the MIRL 'Threaded Index' banner — khipu threads dissolving into a pixel grid."""
import math, random
from PIL import Image, ImageDraw, ImageFont

random.seed(7)

FONTS = "/Users/jeff/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/173e0dab-6a43-4b55-a1f4-e93882c0ec8d/776d21ae-1fb1-4423-95ab-6cc700a464ec/skills/canvas-design/canvas-fonts"
OUT = "/Users/jeff/Documents/Claude/mirl-github-page/dotgithub/profile/assets/mirl-banner.png"

S = 2                      # supersample
W, H = 1280 * S, 320 * S

PAPER   = (242, 236, 224)
PAPER2  = (235, 227, 212)
INK     = (43, 39, 36)
INK_SOFT= (43, 39, 36, 150)
RED     = (200, 64, 44)

def F(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size * S)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# --- subtle vertical paper gradient ---
for y in range(H):
    t = y / H
    c = tuple(int(PAPER[i] + (PAPER2[i] - PAPER[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# --- faint grain ---
for _ in range(2600):
    x, y = random.randint(0, W), random.randint(0, H)
    a = random.randint(4, 12)
    d.point((x, y), fill=(43, 39, 36, a))

# ============================================================
# RIGHT REGISTER: anchor cord + threads dissolving into a grid
# ============================================================
vis_x0 = int(W * 0.43)            # start of visual register
vis_x1 = W - 70 * S               # right margin
anchor_y = 64 * S                 # horizontal datum
bottom   = H - 60 * S

# anchor cord (the loom datum)
d.line([(vis_x0 - 18 * S, anchor_y), (vis_x1, anchor_y)], fill=INK, width=max(2, 3 * S))
# small terminal knots on the cord ends
d.ellipse([vis_x0 - 18 * S - 5 * S, anchor_y - 5 * S, vis_x0 - 18 * S + 5 * S, anchor_y + 5 * S], fill=INK)

n = 30
span = vis_x1 - vis_x0
for i in range(n):
    fx = i / (n - 1)                       # 0 (analogue) -> 1 (digital)
    x = vis_x0 + fx * span
    # thread length: long & varied on left, short on right
    base_len = (bottom - anchor_y)
    length = base_len * (0.92 - 0.55 * fx) * (0.82 + 0.30 * random.random())
    y_end = anchor_y + length

    if fx < 0.55:
        # ---- ANALOGUE: organic knotted thread (wobbly polyline) ----
        pts = []
        steps = 26
        amp = (1 - fx) * 7 * S
        phase = random.random() * math.tau
        for s_ in range(steps + 1):
            ty = anchor_y + (y_end - anchor_y) * s_ / steps
            wob = math.sin(phase + s_ * 0.5) * amp * (s_ / steps)
            pts.append((x + wob, ty))
        w = max(1, int(round((2.1 - 1.1 * fx) * S)))
        d.line(pts, fill=INK, width=w, joint="curve")
        # knots: a few thick beads along the thread
        knots = random.randint(1, 3)
        for _k in range(knots):
            kt = random.uniform(0.25, 0.95)
            kx, ky = pts[int(kt * steps)]
            r = (2.6 - 1.4 * fx) * S
            d.ellipse([kx - r, ky - r, kx + r, ky + r], fill=INK)
        # frayed end
        d.ellipse([pts[-1][0] - 1.6 * S, pts[-1][1] - 1.6 * S,
                   pts[-1][0] + 1.6 * S, pts[-1][1] + 1.6 * S], fill=INK)
    else:
        # ---- DIGITAL: thread quantizes into a stack of square pixels ----
        cell = 9 * S
        ncells = max(2, int(length / cell))
        # probability a cell is "lit" rises toward the right (more digital)
        for c_ in range(ncells):
            cy = anchor_y + 6 * S + c_ * cell
            if cy > bottom:
                break
            lit = random.random() < (0.30 + 0.55 * fx) * (1 - 0.15 * (c_ / max(1, ncells)))
            if not lit:
                continue
            sq = cell * 0.62
            ox = x - sq / 2
            d.rectangle([ox, cy, ox + sq, cy + sq], fill=INK)

# --- a sparse field of background pixels in the far-right upper area (sensor hum) ---
gx0 = int(W * 0.72)
for gx in range(gx0, vis_x1, 11 * S):
    for gy in range(int(anchor_y + 8 * S), int(H * 0.42), 11 * S):
        if random.random() < 0.18:
            r = 1.5 * S
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(43, 39, 36, 90))

# --- THE RED DOT: single focal mark where fiber becomes signal ---
red_fx = 0.55
red_x = vis_x0 + red_fx * span
red_y = anchor_y + (bottom - anchor_y) * 0.30
rr = 7 * S
d.ellipse([red_x - rr, red_y - rr, red_x + rr, red_y + rr], fill=RED)
# faint halo
d.ellipse([red_x - rr*2.2, red_y - rr*2.2, red_x + rr*2.2, red_y + rr*2.2],
          outline=(200, 64, 44, 60), width=max(1, S))

# ============================================================
# LEFT REGISTER: text block (calm zone)
# ============================================================
LX = 72 * S

# top clinical label
mono = F("IBMPlexMono-Regular.ttf", 12)
def spaced(s, n=3): return (" " * n).join(list(s))
label = "UCSB  ·  HISTORY OF ART & ARCHITECTURE"
d.text((LX, 60 * S), label, font=mono, fill=(43, 39, 36, 205))
rule_w = d.textbbox((LX, 60 * S), label, font=mono)[2] - LX
# thin rule under label
d.line([(LX, 84 * S), (LX + rule_w, 84 * S)], fill=(43, 39, 36, 120), width=max(1, S))

# big name — quiet scholarly serif
serif = F("Italiana-Regular.ttf", 52)
d.text((LX - 2 * S, 104 * S), "Material / Image", font=serif, fill=INK)
d.text((LX - 2 * S, 160 * S), "Research Lab", font=serif, fill=INK)

# the acronym, oversized & faint, as a watermark behind nothing -> skip; instead a red slash accent
# small red index mark beside the name (echo of the red dot)
d.rectangle([LX - 2 * S, 100 * S, LX + 1 * S, 150 * S], fill=RED)

# bottom systematic caption
cap = F("IBMPlexMono-Regular.ttf", 11)
d.text((LX, 232 * S), spaced("DIGITAL IMAGING", 1) + "   ·   " +
       spaced("MATERIAL CULTURE", 1) + "   ·   " + spaced("3D", 1) + "   ·   " +
       spaced("ARCHIVES", 1), font=cap, fill=(43, 39, 36, 170))

# tiny specimen-style coordinate marks (corners)
tick = F("IBMPlexMono-Regular.ttf", 10)
d.text((LX, H - 46 * S), "MIRL · UC SANTA BARBARA", font=tick, fill=(43, 39, 36, 130))
d.text((vis_x1 - 70 * S, H - 46 * S), "FIG. 01", font=tick, fill=(43, 39, 36, 130))

# --- downscale for crisp anti-aliasing ---
img = img.resize((1280, 320), Image.LANCZOS)
img.save(OUT)
print("saved", OUT)
