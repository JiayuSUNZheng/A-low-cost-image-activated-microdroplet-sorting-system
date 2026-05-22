# Dataset Tools

Utilities used during dataset preparation.

Extract frames from a video:

```powershell
python video_to_images.py input.mp4 frames --every 1
```

Crop fixed-size training images:

```powershell
python crop_images.py frames cropped --x 300 --y 100 --size 160
```

Use interactive ROI selection:

```powershell
python crop_images.py frames cropped --interactive
```

In interactive mode, use `W`, `A`, `S`, `D` to move the ROI, `SPACE` to save a
crop, and `N` to advance to the next image.
