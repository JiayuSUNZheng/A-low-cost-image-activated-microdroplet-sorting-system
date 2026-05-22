# Troubleshooting

## Camera Not Found

- Check Device Manager for the camera.
- Run the DirectShow device listing command in `docs/software_setup.md`.
- Try a different `--camera-index`.
- Close vendor camera software that may already hold the device.

## No Detections

- Confirm `models/best160-1.engine` and `models/best160-1.dll` exist.
- Confirm the ROI contains droplets.
- Lower `--confidence` during debugging.
- Check illumination and focus.
- Test the detector on a still image before live sorting.

## TensorRT Or DLL Error

- Confirm the DLL is Windows x86-64.
- Confirm TensorRT, CUDA, GPU driver, and engine versions are compatible.
- Rebuild the TensorRT engine on the deployment workstation.
- Check `models/checksums.txt` for file integrity.

## Serial Port Error

- Confirm the Arduino COM port.
- Close Arduino Serial Monitor or other software using the port.
- Confirm baud rate is `9600`.
- Try a simple serial test before running the full sorter.

## Arduino Pulse Missing

- Confirm the correct sketch is uploaded.
- Measure pins 8 and 9 with an oscilloscope.
- Confirm Python sends commands only when droplets pass the virtual gate.
- Confirm USB cable and board power are stable.

## False Triggering

- Increase `--confidence`.
- Narrow `--threshold`.
- Move the virtual gate to a region with clearer droplet images.
- Improve lighting uniformity.
- Retrain with more negative examples and difficult frames.

## Target Droplets Miss The Sorted Outlet

- Verify high-voltage pulse amplitude and duration.
- Tune `--gate-position` and firmware delay values.
- Reduce flow speed.
- Increase droplet spacing.
- Confirm electrode wiring polarity and ground connections.
- Check whether the droplet is centered in the channel before actuation.

## Neighbor Droplets Are Disturbed

- Increase spacing oil flow.
- Reduce droplet generation or reinjection rate.
- Shorten pulse duration only if actuation remains sufficient.
- Reduce voltage only if target droplets still sort reliably.

## Droplets Merge Or Break

- Check surfactant and oil compatibility.
- Reduce abrupt pressure changes.
- Inspect chip surface treatment.
- Check for dust or channel defects.
