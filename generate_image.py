#!/usr/bin/env python3
"""Draw the 18 November 2026 one-day newspaper front page (1024x1024).

Six stories, each verified in news listings dated Wednesday 18 November 2026:
  1. Nvidia beats earnings estimates in its first report without Jensen Huang;
     board rules out his return (NDTV, 18 Nov 2026).
  2. The US loses its measles-free status as cases and deaths mount (AFP, 18 Nov 2026).
  3. Israel's parliament elects an ally of Gadi Eisenkot as speaker, a blow for
     Netanyahu (NDTV, 18 Nov 2026).
  4. Mongolia's president resigns amid graft charges (Manila Times, 18 Nov 2026).
  5. Asif Merchant jailed for 27 years in the US over an Iran-linked plot to
     kill Donald Trump (NDTV, 18 Nov 2026).
  6. Germany and Norway to fund air defences for Ukraine (Manila Times, 18 Nov 2026).

Stories from 17 November (plane crash in Siberia, gene-editing sacking,
Dhoni's IPL retirement, the Manila Quad talks, the Crimea bridge strike)
were deliberately left out: they happened or were first reported on 17 Nov.

Run: python3 generate_image.py  ->  writes entry.png next to this file.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (160, 30, 30)
BLUE = (30, 60, 120)
GREY = (90, 90, 90)
PANEL_BG = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
def icon_chip(d, x, y, s):
    # green AI chip with circuit pins and a rising chart arrow
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=(34, 139, 34))
    d.rounded_rectangle([x + 14, y + 14, x + s - 14, y + s - 14], radius=5,
                        outline=(255, 255, 255), width=3)
    d.text((x + s / 2 - 16, y + s / 2 - 22), "AI", font=font(SANS_B, 34), fill=(255, 255, 255))
    for i in range(3):
        d.line([x + 8 + i * 26, y - 8, x + 8 + i * 26, y], fill=(34, 139, 34), width=4)
        d.line([x + 8 + i * 26, y + s, x + 8 + i * 26, y + s + 8], fill=(34, 139, 34), width=4)
    d.line([x + s - 34, y + s - 12, x + s - 6, y + 12], fill=RED, width=5)
    d.polygon([(x + s - 6, y + 12), (x + s - 20, y + 10), (x + s - 8, y + 24)], fill=RED)


def icon_virus(d, x, y, s):
    # red spiky virus ball
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 12
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        d.line([cx + r * 0.85 * math.cos(a), cy + r * 0.85 * math.sin(a),
                cx + (r + 12) * math.cos(a), cy + (r + 12) * math.sin(a)],
               fill=(200, 40, 40), width=5)
        d.ellipse([cx + (r + 12) * math.cos(a) - 4, cy + (r + 12) * math.sin(a) - 4,
                   cx + (r + 12) * math.cos(a) + 4, cy + (r + 12) * math.sin(a) + 4],
                  fill=(200, 40, 40))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 40, 40))
    d.ellipse([cx - r * 0.45, cy - r * 0.5, cx - r * 0.1, cy - r * 0.15], fill=(255, 120, 120))
    d.ellipse([cx + r * 0.1, cy + r * 0.2, cx + r * 0.4, cy + r * 0.5], fill=(255, 120, 120))


def icon_knesset(d, x, y, s):
    # parliament building: columns under a pediment, with a gavel
    d.polygon([(x, y + 26), (x + s / 2, y), (x + s, y + 26)], fill=BLUE)
    d.rectangle([x + 4, y + 26, x + s - 4, y + 34], fill=BLUE)
    for i in range(4):
        cx = x + 14 + i * (s - 28) / 3
        d.rectangle([cx - 6, y + 38, cx + 6, y + s - 12], fill=BLUE)
    d.rectangle([x + 4, y + s - 12, x + s - 4, y + s - 4], fill=BLUE)


def icon_steppe(d, x, y, s):
    # Mongolian steppe: sun over mountains, downward arrow (resignation)
    d.ellipse([x + s - 34, y + 4, x + s - 6, y + 32], fill=(230, 170, 30))
    d.polygon([(x, y + s), (x + s * 0.35, y + s * 0.35), (x + s * 0.7, y + s)],
              fill=(90, 110, 140))
    d.polygon([(x + s * 0.45, y + s), (x + s * 0.75, y + s * 0.2), (x + s, y + s * 0.55),
               (x + s, y + s)], fill=(60, 80, 110))
    d.line([x + 10, y + 8, x + 10, y + 52], fill=RED, width=6)
    d.polygon([(x + 10, y + 62), (x - 2, y + 44), (x + 22, y + 44)], fill=RED)


def icon_justice(d, x, y, s):
    # scales of justice behind bars
    for i in range(4):
        bx = x + 8 + i * (s - 16) / 3
        d.line([bx, y, bx, y + s], fill=(70, 70, 70), width=4)
    cx = x + s / 2
    d.line([cx, y + 14, cx, y + s - 18], fill=INK, width=5)
    d.line([cx - 30, y + 22, cx + 30, y + 22], fill=INK, width=5)
    d.polygon([(cx - 30, y + 22), (cx - 44, y + 48), (cx - 16, y + 48)], fill=(200, 160, 40))
    d.polygon([(cx + 30, y + 22), (cx + 16, y + 48), (cx + 44, y + 48)], fill=(200, 160, 40))
    d.ellipse([cx - 6, y + 8, cx + 6, y + 20], fill=INK)


def icon_shield(d, x, y, s):
    # defence shield with radar arcs
    d.polygon([(x + 6, y + 6), (x + s - 6, y + 6), (x + s - 6, y + s * 0.55),
               (x + s / 2, y + s - 4), (x + 6, y + s * 0.55)], fill=(40, 90, 160))
    d.polygon([(x + 16, y + 16), (x + s - 16, y + 16), (x + s - 16, y + s * 0.5),
               (x + s / 2, y + s - 14), (x + 16, y + s * 0.5)], fill=(255, 255, 255))
    cx, cy = x + s / 2, y + s * 0.42
    for r in (10, 20, 30):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
              fill=(40, 90, 160), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


# ---------------------------------------------------------------- stories
STORIES = [
    ("TECH", "NVIDIA BEATS ESTIMATES WITHOUT HUANG",
     "First earnings since Jensen Huang's exit top forecasts. The board says the ex-CEO will not return.",
     icon_chip),
    ("HEALTH", "US LOSES MEASLES-FREE STATUS",
     "Cases and deaths mount. America loses the elimination status it has held since 2000.",
     icon_virus),
    ("POLITICS", "ISRAEL ELECTS NEW SPEAKER IN BLOW TO NETANYAHU",
     "The Knesset picks an ally of Gadi Eisenkot as speaker, a setback for the prime minister.",
     icon_knesset),
    ("ASIA", "MONGOLIA'S PRESIDENT RESIGNS",
     "The president steps down amid graft charges, shaking politics in Ulaanbaatar.",
     icon_steppe),
    ("COURTS", "27 YEARS FOR PLOT TO KILL TRUMP",
     "Asif Merchant is jailed in New York over an Iran-linked murder-for-hire plot against the US president.",
     icon_justice),
    ("EUROPE", "GERMANY, NORWAY TO FUND UKRAINE AIR DEFENCES",
     "Berlin and Oslo pledge new money for Kyiv's air defences as Russian strikes go on.",
     icon_shield),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 8], fill=RED)
    draw_centered(d, W // 2, 26, "ONE WORLD, ONE DAY", font(SERIF_B, 64), INK)
    draw_centered(d, W // 2, 102, "WEDNESDAY  18  NOVEMBER  2026",
                  font(SANS_B, 40), RED)
    d.line([24, 158, W - 24, 158], fill=INK, width=3)
    draw_centered(d, W // 2, 168, "Six stories that defined the day \u2014 from Washington to Ulaanbaatar",
                  font(SERIF, 24), GREY)
    d.line([24, 202, W - 24, 202], fill=INK, width=2)

    # ---- 2 x 3 grid of panels ----
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 240
    top = 216
    for i, (tag, headline, caption, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PANEL_BG, outline=INK, width=2)
        # tag + icon row
        d.rectangle([x0, y0, x0 + pw, y0 + 34], fill=INK)
        d.text((x0 + 12, y0 + 5), tag, font=font(SANS_B, 20), fill=(255, 255, 255))
        icon(d, x0 + pw - 96, y0 + 44, 84)
        # headline (left of icon)
        hl = wrap(d, headline, font(SERIF_B, 27), pw - 130)
        hy = y0 + 46
        for line in hl[:3]:
            d.text((x0 + 12, hy), line, font=font(SERIF_B, 27), fill=INK)
            hy += 32
        # caption under headline/icon
        cap = wrap(d, caption, font(SANS, 20), pw - 24)
        cy = y0 + 152
        for line in cap[:3]:
            d.text((x0 + 12, cy), line, font=font(SANS, 20), fill=(40, 40, 40))
            cy += 25

    # ---- footer ----
    fy = top + 3 * ph + 2 * gap + 6
    d.line([24, fy, W - 24, fy], fill=INK, width=2)
    draw_centered(d, W // 2, fy + 10, "ONE WORLD, ONE DAY  \u00b7  18 NOVEMBER 2026  \u00b7  ALL SIX STORIES REPORTED ON THIS DAY",
                  font(SANS_B, 19), INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
