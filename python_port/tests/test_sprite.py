from pathlib import Path

from libresprite_py.sprite import Sprite


def test_create_set_get_pixel() -> None:
    s = Sprite.create(2, 2)
    s.set_pixel(1, 1, (255, 128, 64, 255))
    assert s.get_pixel(1, 1) == (255, 128, 64, 255)


def test_save_load_json_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "sprite.json"
    s = Sprite.create(1, 1)
    s.set_pixel(0, 0, (10, 20, 30, 255))
    s.save_json(p)

    loaded = Sprite.load_json(p)
    assert loaded.width == 1
    assert loaded.height == 1
    assert loaded.get_pixel(0, 0) == (10, 20, 30, 255)


def test_export_ppm_writes_header_and_payload(tmp_path: Path) -> None:
    s = Sprite.create(1, 1)
    s.set_pixel(0, 0, (255, 0, 0, 255))
    out = tmp_path / "out.ppm"
    s.export_ppm(out)
    data = out.read_bytes()
    assert data.startswith(b"P6\n1 1\n255\n")
    assert data.endswith(bytes([255, 0, 0]))
