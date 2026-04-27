"""Minimal sprite domain model for the Python LibreSprite port."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

Color = tuple[int, int, int, int]


def _clamp_u8(v: int) -> int:
    return max(0, min(255, int(v)))


@dataclass(slots=True)
class Sprite:
    width: int
    height: int
    pixels: list[Color]

    @classmethod
    def create(cls, width: int, height: int, color: Color = (0, 0, 0, 0)) -> "Sprite":
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        return cls(width, height, [color for _ in range(width * height)])

    def _idx(self, x: int, y: int) -> int:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            raise IndexError("pixel coordinates out of bounds")
        return y * self.width + x

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        r, g, b, a = color
        self.pixels[self._idx(x, y)] = (_clamp_u8(r), _clamp_u8(g), _clamp_u8(b), _clamp_u8(a))

    def get_pixel(self, x: int, y: int) -> Color:
        return self.pixels[self._idx(x, y)]

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "pixels": [list(px) for px in self.pixels],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Sprite":
        width = int(data["width"])
        height = int(data["height"])
        raw_pixels = data["pixels"]
        if len(raw_pixels) != width * height:
            raise ValueError("pixels length does not match width*height")

        pixels: list[Color] = []
        for px in raw_pixels:
            if len(px) != 4:
                raise ValueError("each pixel must have 4 components")
            pixels.append(tuple(_clamp_u8(c) for c in px))
        return cls(width, height, pixels)

    def save_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n")

    @classmethod
    def load_json(cls, path: str | Path) -> "Sprite":
        return cls.from_dict(json.loads(Path(path).read_text()))

    def export_ppm(self, path: str | Path) -> None:
        """Export sprite to portable pixmap (P6). Alpha is composited over black."""
        header = f"P6\n{self.width} {self.height}\n255\n".encode("ascii")
        data = bytearray()
        for r, g, b, a in self.pixels:
            alpha = a / 255.0
            data.extend((int(r * alpha), int(g * alpha), int(b * alpha)))
        Path(path).write_bytes(header + bytes(data))
