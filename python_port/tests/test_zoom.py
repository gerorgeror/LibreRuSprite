from libresprite_py.zoom import Zoom


def test_linear_values_matches_scale_table() -> None:
    assert Zoom.linear_values() == 25


def test_from_scale_around_one() -> None:
    zoom = Zoom.from_scale(0.99)
    assert (zoom.num, zoom.den) == (1, 1)
    assert zoom.internal_scale == 0.99


def test_zoom_in_and_out() -> None:
    z = Zoom(1, 1)
    assert z.zoom_in().num == 2
    assert z.zoom_out().den == 2


def test_clamps_linear_scale() -> None:
    assert Zoom.from_linear_scale(-100).den == 64
    assert Zoom.from_linear_scale(100).num == 64
