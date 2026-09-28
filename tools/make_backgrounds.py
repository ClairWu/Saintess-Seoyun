#!/usr/bin/env python3
"""
Generate placeholder backgrounds for Saintess Seoyun.

Simple gradient-and-shape stand-ins so the game is playable before real art
exists. The important property is that filenames match the `scene` and
`show` statements in the script, and that they exist at all: Ren'Py does not
report a missing image at lint time, it crashes when the line plays.

Output:  game/images/bg_<name>.png   1920x1080

Regenerate with:
    ~/miniforge3/bin/python tools/make_backgrounds.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080


def vgrad(size, top, bottom):
    """Vertical gradient."""
    w, h = size
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img.resize((w, h), Image.BICUBIC)


def dgrad(size, a, b, angle=35.0):
    """Diagonal gradient, used for skies."""
    w, h = size
    small = Image.new("RGB", (64, 64))
    px = small.load()
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    for y in range(64):
        for x in range(64):
            t = (x / 63 * dx + y / 63 * dy)
            t = max(0.0, min(1.0, (t + 1) / 2 if t < 0 else t))
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return small.resize((w, h), Image.BICUBIC)


def ridge(img, colour, base_y, amp, freq, seed_phase, alpha=255):
    """A soft silhouette band, for hills or structures on the horizon."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = [(0, H)]
    for x in range(0, W + 40, 40):
        y = (base_y
             + amp * math.sin(x / freq + seed_phase)
             + amp * 0.45 * math.sin(x / (freq * 0.43) + seed_phase * 1.7))
        pts.append((x, y))
    pts.append((W, H))
    d.polygon(pts, fill=colour + (alpha,))
    img.alpha_composite(layer)
    return img


def glow(img, centre, radius, colour, strength=0.5):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([centre[0] - radius, centre[1] - radius,
               centre[0] + radius, centre[1] + radius],
              fill=colour + (int(255 * strength),))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(radius * 0.55)))
    return img


def speckle(img, n, colour, ymin, ymax, seed, rmax=3):
    """Small bright points, for stars or distant lights."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = seed
    for _ in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        x = s % W
        s = (s * 1103515245 + 12345) % 2147483648
        y = ymin + (s % max(1, ymax - ymin))
        s = (s * 1103515245 + 12345) % 2147483648
        r = 1 + (s % rmax)
        d.ellipse([x - r, y - r, x + r, y + r], fill=colour + (200,))
    img.alpha_composite(layer)
    return img


def vignette(img, strength=0.45):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * strength)))
    inv = mask.point(lambda v: 255 - v)
    dark.putalpha(inv.point(lambda v: int(v * strength)))
    img.alpha_composite(dark)
    return img


def finish(img, strength=0.45):
    return vignette(img.convert("RGBA"), strength)


# --------------------------------------------------------------------------

def bg_raid():
    """A portal site in modern Korea. Night, sodium light, a wound in the air."""
    img = dgrad((W, H), (18, 22, 34), (44, 40, 46), 60).convert("RGBA")
    img = glow(img, (960, 560), 420, (120, 90, 200), 0.55)
    img = glow(img, (960, 545), 190, (190, 170, 255), 0.5)

    # ground
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon([(0, 700), (W, 690), (W, H), (0, H)], fill=(26, 28, 30, 255))
    img.alpha_composite(layer)

    # floodlight haze
    img = glow(img, (300, 300), 300, (255, 214, 160), 0.18)
    img = glow(img, (1620, 320), 300, (255, 214, 160), 0.18)

    # scattered ground lights
    img = speckle(img, 46, (255, 208, 150), 720, 1020, 7, rmax=4)
    return finish(img)


def bg_arrival():
    """Open country, and a portal mid-collapse. Cold, wide, no shelter."""
    img = dgrad((W, H), (52, 60, 78), (128, 128, 138), 70).convert("RGBA")
    img = ridge(img, (58, 66, 58), 720, 34, 420, 0.4)
    img = ridge(img, (44, 52, 46), 790, 22, 300, 2.1)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon([(0, 800), (W, 792), (W, H), (0, H)], fill=(52, 56, 48, 255))
    img.alpha_composite(layer)

    # the portal, torn rather than open
    img = glow(img, (1400, 430), 300, (170, 150, 255), 0.5)
    img = glow(img, (1400, 425), 130, (235, 225, 255), 0.55)
    return finish(img)


def bg_temple():
    """The Temple. Beautiful, cold, and a great deal of stone."""
    img = vgrad((W, H), (66, 72, 92), (34, 38, 52)).convert("RGBA")

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # floor and colonnade, receding
    d.polygon([(0, 780), (W, 780), (W, H), (0, H)], fill=(48, 50, 62, 255))
    for i, x in enumerate(range(-40, W + 120, 190)):
        top = 300 - i * 6
        wdt = 44 - i * 2
        shade = 74 - i * 4
        d.rectangle([x, top, x + wdt, 782], fill=(shade, shade + 6, shade + 16, 255))
    # architrave
    d.rectangle([0, 250, W, 320], fill=(82, 88, 108, 255))
    d.rectangle([0, 236, W, 252], fill=(98, 104, 126, 255))
    img.alpha_composite(layer)

    # cold light from a high window
    img = glow(img, (960, 200), 340, (150, 180, 220), 0.22)
    return finish(img, )


def bg_ball():
    """The imperial ball. Warm, crowded, and a public event."""
    img = vgrad((W, H), (58, 40, 62), (128, 88, 96)).convert("RGBA")

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # chandeliers
    for cx in (380, 960, 1540):
        d.line([(cx, 0), (cx, 190)], fill=(96, 76, 60, 255), width=4)
        d.ellipse([cx - 70, 190, cx + 70, 250], fill=(210, 176, 110, 255))
        for k in range(5):
            lx = cx - 52 + k * 26
            d.ellipse([lx - 9, 250, lx + 9, 284], fill=(240, 216, 160, 255))
    d.polygon([(0, 860), (W, 860), (W, H), (0, H)], fill=(70, 48, 58, 255))
    img.alpha_composite(layer)

    for cx in (380, 960, 1540):
        img = glow(img, (cx, 240), 240, (255, 216, 150), 0.30)
    return finish(img, 0.5)


def bg_korea():
    """Modern Korea, the alliance's territory. Concrete, floodlights, ranks."""
    img = dgrad((W, H), (34, 40, 52), (72, 76, 84), 25).convert("RGBA")

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([0, 700, W, 760], fill=(46, 50, 58, 255))
    # a blocky skyline
    x = 0
    i = 0
    while x < W:
        wdt = 90 + (i * 37) % 130
        hgt = 180 + (i * 91) % 300
        d.rectangle([x, 700 - hgt, x + wdt, 700], fill=(52, 58, 70, 255))
        for wy in range(700 - hgt + 30, 690, 46):
            for wx in range(x + 16, x + wdt - 16, 34):
                d.rectangle([wx, wy, wx + 14, wy + 20], fill=(126, 138, 158, 255))
        x += wdt + 18
        i += 1
    d.polygon([(0, 760), (W, 760), (W, H), (0, H)], fill=(40, 44, 50, 255))
    img.alpha_composite(layer)

    img = glow(img, (240, 200), 280, (255, 220, 170), 0.16)
    return finish(img, 0.42)


BACKGROUNDS = {
    "raid": bg_raid,
    "arrival": bg_arrival,
    "temple": bg_temple,
    "ball": bg_ball,
    "korea": bg_korea,
}


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "game", "images")
    os.makedirs(out, exist_ok=True)

    for name, fn in BACKGROUNDS.items():
        path = os.path.join(out, "bg_" + name + ".png")
        fn().save(path)
        print("wrote", os.path.relpath(path, root))


if __name__ == "__main__":
    main()
