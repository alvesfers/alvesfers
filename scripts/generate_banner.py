"""Generate the self-hosted profile banner. Requires Python 3 and Pillow.

Run from anywhere: python scripts/generate_banner.py
Fonts default to Windows Segoe UI; override with PROFILE_FONT_DIR if needed.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets"
FONTS = Path(os.environ.get("PROFILE_FONT_DIR", "C:/Windows/Fonts"))
WIDTH, HEIGHT = 1200, 400
PAPER = "#F3F0E9"
INK = "#24312D"
MUTED = "#52615A"
ACCENT = "#B43E20"


def font(size, bold=False):
    return ImageFont.truetype(str(FONTS / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)


def render(frame):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 10, HEIGHT), fill=ACCENT)
    draw.text((52, 36), "ALVESDEV / @alvesfers", font=font(18, True), fill=MUTED)
    draw.text((48, 84), "Fernando Alves", font=font(76, True), fill=INK)
    draw.text((52, 184), "Desenvolvedor full stack", font=font(30), fill=INK)
    draw.text((52, 235), "Do backend à experiência de quem usa.", font=font(23), fill=MUTED)
    draw.line((52, 311, 770, 311), fill="#C9CFC5", width=1)
    draw.text((52, 337), "PHP  /  LARAVEL  /  VUE.JS  /  JAVASCRIPT", font=font(17, True), fill=INK)
    draw.rounded_rectangle((839, 42, 1158, 358), radius=26, fill=INK)
    # A continuous circuit: backend, API, interface. Each dot completes one loop.
    route = [(902, 118), (1096, 118), (1096, 282), (902, 282), (902, 118)]
    draw.line(route, fill="#53645C", width=2)
    for x, y in route[:-1]:
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#95AB9C")
    edges = [194, 164, 194, 164]
    for offset in (0, 1 / 3, 2 / 3):
        distance = ((frame / 72 + offset) % 1) * sum(edges)
        for index, length in enumerate(edges):
            if distance <= length:
                start, end = route[index], route[index + 1]
                x = start[0] + (end[0] - start[0]) * distance / length
                y = start[1] + (end[1] - start[1]) * distance / length
                draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill="#EAA783")
                break
            distance -= length
    draw.text((946, 148), "{ }", font=font(62, True), fill=PAPER)
    draw.text((934, 233), "ideia → código", font=font(20), fill=PAPER)
    draw.text((1045, 337), "SP / BR", font=font(14, True), fill=PAPER)
    return canvas


if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=True)
    frames = [render(frame) for frame in range(72)]
    frames[0].save(OUTPUT / "profile-banner.png", optimize=True)
    palette = frames[0].quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(
        OUTPUT / "profile-banner.gif", save_all=True, append_images=indexed[1:],
        duration=70, loop=0, optimize=True, disposal=1,
    )
    print(f"Generated {len(indexed)} frames in {OUTPUT}")
