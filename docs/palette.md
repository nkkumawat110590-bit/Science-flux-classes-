# Colour

One hue per land-use system, in fixed slot order, and two lightness steps of
that hue for the two depths. Colour carries identity (which system) and order
(which depth) and nothing else - it never encodes a value.

| Land use | Hue | 0-15 cm | 15-30 cm |
| --- | --- | --- | --- |
| Coniferous forest | blue | `#4592f2` | `#055fba` |
| Grazing land | orange | `#ff8350` | `#ce4d11` |
| Wasteland | aqua | `#44ca93` | `#009562` |
| Apple orchard | yellow | `#ea9e00` | `#b36b00` |
| Paddy field | magenta | `#f587b0` | `#bd547e` |
| Maize field | green | `#319e2c` | `#006b00` |
| Vegetable field | violet | `#7a72e4` | `#4e3fad` |

Surface `#fcfcfb`; ink `#0b0b0b` primary, `#52514e` secondary, `#8a8880` muted.
Text always wears ink, never a series colour - a coloured chip beside the
sample line carries identity instead.

## How the steps were derived

The seven hues are the first seven categorical slots of the reference palette,
in their published order - that order is the colourblind-safety mechanism, not
decoration, so it is kept as-is. Each depth pair is that hue moved +-0.0825 in
OKLab lightness, then clamped into the L 0.45-0.755 band (yellow, magenta and
violet sit near a band edge, so their pairs shift rather than straddle their
base). The lighter step is the shallower soil.

## Validation

Run against the palette validator, light mode:

- **Each depth pair, all pairs**: passes lightness band, chroma floor, CVD
  separation and the normal-vision floor. Worst case is grazing land at CVD
  ΔE 15.4 (deutan) and normal-vision ΔE 15.5 - both clear of the ≥ 8 and ≥ 15
  gates.
- **The seven 0-15 cm colours, adjacent pairs**: worst adjacent CVD ΔE 8.7
  (aqua↔orange), worst normal-vision ΔE 18.8. Four of the seven sit below 3:1
  contrast on the light surface, so the stacked survey figure direct-labels
  every trace - that is the required relief, not a nicety.
- **The seven 15-30 cm colours, adjacent pairs**: worst adjacent CVD ΔE 8.9,
  worst normal-vision ΔE 15.4, and all seven clear 3:1 contrast.

## Secondary encoding

Colour never carries meaning alone anywhere in the output:

- single-spectrum reports name the system and depth in the title;
- depth-pair figures dash the 15-30 cm trace and carry a legend;
- the stacked survey direct-labels each trace;
- the band-ratio bars are grouped under named x-axis ticks, and their depth
  pair is one hue in two steps because depth is ordered, not categorical.

## Swapping in your own colours

Edit `PALETTE` in `src/band_model.py` - seven `(0-15, 15-30)` hex pairs - and
rerun `python src/generate_spectra.py`. If the colours are from another
system, hold them to the same gates before shipping.
