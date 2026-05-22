"""Real-time YOLO/TensorRT droplet sorting control.

This script captures frames from a DirectShow camera, crops a region of
interest, runs the TensorRT detector, and sends compact serial commands to an
Arduino sketch that generates delayed trigger pulses for droplet actuation.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from threading import Event, Thread

import cv2
import serial
from pygrabber.dshow_graph import FilterGraph

from python_trt import Detector, visualize


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "best160-1.engine"
DEFAULT_DLL_PATH = PROJECT_ROOT / "models" / "best160-1.dll"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run real-time image-activated droplet sorting."
    )
    parser.add_argument("--serial-port", default="COM5", help="Arduino serial port.")
    parser.add_argument("--baud-rate", type=int, default=9600)
    parser.add_argument("--serial-timeout", type=float, default=5.0)
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--capture-interval", type=float, default=0.010)
    parser.add_argument("--frame-roi-width", type=int, default=640)
    parser.add_argument("--frame-roi-start-x", type=int, default=260)
    parser.add_argument("--frame-roi-start-y", type=int, default=230)
    parser.add_argument("--gate-position", type=int, default=290)
    parser.add_argument("--threshold", type=int, default=50)
    parser.add_argument("--confidence", type=float, default=0.88)
    parser.add_argument("--droplet-distance", type=float, default=150.0)
    parser.add_argument("--window-name", default="frame_window")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--dll-path", type=Path, default=DEFAULT_DLL_PATH)
    parser.add_argument("--warmup-command", default="5")
    parser.add_argument("--warmup-seconds", type=float, default=4.0)
    return parser.parse_args()


def serial_command_for_detection(
    class_id: int, distance: float, threshold: float
) -> bytes | None:
    """Map droplet class and virtual-gate distance to Arduino commands."""
    if 0.5 * threshold < distance <= threshold:
        bin_index = 0
    elif 0 <= distance <= 0.5 * threshold:
        bin_index = 1
    elif -0.5 * threshold <= distance < 0:
        bin_index = 2
    elif -1.0 * threshold <= distance < -0.5 * threshold:
        bin_index = 3
    else:
        return None

    if class_id == 1:
        return str(bin_index).encode("ascii")
    if class_id == 2:
        return str(bin_index + 4).encode("ascii")
    return None


class SortingRuntime:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.serial = serial.Serial(
            args.serial_port,
            args.baud_rate,
            timeout=args.serial_timeout,
        )
        self.serial.write(args.warmup_command.encode("ascii"))
        time.sleep(args.warmup_seconds)

        self.detector = Detector(
            model_path=str(args.model_path).encode("utf-8"),
            dll_path=str(args.dll_path),
        )
        self.graph = FilterGraph()

    @property
    def delay_unit_ms(self) -> float:
        return (
            1000
            * self.args.capture_interval
            * (2 * self.args.threshold / self.args.droplet_distance)
            / 4
        )

    def capture_loop(self, event: Event) -> None:
        while not event.is_set():
            self.graph.grab_frame()
            event.wait(self.args.capture_interval)

    def show_image(self, image) -> None:
        args = self.args
        y0 = args.frame_roi_start_y
        y1 = y0 + 160
        x0 = args.frame_roi_start_x
        x1 = x0 + args.frame_roi_width

        frame_roi = image[y0:y1, x0:x1]
        frame_roi = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2RGB)

        detections = self.detector.predict(frame_roi)
        frame_roi = visualize(frame_roi, detections)

        for detected_droplet in detections:
            x_center = int(detected_droplet[0] + detected_droplet[2] * 0.5)
            y_center = int(detected_droplet[1] + detected_droplet[3] * 0.5)
            class_id = int(detected_droplet[4])
            score = float(detected_droplet[5])
            distance = x_center - args.gate_position

            if score <= args.confidence:
                continue

            command = serial_command_for_detection(
                class_id=class_id,
                distance=distance,
                threshold=args.threshold,
            )
            if command is None:
                continue

            cv2.circle(frame_roi, (x_center + 10, y_center), 10, (255, 0, 0), 4)
            self.serial.write(command)

        frame_roi = cv2.cvtColor(frame_roi, cv2.COLOR_RGB2BGR)
        cv2.circle(frame_roi, (args.gate_position, 40), 5, (255, 0, 0), 2)
        cv2.circle(frame_roi, (args.gate_position - args.threshold, 40), 5, (255, 0, 0), 2)
        cv2.circle(frame_roi, (args.gate_position + args.threshold, 40), 5, (255, 0, 0), 2)
        cv2.line(frame_roi, (200, 140), (520, 140), (0, 255, 0), 3)
        image[y0:y1, x0:x1, :] = frame_roi

        cv2.imshow(args.window_name, image)
        cv2.waitKey(1)

    def run(self) -> None:
        print(f"Delay unit: {self.delay_unit_ms:.3f} ms")
        devices = self.graph.get_input_devices()
        print(f"Connecting to device {devices[self.args.camera_index]}")

        self.graph.add_video_input_device(self.args.camera_index)
        self.graph.add_sample_grabber(lambda image: self.show_image(image))
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()

        event = Event()
        capture_thread = Thread(target=self.capture_loop, args=(event,))
        capture_thread.start()

        try:
            input(
                f"Capturing images every {self.args.capture_interval}s. "
                "Press ENTER to terminate."
            )
        finally:
            event.set()
            capture_thread.join()
            self.detector.free()
            self.serial.close()
            cv2.destroyAllWindows()


def main() -> None:
    SortingRuntime(parse_args()).run()


if __name__ == "__main__":
    main()
