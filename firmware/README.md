# Firmware

Arduino sketches convert one-byte serial commands from the Python sorter into
timed output pulses for the high-voltage trigger driver.

## Sketches

- `arduino_one_class_sorting/`: one output pin for one target class.
- `arduino_two_class_sorting/`: separate output pins for class-1 and class-2
  target droplets.

Default settings:

- serial baud rate: 9600
- output pulse duration: 4 ms
- class-1 output pin: 8
- class-2 output pin: 9 in the two-class sketch

Always test Arduino output pins with an oscilloscope before connecting the
high-voltage trigger driver.
