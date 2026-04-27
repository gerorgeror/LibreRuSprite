"""Small filter ports from `src/filters` for the Python rewrite."""

from __future__ import annotations

from dataclasses import dataclass

from libresprite_py.sprite import Sprite


@dataclass(slots=True)
class ChannelTarget:
    red: bool = True
    green: bool = True
    blue: bool = True
    alpha: bool = False


def invert_rgba(color: tuple[int, int, int, int], target: ChannelTarget | None = None) -> tuple[int, int, int, int]:
    target = target or ChannelTarget()
    r, g, b, a = color
    if target.red:
        r ^= 0xFF
    if target.green:
        g ^= 0xFF
    if target.blue:
        b ^= 0xFF
    if target.alpha:
        a ^= 0xFF
    return r, g, b, a


def invert_sprite(sprite: Sprite, target: ChannelTarget | None = None) -> Sprite:
    target = target or ChannelTarget()
    out = Sprite.create(sprite.width, sprite.height)
    for y in range(sprite.height):
        for x in range(sprite.width):
            out.set_pixel(x, y, invert_rgba(sprite.get_pixel(x, y), target))
    return out
