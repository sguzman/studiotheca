#!/usr/bin/env python3
"""Deterministic candidate exports from the approved Dusk Raven Works raster.

Requires Pillow only for generation. The archive's core validator is stdlib-only.
The source image is never overwritten; generated layouts are not approved logos.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

SOURCE_HASH = "8a0e0d072a5f601366de6861976a060e52d96685ec4a129c8de4243fca7f8200"
SOURCE_SIZE = (1254, 1254)


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def banner(im: Image.Image, size: tuple[int, int], foreground_ratio: float) -> Image.Image:
    width, height = size
    background = ImageOps.fit(
        im, (width, height), method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.35)
    ).filter(ImageFilter.GaussianBlur(max(20, width // 35)))
    background = Image.blend(background, Image.new("RGB", size, (8, 7, 20)), 0.32)
    side = round(height * foreground_ratio)
    foreground = im.resize((side, side), Image.Resampling.LANCZOS)
    if side > height:
        y = max(0, (side - height) // 3)
        foreground = foreground.crop((0, y, side, y + height))
    elif side < height:
        box = Image.new("RGB", (side, height), (8, 7, 20))
        box.paste(foreground, (0, (height - side) // 2))
        foreground = box
    edge = min(100, max(24, foreground.width // 10))
    mask = Image.new("L", foreground.size, 0)
    draw = ImageDraw.Draw(mask)
    for i in range(edge):
        alpha = int(255 * i / edge)
        draw.line((i, 0, i, height), fill=alpha)
        draw.line((foreground.width - i - 1, 0, foreground.width - i - 1, height), fill=alpha)
    draw.rectangle((edge, 0, foreground.width - edge, height), fill=255)
    background.paste(foreground, ((width - foreground.width) // 2, 0), mask)
    return background


def build(source: Path, output: Path, verify: bool = True) -> dict:
    if verify and checksum(source) != SOURCE_HASH:
        raise ValueError("Wrong source SHA-256: refusing to generate a derivative")
    original = Image.open(source).convert("RGB")
    if verify and original.size != SOURCE_SIZE:
        raise ValueError("Wrong source dimensions")
    output.mkdir(parents=True, exist_ok=True)
    specs = [
        ("avatar-full-512.png", original.resize((512, 512), Image.Resampling.LANCZOS), "PNG", {}),
        ("avatar-full-256.png", original.resize((256, 256), Image.Resampling.LANCZOS), "PNG", {}),
        ("avatar-full-128.webp", original.resize((128, 128), Image.Resampling.LANCZOS), "WEBP", {"quality": 85}),
        ("avatar-full-64.webp", original.resize((64, 64), Image.Resampling.LANCZOS), "WEBP", {"quality": 85}),
        ("avatar-full-32.webp", original.resize((32, 32), Image.Resampling.LANCZOS), "WEBP", {"quality": 85}),
        ("banner-16x9-1600x900.webp", banner(original, (1600, 900), 1.0), "WEBP", {"quality": 88}),
        ("header-3x1-1500x500.webp", banner(original, (1500, 500), 2.0), "WEBP", {"quality": 88}),
    ]
    manifest = {
        "schema": "studiotheca.artwork-exports.v1",
        "source_file": source.name,
        "source_sha256": checksum(source),
        "source_dimensions": list(original.size),
        "status": "draft derivative exports; not canonical logos",
        "exports": []
    }
    for name, img, fmt, opts in specs:
        path = output / name
        img.save(path, fmt, **opts)
        manifest["exports"].append({
            "file": name, "dimensions": list(img.size), "format": fmt,
            "bytes": path.stat().st_size, "sha256": checksum(path),
            "role": "layout proof, unapproved"
        })
    (output / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="The exact verified original PNG")
    parser.add_argument("output", type=Path, help="Export destination directory")
    parser.add_argument(
        "--skip-source-check", action="store_true",
        help="Synthetic fixtures only; never use for production artwork"
    )
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output, not args.skip_source_check), indent=2))
