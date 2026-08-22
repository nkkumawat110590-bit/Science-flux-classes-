# Soil FTIR spectra for seven land-use systems, two depths

Fourteen mid-infrared transmittance spectra - seven land-use systems at
0-15 cm and 15-30 cm - generated from an explicit band model, together with
the code, the band table and the diagnostic ratios read off them.

| # | Land use | 0-15 cm | 15-30 cm |
| - | --- | --- | --- |
| 1 | Coniferous forest | [spectrum](output/spectra/coniferous_forest_0_15cm.pdf) | [spectrum](output/spectra/coniferous_forest_15_30cm.pdf) |
| 2 | Grazing land | [spectrum](output/spectra/grazing_land_0_15cm.pdf) | [spectrum](output/spectra/grazing_land_15_30cm.pdf) |
| 3 | Wasteland | [spectrum](output/spectra/wasteland_0_15cm.pdf) | [spectrum](output/spectra/wasteland_15_30cm.pdf) |
| 4 | Apple orchard | [spectrum](output/spectra/apple_orchard_0_15cm.pdf) | [spectrum](output/spectra/apple_orchard_15_30cm.pdf) |
| 5 | Paddy field | [spectrum](output/spectra/paddy_field_0_15cm.pdf) | [spectrum](output/spectra/paddy_field_15_30cm.pdf) |
| 6 | Maize field | [spectrum](output/spectra/maize_field_0_15cm.pdf) | [spectrum](output/spectra/maize_field_15_30cm.pdf) |
| 7 | Vegetable field | [spectrum](output/spectra/vegetable_field_0_15cm.pdf) | [spectrum](output/spectra/vegetable_field_15_30cm.pdf) |

## Read this first

**The fourteen spectra are simulated.** They are computed from the band model
in `src/band_model.py`, not measured on soil. Every figure carries that
statement on its face. They are suitable for method development, for teaching
what these systems are expected to look like, and for testing a processing
pipeline; they are **not** a substitute for running samples, and they must not
be reported as measurements.

The one piece of measured data here is `data/reference/`, digitised from the
supplied Bruker OPUS report (`Sample 9`, coniferous forest, 30/06/2025).

## What is in the box

```
data/reference/    the supplied report's trace, digitised out of the PDF
output/spectra/    fourteen single-sample reports (PDF + PNG), OPUS-like layout
output/data/       fourteen spectra as CSV: wavenumber, %T, absorbance
output/peak_tables/  picked band minima with assignments, one file per sample
output/figures/    depth-pair overlays, the two all-land-use stacks, the
                   organic-to-mineral bar chart, and the reference check
output/all_spectra.pdf   all fourteen reports in one file
output/peak_summary.csv  every picked band across all fourteen samples
output/band_indices.csv  diagnostic band heights and ratios
docs/              band assignments, land-use profiles, band ratios
```

## How the spectra are built

Absorbance is a sum of pseudo-Voigt bands on a smooth matrix baseline, and
transmittance follows from it:

```
A(v) = A_base(v) + SUM_b  h_b * m_group(b) * m_depth(b) * pV(v; c_b, w_b)
T(v) = 100 * 10 ** (-A(v))
```

- `h_b` is the band strength of a notional average soil - see
  [docs/band_assignments.md](docs/band_assignments.md) for all 32 bands and
  their assignments.
- `m_group` and `m_depth` are how one land use and one depth depart from that
  average - see [docs/land_use_profiles.md](docs/land_use_profiles.md), which
  states the reasoning for each system.
- Band positions, widths and heights carry small reproducible jitter, plus
  detector noise and a residual baseline tilt, so the fourteen spectra differ
  the way replicate samples do rather than being scaled copies of one curve.
  Every sample is seeded from its own name, so a rerun reproduces it exactly.

Range 4000-400 cm-1 at 1.93 cm-1 spacing, the point spacing of the supplied
report.

## What the model says about these systems

Full table in [docs/band_ratios.md](docs/band_ratios.md); the short version,
as `A(2925)/A(1032)` - aliphatic C-H against the silicate stretch, a proxy for
organic enrichment:

| Land use | 0-15 cm | 15-30 cm |
| --- | ---: | ---: |
| Coniferous forest | 0.307 | 0.113 |
| Grazing land | 0.193 | 0.088 |
| Apple orchard | 0.149 | 0.093 |
| Maize field | 0.132 | 0.069 |
| Vegetable field | 0.103 | 0.055 |
| Paddy field | 0.099 | 0.072 |
| Wasteland | 0.036 | 0.031 |

The three features that separate the systems most clearly are the aliphatic
pair at 2925/2855, the carbonate set at 2515/1795/1420/875, and the fertiliser
bands at 1384 (nitrate) and 1120 (sulfate). Depth always costs organic
absorption and always gains mineral absorption; how much depends on the
system - a forest profile loses more than half of its aliphatic band between
the two depths, a wasteland profile barely changes.

## Relation to the supplied report

`output/figures/reference_check.pdf` puts the digitised reference trace above
the model's coniferous forest 0-15 cm spectrum. Band positions agree. Band
depths do not: the supplied report spans only about 70-101 %T, an unusually
low contrast for a soil spectrum, whereas the model uses conventional band
intensities with the 1032 cm-1 silicate stretch reaching roughly 35-50 %T.
That is a deliberate choice - matching the report's contrast would have made
the weaker organic bands unreadable across the set.

## Running it

```sh
pip install -r requirements.txt
python src/generate_spectra.py     # rebuilds everything under output/
python src/make_docs.py            # rebuilds the tables under docs/
```

To re-digitise the reference from the original PDF:

```sh
python src/extract_reference.py <report.pdf> data/reference/coniferous_forest_0_15_reference.csv
```

## Adjusting the model

Both files are meant to be edited. Add or move a band in the `BANDS` table of
`src/band_model.py`; change how a system behaves in its `LandUse` entry
(`groups` for the surface soil, `organic_depth_ratio` / `mineral_depth_ratio` /
`depth_overrides` for the subsoil). `CONTRAST` in `src/generate_spectra.py`
scales the whole band system if the spectra want to be shallower or deeper.
Rerun both scripts afterwards so the figures and the tables stay in step.
