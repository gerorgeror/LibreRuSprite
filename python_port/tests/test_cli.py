import sys
from pathlib import Path

from libresprite_py.cli import main
from libresprite_py.sprite import Sprite


def test_cli_zoom(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["libresprite-py", "zoom", "--scale", "1.0", "--direction", "in"])
    rc = main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "num=2 den=1" in out


def test_cli_project_flow(monkeypatch, tmp_path: Path) -> None:
    project = tmp_path / "sprite.json"
    ppm = tmp_path / "sprite.ppm"

    monkeypatch.setattr(
        sys,
        "argv",
        ["libresprite-py", "new", "--width", "2", "--height", "2", "--output", str(project)],
    )
    assert main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "libresprite-py",
            "paint",
            "--project",
            str(project),
            "--x",
            "1",
            "--y",
            "0",
            "--color",
            "255,0,0,255",
        ],
    )
    assert main() == 0

    sprite = Sprite.load_json(project)
    assert sprite.get_pixel(1, 0) == (255, 0, 0, 255)

    monkeypatch.setattr(
        sys,
        "argv",
        ["libresprite-py", "export-ppm", "--project", str(project), "--output", str(ppm)],
    )
    assert main() == 0
    assert ppm.exists()
