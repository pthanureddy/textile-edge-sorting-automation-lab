from __future__ import annotations

import argparse
import json
from pathlib import Path

from textile_edge_sorting.pipeline import process_textile_item


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Classify a textile item from a sensor frame and PPM image patch.")
    parser.add_argument("--frame-file", type=Path, required=True, help="Text file containing one serial-style frame per line.")
    parser.add_argument("--image", type=Path, required=True, help="ASCII P3 PPM textile image patch.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    first_frame = next(line for line in args.frame_file.read_text(encoding="utf-8").splitlines() if line.strip())
    image_ppm = args.image.read_text(encoding="utf-8")
    response = process_textile_item(first_frame, image_ppm)
    print(json.dumps(response.model_dump(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
