# Data And Model Training

The detector can be retrained for different chips, magnifications, cell types,
droplet sizes, or target classes. The provided model uses three droplet classes:

- `0`: empty droplet
- `1`: single-cell droplet
- `2`: multi-cell droplet

## Data Collection

1. Record videos of droplets flowing through the imaging region.
2. Include empty, single-cell, and multi-cell droplets.
3. Record under illumination and focus conditions similar to sorting operation.
4. Avoid motion blur by matching exposure time to droplet speed.
5. Capture enough background variation to make the model robust to small
   changes in chip position and lighting.

## Frame Extraction

Use the frame extraction utility:

```powershell
python software/dataset_tools/video_to_images.py input.mp4 frames --every 1
```

Use `--every N` to save fewer frames when adjacent frames are too similar.

## Image Cropping

Crop droplet regions to square training images:

```powershell
python software/dataset_tools/crop_images.py frames cropped --x 300 --y 100 --size 160
```

Interactive mode:

```powershell
python software/dataset_tools/crop_images.py frames cropped --interactive
```

Interactive keys:

- `W`, `A`, `S`, `D`: move the crop region
- `SPACE`: save a crop
- `N`: advance to the next image

The demonstrated model used 160 x 160 training images and 320 labeled images.
More images are recommended when changing cells, optics, illumination, or chip
geometry.

## Labeling

Use LabelImg or another YOLO-format annotation tool.

Label every visible droplet in each crop:

- class `0`: droplet with no cell
- class `1`: droplet with one cell
- class `2`: droplet with two or more cells

Recommended checks:

- Verify that class indices match the runtime expectation.
- Verify bounding boxes cover the droplet body and visible cell content.
- Split images into train/validation sets from different video segments.
- Do not use nearly identical adjacent frames in both train and validation.

## YOLOv5s Training Parameters

Starting parameters used for the provided detector:

- model family: YOLOv5s
- image size: 160 x 160
- labeled images: 320
- batch size: 126
- epochs: 500
- training platform: Google Colab or equivalent GPU workstation

Example class configuration:

```yaml
nc: 3
names: ["0", "1", "2"]
```

## Runtime Export

The real-time sorter uses TensorRT for inference. A typical workflow is:

1. Train YOLOv5s and export PyTorch weights.
2. Validate detection accuracy on held-out images.
3. Export to ONNX or TensorRT using a version compatible with the deployment
   workstation.
4. Place the runtime artifacts in `models/`.
5. Update checksums in `models/checksums.txt`.
6. Run the sorter with high voltage disconnected and verify overlays.

Rebuild the TensorRT engine whenever CUDA, TensorRT, GPU model, or driver
versions change.

## Acceptance Criteria

Before using a new model for high-voltage sorting:

- detection overlay follows droplets frame by frame
- empty, single-cell, and multi-cell classes are visually correct
- confidence threshold rejects low-quality detections
- false positives in the virtual-gate region are rare
- runtime inference stays below the required latency for the chosen flow speed
