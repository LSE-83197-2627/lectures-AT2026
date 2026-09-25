#!/usr/bin/env python3
"""Make circular PNGs of the instructor photos for the README.

GitHub strips inline styles from README HTML, so photos cannot be cropped to a
circle with CSS there; the crop is baked into the image instead (transparent
corners). People without a photo get a circle with their initials.

usage: python make_round.py    (writes into round/ next to this script)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "round"
SIZE = 200   # output size in px; the README shows them smaller
SCALE = 4    # draw the mask larger, then shrink, for smooth edges

PHOTOS = {"oliver": "oliver.webp", "zach": "zach.webp", "ed": "ed.webp",
          "serena": "serena.jpg.webp", "kevin": "kevin.webp"}
# name: (initials, background, text colour), matching the slide theme
INITIALS = {"federico": ("FP", "#f7efe6", "#b0603a")}
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def circle_mask():
    big = Image.new("L", (SIZE * SCALE, SIZE * SCALE), 0)
    ImageDraw.Draw(big).ellipse((0, 0, SIZE * SCALE - 1, SIZE * SCALE - 1), fill=255)
    return big.resize((SIZE, SIZE), Image.LANCZOS)


def round_photo(src):
    im = Image.open(src).convert("RGB")
    side = min(im.size)  # centre-crop to a square first
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((SIZE, SIZE), Image.LANCZOS)
    im.putalpha(circle_mask())
    return im


def initials_circle(text, bg, fg):
    big = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.ellipse((0, 0, SIZE * SCALE - 1, SIZE * SCALE - 1), fill=bg)
    font = ImageFont.truetype(FONT, int(SIZE * SCALE * 0.34))
    d.text((SIZE * SCALE / 2, SIZE * SCALE / 2), text, font=font, fill=fg, anchor="mm")
    return big.resize((SIZE, SIZE), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, src in PHOTOS.items():
        round_photo(HERE / src).save(OUT / f"{name}.png")
        print(f"wrote round/{name}.png")
    for name, (text, bg, fg) in INITIALS.items():
        initials_circle(text, bg, fg).save(OUT / f"{name}.png")
        print(f"wrote round/{name}.png")
