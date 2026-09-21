"""Digitise the reference FTIR spectrum out of the supplied Bruker OPUS PDF report.

The OPUS report draws the trace as a few thousand very thin (0.2 pt) straight
line segments.  We collect those segments, calibrate page coordinates against
the printed axis labels, and write a plain (wavenumber, transmittance) table.

Axis calibration (page units, taken from the label bounding boxes):
    x = 154.75 pt -> 3500 cm-1        x = 742.80 pt ->  500 cm-1
    y = 285.70 pt ->   75 %T          y =  94.75 pt ->   95 %T
"""

import csv
import sys
from pathlib import Path

import pymupdf

X1, W1 = 154.75, 3500.0
X2, W2 = 742.80, 500.0
Y1, T1 = 285.70, 75.0
Y2, T2 = 94.75, 95.0

CURVE_WIDTH = 0.21  # pt; the trace is thinner than the axis frame (0.375 pt)
MIN_DX = 0.05       # pt; drops the vertical leader lines of the peak labels
MAX_DX = 1.00       # pt; drops their long diagonal connectors (dx >= 9.6 pt)


def x_to_wavenumber(x: float) -> float:
    return W1 + (x - X1) * (W2 - W1) / (X2 - X1)


def y_to_transmittance(y: float) -> float:
    return T1 + (y - Y1) * (T2 - T1) / (Y2 - Y1)


def extract(pdf_path: Path):
    doc = pymupdf.open(pdf_path)
    page = doc[0]
    points = []
    for path in page.get_drawings():
        if path["type"] != "s" or (path.get("width") or 1.0) > CURVE_WIDTH:
            continue
        for item in path["items"]:
            if item[0] != "l":
                continue
            a, b = item[1], item[2]
            if not (MIN_DX <= abs(b.x - a.x) <= MAX_DX):
                continue  # peak-label leader line, not part of the trace
            for pt in (a, b):
                points.append((x_to_wavenumber(pt.x), y_to_transmittance(pt.y)))

    # de-duplicate on wavenumber, keep ascending order
    points.sort(key=lambda p: p[0])
    out, last = [], None
    for wn, tr in points:
        if last is not None and abs(wn - last) < 1e-6:
            continue
        out.append((wn, tr))
        last = wn
    return out


def main():
    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    pts = extract(pdf_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["wavenumber_cm-1", "transmittance_percent"])
        for wn, tr in pts:
            w.writerow([f"{wn:.2f}", f"{tr:.3f}"])
    print(f"{len(pts)} points  {pts[0][0]:.1f}-{pts[-1][0]:.1f} cm-1  "
          f"T {min(p[1] for p in pts):.1f}-{max(p[1] for p in pts):.1f} %")


if __name__ == "__main__":
    main()
