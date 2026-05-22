# Software Setup

The real-time sorter is designed for Windows because it uses DirectShow camera
capture and a Windows x86-64 TensorRT DLL.

## Target Workstation

Recommended starting environment:

- Windows 11, 64-bit
- NVIDIA GPU with CUDA support
- Python 3.9
- OpenCV 4.5
- PyTorch 1.11.0
- TensorRT 8.2.5.1
- Arduino IDE or Arduino CLI

The demonstrated workstation used an AMD Ryzen 7 5800H CPU, 16 GB RAM, and an
NVIDIA GTX 3060Ti 6 GB GPU.

## Python Environment

Create and activate a Python 3.9 environment, then install:

```powershell
pip install -r software/requirements-windows.txt
```

Core Python packages:

- `opencv-python`
- `numpy`
- `pyserial`
- `pygrabber`
- `PyQt5`
- `imutils`
- `torch`

TensorRT itself is installed separately from NVIDIA packages. Confirm the
TensorRT Python/runtime libraries match the GPU driver and CUDA environment.

## Model Files

Model artifacts are stored in `models/`:

- `best160-1.pt`: YOLOv5s PyTorch weights
- `best160-1.engine`: TensorRT engine
- `best160-1.dll`: Windows inference wrapper used by `python_trt.py`
- `checksums.txt`: SHA256 checksums

The `.engine` file is platform-specific. Rebuild it when changing GPU,
TensorRT, CUDA, or driver versions.

## Arduino Setup

1. Connect the Arduino by USB.
2. Open Device Manager and identify the COM port.
3. Upload one of the sketches in `firmware/`.
4. Confirm the baud rate is `9600`.
5. Keep the high-voltage module disconnected for the first serial test.

## Camera Setup

Check available DirectShow camera indices:

```powershell
python -c "from pygrabber.dshow_graph import FilterGraph; print(FilterGraph().get_input_devices())"
```

Use the index of the high-speed camera in the runtime command.

## Dry Run Command

Run without high voltage connected:

```powershell
python software/realtime_sorting/sort_with_tensorrt.py --serial-port COM5 --camera-index 0
```

If the model files are in another location:

```powershell
python software/realtime_sorting/sort_with_tensorrt.py `
  --serial-port COM5 `
  --camera-index 0 `
  --model-path C:\path\to\best160-1.engine `
  --dll-path C:\path\to\best160-1.dll
```

## Runtime Parameters

Common parameters:

- `--serial-port`: Arduino COM port.
- `--baud-rate`: default `9600`.
- `--camera-index`: DirectShow camera index.
- `--capture-interval`: default `0.010` s.
- `--frame-roi-start-x`: ROI x start.
- `--frame-roi-start-y`: ROI y start.
- `--frame-roi-width`: ROI width.
- `--gate-position`: virtual-gate x-position inside the ROI.
- `--threshold`: trigger-bin half-width around the virtual gate.
- `--confidence`: minimum detector confidence for triggering.
- `--droplet-distance`: estimated spacing between droplet centers.

Use conservative threshold and confidence values during initial tuning. Increase
sorting speed only after the detection overlay and Arduino output pulses are
stable.
