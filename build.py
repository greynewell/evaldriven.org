#!/usr/bin/env python3
"""Generate OG image for evaldriven.org with current signatory count."""

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
REPO = "greynewell/evaldriven.org"


def fetch_stargazer_count():
    """Fetch stargazer count via gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{REPO}", "--jq", ".stargazers_count"],
            capture_output=True, text=True, timeout=30,
        )
        return int(result.stdout.strip())
    except Exception:
        return 0


def build_og_image(count):
    """Generate a 1200x630 OG image with the signatory count."""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)

    def mono(size):
        for name in ["DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                      "Courier New.ttf", "cour.ttf"]:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default(size)

    def bold(size):
        for name in ["DejaVuSansMono-Bold.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                      "Courier New Bold.ttf", "courbd.ttf"]:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return mono(size)

    draw.rectangle([20, 20, W - 21, H - 21], outline="#000000", width=3)

    check_font = mono(72)
    draw.text((W // 2, 120), "\u2713", fill="#000000", font=check_font, anchor="mm")

    title_font = bold(52)
    draw.text((W // 2, 220), "EVAL-DRIVEN", fill="#000000", font=title_font, anchor="mm")
    draw.text((W // 2, 285), "DEVELOPMENT", fill="#000000", font=title_font, anchor="mm")

    draw.line([(200, 330), (W - 200, 330)], fill="#000000", width=2)

    sub_font = mono(30)
    draw.text((W // 2, 380), "A manifesto for evaluation-driven", fill="#333333", font=sub_font, anchor="mm")
    draw.text((W // 2, 420), "AI development", fill="#333333", font=sub_font, anchor="mm")

    count_font = bold(36)
    draw.text((W // 2, 500), f"{count} signatories", fill="#000000", font=count_font, anchor="mm")

    url_font = mono(22)
    draw.text((W // 2, 565), "evaldriven.org", fill="#555555", font=url_font, anchor="mm")

    path = ROOT / "og.png"
    img.save(path, "PNG")
    return path


def main():
    count = fetch_stargazer_count()
    print(f"Stargazer count: {count}", file=sys.stderr)
    path = build_og_image(count)
    print(f"Generated {path} ({path.stat().st_size} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
