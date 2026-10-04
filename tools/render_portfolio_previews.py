#!/usr/bin/env python3
"""Render deterministic GitHub portfolio previews from the current app captures."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "screenshots"
W, H = 1920, 1080

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (242, 247, 255)
MUTED = (165, 179, 199)
GOLD = (247, 193, 67)
BLUE = (60, 134, 255)
GREEN = (55, 214, 153)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def background() -> Image.Image:
    image = Image.new("RGB", (W, H))
    px = image.load()
    for y in range(H):
        for x in range(W):
            base = y / H
            glow = max(0.0, 1.0 - (((x - 1500) / 950) ** 2 + ((y - 460) / 720) ** 2))
            px[x, y] = (
                int(7 + 3 * base + 6 * glow),
                int(12 + 6 * base + 15 * glow),
                int(23 + 11 * base + 23 * glow),
            )
    return image


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def phone(source: Path, width: int, *, border: int = 10, radius: int = 38) -> Image.Image:
    shot = Image.open(source).convert("RGB")
    height = round(width * shot.height / shot.width)
    shot = shot.resize((width, height), Image.Resampling.LANCZOS)
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)
    frame = Image.new("RGBA", (width + border * 2, height + border * 2), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle(
        (0, 0, frame.width - 1, frame.height - 1),
        radius=radius + border,
        fill=(22, 29, 42, 255),
        outline=(83, 98, 120, 255),
        width=2,
    )
    frame.paste(shot, (border, border), mask)
    return frame


def paste_shadow(canvas: Image.Image, item: Image.Image, xy: tuple[int, int], blur=28, opacity=150):
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    alpha = item.getchannel("A")
    solid = Image.new("RGBA", item.size, (0, 0, 0, opacity))
    solid.putalpha(alpha.point(lambda value: value * opacity // 255))
    shadow.alpha_composite(solid, (xy[0] + 12, xy[1] + 24))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
    canvas.alpha_composite(item, xy)


def pill(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color=GOLD):
    f = font(22, True)
    bounds = draw.textbbox((0, 0), text, font=f)
    pw = bounds[2] - bounds[0] + 42
    rounded_rect(draw, (x, y, x + pw, y + 48), 24, (*color, 255))
    draw.text((x + 21, y + 11), text, font=f, fill=(9, 16, 27, 255))
    return x + pw


def draw_brand(draw: ImageDraw.ImageDraw, x=110, y=88):
    rounded_rect(draw, (x, y, x + 54, y + 54), 16, GOLD)
    draw.text((x + 13, y + 7), "D", font=font(31, True), fill=(14, 20, 30))
    draw.text((x + 72, y + 4), "DEUTSCHIQ", font=font(33, True), fill=INK)


def cover():
    canvas = background().convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_brand(draw)

    draw.text((110, 238), "German that", font=font(78, True), fill=INK)
    draw.text((110, 326), "remembers", font=font(78, True), fill=GOLD)
    draw.text((110, 414), "your mistakes.", font=font(78, True), fill=INK)

    copy = [
        "Placement, a personal learning path, spaced review",
        "and an AI tutor — inside one Telegram Mini App.",
    ]
    for i, line in enumerate(copy):
        draw.text((114, 554 + i * 42), line, font=font(27), fill=MUTED)

    px = 112
    for label, color in (("A1–B2", GOLD), ("80 LESSONS", BLUE), ("3 UI LANGUAGES", GREEN)):
        px = pill(draw, px, 700, label, color) + 16

    draw.text((112, 862), "ADAPTIVE LEARNING  •  FASTAPI  •  REACT  •  TELEGRAM", font=font(20, True), fill=(111, 130, 158))

    left = phone(SHOTS / "03-lesson.png", 292)
    center = phone(SHOTS / "01-home.png", 354)
    right = phone(SHOTS / "05-analytics.png", 292)
    paste_shadow(canvas, left, (965, 235), blur=24, opacity=125)
    paste_shadow(canvas, right, (1594, 235), blur=24, opacity=125)
    paste_shadow(canvas, center, (1263, 128), blur=34, opacity=185)

    # Give the device group a quiet base rather than leaving it floating.
    base = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(base)
    bd.ellipse((930, 944, 1920, 1088), fill=(33, 93, 180, 38))
    canvas = Image.alpha_composite(canvas, base.filter(ImageFilter.GaussianBlur(28)))
    return canvas.convert("RGB")


def product_preview():
    canvas = background().convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_brand(draw, 110, 68)
    draw.text((110, 157), "One connected learning loop.", font=font(61, True), fill=INK)
    draw.text(
        (112, 235),
        "From the first placement question to a plan, guided practice and personal support.",
        font=font(26),
        fill=MUTED,
    )

    items = [
        ("01", "PLACE", "02-diagnostic.png", GOLD),
        ("02", "UNDERSTAND", "08-result.png", BLUE),
        ("03", "PLAN", "04-plan.png", GREEN),
        ("04", "PRACTISE", "06-ai-tutor.png", GOLD),
        ("05", "PROGRESS", "07-profile.png", BLUE),
    ]
    card_w, gap, start_x = 292, 48, 162
    for index, (number, label, filename, accent) in enumerate(items):
        x = start_x + index * (card_w + gap)
        draw.text((x + 5, 330), number, font=font(23, True), fill=accent)
        draw.text((x + 52, 330), label, font=font(22, True), fill=(190, 204, 223))
        line_y = 372
        draw.rounded_rectangle((x, line_y, x + card_w, line_y + 4), radius=2, fill=(*accent, 185))
        device = phone(SHOTS / filename, card_w - 12, border=8, radius=30)
        paste_shadow(canvas, device, (x - 2, 402), blur=20, opacity=135)

    return canvas.convert("RGB")


def main():
    required = [SHOTS / f"{i:02d}-{name}.png" for i, name in enumerate(
        ["home", "diagnostic", "lesson", "plan", "analytics", "ai-tutor", "profile", "result"], 1
    )]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing screenshots:\n" + "\n".join(missing))

    cover().save(SHOTS / "deutschiq-cover.png", optimize=True)
    product_preview().save(SHOTS / "deutschiq-product-preview.png", optimize=True)
    print("Rendered deutschiq-cover.png and deutschiq-product-preview.png")


if __name__ == "__main__":
    main()
