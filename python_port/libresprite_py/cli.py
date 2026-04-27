from __future__ import annotations

import argparse

from libresprite_py.sprite import Sprite
from libresprite_py.zoom import Zoom


def _parse_color(value: str) -> tuple[int, int, int, int]:
    parts = [int(p.strip()) for p in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("color must be r,g,b,a")
    return parts[0], parts[1], parts[2], parts[3]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="libresprite-py",
        description="Early Python rewrite utilities for LibreSprite.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    zoom_cmd = sub.add_parser("zoom", help="Inspect zoom levels")
    zoom_cmd.add_argument("--scale", type=float, default=1.0, help="Base scale value")
    zoom_cmd.add_argument(
        "--direction",
        choices=("in", "out", "none"),
        default="none",
        help="Change zoom level after resolving nearest scale",
    )

    new_cmd = sub.add_parser("new", help="Create a new sprite project JSON")
    new_cmd.add_argument("--width", type=int, required=True)
    new_cmd.add_argument("--height", type=int, required=True)
    new_cmd.add_argument("--output", required=True, help="Path to sprite JSON")

    paint_cmd = sub.add_parser("paint", help="Paint one pixel in a sprite project")
    paint_cmd.add_argument("--project", required=True)
    paint_cmd.add_argument("--x", type=int, required=True)
    paint_cmd.add_argument("--y", type=int, required=True)
    paint_cmd.add_argument("--color", type=_parse_color, required=True, help="r,g,b,a")

    export_cmd = sub.add_parser("export-ppm", help="Export sprite project to PPM image")
    export_cmd.add_argument("--project", required=True)
    export_cmd.add_argument("--output", required=True)

    return parser


def _run_zoom(args: argparse.Namespace) -> int:
    zoom = Zoom.from_scale(args.scale)
    if args.direction == "in":
        zoom = zoom.zoom_in()
    elif args.direction == "out":
        zoom = zoom.zoom_out()

    print(f"num={zoom.num} den={zoom.den} scale={zoom.scale:.6f} internal={zoom.internal_scale:.6f}")
    return 0


def _run_new(args: argparse.Namespace) -> int:
    sprite = Sprite.create(args.width, args.height)
    sprite.save_json(args.output)
    print(f"created {args.output} ({args.width}x{args.height})")
    return 0


def _run_paint(args: argparse.Namespace) -> int:
    sprite = Sprite.load_json(args.project)
    sprite.set_pixel(args.x, args.y, args.color)
    sprite.save_json(args.project)
    print(f"painted ({args.x},{args.y}) in {args.project}")
    return 0


def _run_export_ppm(args: argparse.Namespace) -> int:
    sprite = Sprite.load_json(args.project)
    sprite.export_ppm(args.output)
    print(f"exported {args.output}")
    return 0


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "zoom":
        return _run_zoom(args)
    if args.command == "new":
        return _run_new(args)
    if args.command == "paint":
        return _run_paint(args)
    if args.command == "export-ppm":
        return _run_export_ppm(args)
    raise RuntimeError(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
