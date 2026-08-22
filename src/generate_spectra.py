"""Generate simulated FTIR spectra for seven land-use systems at two depths.

Outputs, all under ``output/``:

    data/<land_use>_<depth>.csv        wavenumber / transmittance / absorbance
    spectra/<land_use>_<depth>.pdf     single-spectrum report, OPUS-like layout
    spectra/<land_use>_<depth>.png     the same figure as a raster
    peak_tables/<land_use>_<depth>.csv picked band minima with assignments
    figures/*.pdf|png                  depth-pair, all-land-use and validation
                                       comparison figures
    peak_summary.csv                   every picked band, all fourteen samples

Every figure is stamped as simulated.  Run ``python src/generate_spectra.py``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.signal import find_peaks

from band_model import (BANDS, DEPTHS, INK_MUTED, INK_PRIMARY, INK_SECONDARY,
                        LAND_USES, PALETTE, SURFACE, LandUse, colour_for,
                        group_multiplier)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

WN_MIN, WN_MAX, WN_STEP = 400.0, 4000.0, 1.928934   # OPUS-like point spacing
CONTRAST = 0.62      # global absorbance scale of the band system
NOISE_RMS = 0.0009   # absorbance units, comparable to a good KBr-pellet run

STAMP = ("Simulated spectrum - generated from the band model in "
         "src/band_model.py. Not measured data.")


def wavenumbers() -> np.ndarray:
    n = int(round((WN_MAX - WN_MIN) / WN_STEP)) + 1
    return WN_MIN + WN_STEP * np.arange(n)


def pseudo_voigt(v: np.ndarray, center: float, fwhm: float, eta: float) -> np.ndarray:
    sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    gauss = np.exp(-0.5 * ((v - center) / sigma) ** 2)
    gamma = fwhm / 2.0
    lorentz = gamma ** 2 / ((v - center) ** 2 + gamma ** 2)
    return (1.0 - eta) * gauss + eta * lorentz


def matrix_baseline(v: np.ndarray) -> np.ndarray:
    """Scattering / lattice continuum: rises steadily towards low wavenumber."""
    return 0.012 + 0.075 * np.exp(-(v - WN_MIN) / 850.0) + 0.004 * np.exp(-(4000.0 - v) / 700.0)


def seed_for(land_use: LandUse, deep: bool) -> int:
    tag = f"{land_use.key}|{'15-30' if deep else '0-15'}"
    return int(hashlib.sha256(tag.encode()).hexdigest()[:8], 16)


def synthesise(land_use: LandUse, deep: bool):
    """Return (wavenumber, transmittance %, absorbance) for one sample."""
    v = wavenumbers()
    rng = np.random.default_rng(seed_for(land_use, deep))
    absorbance = matrix_baseline(v).copy()

    for band in BANDS:
        m = group_multiplier(land_use, band.group, deep)
        if m <= 0.0:
            continue
        # small, reproducible position and width jitter, as between real samples
        center = band.center + rng.normal(0.0, min(1.6, 0.0025 * band.center))
        fwhm = band.fwhm * float(rng.normal(1.0, 0.03))
        height = band.height * m * float(rng.normal(1.0, 0.04))
        absorbance += height * pseudo_voigt(v, center, fwhm, band.eta)

    absorbance *= CONTRAST
    # gentle sloping baseline offset, as left by a real background correction
    absorbance += rng.uniform(-0.004, 0.010) * (v - WN_MIN) / (WN_MAX - WN_MIN)
    absorbance += rng.normal(0.0, NOISE_RMS, size=v.size)

    transmittance = 100.0 * np.power(10.0, -absorbance)
    return v, transmittance, absorbance


# --------------------------------------------------------------------------
# peak picking
# --------------------------------------------------------------------------
def pick_peaks(v, absorbance, max_peaks=24, prominence=0.008):
    idx, props = find_peaks(absorbance, prominence=prominence, distance=6)
    if idx.size == 0:
        return []
    order = np.argsort(props["prominences"])[::-1][:max_peaks]
    idx = np.sort(idx[order])
    return [int(i) for i in idx]


def nearest_assignment(wn: float):
    band = min(BANDS, key=lambda b: abs(b.center - wn))
    if abs(band.center - wn) > max(35.0, 0.9 * band.fwhm):
        return "", ""
    return band.assignment, band.group


# --------------------------------------------------------------------------
# plotting
# --------------------------------------------------------------------------
def style_axes(ax, colour_mode=False):
    ax.set_xlim(4000, 400)
    ax.set_xlabel("Wavenumber cm-1")
    ax.set_ylabel("Transmittance [%]")
    ax.tick_params(direction="out", length=3, labelsize=9)
    for spine in ax.spines.values():
        spine.set_linewidth(0.6)
    ax.set_xticks(np.arange(500, 4001, 500))
    if not colour_mode:
        return
    # recessive frame and grid; the trace is the only saturated thing on the page
    ax.set_facecolor(SURFACE)
    ax.grid(True, axis="y", color="#e6e5e1", lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color("#d5d4cf")
    ax.tick_params(colors=INK_SECONDARY)
    ax.xaxis.label.set_color(INK_SECONDARY)
    ax.yaxis.label.set_color(INK_SECONDARY)


def draw_spectrum(ax, land_use, top, bottom, v, t, peaks, colour=None):
    """Draw one transmittance trace with tiered peak labels.

    The wavenumbers are printed on their own, without the vertical leader
    lines an OPUS report draws from each band down to its label.
    """
    if colour is None:
        ax.plot(v, t, color="black", lw=0.7)
        style_axes(ax)
    else:
        # absorption reads as the area the trace drops away from full pass
        ax.fill_between(v, t, t.max(), color=colour, alpha=0.13, lw=0, zorder=1)
        ax.plot(v, t, color=colour, lw=0.9, zorder=2)
        style_axes(ax, colour_mode=True)

    tmin, tmax = float(t.min()), float(t.max())
    span = tmax - tmin
    ax.set_ylim(tmin - 0.26 * span, tmax + 0.05 * span)

    # crowded labels stack on successive tiers instead of overprinting
    tier_last = []
    min_sep = 55.0          # cm-1 needed between two rotated labels on a tier
    tier_gap = 0.075 * span
    for i in sorted(peaks, key=lambda k: -v[k]):
        wn = float(v[i])
        tier = None
        for n, last in enumerate(tier_last):
            if abs(last - wn) > min_sep:
                tier, tier_last[n] = n, wn
                break
        if tier is None:
            if len(tier_last) >= 3:
                continue        # too crowded to label legibly
            tier_last.append(wn)
            tier = len(tier_last) - 1
        top_y = tmin - 0.035 * span - tier * tier_gap
        ax.text(wn, top_y, f"{wn:.2f}", rotation=90, ha="center", va="top",
                fontsize=6.4, color=INK_MUTED if colour else "black")

    ax.set_title(f"{land_use.name}  |  {top}-{bottom} cm  |  soil FTIR (simulated)",
                 fontsize=12, pad=10,
                 color=INK_PRIMARY if colour else "black")


def plot_single(land_use: LandUse, top: int, bottom: int, v, t, peaks,
                path_stem: Path, colour: str = None):
    fig, ax = plt.subplots(figsize=(11.0, 7.4))
    fig.subplots_adjust(left=0.085, right=0.975, top=0.90, bottom=0.16)
    if colour:
        fig.patch.set_facecolor(SURFACE)
        # a chip carries the land-use identity; the text itself stays ink
        fig.patches.append(plt.Rectangle((0.085, 0.049), 0.013, 0.019, lw=0,
                                         facecolor=colour,
                                         transform=fig.transFigure, zorder=5))
    draw_spectrum(ax, land_use, top, bottom, v, t, peaks, colour=colour)
    fig.text(0.105 if colour else 0.085, 0.049 if colour else 0.055,
             f"Sample: {land_use.short}_{top}-{bottom}cm     "
             f"Range 4000-400 cm-1     Resolution 4 cm-1 (model)",
             fontsize=8, color=INK_SECONDARY if colour else "black",
             va="bottom" if colour else "baseline")
    fig.text(0.085, 0.022 if colour else 0.028, STAMP, fontsize=7.5,
             style="italic", color=INK_MUTED if colour else "0.35")
    fig.savefig(path_stem.with_suffix(".pdf"), facecolor=fig.get_facecolor())
    fig.savefig(path_stem.with_suffix(".png"), dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_depth_pair(land_use: LandUse, series, path_stem: Path):
    """The two depths of one system, in that system's hue, light over deep."""
    fig, ax = plt.subplots(figsize=(11.0, 6.4))
    fig.patch.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.085, right=0.975, top=0.90, bottom=0.17)
    styles = {"0-15": (PALETTE[land_use.key][0], "-"),
              "15-30": (PALETTE[land_use.key][1], (0, (5, 1.6)))}
    for (label, v, t) in series:
        colour, dash = styles[label]
        ax.plot(v, t, lw=1.0, color=colour, linestyle=dash, label=f"{label} cm")
    style_axes(ax, colour_mode=True)
    leg = ax.legend(frameon=False, fontsize=9, loc="lower left")
    for text in leg.get_texts():
        text.set_color(INK_SECONDARY)
    ax.set_title(f"{land_use.name} - depth comparison (simulated)",
                 fontsize=12, pad=10, color=INK_PRIMARY)
    fig.text(0.085, 0.035, STAMP, fontsize=7.5, style="italic", color=INK_MUTED)
    fig.savefig(path_stem.with_suffix(".pdf"), facecolor=fig.get_facecolor())
    fig.savefig(path_stem.with_suffix(".png"), dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_all_land_uses(depth_label: str, series, path_stem: Path):
    """Stacked survey of all seven systems, listed top-down in the given order.

    Each trace is direct-labelled, which is also the relief the palette's
    lighter steps need: identity never rests on colour alone.
    """
    deep = depth_label.startswith("15")
    fig, ax = plt.subplots(figsize=(11.0, 9.0))
    fig.patch.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.075, right=0.97, top=0.93, bottom=0.10)
    step = 58.0
    n = len(series)
    for i, (name, v, t) in enumerate(series):
        colour = PALETTE[LAND_USES[i].key][1 if deep else 0]
        offset = (n - 1 - i) * step
        ax.fill_between(v, t + offset, t.max() + offset, color=colour,
                        alpha=0.10, lw=0, zorder=1)
        ax.plot(v, t + offset, lw=0.85, color=colour, zorder=2)
        j = int(np.argmin(np.abs(v - 3950.0)))
        ax.text(3960, t[j] + offset + 7.0, name, fontsize=9.5, ha="left",
                va="bottom", color=INK_PRIMARY)
    ax.set_xlim(4000, 400)
    ax.set_xlabel("Wavenumber cm-1", color=INK_SECONDARY)
    ax.set_ylabel("Transmittance [%] (offset for clarity)", color=INK_SECONDARY)
    ax.set_xticks(np.arange(500, 4001, 500))
    ax.set_yticks([])
    ax.set_facecolor(SURFACE)
    ax.tick_params(colors=INK_SECONDARY)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#d5d4cf")
    ax.set_title(f"All seven land-use systems, {depth_label} cm (simulated)",
                 fontsize=12, pad=12, color=INK_PRIMARY)
    fig.text(0.075, 0.022, STAMP, fontsize=7.5, style="italic", color=INK_MUTED)
    fig.savefig(path_stem.with_suffix(".pdf"), facecolor=fig.get_facecolor())
    fig.savefig(path_stem.with_suffix(".png"), dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_reference_check(v, t, path_stem: Path):
    ref = ROOT / "data/reference/coniferous_forest_0_15_reference.csv"
    if not ref.exists():
        return
    rows = list(csv.reader(ref.open()))[1:]
    rv = np.array([float(r[0]) for r in rows])
    rt = np.array([float(r[1]) for r in rows])

    fig, axes = plt.subplots(2, 1, figsize=(11.0, 8.2), sharex=True)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.12, hspace=0.15)
    axes[0].plot(rv, rt, color="black", lw=0.7)
    axes[0].set_title("Supplied report, digitised from the PDF (measured)", fontsize=10)
    axes[1].plot(v, t, color="#1f4e79", lw=0.7)
    axes[1].set_title("Coniferous forest 0-15 cm, this model (simulated)", fontsize=10)
    for ax in axes:
        ax.set_xlim(4000, 400)
        ax.set_ylabel("Transmittance [%]")
        ax.set_xticks(np.arange(500, 4001, 500))
    axes[1].set_xlabel("Wavenumber cm-1")
    fig.suptitle("Model against the supplied reference trace", fontsize=12)
    fig.text(0.09, 0.03,
             "Band positions are shared; the supplied report has an unusually low "
             "band contrast, so absolute depths differ by design.",
             fontsize=7.5, style="italic", color="0.35")
    fig.savefig(path_stem.with_suffix(".pdf"))
    fig.savefig(path_stem.with_suffix(".png"), dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# diagnostic band-ratio indices
# --------------------------------------------------------------------------
DIAGNOSTIC = {
    "A2925_aliphatic": 2925.0,
    "A1717_carboxyl": 1717.0,
    "A1650_aromatic_amide": 1650.0,
    "A1560_amideII": 1560.0,
    "A1420_carbonate": 1420.0,
    "A1384_nitrate": 1384.0,
    "A1160_polysaccharide": 1160.0,
    "A1032_silicate": 1032.0,
    "A798_quartz": 798.0,
    "A535_iron_oxide": 535.0,
}


def band_height(v, a, center, half_window=15.0, base_window=120.0):
    """Peak absorbance above a local tangent baseline.

    The baseline anchors are the lowest points on either side of the band,
    which is how band heights are read off a real spectrum and keeps a
    neighbouring band from dragging the anchor up.
    """
    core = np.abs(v - center) <= half_window
    peak = float(a[core].max())
    left_mask = (v >= center - base_window) & (v <= center - half_window)
    right_mask = (v >= center + half_window) & (v <= center + base_window)
    if not left_mask.any() or not right_mask.any():
        return float("nan")
    li = int(np.argmin(np.where(left_mask, a, np.inf)))
    ri = int(np.argmin(np.where(right_mask, a, np.inf)))
    frac = (center - v[li]) / (v[ri] - v[li])
    baseline = a[li] + frac * (a[ri] - a[li])
    return float(peak - baseline)


def compute_indices(v, a):
    h = {name: band_height(v, a, wn) for name, wn in DIAGNOSTIC.items()}
    ali, arom = h["A2925_aliphatic"], h["A1650_aromatic_amide"]
    mineral = h["A1032_silicate"]
    out = dict(h)
    out["ratio_2925_1032_organic_to_mineral"] = ali / mineral if mineral else float("nan")
    out["ratio_1650_1032_humified_to_mineral"] = arom / mineral if mineral else float("nan")
    out["ratio_2925_1650_aliphaticity"] = ali / arom if arom else float("nan")
    out["ratio_1717_1650_carboxyl_to_aromatic"] = (
        h["A1717_carboxyl"] / arom if arom else float("nan"))
    out["hydrophobicity_2925_over_1650_plus_1160"] = (
        ali / (arom + h["A1160_polysaccharide"]))
    return out


def plot_index_bars(rows, path_stem: Path):
    """Organic-to-mineral band ratio for every system and both depths."""
    names = [r["land_use"] for r in rows if r["depth_cm"] == "0-15"]
    top = [r["ratio_2925_1032_organic_to_mineral"] for r in rows if r["depth_cm"] == "0-15"]
    deep = [r["ratio_2925_1032_organic_to_mineral"] for r in rows if r["depth_cm"] == "15-30"]

    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.88, bottom=0.26)
    # depth is an ordered pair, so it takes one hue in two steps, not two hues
    ax.bar(x - 0.20, top, 0.36, label="0-15 cm", color="#6da7ec")
    ax.bar(x + 0.20, deep, 0.36, label="15-30 cm", color="#1c5cab")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=25, ha="right", fontsize=9,
                       color=INK_SECONDARY)
    ax.set_ylabel("A(2925) / A(1032)", color=INK_SECONDARY)
    ax.grid(True, axis="y", color="#e6e5e1", lw=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Aliphatic C-H to silicate band ratio - organic enrichment "
                 "by land use and depth (simulated)", fontsize=11.5, pad=10,
                 color=INK_PRIMARY)
    leg = ax.legend(frameon=False, fontsize=9)
    for text in leg.get_texts():
        text.set_color(INK_SECONDARY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=INK_SECONDARY)
    fig.text(0.09, 0.02, STAMP, fontsize=7.5, style="italic", color=INK_MUTED)
    fig.savefig(path_stem.with_suffix(".pdf"), facecolor=fig.get_facecolor())
    fig.savefig(path_stem.with_suffix(".png"), dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def write_spectrum_csv(path: Path, v, t, a):
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["wavenumber_cm-1", "transmittance_percent", "absorbance"])
        for i in range(v.size):
            w.writerow([f"{v[i]:.4f}", f"{t[i]:.4f}", f"{a[i]:.6f}"])


def write_peak_csv(path: Path, land_use, top, bottom, v, t, a, peaks):
    rows = []
    for i in peaks:
        assignment, group = nearest_assignment(float(v[i]))
        rows.append([land_use.name, f"{top}-{bottom}", f"{v[i]:.2f}",
                     f"{t[i]:.2f}", f"{a[i]:.4f}", group, assignment])
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["land_use", "depth_cm", "wavenumber_cm-1",
                    "transmittance_percent", "absorbance", "band_group", "assignment"])
        w.writerows(rows)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", default=str(OUT))
    args = ap.parse_args()
    out = Path(args.outdir)

    for sub in ("data", "spectra", "spectra_colour", "peak_tables", "figures"):
        (out / sub).mkdir(parents=True, exist_ok=True)

    summary_rows = []
    index_rows = []
    per_land_use = {}
    per_depth = {"0-15": [], "15-30": []}

    for lu in LAND_USES:
        per_land_use[lu.key] = []
        for top, bottom in DEPTHS:
            deep = top > 0
            label = f"{top}-{bottom}"
            v, t, a = synthesise(lu, deep)
            peaks = pick_peaks(v, a)
            stem = f"{lu.key}_{top}_{bottom}cm"

            write_spectrum_csv(out / "data" / f"{stem}.csv", v, t, a)
            summary_rows += write_peak_csv(out / "peak_tables" / f"{stem}.csv",
                                           lu, top, bottom, v, t, a, peaks)
            plot_single(lu, top, bottom, v, t, peaks, out / "spectra" / stem)
            plot_single(lu, top, bottom, v, t, peaks,
                        out / "spectra_colour" / stem, colour=colour_for(lu, deep))

            idx = {"land_use": lu.name, "depth_cm": label}
            idx.update(compute_indices(v, a))
            index_rows.append(idx)

            per_land_use[lu.key].append((label, v, t))
            per_depth[label].append((lu.name, v, t))
            print(f"{lu.name:20s} {label:>6s} cm   "
                  f"Tmin {t.min():5.1f} %   Tmax {t.max():5.1f} %   {len(peaks)} bands")

        plot_depth_pair(lu, per_land_use[lu.key], out / "figures" / f"{lu.key}_depth_pair")

    for label, series in per_depth.items():
        plot_all_land_uses(label, series, out / "figures" / f"all_land_uses_{label.replace('-', '_')}cm")

    v, t, _ = synthesise(LAND_USES[0], False)
    plot_reference_check(v, t, out / "figures" / "reference_check")

    with (out / "peak_summary.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["land_use", "depth_cm", "wavenumber_cm-1",
                    "transmittance_percent", "absorbance", "band_group", "assignment"])
        w.writerows(summary_rows)

    with (out / "band_indices.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(index_rows[0].keys()))
        w.writeheader()
        for row in index_rows:
            w.writerow({k: (f"{val:.4f}" if isinstance(val, float) else val)
                        for k, val in row.items()})
    plot_index_bars(index_rows, out / "figures" / "organic_to_mineral_ratio")

    # two combined PDFs holding all fourteen reports, in the requested order
    for name, tint in (("all_spectra.pdf", False), ("all_spectra_colour.pdf", True)):
        with PdfPages(out / name) as pdf:
            for lu in LAND_USES:
                for top, bottom in DEPTHS:
                    deep = top > 0
                    v, t, a = synthesise(lu, deep)
                    peaks = pick_peaks(v, a)
                    colour = colour_for(lu, deep) if tint else None
                    fig, ax = plt.subplots(figsize=(11.0, 7.4))
                    if colour:
                        fig.patch.set_facecolor(SURFACE)
                    fig.subplots_adjust(left=0.085, right=0.975, top=0.90, bottom=0.16)
                    draw_spectrum(ax, lu, top, bottom, v, t, peaks, colour=colour)
                    fig.text(0.085, 0.028, STAMP, fontsize=7.5, style="italic",
                             color=INK_MUTED if colour else "0.35")
                    pdf.savefig(fig, facecolor=fig.get_facecolor())
                    plt.close(fig)

    print(f"\nwrote {len(summary_rows)} picked bands across "
          f"{len(LAND_USES) * len(DEPTHS)} spectra into {out}")


if __name__ == "__main__":
    main()
