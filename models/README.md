# Models

This directory contains the trained YOLOv5s/TensorRT artifacts used by the
real-time sorter.

- `best160-1.pt`: PyTorch YOLOv5s weights.
- `best160-1.engine`: TensorRT engine used by the real-time sorter.
- `best160-1.dll`: Windows x86-64 TensorRT inference wrapper used by
  `software/realtime_sorting/python_trt.py`.

The TensorRT engine is platform-specific. Rebuild it if the CUDA, TensorRT,
GPU, or driver environment differs from the original Windows 11 workstation.
