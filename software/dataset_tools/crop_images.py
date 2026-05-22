"""Crop fixed-size training images from source frames."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


IMAGE_EXTENSIONS = {".bmp", ".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crop fixed-size regions from a directory of images."
    )
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--x", type=int, default=300, help="Crop start x position.")
    parser.add_argument("--y", type=int, default=100, help="Crop start y position.")
    parser.add_argument("--size", type=int, default=160, help="Square crop size.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Use WASD to move ROI, SPACE to save, and N for next image.",
    )
    return parser.parse_args()


def image_paths(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def write_crop(image, source_path: Path, output_dir: Path, x: int, y: int, size: int) -> Path:
    cropped = image[y : y + size, x : x + size]
    output_path = output_dir / f"{source_path.stem}_crop{source_path.suffix}"
    cv2.imwrite(str(output_path), cropped)
    return output_path


def interactive_crop(paths: list[Path], output_dir: Path, x: int, y: int, size: int) -> None:
    for source_path in paths:
        crop_index = 0
        next_image = False
        while not next_image:
            frame = cv2.imread(str(source_path))
            if frame is None:
                break

            preview = frame.copy()
            cv2.rectangle(preview, (x, y), (x + size, y + size), (255, 0, 255), 1)
            cv2.imshow("Crop ROI", preview)
            keycode = cv2.waitKey(1)

            if keycode == ord(" "):
                cropped = frame[y : y + size, x : x + size]
                output_path = output_dir / (
                    f"{source_path.stem}_crop{crop_index}{source_path.suffix}"
                )
                cv2.imwrite(str(output_path), cropped)
                print(f"Saved {output_path}")
                crop_index += 1
            elif keycode == ord("w"):
                y -= 10
            elif keycode == ord("s"):
                y += 10
            elif keycode == ord("a"):
                x -= 10
            elif keycode == ord("d"):
                x += 10
            elif keycode == ord("n"):
                next_image = True

    cv2.destroyAllWindows()


def batch_crop(paths: list[Path], output_dir: Path, x: int, y: int, size: int) -> None:
    for source_path in paths:
        frame = cv2.imread(str(source_path))
        if frame is None:
            print(f"Skipping unreadable image: {source_path}")
            continue

        output_path = write_crop(frame, source_path, output_dir, x, y, size)
        print(f"Saved {output_path}")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = image_paths(args.input_dir)

    if args.interactive:
        interactive_crop(paths, args.output_dir, args.x, args.y, args.size)
    else:
        batch_crop(paths, args.output_dir, args.x, args.y, args.size)


if __name__ == "__main__":
    main()
