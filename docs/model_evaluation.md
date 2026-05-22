# Model Evaluation

The detector must be evaluated before it is used to trigger high voltage.

## Detection Metrics

Use the standard object-detection metrics produced by YOLO training:

- precision
- recall
- mAP@0.5
- mAP@0.5:0.95
- confusion matrix

For sorting, false positives near the virtual gate are especially important
because they can trigger unwanted actuation.

## Visual Evaluation

Review detection overlays on videos recorded from the actual sorting setup.

Check that:

- class `0` droplets are not triggered
- class `1` droplets are detected consistently
- class `2` droplets are classified separately from class `1`
- bounding boxes are stable while droplets move through the ROI
- detections do not flicker at the virtual gate
- lighting changes do not create false droplets

## Runtime Evaluation

Measure inference time on the deployment workstation. The demonstrated target is
less than 5 ms per input image. The total detection and command loop must stay
within the droplet arrival interval.

If throughput is unstable:

- reduce ROI width
- rebuild the TensorRT engine for the target GPU
- increase confidence threshold
- reduce camera frame size if supported
- lower droplet generation or reinjection speed

## Sorting Evaluation

Run evaluation in stages:

1. camera and model overlay only
2. Arduino trigger output only
3. high-voltage output into dummy load
4. chip connected with non-biological test droplets
5. full sample sorting

Record sorted outlet composition and calculate sorting accuracy from collected
droplets. The demonstrated setup reached 96.4% after tuning.
