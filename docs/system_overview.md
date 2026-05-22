# System Overview

The sorter is a closed-loop system that combines imaging, object detection,
timing logic, and high-voltage dielectrophoretic actuation.

## Subsystems

1. Microfluidic chip
   - Generates or receives droplets.
   - Spaces droplets before they reach the sorting junction.
   - Uses liquid-metal electrodes near the sorting junction.
   - Routes non-target droplets to the waste outlet and target droplets to the
     sorted outlet.

2. Imaging path
   - A high-speed camera is mounted on a microscope.
   - The runtime target is 120 FPS acquisition.
   - The demonstrated runtime frame size is 1280 x 640 every 10 ms.
   - The Python runtime crops a configurable ROI before inference.

3. Detection path
   - YOLOv5s detects droplet classes from the ROI.
   - TensorRT is used for low-latency inference.
   - The training crop size is 160 x 160.
   - The demonstrated target is less than 5 ms inference per image.

4. Trigger path
   - Python computes each detected droplet center.
   - The x-center is compared with a virtual gate.
   - If the droplet is a target class and lies inside a trigger bin, Python
     sends a one-byte serial command to Arduino.
   - Arduino converts that command into a delayed TTL-level pulse.

5. Actuation path
   - Arduino triggers a switching/driver stage.
   - The driver triggers the DC-DC high-voltage output.
   - The demonstrated actuation pulse is about 1.2 kV for 4 ms.
   - The electric field pulls the target droplet toward the sorted outlet.

## Data Flow

```text
camera frame
  -> crop ROI
  -> YOLOv5s/TensorRT detections
  -> class + confidence + bounding-box center
  -> virtual gate / trigger-bin decision
  -> serial command
  -> Arduino delay and output pulse
  -> high-voltage pulse
  -> droplet displacement at sorting junction
```

## Virtual Gate

The virtual gate is an x-position inside the ROI. It prevents repeated commands
for the same droplet and gives the system a timing reference before the droplet
reaches the electrodes.

Default runtime settings in `software/realtime_sorting/sort_with_tensorrt.py`:

- `--gate-position 290`
- `--threshold 50`
- `--droplet-distance 150`
- `--capture-interval 0.010`

The trigger region is divided into four bins around the gate. Each bin maps to
a different Arduino command so that the firmware can compensate timing.

## Arduino Command Protocol

The two-class runtime uses single ASCII byte commands:

| Command | Droplet class | Gate bin | Default Arduino delay |
| --- | --- | --- | --- |
| `0` | class 1 | far right of gate | 1 ms |
| `1` | class 1 | near right of gate | 1 ms |
| `2` | class 1 | near left of gate | 1.5 ms |
| `3` | class 1 | far left of gate | 1.5 ms |
| `4` | class 2 | far right of gate | 1 ms |
| `5` | class 2 | near right of gate | 1 ms |
| `6` | class 2 | near left of gate | 1.5 ms |
| `7` | class 2 | far left of gate | 1.5 ms |

Default output pins:

- class 1: Arduino digital pin 8
- class 2: Arduino digital pin 9

The firmware pulse duration is 4 ms. Adjust firmware delay values only after a
camera/serial dry run confirms that detections and command timing are stable.

## Performance Targets

- Detection and decision loop: up to 100 Hz in the demonstrated setup.
- Detector latency target: less than 5 ms per input image.
- Demonstration sorting accuracy after tuning: 96.4%.

These are setup-dependent targets. Revalidate them after any change in camera,
magnification, chip, flow rate, GPU, TensorRT version, or high-voltage module.
