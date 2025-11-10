#!/usr/bin/env python3
# Requiere Python 3.6+
import sys
import base64
from PIL import Image

def png_to_embedded_svg(png_path: str, svg_path: str):
    img = Image.open(png_path)
    width, height = img.size

    with open(png_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" preserveAspectRatio="xMidYMid meet">
  <image width="{width}" height="{height}" href="data:image/png;base64,{b64}" />
</svg>
"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python embed_png_as_svg.py input.png output.svg")
        sys.exit(1)
    png_to_embedded_svg(sys.argv[1], sys.argv[2])

