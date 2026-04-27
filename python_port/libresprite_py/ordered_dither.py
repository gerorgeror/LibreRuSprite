"""Python port of ordered dithering primitives from `src/render/ordered_dither.h`."""

from __future__ import annotations

from dataclasses import dataclass, field

Color = tuple[int, int, int, int]


def _clamp_u8(value: int) -> int:
    return max(0, min(255, value))


def color_distance(c1: Color, c2: Color) -> int:
    r1, g1, b1, a1 = c1
    r2, g2, b2, a2 = c2
    return int(
        (r1 - r2) * (r1 - r2) * 21
        + (g1 - g2) * (g1 - g2) * 71
        + (b1 - b2) * (b1 - b2) * 7
        + (a1 - a2) * (a1 - a2)
    )


@dataclass(slots=True)
class BayerMatrix:
    size: int
    _matrix: list[int] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.size < 2 or (self.size & (self.size - 1)) != 0:
            raise ValueError("size must be a power of two and >= 2")
        self._matrix = [self._dn(i, j, self.size) for i in range(self.size) for j in range(self.size)]

    @staticmethod
    def _d2(i: int, j: int) -> int:
        return (0, 2, 3, 1)[i * 2 + j]

    def _dn(self, i: int, j: int, n: int) -> int:
        if n == 2:
            return self._d2(i, j)
        half = n // 2
        return 4 * self._dn(i % half, j % half, half) + self._dn(i // half, j // half, 2)

    def max_value(self) -> int:
        return self.size * self.size

    def at(self, i: int, j: int) -> int:
        return self._matrix[(i % self.size) * self.size + (j % self.size)]


@dataclass(slots=True)
class Palette:
    colors: list[Color]

    def get(self, index: int) -> Color:
        return self.colors[index]

    def find_bestfit(self, color: Color, transparent_index: int = -1) -> int:
        best_idx = 0
        best_dist = 1 << 60
        for idx, candidate in enumerate(self.colors):
            if idx == transparent_index:
                continue
            dist = color_distance(candidate, color)
            if dist < best_dist:
                best_idx = idx
                best_dist = dist
        return best_idx


def dither_rgb_pixel_to_index(
    matrix: BayerMatrix,
    color: Color,
    x: int,
    y: int,
    palette: Palette,
    transparent_index: int = -1,
) -> int:
    r, g, b, a = color
    if transparent_index >= 0 and a == 0:
        return transparent_index

    nearest1_idx = palette.find_bestfit(color, transparent_index)
    nearest1 = palette.get(nearest1_idx)

    r2 = _clamp_u8(r - (nearest1[0] - r))
    g2 = _clamp_u8(g - (nearest1[1] - g))
    b2 = _clamp_u8(b - (nearest1[2] - b))
    a2 = _clamp_u8(a - (nearest1[3] - a))
    nearest2_idx = palette.find_bestfit((r2, g2, b2, a2), transparent_index)

    if nearest1_idx == nearest2_idx:
        return nearest1_idx

    nearest2 = palette.get(nearest2_idx)
    d = color_distance(nearest1, color)
    D = color_distance(nearest1, nearest2)
    if D == 0:
        return nearest1_idx

    d = matrix.max_value() * d // D
    threshold = matrix.at(x, y)
    return nearest2_idx if d > threshold else nearest1_idx
