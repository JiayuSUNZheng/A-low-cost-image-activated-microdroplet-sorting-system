# Operation Protocol

This protocol is written for a complete system with chip, microscope, camera,
Arduino, high-voltage trigger chain, and syringe pumps assembled.

## 1. Pre-Run Inspection

1. Inspect the chip channels for dust, blocked channels, collapsed PDMS, or
   incomplete bonding.
2. Inspect liquid-metal electrodes for continuity and no leakage into fluidic
   channels.
3. Confirm all tubing is connected to the intended inlets and outlets.
4. Confirm sorted and waste outlets are connected to collection tubing.
5. Confirm the high-voltage output is disabled and discharged.

## 2. Fluidic Startup

For upstream generation:

1. Start continuous oil at about 2.8 uL/min.
2. Start spacing oil at about 0.4 uL/min.
3. Start cell suspension at about 0.17 uL/min.
4. Wait until droplets are stable and monodisperse.
5. Tune pump rates until droplet spacing is close to 100 um.

For reinjection:

1. Load collected droplets into the reinjection module.
2. Start reinjection at about 2.97 uL/min.
3. Start spacing oil at about 0.4 uL/min.
4. Tune spacing oil until adjacent droplets are separated before sorting.

## 3. Imaging Alignment

1. Focus on the main channel before the sorting junction.
2. Adjust illumination for visible droplet boundaries and cell contents.
3. Run the Python sorter with high voltage disconnected.
4. Tune ROI start x/y and ROI width until droplets are fully visible.
5. Confirm the detection overlay follows droplets without large false positives.

Example:

```powershell
python software/realtime_sorting/sort_with_tensorrt.py `
  --serial-port COM5 `
  --camera-index 0 `
  --frame-roi-start-x 260 `
  --frame-roi-start-y 230 `
  --frame-roi-width 640
```

## 4. Virtual Gate Tuning

1. Place the virtual gate upstream of the electrode center.
2. Start with `--gate-position 290` and `--threshold 50`.
3. Confirm target droplets are marked once, not repeatedly.
4. If droplets are triggered too early, move the gate downstream or increase the
   Arduino delay.
5. If droplets are triggered too late, move the gate upstream or reduce the
   Arduino delay.

The demonstrated optical setup used a virtual gate about 350 pixels upstream
from the electrode center. Recalibrate this distance for every camera/magnifier
combination.

## 5. Arduino And Pulse Dry Run

Keep high voltage disconnected from the chip.

1. Upload the selected Arduino sketch.
2. Run the Python sorter.
3. Measure Arduino output pins with an oscilloscope.
4. Confirm trigger pulses are 4 ms.
5. Confirm commands occur only when target droplets pass through the gate.
6. Confirm class-to-pin mapping if using two-class sorting.

## 6. High-Voltage Verification

With the chip still disconnected:

1. Connect Arduino output to the trigger driver.
2. Connect the high-voltage output to a rated dummy load.
3. Measure output with a high-voltage probe.
4. Confirm about 1.2 kV pulse amplitude.
5. Confirm pulse decay is fast enough for the intended sorting frequency.
6. Confirm the module does not self-trigger or latch on.

## 7. Sorting Run

1. Connect the high-voltage output to chip electrodes.
2. Start at low droplet density and conservative flow rates.
3. Enable the Python sorter.
4. Enable high voltage.
5. Observe target droplets at the sorting junction.
6. Tune voltage, gate, threshold, and delay bins until target droplets enter the
   sorted outlet while non-target droplets remain in the waste outlet.
7. Increase flow rate only after stable sorting is observed.

## 8. Collection And Shutdown

1. Collect sorted droplets from the sorted outlet.
2. Record runtime parameters, pump rates, voltage, pulse width, ROI, gate, and
   threshold.
3. Disable high voltage before stopping fluid flow.
4. Discharge high-voltage wiring.
5. Stop pumps.
6. Flush or dispose of chip and tubing according to sample safety rules.
