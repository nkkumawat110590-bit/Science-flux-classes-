# Diagnostic band ratios

Read off the generated spectra by `compute_indices` in
`src/generate_spectra.py`: peak absorbance above a tangent baseline
anchored on the lowest point either side of the band.

| Land use | Depth (cm) | A2925/A1032 | A1650/A1032 | A2925/A1650 | A1717/A1650 | A1420 | A1384 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Coniferous forest | 0-15 | 0.307 | 0.286 | 1.074 | 0.918 | 0.009 | 0.005 |
| Coniferous forest | 15-30 | 0.113 | 0.118 | 0.955 | 0.894 | 0.010 | 0.004 |
| Grazing land | 0-15 | 0.193 | 0.233 | 0.831 | 0.767 | 0.022 | 0.015 |
| Grazing land | 15-30 | 0.088 | 0.105 | 0.835 | 0.729 | 0.024 | 0.019 |
| Wasteland | 0-15 | 0.036 | 0.060 | 0.604 | 0.551 | 0.053 | 0.037 |
| Wasteland | 15-30 | 0.031 | 0.046 | 0.687 | 0.697 | 0.067 | 0.050 |
| Apple orchard | 0-15 | 0.149 | 0.163 | 0.915 | 0.939 | 0.040 | 0.034 |
| Apple orchard | 15-30 | 0.093 | 0.094 | 0.991 | 0.943 | 0.055 | 0.042 |
| Paddy field | 0-15 | 0.099 | 0.189 | 0.525 | 0.727 | 0.015 | 0.013 |
| Paddy field | 15-30 | 0.072 | 0.110 | 0.659 | 0.807 | 0.017 | 0.011 |
| Maize field | 0-15 | 0.132 | 0.145 | 0.904 | 0.954 | 0.028 | 0.032 |
| Maize field | 15-30 | 0.069 | 0.080 | 0.860 | 0.899 | 0.036 | 0.029 |
| Vegetable field | 0-15 | 0.103 | 0.134 | 0.767 | 0.852 | 0.027 | 0.049 |
| Vegetable field | 15-30 | 0.055 | 0.067 | 0.827 | 0.880 | 0.036 | 0.040 |

Caveats worth carrying into any interpretation:

- `A1384` sits on the shoulder of the broad carbonate v3 band at 1420,
  so it reads high in the carbonate-rich systems (wasteland, orchard)
  even though their nitrate multiplier is low. Real spectra behave the
  same way; the 1384 band is only diagnostic once carbonate is ruled out.
- `A1032` carries a polysaccharide contribution as well as the silicate
  stretch, so `A2925/A1032` tracks organic enrichment rather than
  measuring organic carbon.
