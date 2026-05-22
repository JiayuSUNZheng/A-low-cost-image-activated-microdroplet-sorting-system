"""Extract image frames from a droplet video."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a video to image frames.")
    parser.add_argument("video", type=Path, help="Input video path.")
    parser.add_argument("output_dir", type=Path, help="Directory for extracted frames.")
    parser.add_argument("--every", type=int, default=1, help="Save every Nth frame.")
    parser.add_argument("--prefix", default="frame", help="Output filename prefix.")
    parser.add_argument("--extension", default="jpg", help="Output image extension.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise SystemExit(f"Could not open video: {args.video}")

    frame_index = 0
    saved_index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break

        if frame_index % args.every == 0:
            output_path = args.output_dir / (
                f"{args.prefix}_{saved_index:06d}.{args.extension}"
            )
            cv2.imwrite(str(output_path), frame)
            saved_index += 1

        frame_index += 1

    capture.release()
    print(f"Saved {saved_index} frames to {args.output_dir}")


if __name__ == "__main__":
    main()
