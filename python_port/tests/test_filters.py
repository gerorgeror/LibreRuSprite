from libresprite_py.filters import ChannelTarget, invert_rgba, invert_sprite
from libresprite_py.sprite import Sprite


def test_invert_rgba_default_inverts_rgb_only() -> None:
    assert invert_rgba((10, 20, 30, 40)) == (245, 235, 225, 40)


def test_invert_rgba_alpha_only() -> None:
    target = ChannelTarget(red=False, green=False, blue=False, alpha=True)
    assert invert_rgba((10, 20, 30, 40), target) == (10, 20, 30, 215)


def test_invert_sprite_roundtrip_size() -> None:
    s = Sprite.create(2, 1)
    s.set_pixel(0, 0, (0, 0, 0, 255))
    s.set_pixel(1, 0, (255, 255, 255, 128))

    out = invert_sprite(s)
    assert out.width == 2
    assert out.height == 1
    assert out.get_pixel(0, 0) == (255, 255, 255, 255)
    assert out.get_pixel(1, 0) == (0, 0, 0, 128)
