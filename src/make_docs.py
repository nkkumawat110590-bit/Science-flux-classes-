"""Write the band-assignment and land-use reference tables from the model."""

import csv
from pathlib import Path

from band_model import BANDS, LAND_USES, MINERAL_GROUPS, ORGANIC_GROUPS, group_multiplier

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def band_table() -> str:
    lines = [
        "# Band assignments",
        "",
        "Every band used by `src/band_model.py`, in the order it is applied.",
        "`Height` is the model absorbance of the notional average soil, before",
        "the land-use and depth multipliers of the next table are applied.",
        "",
        "| Wavenumber (cm-1) | FWHM (cm-1) | Height | Group | Assignment |",
        "| ---: | ---: | ---: | --- | --- |",
    ]
    for b in sorted(BANDS, key=lambda b: -b.center):
        lines.append(f"| {b.center:.0f} | {b.fwhm:.0f} | {b.height:.3f} | "
                     f"`{b.group}` | {b.assignment} |")
    lines += [
        "",
        "Groups classed as organic: " + ", ".join(f"`{g}`" for g in sorted(ORGANIC_GROUPS)) + ".",
        "",
        "Groups classed as mineral: " + ", ".join(f"`{g}`" for g in sorted(MINERAL_GROUPS)) + ".",
        "",
    ]
    return "\n".join(lines)


def land_use_table() -> str:
    groups = sorted({b.group for b in BANDS})
    lines = [
        "# Land-use profiles",
        "",
        "How each system departs from the average soil of the band table, and",
        "why. A multiplier of 1.00 leaves the band at its table height.",
        "",
    ]
    for lu in LAND_USES:
        lines += [f"## {lu.name}", "", lu.rationale, "",
                  "| Group | 0-15 cm | 15-30 cm | 15-30 / 0-15 |",
                  "| --- | ---: | ---: | ---: |"]
        for g in groups:
            top = group_multiplier(lu, g, False)
            deep = group_multiplier(lu, g, True)
            lines.append(f"| `{g}` | {top:.2f} | {deep:.2f} | {deep / top:.2f} |")
        lines.append("")
    return "\n".join(lines)


def index_table() -> str:
    path = ROOT / "output/band_indices.csv"
    if not path.exists():
        return ""
    rows = list(csv.DictReader(path.open()))
    cols = [
        ("ratio_2925_1032_organic_to_mineral", "A2925/A1032"),
        ("ratio_1650_1032_humified_to_mineral", "A1650/A1032"),
        ("ratio_2925_1650_aliphaticity", "A2925/A1650"),
        ("ratio_1717_1650_carboxyl_to_aromatic", "A1717/A1650"),
        ("A1420_carbonate", "A1420"),
        ("A1384_nitrate", "A1384"),
    ]
    lines = [
        "# Diagnostic band ratios",
        "",
        "Read off the generated spectra by `compute_indices` in",
        "`src/generate_spectra.py`: peak absorbance above a tangent baseline",
        "anchored on the lowest point either side of the band.",
        "",
        "| Land use | Depth (cm) | " + " | ".join(c[1] for c in cols) + " |",
        "| --- | --- | " + " | ".join("---:" for _ in cols) + " |",
    ]
    for r in rows:
        vals = " | ".join(f"{float(r[c[0]]):.3f}" for c in cols)
        lines.append(f"| {r['land_use']} | {r['depth_cm']} | {vals} |")
    lines += [
        "",
        "Caveats worth carrying into any interpretation:",
        "",
        "- `A1384` sits on the shoulder of the broad carbonate v3 band at 1420,",
        "  so it reads high in the carbonate-rich systems (wasteland, orchard)",
        "  even though their nitrate multiplier is low. Real spectra behave the",
        "  same way; the 1384 band is only diagnostic once carbonate is ruled out.",
        "- `A1032` carries a polysaccharide contribution as well as the silicate",
        "  stretch, so `A2925/A1032` tracks organic enrichment rather than",
        "  measuring organic carbon.",
        "",
    ]
    return "\n".join(lines)


def main():
    DOCS.mkdir(exist_ok=True)
    (DOCS / "band_assignments.md").write_text(band_table())
    (DOCS / "land_use_profiles.md").write_text(land_use_table())
    idx = index_table()
    if idx:
        (DOCS / "band_ratios.md").write_text(idx)
    print("wrote docs/band_assignments.md, docs/land_use_profiles.md"
          + (", docs/band_ratios.md" if idx else ""))


if __name__ == "__main__":
    main()
