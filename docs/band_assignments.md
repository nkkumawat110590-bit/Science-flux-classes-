# Band assignments

Every band used by `src/band_model.py`, in the order it is applied.
`Height` is the model absorbance of the notional average soil, before
the land-use and depth multipliers of the next table are applied.

| Wavenumber (cm-1) | FWHM (cm-1) | Height | Group | Assignment |
| ---: | ---: | ---: | --- | --- |
| 3695 | 20 | 0.030 | `clay_oh` | Kaolinite inner-surface O-H stretch |
| 3620 | 22 | 0.045 | `clay_oh` | Al-Al-OH stretch of 1:1 / 2:1 clays |
| 3400 | 330 | 0.150 | `water_oh` | Broad O-H stretch: sorbed water, phenolic and alcoholic OH |
| 2925 | 32 | 0.060 | `aliphatic` | Asymmetric C-H stretch of aliphatic CH2 |
| 2855 | 28 | 0.038 | `aliphatic` | Symmetric C-H stretch of aliphatic CH2 |
| 2515 | 45 | 0.020 | `carbonate` | Carbonate combination band (calcite) |
| 2160 | 70 | 0.012 | `silica_ot` | Quartz / silicate overtone-combination band |
| 1795 | 28 | 0.010 | `carbonate` | Carbonate overtone (calcite) |
| 1717 | 42 | 0.070 | `carboxyl` | C=O stretch of carboxylic acids, ketones and aldehydes |
| 1650 | 62 | 0.090 | `aromatic_amide` | Aromatic C=C, amide I C=O and H-O-H bending |
| 1560 | 48 | 0.045 | `aromatic_amide` | Amide II N-H bend / C-N stretch; COO- asymmetric stretch |
| 1508 | 30 | 0.030 | `aromatic_amide` | Aromatic skeletal C=C of lignin |
| 1457 | 38 | 0.045 | `ch_bend` | C-H deformation of CH2 / CH3; lignin methoxyl |
| 1420 | 95 | 0.055 | `carbonate` | Carbonate v3 asymmetric stretch; COO- symmetric stretch |
| 1384 | 22 | 0.030 | `nitrate` | Nitrate v3; C-H bending of CH3 |
| 1265 | 70 | 0.050 | `phenolic_co` | C-O stretch and O-H deformation of phenols, aryl ethers |
| 1160 | 55 | 0.070 | `polysacch` | C-O-C and C-O stretch of polysaccharides |
| 1120 | 45 | 0.030 | `sulfate` | Sulfate v3; Si-O of amorphous silica |
| 1080 | 70 | 0.230 | `silicate` | Si-O-Si asymmetric stretch (quartz, phyllosilicates) |
| 1032 | 78 | 0.420 | `silicate` | Si-O stretch of clay minerals; C-O of polysaccharides |
| 1005 | 55 | 0.120 | `phosphate` | P-O stretch of phosphates; Si-O of 2:1 clays |
| 915 | 38 | 0.055 | `clay_bend` | Al-Al-OH deformation of dioctahedral clays |
| 875 | 24 | 0.030 | `carbonate` | Carbonate v2 out-of-plane bend (calcite) |
| 798 | 16 | 0.070 | `quartz` | Quartz doublet, Si-O symmetric stretch |
| 778 | 16 | 0.062 | `quartz` | Quartz doublet, Si-O symmetric stretch |
| 738 | 26 | 0.028 | `aromatic_oop` | Aromatic C-H out-of-plane deformation |
| 694 | 22 | 0.030 | `quartz` | Quartz / Si-O-Al vibration |
| 610 | 34 | 0.045 | `feox` | Fe-O and Si-O-Al bending |
| 535 | 55 | 0.075 | `feox` | Fe-O stretch of iron oxides (goethite / hematite) |
| 520 | 42 | 0.095 | `clay_bend` | Si-O-Al bending of octahedral sheet |
| 470 | 45 | 0.170 | `silicate` | Si-O-Si bending of quartz and phyllosilicates |
| 430 | 50 | 0.130 | `silicate` | Si-O bending / lattice modes |

Groups classed as organic: `aliphatic`, `aromatic_amide`, `aromatic_oop`, `carboxyl`, `ch_bend`, `phenolic_co`, `polysacch`.

Groups classed as mineral: `clay_bend`, `clay_oh`, `feox`, `phosphate`, `quartz`, `silica_ot`, `silicate`.
