"""Python port of LibreSprite zoom scale logic from src/render/zoom.cpp."""

from __future__ import annotations

from dataclasses import dataclass

SCALES: tuple[tuple[int, int], ...] = (
    (1, 64),
    (1, 48),
    (1, 32),
    (1, 24),
    (1, 16),
    (1, 12),
    (1, 8),
    (1, 6),
    (1, 5),
    (1, 4),
    (1, 3),
    (1, 2),
    (1, 1),  # 100%
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (8, 1),
    (12, 1),
    (16, 1),
    (24, 1),
    (32, 1),
    (48, 1),
    (64, 1),
)


@dataclass(slots=True)
class Zoom:
    """Zoom value represented as a fraction (numerator/denominator)."""

    num: int
    den: int
    _internal_scale: float | None = None

    def __post_init__(self) -> None:
        if self.num <= 0 or self.den <= 0:
            raise ValueError("num and den must be positive")
        if self._internal_scale is None:
            self._internal_scale = self.scale

    @property
    def scale(self) -> float:
        return self.num / self.den

    @property
    def internal_scale(self) -> float:
        return float(self._internal_scale)

    @property
    def linear_scale(self) -> int:
        for i, pair in enumerate(SCALES):
            if pair == (self.num, self.den):
                return i
        return self.find_closest_linear_scale(self.scale)

    def zoom_in(self) -> "Zoom":
        i = self.linear_scale
        if i < len(SCALES) - 1:
            n, d = SCALES[i + 1]
            return Zoom(n, d)
        return Zoom(self.num, self.den)

    def zoom_out(self) -> "Zoom":
        i = self.linear_scale
        if i > 0:
            n, d = SCALES[i - 1]
            return Zoom(n, d)
        return Zoom(self.num, self.den)

    @classmethod
    def from_scale(cls, scale: float) -> "Zoom":
        i = cls.find_closest_linear_scale(scale)
        n, d = SCALES[i]
        return cls(n, d, _internal_scale=scale)

    @classmethod
    def from_linear_scale(cls, index: int) -> "Zoom":
        index = max(0, min(index, len(SCALES) - 1))
        n, d = SCALES[index]
        return cls(n, d)

    @staticmethod
    def find_closest_linear_scale(scale: float) -> int:
        for i in range(1, len(SCALES) - 1):
            min_scale = SCALES[i - 1][0] / SCALES[i - 1][1]
            mid_scale = SCALES[i][0] / SCALES[i][1]
            max_scale = SCALES[i + 1][0] / SCALES[i + 1][1]
            if (min_scale + mid_scale) / 2.0 <= scale <= (mid_scale + max_scale) / 2.0:
                return i

        return 0 if scale < 1.0 else len(SCALES) - 1

    @staticmethod
    def linear_values() -> int:
        return len(SCALES)
