"""Band model for soil FTIR spectra of seven land-use systems at two depths.

The spectra produced from this model are SIMULATED.  They are built from a
band table of infrared features that are routinely reported for soils, whose
intensities are then modulated by land-use and depth factors taken from the
soil-organic-matter / mineralogy trends described in the literature.  Nothing
here is measured data; the only measured input in this repository is the
digitised reference trace in ``data/reference/``.

Model
-----
Absorbance is built as a sum of pseudo-Voigt bands on a smooth matrix
baseline::

    A(v) = A_base(v) + SUM_b  h_b * m_group(b) * m_depth(b) * pV(v; c_b, w_b)
    T(v) = 100 * 10 ** (-A(v))

``h_b`` is the band strength of a notional "average" soil; the land-use and
depth multipliers below express how each system departs from it.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Band:
    center: float       # cm-1
    fwhm: float         # cm-1
    height: float       # absorbance of the reference soil
    group: str          # modulation group
    assignment: str     # spectroscopic assignment
    eta: float = 0.4    # Lorentzian fraction of the pseudo-Voigt (0 = Gaussian)


# --------------------------------------------------------------------------
# Band table.  Positions/assignments follow standard soil FTIR practice
# (Stevenson 1994; Nguyen et al. 1991; Madejova & Komadel 2001; Tatzber et al.
# 2007; Margenot et al. 2015).  Heights are model values, not measurements.
# --------------------------------------------------------------------------
BANDS: List[Band] = [
    Band(3695, 20, 0.030, "clay_oh",        "Kaolinite inner-surface O-H stretch", 0.6),
    Band(3620, 22, 0.045, "clay_oh",        "Al-Al-OH stretch of 1:1 / 2:1 clays", 0.6),
    Band(3400, 330, 0.150, "water_oh",      "Broad O-H stretch: sorbed water, phenolic and alcoholic OH", 0.2),
    Band(2925, 32, 0.060, "aliphatic",      "Asymmetric C-H stretch of aliphatic CH2", 0.5),
    Band(2855, 28, 0.038, "aliphatic",      "Symmetric C-H stretch of aliphatic CH2", 0.5),
    Band(2515, 45, 0.020, "carbonate",      "Carbonate combination band (calcite)", 0.4),
    Band(2160, 70, 0.012, "silica_ot",      "Quartz / silicate overtone-combination band", 0.3),
    Band(1795, 28, 0.010, "carbonate",      "Carbonate overtone (calcite)", 0.4),
    Band(1717, 42, 0.070, "carboxyl",       "C=O stretch of carboxylic acids, ketones and aldehydes", 0.5),
    Band(1650, 62, 0.090, "aromatic_amide", "Aromatic C=C, amide I C=O and H-O-H bending", 0.4),
    Band(1560, 48, 0.045, "aromatic_amide", "Amide II N-H bend / C-N stretch; COO- asymmetric stretch", 0.4),
    Band(1508, 30, 0.030, "aromatic_amide", "Aromatic skeletal C=C of lignin", 0.5),
    Band(1457, 38, 0.045, "ch_bend",        "C-H deformation of CH2 / CH3; lignin methoxyl", 0.4),
    Band(1420, 95, 0.055, "carbonate",      "Carbonate v3 asymmetric stretch; COO- symmetric stretch", 0.3),
    Band(1384, 22, 0.030, "nitrate",        "Nitrate v3; C-H bending of CH3", 0.6),
    Band(1265, 70, 0.050, "phenolic_co",    "C-O stretch and O-H deformation of phenols, aryl ethers", 0.4),
    Band(1160, 55, 0.070, "polysacch",      "C-O-C and C-O stretch of polysaccharides", 0.4),
    Band(1120, 45, 0.030, "sulfate",        "Sulfate v3; Si-O of amorphous silica", 0.4),
    Band(1080, 70, 0.230, "silicate",       "Si-O-Si asymmetric stretch (quartz, phyllosilicates)", 0.3),
    Band(1032, 78, 0.420, "silicate",       "Si-O stretch of clay minerals; C-O of polysaccharides", 0.3),
    Band(1005, 55, 0.120, "phosphate",      "P-O stretch of phosphates; Si-O of 2:1 clays", 0.4),
    Band(915, 38, 0.055, "clay_bend",       "Al-Al-OH deformation of dioctahedral clays", 0.5),
    Band(875, 24, 0.030, "carbonate",       "Carbonate v2 out-of-plane bend (calcite)", 0.5),
    Band(798, 16, 0.070, "quartz",          "Quartz doublet, Si-O symmetric stretch", 0.6),
    Band(778, 16, 0.062, "quartz",          "Quartz doublet, Si-O symmetric stretch", 0.6),
    Band(738, 26, 0.028, "aromatic_oop",    "Aromatic C-H out-of-plane deformation", 0.5),
    Band(694, 22, 0.030, "quartz",          "Quartz / Si-O-Al vibration", 0.5),
    Band(610, 34, 0.045, "feox",            "Fe-O and Si-O-Al bending", 0.4),
    Band(535, 55, 0.075, "feox",            "Fe-O stretch of iron oxides (goethite / hematite)", 0.3),
    Band(520, 42, 0.095, "clay_bend",       "Si-O-Al bending of octahedral sheet", 0.4),
    Band(470, 45, 0.170, "silicate",        "Si-O-Si bending of quartz and phyllosilicates", 0.3),
    Band(430, 50, 0.130, "silicate",        "Si-O bending / lattice modes", 0.3),
]

ORGANIC_GROUPS = {"aliphatic", "carboxyl", "aromatic_amide", "ch_bend",
                  "phenolic_co", "polysacch", "aromatic_oop"}
MINERAL_GROUPS = {"clay_oh", "silicate", "quartz", "clay_bend", "feox",
                  "silica_ot", "phosphate"}


@dataclass(frozen=True)
class LandUse:
    key: str
    name: str
    short: str
    rationale: str
    groups: Dict[str, float]              # multipliers at 0-15 cm
    organic_depth_ratio: float            # 15-30 cm / 0-15 cm for organic bands
    mineral_depth_ratio: float = 1.08     # mineral bands are relatively enriched
    depth_overrides: Dict[str, float] = field(default_factory=dict)


# --------------------------------------------------------------------------
# Land-use profiles.  Multipliers are relative to the notional average soil
# (1.0 = the band table height above).
# --------------------------------------------------------------------------
LAND_USES: List[LandUse] = [
    LandUse(
        key="coniferous_forest", name="Coniferous forest", short="C.Forest",
        rationale=(
            "Continuous needle-litter input under an acidic, undisturbed profile: "
            "the largest and least decomposed organic-carbon pool of the set. "
            "Strong aliphatic (2925/2855), carboxyl (1717) and lignin-derived "
            "aromatic (1508, 1265) absorption; carbonate effectively absent "
            "because base cations are leached."),
        groups={"aliphatic": 1.95, "carboxyl": 1.60, "aromatic_amide": 1.50,
                "ch_bend": 1.45, "phenolic_co": 1.55, "polysacch": 1.40,
                "aromatic_oop": 1.40, "water_oh": 1.30, "carbonate": 0.15,
                "nitrate": 0.20, "sulfate": 0.55, "phosphate": 0.70,
                "silicate": 0.82, "quartz": 0.88, "clay_oh": 1.00,
                "clay_bend": 0.92, "feox": 0.85, "silica_ot": 0.85},
        organic_depth_ratio=0.45, mineral_depth_ratio=1.14,
        depth_overrides={"carbonate": 1.4, "nitrate": 0.5},
    ),
    LandUse(
        key="grazing_land", name="Grazing land", short="Grazing",
        rationale=(
            "Dense fibrous root turnover and dung returns build a microbially "
            "processed surface pool: pronounced amide I/II (1650, 1560) and "
            "polysaccharide (1160/1032) absorption, with treading-induced "
            "compaction giving a comparatively small depth gradient."),
        groups={"aliphatic": 1.35, "carboxyl": 1.20, "aromatic_amide": 1.38,
                "ch_bend": 1.20, "phenolic_co": 1.15, "polysacch": 1.45,
                "aromatic_oop": 1.10, "water_oh": 1.15, "carbonate": 0.60,
                "nitrate": 0.55, "sulfate": 0.80, "phosphate": 0.95,
                "silicate": 0.95, "quartz": 0.98, "clay_oh": 1.02,
                "clay_bend": 1.00, "feox": 0.95, "silica_ot": 0.95},
        organic_depth_ratio=0.58, mineral_depth_ratio=1.10,
        depth_overrides={"carbonate": 1.45, "nitrate": 0.45},
    ),
    LandUse(
        key="wasteland", name="Wasteland", short="Wasteland",
        rationale=(
            "Sparse vegetation, erosion of the fines and carbonate accumulation "
            "leave a mineral-dominated spectrum: weak organic bands, strong "
            "quartz doublet (798/778) and Si-O (1032, 470), and clear calcite "
            "features at 1420 and 875. Little contrast between the two depths."),
        groups={"aliphatic": 0.32, "carboxyl": 0.30, "aromatic_amide": 0.45,
                "ch_bend": 0.40, "phenolic_co": 0.35, "polysacch": 0.35,
                "aromatic_oop": 0.40, "water_oh": 0.70, "carbonate": 1.70,
                "nitrate": 0.30, "sulfate": 0.90, "phosphate": 0.75,
                "silicate": 1.25, "quartz": 1.38, "clay_oh": 1.10,
                "clay_bend": 1.20, "feox": 1.22, "silica_ot": 1.20},
        organic_depth_ratio=0.82, mineral_depth_ratio=1.04,
        depth_overrides={"carbonate": 1.25},
    ),
    LandUse(
        key="apple_orchard", name="Apple orchard", short="Orchard",
        rationale=(
            "Perennial cover with leaf-fall and pruning residues plus routine "
            "liming and basin irrigation: moderately humified organic bands over "
            "a carbonate-bearing matrix, and a deeper root system that carries "
            "organic carbon further down the profile than annual crops."),
        groups={"aliphatic": 1.18, "carboxyl": 1.12, "aromatic_amide": 1.12,
                "ch_bend": 1.10, "phenolic_co": 1.20, "polysacch": 1.10,
                "aromatic_oop": 1.10, "water_oh": 1.05, "carbonate": 1.28,
                "nitrate": 0.95, "sulfate": 1.00, "phosphate": 1.15,
                "silicate": 1.00, "quartz": 1.02, "clay_oh": 1.00,
                "clay_bend": 1.02, "feox": 1.00, "silica_ot": 1.00},
        organic_depth_ratio=0.68, mineral_depth_ratio=1.07,
        depth_overrides={"carbonate": 1.50, "nitrate": 0.55},
    ),
    LandUse(
        key="paddy_field", name="Paddy field", short="Paddy",
        rationale=(
            "Seasonal submergence slows decomposition and favours aromatic, "
            "humified carbon (1650, 1560) while redox cycling redistributes iron "
            "(610, 535); rice phytoliths and puddling add amorphous silica near "
            "1120-1032. The plough pan keeps the depth contrast modest."),
        groups={"aliphatic": 0.98, "carboxyl": 1.28, "aromatic_amide": 1.35,
                "ch_bend": 1.00, "phenolic_co": 1.25, "polysacch": 1.15,
                "aromatic_oop": 1.20, "water_oh": 1.22, "carbonate": 0.50,
                "nitrate": 0.40, "sulfate": 0.95, "phosphate": 1.05,
                "silicate": 1.20, "quartz": 1.05, "clay_oh": 1.08,
                "clay_bend": 1.10, "feox": 1.38, "silica_ot": 1.15},
        organic_depth_ratio=0.72, mineral_depth_ratio=1.09,
        depth_overrides={"feox": 1.25, "nitrate": 0.40, "carbonate": 1.30},
    ),
    LandUse(
        key="maize_field", name="Maize field", short="Maize",
        rationale=(
            "Annual tillage with coarse stover returns: a fresh, weakly humified "
            "surface pool - relatively strong polysaccharide (1160/1032) and "
            "aliphatic bands against modest aromatic absorption - and a sharp "
            "fall below the plough layer."),
        groups={"aliphatic": 1.02, "carboxyl": 0.95, "aromatic_amide": 0.92,
                "ch_bend": 1.00, "phenolic_co": 0.90, "polysacch": 1.22,
                "aromatic_oop": 0.90, "water_oh": 1.00, "carbonate": 0.85,
                "nitrate": 1.25, "sulfate": 1.05, "phosphate": 1.10,
                "silicate": 1.05, "quartz": 1.08, "clay_oh": 1.00,
                "clay_bend": 1.02, "feox": 1.00, "silica_ot": 1.02},
        organic_depth_ratio=0.60, mineral_depth_ratio=1.09,
        depth_overrides={"nitrate": 0.50, "carbonate": 1.35},
    ),
    LandUse(
        key="vegetable_field", name="Vegetable field", short="Vegetable",
        rationale=(
            "Intensive, short-duration cropping with heavy fertiliser and manure "
            "use: the fertiliser signature dominates the mid-region - nitrate at "
            "1384, sulfate near 1120 and phosphate near 1005 - while frequent "
            "shallow tillage keeps the organic pool small and rapidly turned "
            "over."),
        groups={"aliphatic": 0.88, "carboxyl": 0.92, "aromatic_amide": 0.88,
                "ch_bend": 0.95, "phenolic_co": 0.85, "polysacch": 1.05,
                "aromatic_oop": 0.85, "water_oh": 1.05, "carbonate": 0.90,
                "nitrate": 1.95, "sulfate": 1.60, "phosphate": 1.55,
                "silicate": 1.02, "quartz": 1.02, "clay_oh": 0.98,
                "clay_bend": 1.00, "feox": 0.98, "silica_ot": 1.00},
        organic_depth_ratio=0.62, mineral_depth_ratio=1.08,
        depth_overrides={"nitrate": 0.62, "sulfate": 0.80, "carbonate": 1.30},
    ),
]

DEPTHS = [(0, 15), (15, 30)]

LAND_USE_BY_KEY = {lu.key: lu for lu in LAND_USES}


def group_multiplier(land_use: LandUse, group: str, deep: bool) -> float:
    """Combined land-use and depth multiplier for one modulation group."""
    m = land_use.groups.get(group, 1.0)
    if not deep:
        return m
    if group in land_use.depth_overrides:
        return m * land_use.depth_overrides[group]
    if group in ORGANIC_GROUPS:
        return m * land_use.organic_depth_ratio
    if group in MINERAL_GROUPS:
        return m * land_use.mineral_depth_ratio
    if group == "water_oh":
        return m * 0.95
    return m
