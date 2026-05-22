# Real-Time Sorting Software

`sort_with_tensorrt.py` is the main runtime for live image-activated sorting.
It captures DirectShow frames, crops the droplet ROI, runs TensorRT inference,
draws the detection overlay, and sends serial commands to Arduino.

## Run

```powershell
python software/realtime_sorting/sort_with_tensorrt.py --serial-port COM5 --camera-index 0
```

## Important Parameters

- `--serial-port`: Arduino COM port.
- `--baud-rate`: serial baud rate, default `9600`.
- `--camera-index`: DirectShow camera index.
- `--capture-interval`: frame grab interval, default `0.010` s.
- `--frame-roi-start-x`: ROI x start in the camera frame.
- `--frame-roi-start-y`: ROI y start in the camera frame.
- `--frame-roi-width`: ROI width.
- `--gate-position`: virtual-gate x-position inside the ROI.
- `--threshold`: width of trigger bins around the virtual gate.
- `--confidence`: minimum detection confidence for triggering.
- `--model-path`: TensorRT engine path.
- `--dll-path`: inference DLL path.

Default model paths point to:

```text
models/best160-1.engine
models/best160-1.dll
```

## Dry Run Checklist

Run with the high-voltage module disconnected.

1. Confirm the camera frame appears.
2. Confirm the ROI contains droplets before the sorting junction.
3. Confirm bounding boxes are drawn on droplets.
4. Confirm class labels match visual droplet contents.
5. Confirm Arduino pins pulse only for target classes.
6. Confirm each droplet triggers once at the virtual gate.

## Tuning Sequence

1. Tune ROI x/y/width until droplets are fully visible.
2. Tune `--confidence` to reduce false triggers.
3. Tune `--gate-position` so commands are sent early enough for actuation.
4. Tune `--threshold` to avoid repeated commands.
5. Tune Arduino delay values while watching oscilloscope pulses.
6. Connect high voltage only after dry-run behavior is stable.
