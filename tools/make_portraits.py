#!/usr/bin/env python3
"""
Generate placeholder character portrait sprites for Saintess Seoyun.

These are stand-ins, not final art. Each is a clean flat-vector placeholder
with a distinct silhouette and palette per character, so the cast is legible
on screen and real artwork can be dropped in later without touching the
Ren'Py definitions.

Output:  game/characters/<name>.png   640x1100, RGBA

Regenerate with:
    ~/miniforge3/bin/python tools/make_portraits.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter

W, H = 640, 880

# Vertical landmarks shared by every sprite, so a line of dialogue can put
# several characters on screen at the same height.
#
# Proportions: a bust portrait, roughly three heads tall including the hair
# mass. The head is deliberately large relative to the canvas so the face
# reads at textbox size, and the body is cropped just below the chest so the
# frame is filled by the character rather than by empty cloth.
HEAD_CX, HEAD_CY = 320, 250
HEAD_RX, HEAD_RY = 104, 116
BROW_Y = 250
EYE_Y = 292
CHEEK_Y = 322
MOUTH_Y = 340
NECK_TOP, NECK_BOT = 348, 424
SHOULDER_Y = 442
BOTTOM = H


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

def face_outline(cx, cy, rx, ry, taper=0.16, n=260):
    """Egg-shaped head: full width at the brow, narrowing into a rounded chin."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        s, c = math.sin(t), math.cos(t)
        squeeze = 1.0 - taper * (max(0.0, -c) ** 1.6)
        pts.append((cx + rx * s * squeeze, cy - ry * c))
    return pts


def blob(cx, top, bot, half_at, samples=48):
    """Smooth mass for hair and shoulders.

    `half_at` is a list of (y, half_width) control points; the outline is
    resampled and closed with straight lines, which is enough to keep the
    silhouette off-axis instead of boxy.
    """
    left, right = [], []
    for y, hw in half_at:
        left.append((cx - hw, y))
        right.append((cx + hw, y))
    pts = list(reversed(left)) + right
    return pts


def shade(overlay, pts, colour, blur=18, alpha=70):
    """Soft interior shading, so shapes are not flat."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).polygon(pts, fill=colour + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    overlay.alpha_composite(layer)


def lighten(c, f):
    return tuple(min(255, int(v + (255 - v) * f)) for v in c[:3])


def darken(c, f):
    return tuple(max(0, int(v * (1 - f))) for v in c[:3])


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# --------------------------------------------------------------------------
# features
# --------------------------------------------------------------------------

def draw_eyes(d, cx, iris, spec):
    """Almond eyes with lash line, iris, pupil and two highlights."""
    gap = spec["eye_gap"]
    ew, eh = spec["eye_w"], spec["eye_h"]
    for side in (-1, 1):
        ex = cx + side * gap
        pts = []
        n = 80
        for i in range(n):
            t = 2 * math.pi * i / n
            pts.append((ex + (ew / 2) * math.cos(t),
                        EYE_Y + (eh / 2) * math.sin(t) * (1.0 - 0.25 * math.cos(t))))
        d.polygon(pts, fill=(250, 248, 245, 255))

        # iris, clipped to the eye by a second pass of the eye shape
        ir = eh * 0.46
        d.ellipse([ex - ir, EYE_Y - ir, ex + ir, EYE_Y + ir], fill=iris + (255,))
        d.ellipse([ex - ir * 0.45, EYE_Y - ir * 0.45, ex + ir * 0.45, EYE_Y + ir * 0.45],
                  fill=darken(iris, 0.55) + (255,))

        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        clip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(clip)
        cd.ellipse([ex - ir, EYE_Y - ir, ex + ir, EYE_Y + ir], fill=iris + (255,))
        cd.ellipse([ex - ir * 0.45, EYE_Y - ir * 0.45, ex + ir * 0.45, EYE_Y + ir * 0.45],
                   fill=darken(iris, 0.55) + (255,))
        clip.putalpha(Image.composite(clip.getchannel("A"), Image.new("L", (W, H), 0), mask))

        # highlights
        cd2 = ImageDraw.Draw(clip)
        cd2.ellipse([ex - ir * 0.5, EYE_Y - ir * 0.75, ex - ir * 0.05, EYE_Y - ir * 0.3],
                    fill=(255, 255, 255, 235))
        cd2.ellipse([ex + ir * 0.2, EYE_Y + ir * 0.25, ex + ir * 0.5, EYE_Y + ir * 0.55],
                    fill=(255, 255, 255, 130))

        d._image.alpha_composite(clip)

        # upper lash line, thicker at the outer corner
        d.arc([ex - ew / 2, EYE_Y - eh / 2, ex + ew / 2, EYE_Y + eh / 2], 195, 345,
              fill=spec["lash"], width=4)
        d.line([(ex - side * ew * 0.48, EYE_Y - eh * 0.12),
                (ex + side * ew * 0.30, EYE_Y - eh * 0.46)],
               fill=spec["lash"], width=5)


def draw_brows(d, cx, spec):
    colour = spec["hair_dark"]
    for side in (-1, 1):
        ex = cx + side * spec["eye_gap"]
        pts = [
            (ex - side * spec["eye_w"] * 0.52, BROW_Y + 4),
            (ex - side * spec["eye_w"] * 0.10, BROW_Y - 6),
            (ex + side * spec["eye_w"] * 0.40, BROW_Y - 1),
            (ex + side * spec["eye_w"] * 0.55, BROW_Y + 5),
        ]
        d.line(pts, fill=colour + (255,), width=5, joint="curve")


def draw_mouth(d, cx, spec):
    w = spec["mouth_w"]
    d.arc([cx - w / 2, MOUTH_Y - 5, cx + w / 2, MOUTH_Y + 7], 20, 160,
          fill=spec["mouth"], width=3)
    d.line([(cx - w * 0.18, MOUTH_Y - 3), (cx + w * 0.18, MOUTH_Y - 3)],
           fill=darken(spec["mouth"], 0.35) + (200,), width=2)


def draw_nose(d, cx, spec):
    d.line([(cx + 3, CHEEK_Y - 22), (cx + 6, CHEEK_Y - 6), (cx - 1, CHEEK_Y - 4)],
           fill=darken(spec["skin"], 0.22) + (170,), width=3, joint="curve")


def blush(d, cx, spec):
    for side in (-1, 1):
        bx = cx + side * 64
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(
            [bx - 34, CHEEK_Y - 10, bx + 34, CHEEK_Y + 24], fill=(226, 130, 128, 90))
        d._image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(14)))


# --------------------------------------------------------------------------
# hair
# --------------------------------------------------------------------------

def hair_back(d, spec):
    """Hair mass behind the head, silhouette determined by style."""
    cx = HEAD_CX
    base, light, dark = spec["hair_base"], spec["hair_light"], spec["hair_dark"]
    style = spec["hair"]

    if style == "long_tied":
        # Rounded crown, falling past the shoulders, gathered into a tail.
        d.polygon(blob(cx, 0, 0, [
            (150, 78), (200, 128), (272, 152), (350, 156), (420, 148),
            (500, 122), (580, 150), (640, 132), (700, 104), (780, 66), (860, 34),
        ]), fill=base + (255,))
        d.ellipse([cx - 92, 578, cx + 92, 646], fill=light + (255,))
        d.ellipse([cx - 92, 578, cx + 92, 616], fill=darken(light, 0.22) + (255,))

    elif style == "refined_side":
        d.polygon(blob(cx, 0, 0, [
            (144, 66), (196, 120), (280, 146), (360, 148), (430, 140),
            (500, 114), (560, 96), (660, 84),
        ]), fill=base + (255,))

    elif style == "severe_short":
        d.polygon(blob(cx, 0, 0, [
            (130, 52), (188, 110), (272, 138), (352, 140), (420, 132),
            (480, 106), (520, 88), (560, 70),
        ]), fill=base + (255,))
        for side in (-1, 1):
            d.polygon([
                (cx + side * 112, 292), (cx + side * 130, 314),
                (cx + side * 126, 386), (cx + side * 108, 376),
            ], fill=base + (255,))

    elif style == "elegant_updo":
        d.polygon(blob(cx, 0, 0, [
            (150, 78), (208, 128), (288, 150), (360, 152), (428, 142),
            (496, 116), (560, 96), (680, 82),
        ]), fill=base + (255,))
        # pinned volume at the crown
        d.ellipse([cx - 100, 88, cx + 100, 254], fill=base + (255,))
        d.ellipse([cx - 64, 108, cx + 64, 216], fill=light + (255,))
        # loose tendrils at the temples
        for side, off in ((-1, 12), (1, 30)):
            d.polygon([
                (cx + side * 130, 296), (cx + side * (150 + off * 0.4), 372),
                (cx + side * (136 + off * 0.3), 462), (cx + side * (116 + off * 0.2), 492),
                (cx + side * 120, 372),
            ], fill=base + (255,))


def hair_bangs(d, spec):
    """Fringe, plus a soft cast shadow on the forehead."""
    cx = HEAD_CX
    base, light, dark = spec["hair_base"], spec["hair_light"], spec["hair_dark"]
    style = spec["hair"]

    # Every fringe starts above the crown of the head (the back-hair mass
    # already covers that) and its lower edge sits just above the brow, so no
    # strip of scalp shows between hairline and forehead.
    if style == "long_tied":
        d.polygon([
            (cx - 126, 264), (cx - 110, 190), (cx - 58, 148), (cx + 20, 136),
            (cx + 106, 176), (cx + 128, 244), (cx + 100, 254), (cx + 44, 260),
            (cx - 30, 254), (cx - 92, 264), (cx - 122, 268),
        ], fill=base + (255,))
        d.polygon([
            (cx - 118, 226), (cx - 30, 178), (cx + 100, 210), (cx + 56, 236),
            (cx - 44, 206), (cx - 112, 240),
        ], fill=light + (255,))

    elif style == "refined_side":
        d.polygon([
            (cx - 128, 262), (cx - 112, 196), (cx - 68, 152), (cx - 6, 132),
            (cx + 62, 134), (cx + 116, 168), (cx + 128, 250), (cx + 100, 262),
            (cx + 52, 256), (cx - 12, 272), (cx - 76, 260), (cx - 124, 272),
        ], fill=base + (255,))
        d.polygon([
            (cx - 104, 212), (cx - 34, 168), (cx + 66, 178), (cx + 118, 214),
            (cx + 54, 202), (cx - 30, 200),
        ], fill=light + (255,))

    elif style == "severe_short":
        d.polygon([
            (cx - 130, 252), (cx - 108, 180), (cx - 56, 138), (cx + 26, 124),
            (cx + 114, 160), (cx + 108, 244), (cx + 76, 236), (cx + 20, 254),
            (cx - 48, 244), (cx - 108, 256),
        ], fill=base + (255,))
        d.polygon([
            (cx - 102, 196), (cx - 26, 156), (cx + 70, 166), (cx + 114, 202),
            (cx + 50, 188), (cx - 30, 186),
        ], fill=light + (255,))

    elif style == "elegant_updo":
        d.polygon([
            (cx - 128, 262), (cx - 112, 194), (cx - 62, 150), (cx + 22, 138),
            (cx + 112, 180), (cx + 128, 248), (cx + 100, 258), (cx + 48, 254),
            (cx - 18, 264), (cx - 86, 254), (cx - 124, 268),
        ], fill=base + (255,))
        d.polygon([
            (cx - 106, 212), (cx - 30, 168), (cx + 70, 178), (cx + 118, 214),
            (cx + 56, 200), (cx - 32, 198),
        ], fill=light + (255,))

    # fringe shadow across the brow
    shade(d._image, [
        (cx - 112, 240), (cx - 30, 226), (cx + 88, 240), (cx + 110, 262),
        (cx + 60, 248), (cx - 30, 264), (cx - 106, 260),
    ], dark, blur=20, alpha=70)


def hair_rim(d, spec):
    """Light catching the outer edge of the hair mass."""
    cx = HEAD_CX
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.arc([cx - 138, 128, cx + 138, 396], 176, 262,
           fill=lighten(spec["hair_light"], 0.5) + (150,), width=7)
    d._image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(4)))


# --------------------------------------------------------------------------
# body and clothing
# --------------------------------------------------------------------------

def draw_body(d, spec):
    cx = HEAD_CX
    main, shadow, accent, trim = (spec["cloth"], spec["cloth_shadow"],
                                  spec["cloth_accent"], spec["trim"])
    collar = spec["collar"]

    shoulders = [
        (cx - 104, NECK_BOT - 4), (cx - 140, NECK_BOT + 22), (cx - 186, SHOULDER_Y + 18),
        (cx - 214, SHOULDER_Y + 96), (cx - 228, SHOULDER_Y + 200), (cx - 234, BOTTOM),
        (cx + 234, BOTTOM), (cx + 228, SHOULDER_Y + 200), (cx + 214, SHOULDER_Y + 96),
        (cx + 186, SHOULDER_Y + 18), (cx + 140, NECK_BOT + 22), (cx + 104, NECK_BOT - 4),
    ]
    d.polygon(shoulders, fill=main + (255,))

    # form shadow down both sides
    shade(d._image, [
        (cx - 234, BOTTOM), (cx - 214, SHOULDER_Y + 96), (cx - 186, SHOULDER_Y + 18),
        (cx - 140, NECK_BOT + 22), (cx - 66, NECK_BOT + 8), (cx - 84, BOTTOM),
    ], shadow, blur=32, alpha=80)
    shade(d._image, [
        (cx + 234, BOTTOM), (cx + 214, SHOULDER_Y + 96), (cx + 186, SHOULDER_Y + 18),
        (cx + 140, NECK_BOT + 22), (cx + 66, NECK_BOT + 8), (cx + 84, BOTTOM),
    ], shadow, blur=32, alpha=80)

    # fabric folds, vertical and soft, so the chest is not a flat sheet
    for x in (-120, -62, 62, 120):
        shade(d._image, [
            (cx + x - 16, NECK_BOT + 150), (cx + x - 6, NECK_BOT + 240),
            (cx + x - 4, BOTTOM), (cx + x + 18, BOTTOM), (cx + x + 14, NECK_BOT + 240),
            (cx + x + 4, NECK_BOT + 150),
        ], shadow, blur=18, alpha=54)

    if collar == "stand":
        # high standing collar, open at the front
        d.polygon([
            (cx - 70, NECK_BOT - 6), (cx - 46, NECK_BOT + 2), (cx, NECK_BOT + 22),
            (cx + 46, NECK_BOT + 2), (cx + 70, NECK_BOT - 6),
            (cx + 78, NECK_BOT + 74), (cx + 40, NECK_BOT + 96),
            (cx, NECK_BOT + 70), (cx - 40, NECK_BOT + 96), (cx - 78, NECK_BOT + 74),
        ], fill=accent + (255,))
        d.line([(cx - 64, NECK_BOT + 4), (cx - 68, NECK_BOT + 72)],
               fill=trim + (255,), width=4)
        d.line([(cx + 64, NECK_BOT + 4), (cx + 68, NECK_BOT + 72)],
               fill=trim + (255,), width=4)
        d.line([(cx - 40, NECK_BOT + 94), (cx, NECK_BOT + 68), (cx + 40, NECK_BOT + 94)],
               fill=trim + (255,), width=4)
        # epaulettes, sitting on the shoulder slope rather than beside it
        for side in (-1, 1):
            ex = cx + side * 142
            d.polygon([
                (ex - side * 46, SHOULDER_Y + 16), (ex + side * 30, SHOULDER_Y + 30),
                (ex + side * 34, SHOULDER_Y + 78), (ex - side * 40, SHOULDER_Y + 64),
            ], fill=trim + (255,))
            d.ellipse([ex - 22, SHOULDER_Y + 26, ex + 22, SHOULDER_Y + 62],
                      fill=lighten(trim, 0.4) + (255,))

    elif collar == "v":
        d.polygon([
            (cx - 96, NECK_BOT + 4), (cx - 44, NECK_BOT + 10), (cx, NECK_BOT + 118),
            (cx + 44, NECK_BOT + 10), (cx + 96, NECK_BOT + 4),
            (cx + 86, NECK_BOT - 34), (cx - 86, NECK_BOT - 34),
        ], fill=accent + (255,))
        d.polygon([
            (cx - 86, NECK_BOT - 36), (cx - 44, NECK_BOT + 10), (cx, NECK_BOT + 118),
            (cx + 44, NECK_BOT + 10), (cx + 86, NECK_BOT - 36),
            (cx + 104, NECK_BOT + 36), (cx, NECK_BOT + 140), (cx - 104, NECK_BOT + 36),
        ], fill=main + (255,))
        d.line([(cx - 104, NECK_BOT + 36), (cx, NECK_BOT + 140), (cx + 104, NECK_BOT + 36)],
               fill=trim + (255,), width=5)
        d.line([(cx - 96, NECK_BOT + 4), (cx - 40, NECK_BOT + 26), (cx, NECK_BOT + 106)],
               fill=trim + (255,), width=5)
        d.line([(cx + 96, NECK_BOT + 4), (cx + 40, NECK_BOT + 26), (cx, NECK_BOT + 106)],
               fill=trim + (255,), width=5)

    elif collar == "open_lapel":
        d.polygon([
            (cx - 104, NECK_BOT - 6), (cx - 34, NECK_BOT + 10), (cx, NECK_BOT + 88),
            (cx + 34, NECK_BOT + 10), (cx + 104, NECK_BOT - 6),
            (cx + 96, NECK_BOT + 170), (cx - 96, NECK_BOT + 170),
        ], fill=accent + (255,))
        d.polygon([
            (cx - 44, NECK_BOT + 6), (cx - 20, NECK_BOT + 40), (cx, NECK_BOT + 74),
            (cx + 20, NECK_BOT + 40), (cx + 44, NECK_BOT + 6),
            (cx + 56, NECK_BOT + 150), (cx + 40, NECK_BOT + 178),
            (cx - 40, NECK_BOT + 178), (cx - 56, NECK_BOT + 150),
        ], fill=lighten(accent, 0.55) + (255,))
        d.line([(cx, NECK_BOT + 74), (cx, NECK_BOT + 178)],
               fill=darken(accent, 0.2) + (110,), width=3)
        d.line([(cx - 104, NECK_BOT - 6), (cx - 34, NECK_BOT + 22), (cx - 46, NECK_BOT + 170)],
               fill=trim + (255,), width=6)
        d.line([(cx + 104, NECK_BOT - 6), (cx + 34, NECK_BOT + 22), (cx + 46, NECK_BOT + 170)],
               fill=trim + (255,), width=6)

    if spec.get("necklace"):
        d.arc([cx - 58, NECK_BOT - 6, cx + 58, NECK_BOT + 66], 0, 180,
              fill=trim + (255,), width=4)
        d.ellipse([cx - 8, NECK_BOT + 46, cx + 8, NECK_BOT + 62], fill=spec["gem"] + (255,))


# --------------------------------------------------------------------------
# render
# --------------------------------------------------------------------------

def render(spec):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d._image = img
    cx = HEAD_CX

    hair_back(d, spec)

    # neck, then head
    d.polygon([(cx - 34, NECK_TOP), (cx + 34, NECK_TOP), (cx + 40, NECK_BOT + 8),
               (cx - 40, NECK_BOT + 8)], fill=spec["skin"] + (255,))
    shade(img, [(cx - 40, NECK_BOT + 8), (cx - 34, NECK_TOP), (cx + 34, NECK_TOP),
                (cx + 40, NECK_BOT + 8), (cx + 12, NECK_BOT + 10), (cx - 14, NECK_BOT + 10)],
          darken(spec["skin"], 0.32), blur=16, alpha=95)

    draw_body(d, spec)

    head = face_outline(cx, HEAD_CY, HEAD_RX, HEAD_RY)
    for side in (-1, 1):
        d.ellipse([cx + side * 100 - 14, HEAD_CY - 2, cx + side * 100 + 14, HEAD_CY + 40],
                  fill=spec["skin"] + (255,))
    d.polygon(head, fill=spec["skin"] + (255,))
    shade(img, [(cx + 12, HEAD_CY - 118), (cx + 98, HEAD_CY - 24), (cx + 88, HEAD_CY + 100),
                (cx + 6, HEAD_CY + 124), (cx + 38, HEAD_CY), (cx + 42, HEAD_CY - 100)],
          darken(spec["skin"], 0.13), blur=28, alpha=54)

    draw_nose(d, cx, spec)
    draw_brows(d, cx, spec)
    draw_eyes(d, cx, spec["iris"], spec)
    draw_mouth(d, cx, spec)
    blush(d, cx, spec)

    hair_bangs(d, spec)
    hair_rim(d, spec)

    return img


# --------------------------------------------------------------------------
# the cast
# --------------------------------------------------------------------------

COMMON = dict(
    eye_gap=58, eye_w=56, eye_h=36, mouth_w=34,
    lash=(38, 30, 34), mouth=(198, 116, 112), gem=(72, 150, 150),
    necklace=False, collar="stand",
)

SPECS = [
    dict(
        COMMON,
        key="seoyun", hair="long_tied", collar="v",
        skin=(246, 220, 205), skin_shadow=(196, 152, 138),
        hair_base=(58, 44, 46), hair_light=(104, 78, 72), hair_dark=(32, 24, 27),
        iris=(126, 92, 72), lash=(40, 30, 34),
        cloth=(226, 214, 214), cloth_shadow=(168, 152, 158),
        cloth_accent=(206, 116, 118), trim=(232, 196, 120),
        necklace=True,
    ),
    dict(
        COMMON,
        key="jace", hair="refined_side", collar="v",
        skin=(250, 224, 206), skin_shadow=(206, 160, 142),
        hair_base=(226, 190, 118), hair_light=(250, 232, 178), hair_dark=(176, 134, 68),
        iris=(104, 156, 208), lash=(74, 62, 46),
        cloth=(238, 238, 244), cloth_shadow=(186, 192, 206),
        cloth_accent=(74, 116, 186), trim=(222, 194, 116),
        mouth=(196, 110, 108),
    ),
    dict(
        COMMON,
        key="ciel", hair="severe_short", collar="stand",
        skin=(240, 214, 196), skin_shadow=(190, 146, 126),
        hair_base=(96, 46, 40), hair_light=(148, 84, 66), hair_dark=(56, 24, 22),
        iris=(150, 108, 70), lash=(46, 28, 24), eye_gap=58, eye_w=56,
        cloth=(58, 68, 92), cloth_shadow=(34, 40, 58),
        cloth_accent=(44, 52, 72), trim=(178, 186, 198),
        mouth=(178, 100, 98),
    ),
    dict(
        COMMON,
        key="irene", hair="elegant_updo", collar="open_lapel",
        skin=(248, 222, 206), skin_shadow=(200, 156, 138),
        hair_base=(104, 62, 48), hair_light=(160, 108, 84), hair_dark=(60, 32, 26),
        iris=(116, 92, 68), lash=(52, 34, 28),
        cloth=(74, 92, 68), cloth_shadow=(44, 58, 42),
        cloth_accent=(48, 64, 48), trim=(206, 176, 104),
        gem=(196, 128, 92), necklace=True,
        mouth=(200, 112, 108),
    ),
]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "game", "characters")
    os.makedirs(out, exist_ok=True)

    for spec in SPECS:
        path = os.path.join(out, spec["key"] + ".png")
        render(spec).save(path)
        print("wrote", os.path.relpath(path, root))


if __name__ == "__main__":
    main()
