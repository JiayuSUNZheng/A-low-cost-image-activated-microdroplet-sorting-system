# Arduino One-Class Sorting

Use this sketch when a single droplet class should trigger one high-voltage
output path.

Default behavior:

- output pin: 8
- serial baud rate: 9600
- output pulse duration: 4 ms
- commands: `0`, `1`, `2`, `3`

The commands encode coarse timing bins around the virtual gate. Tune the delay
values in the sketch after measuring actual camera-to-electrode timing.
