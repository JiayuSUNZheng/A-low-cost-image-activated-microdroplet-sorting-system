# Arduino Two-Class Sorting

Use this sketch when class-1 and class-2 droplets should drive separate trigger
outputs.

Default pins:

- class 1: pin 8
- class 2: pin 9

Command mapping:

| Command | Class | Output pin |
| --- | --- | --- |
| `0` to `3` | class 1 | 8 |
| `4` to `7` | class 2 | 9 |

The commands also encode coarse timing bins around the virtual gate. Tune the
delay values in the sketch after measuring actual camera-to-electrode timing.
