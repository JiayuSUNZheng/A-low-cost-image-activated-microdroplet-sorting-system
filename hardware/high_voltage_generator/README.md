# High-Voltage Generator

The high-voltage generator receives a TTL-level trigger from Arduino and applies
a short pulse to the chip electrodes.

Signal chain:

```text
Arduino digital output -> triggered driver module
  -> DC-DC boost converter -> chip electrodes
```

Starting point for reproduction:

- Arduino serial baud rate: 9600
- Arduino output pulse duration: 4 ms
- high-voltage pulse amplitude: about 1.2 kV
- desired voltage decay: below the actuation threshold before the next sorting
  event

The available BOM is intentionally minimal. It identifies the major modules but
does not replace electrical design review, enclosure design, grounding, current
limiting, or lab safety approval.

See:

- `minimal_bom.md`
- `source_bom.docx`
- `docs/safety.md`
- `docs/hardware_setup.md`
