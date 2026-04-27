from __future__ import annotations

import argparse

from libresprite_py.zoom import Zoom


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="libresprite-py",
        description="Early Python rewrite utilities for LibreSprite.",
    )
    parser.add_argument("--scale", type=float, default=1.0, help="Base scale value")
    parser.add_argument(
        "--direction",
        choices=("in", "out", "none"),
        default="none",
        help="Change zoom level after resolving nearest scale",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    zoom = Zoom.from_scale(args.scale)
    if args.direction == "in":
        zoom = zoom.zoom_in()
    elif args.direction == "out":
        zoom = zoom.zoom_out()

    print(f"num={zoom.num} den={zoom.den} scale={zoom.scale:.6f} internal={zoom.internal_scale:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
