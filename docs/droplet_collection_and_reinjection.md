# Droplet Collection And Reinjection

The sorter can process droplets generated upstream on the same chip or droplets
collected off-chip and reinjected later.

## Off-Chip Collection

Use a collection module with three tubing connections:

- left tubing: connected to a syringe
- middle tubing: inlet from the droplet generation chip during collection
- right tubing: outlet to the sorting chip during reinjection

During collection, connect the middle tubing to the outlet of the droplet
generation chip and collect emulsion into the module.

## Reinjection

1. Connect the collection module outlet to the sorting chip reinjection inlet.
2. Start reinjection at about 2.97 uL/min.
3. Start spacing oil at about 0.4 uL/min.
4. Watch droplets enter the main channel.
5. Increase or decrease spacing oil until droplets are separated before the
   sorting junction.

The goal is to keep adjacent droplets far enough apart that the actuation pulse
does not disturb droplets immediately before or after the target droplet.

## Tuning Tips

- If droplets arrive as dense trains, increase spacing oil or reduce reinjection
  rate.
- If droplets break or merge, reduce pressure changes and check surfactant
  concentration.
- If droplets arrive off-center, inspect inlet geometry and tubing alignment.
- If reinjected droplets are difficult to classify, retrain the detector using
  reinjection videos.
