# Hardware Setup

This guide describes the physical build needed to reproduce the droplet sorting
system. Dimensions and flow rates below are starting points for the provided
chip design and demonstration setup.

## Required Hardware

- Microfluidic sorting chip fabricated from `hardware/microfluidic_chip/`.
- Microscope with enough working distance for tubing, chip, and electrodes.
- High-speed camera capable of about 120 FPS acquisition.
- Windows GPU workstation.
- Arduino-compatible MCU.
- Triggered high-voltage pulse generator.
- DC-DC boost converter capable of about 1.2 kV output.
- Breadboard or custom PCB for low-voltage trigger wiring.
- Syringe pumps for sample, continuous oil, spacing oil, and reinjection.
- PTFE or compatible tubing, fittings, syringes, and collection tubing.
- 3D printed or machined holders from `hardware/holders/`.
- Oscilloscope and high-voltage probe for verification.

## Chip And Electrode Geometry

The chip design is provided as:

```text
hardware/microfluidic_chip/droplet_sorting_chip.dwg
```

Starting geometry values:

- main channel width: 145 um
- typical droplet diameter: about 40 um
- typical droplet interval: about 100 um
- electrode width: 20 um
- electrode gap: 20 um
- positive electrode protrusion: 20 um

The sorting junction uses one positive electrode between two ground electrodes.
Target droplets are pulled toward the sorted outlet when the high-voltage pulse
is applied.

## Chip Fabrication

1. Fabricate the channel mold using the DWG design and the lab's standard
   soft-lithography workflow.
2. Cast PDMS, cure, peel, and punch inlets/outlets.
3. Bond the PDMS device to a glass slide.
4. Fill the one-port-open electrode channels with liquid metal.
5. Before operation, coat fluidic channels with a hydrophobic surface modifier.
6. Inspect all channels and electrodes under the microscope before connecting
   pressure or voltage.

## Fluidic Connections

The chip supports both upstream droplet generation and reinjection.

In-chip generation starting points:

- cell suspension: 0.17 uL/min
- continuous oil phase: 2.8 uL/min
- spacing oil: 0.4 uL/min

Reinjection starting points:

- collected droplet reinjection: 2.97 uL/min
- spacing oil: 0.4 uL/min

Use spacing oil to increase distance between adjacent droplets before the
sorting junction. Insufficient spacing can cause the high-voltage pulse to
affect neighboring droplets.

## Imaging Setup

1. Mount the chip on the microscope.
2. Mount the high-speed camera using the provided holder or an equivalent
   rigid adapter.
3. Focus on the main channel upstream of the sorting electrodes.
4. Adjust illumination so droplets and cell contents are visible without
   saturating the image.
5. Confirm camera acquisition at the target frame rate before connecting the
   high-voltage module.

The runtime software crops a 160-pixel-high ROI from each frame. Align the ROI
so droplets are fully visible before reaching the virtual gate.

## High-Voltage Trigger Chain

Logical signal chain:

```text
Python serial command -> Arduino output pin -> trigger driver
  -> DC-DC boost converter -> chip electrodes
```

Demonstration starting point:

- high-voltage pulse amplitude: about 1.2 kV
- pulse duration: 4 ms
- observed droplet actuation delay: about 120 ms

Before connecting the chip:

1. Disconnect the chip electrodes.
2. Trigger Arduino manually or from Python.
3. Measure the Arduino pin with an oscilloscope.
4. Measure the high-voltage output with a rated high-voltage probe.
5. Confirm pulse width, amplitude, decay, and repetition behavior.
6. Only then connect the chip electrodes.

## Holders

Provided STL files:

- `hardware/holders/camera_holder.stl`
- `hardware/holders/amplifier_holder.stl`

Check dimensions against your microscope, camera body, stage, and high-voltage
module before printing. Printed parts must not expose high-voltage conductors.
