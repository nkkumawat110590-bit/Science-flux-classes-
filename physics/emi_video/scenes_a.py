"""Scenes 1-5: Title, Magnetic Flux, Faraday's Law, Lenz's Law, AC Generator."""
import numpy as np
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon, Arc, Wedge
from core import *

TAG = "ELECTROMAGNETIC INDUCTION"


def seg(t, pts):
    """Piecewise eased interpolation. pts = [(t0,v0),(t1,v1),...]"""
    if t <= pts[0][0]:
        return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts[:-1], pts[1:]):
        if t <= tb:
            if tb == ta:
                return vb
            return va + (vb - va) * ease((t - ta) / (tb - ta))
    return pts[-1][1]


# ==================================================================== 1 TITLE
def scene_title(ax, t, dur):
    a = fade(t, 0.8, 0.6, dur)
    glow = 0.55 + 0.45 * np.sin(2 * np.pi * t / 2.2)

    ax.text(8.0, 7.15, "ELECTROMAGNETIC", color=CYAN, fontsize=60,
            fontweight="bold", va="center", ha="center", alpha=a, zorder=5)
    ax.text(8.0, 6.15, "INDUCTION", color=WHITE, fontsize=60, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=5)
    ax.plot([5.2, 10.8], [5.5, 5.5], color=ORANGE, lw=3, alpha=a, zorder=5)
    ax.text(8.0, 5.02, "Faraday's Law  ·  Lenz's Law  ·  Practical Applications",
            color=YELLOW, fontsize=24, va="center", ha="center", alpha=a, zorder=5)

    # mini live demo
    mx = seg(t, [(0.9, 2.9), (2.6, 5.55), (3.4, 5.55), (4.4, 2.9)])
    cy = 3.05
    solenoid(ax, 6.55, cy, 2.0, 0.72, n=8, color=COPPER, alpha=a * (0.6 + 0.4 * glow), lw=3.2)
    bar_magnet(ax, mx, cy, north_left=False, alpha=a, fs=17)
    wire(ax, [(7.55, cy - 0.72), (8.6, cy - 0.72), (8.6, cy), (9.25, cy)], alpha=a)
    wire(ax, [(7.55, cy + 0.72), (8.6, cy + 0.72), (8.6, cy), (9.25, cy)], alpha=a)
    d = 0.0
    if 0.9 < t < 2.6:
        d = 0.72
    elif 3.4 < t < 4.4:
        d = -0.72
    galvanometer(ax, 10.1, cy, r=0.72, defl=d, alpha=a)

    ax.text(8.0, 1.35, "JEE Main   ·   JEE Advanced   ·   NEET",
            color=MUTED, fontsize=20, va="center", ha="center", alpha=a, zorder=5)


# ==================================================================== 2 FLUX
def scene_flux(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Magnetic Flux  —  the foundation", TAG, alpha=a)

    th = np.radians(seg(t, [(1.6, 0), (7.0, 90), (9.0, 90), (13.5, 0), (15.0, 0), (17.0, 60)]))
    cx, cy, R = 4.35, 5.05, 1.55

    field_lines_h(ax, 0.75, 7.95, np.linspace(cy - 2.0, cy + 2.0, 7),
                  color=CYAN, alpha=0.42 * a, lw=1.4)
    ax.text(0.95, cy + 2.45, r"$\vec{B}$", color=CYAN, fontsize=23, alpha=a,
            va="center", ha="center", zorder=4)

    ax.plot([cx, cx], [cy - 2.25, cy + 2.25], color=MUTED, lw=1.2, ls="--",
            alpha=0.5 * a, zorder=3)

    # loop drawn edge-on: major axis perpendicular to the normal
    ang = np.degrees(th)
    ax.add_patch(Ellipse((cx, cy), width=2 * R * 0.26, height=2 * R, angle=ang,
                         fill=False, edgecolor=COPPER, lw=4.0, alpha=a, zorder=6))
    # normal (area) vector
    arrow(ax, cx, cy, cx + 2.05 * np.cos(th), cy + 2.05 * np.sin(th),
          color=LIME, lw=3.2, alpha=a, head=0.3, z=7)
    ax.text(cx + 2.35 * np.cos(th), cy + 2.35 * np.sin(th), r"$\hat{n}$", color=LIME,
            fontsize=22, va="center", ha="center", alpha=a, zorder=7)
    if np.degrees(th) > 6:
        ax.add_patch(Arc((cx, cy), 2.0, 2.0, theta1=0, theta2=np.degrees(th),
                         edgecolor=YELLOW, lw=2.2, alpha=a, zorder=7))
        ax.text(cx + 1.28 * np.cos(th / 2), cy + 1.28 * np.sin(th / 2), r"$\theta$",
                color=YELLOW, fontsize=21, va="center", ha="center", alpha=a, zorder=8)

    ax.text(cx, 2.5, "loop seen edge-on", color=MUTED, fontsize=14,
            va="center", ha="center", alpha=a, zorder=5)

    # ---- right column
    formula(ax, 12.0, 7.05, r"$\phi = \vec{B}\cdot\vec{A} = BA\cos\theta$", fs=27,
            color=YELLOW, alpha=a, bw=6.6, bh=1.05)
    c = float(np.cos(th))
    ax.text(12.0, 5.95, r"$\theta = %d^\circ$        $\cos\theta = %.2f$"
            % (round(np.degrees(th)), c), color=WHITE, fontsize=22,
            va="center", ha="center", alpha=a, zorder=5)

    # live flux bar
    bx, by, bw2, bh2 = 8.9, 5.05, 6.2, 0.52
    panel(ax, bx, by, bw2, bh2, fc="#101736", ec="#2A3563", alpha=a, lw=1.4, z=3)
    ax.add_patch(Rectangle((bx + 0.04, by + 0.04), max(0.0, c) * (bw2 - 0.08), bh2 - 0.08,
                           facecolor=CYAN, edgecolor="none", alpha=0.9 * a, zorder=4))
    ax.text(bx, by - 0.32, r"$\phi\,/\,\phi_{max}$", color=MUTED, fontsize=15,
            va="center", ha="left", alpha=a, zorder=4)
    ax.text(bx + bw2, by - 0.32, "%.2f" % max(0.0, c), color=CYAN, fontsize=16,
            fontweight="bold", va="center", ha="right", alpha=a, zorder=4)

    b1 = fade(t - 2.0, 0.5)
    b2 = fade(t - 3.6, 0.5)
    b3 = fade(t - 5.2, 0.5)
    b4 = fade(t - 6.8, 0.5)
    bullet(ax, 9.0, 4.0, r"$\theta=0^\circ$ : plane $\perp \vec{B}$  →  $\phi$ maximum $=BA$",
           alpha=a * b1, fs=18, dot=LIME)
    bullet(ax, 9.0, 3.35, r"$\theta=90^\circ$ : plane $\parallel \vec{B}$  →  $\phi = 0$",
           alpha=a * b2, fs=18, dot=ORANGE)
    bullet(ax, 9.0, 2.70, "Flux is a SCALAR.  SI unit : weber (Wb) = T·m²",
           alpha=a * b3, fs=18, dot=CYAN)
    bullet(ax, 9.0, 2.05, r"For $N$ turns, flux linkage $=N\phi$   (unit Wb-turns)",
           alpha=a * b4, fs=18, dot=VIOLET)

    footer(ax, "θ is measured between the AREA VECTOR n̂ and B — never between the plane and B.",
           alpha=a)


# ==================================================================== 3 FARADAY
_F_T = np.linspace(0, 26, 1600)


def _magnet_x(t):
    return seg(t, [(0, 2.2), (2.0, 2.2), (7.0, 5.6), (11.0, 5.6),
                   (16.0, 2.2), (18.0, 2.2), (20.5, 5.6), (26.0, 5.6)])


def _flux_of_x(x):
    return 1.0 / (1.0 + np.exp(-(x - 4.25) / 0.5))


_F_PHI = np.array([_flux_of_x(_magnet_x(tt)) for tt in _F_T])
_F_EMF = -np.gradient(_F_PHI, _F_T)
_F_REF = float(np.max(np.abs(_F_EMF))) or 1.0


def scene_faraday(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Faraday's Law of Induction", TAG, alpha=a)

    i = int(np.clip(np.searchsorted(_F_T, t), 0, len(_F_T) - 1))
    phi, emf = _F_PHI[i], _F_EMF[i]
    defl = float(np.clip(emf / _F_REF, -1, 1))

    cy = 6.45
    solenoid(ax, 6.2, cy, 2.4, 0.86, n=9, color=COPPER, alpha=a, lw=3.0, z=5)
    bar_magnet(ax, _magnet_x(t), cy, north_left=False, alpha=a, z=8)
    if abs(defl) > 0.04:
        vx = 0.85 if emf < 0 else -0.85
        arrow(ax, _magnet_x(t), cy + 1.22, _magnet_x(t) + vx, cy + 1.22,
              color=LIME, lw=2.8, alpha=a, head=0.26, z=9)
        ax.text(_magnet_x(t) + vx / 2, cy + 1.56, r"$\vec{v}$", color=LIME, fontsize=19,
                va="center", ha="center", alpha=a, zorder=9)

    wire(ax, [(7.45, cy + 0.86), (8.35, cy + 0.86), (8.35, cy + 0.30), (10.42, cy + 0.30)],
         alpha=a, z=4)
    wire(ax, [(7.45, cy - 0.86), (8.35, cy - 0.86), (8.35, cy - 0.30), (10.42, cy - 0.30)],
         alpha=a, z=4)
    galvanometer(ax, 11.2, cy, r=0.82, defl=defl, alpha=a)

    formula(ax, 13.95, cy, r"$\varepsilon = -N\dfrac{d\phi}{dt}$", fs=26, color=YELLOW,
            alpha=a, bw=3.2, bh=1.5)

    # status line
    if abs(emf) < 0.02 * _F_REF:
        msg, mc = "Magnet at rest  →  φ constant  →  NO induced EMF", MUTED
    elif emf < 0:
        msg, mc = ("Magnet ENTERING  →  φ increases  →  ε negative  →  needle swings LEFT", LIME)
    else:
        msg, mc = ("Magnet LEAVING  →  φ decreases  →  ε positive  →  needle swings RIGHT", ORANGE)
    if t > 20.0:
        msg, mc = ("SAME magnet, FASTER motion  →  larger |dφ/dt|  →  bigger deflection", PINK)
    ax.text(8.0, 5.02, msg, color=mc, fontsize=20, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=6)

    # graphs
    u = t / dur
    M1 = mini_axes(ax, 0.5, 1.15, 7.3, 3.25, "t", r"$\phi$", alpha=a, zero_line=False)
    M2 = mini_axes(ax, 8.2, 1.15, 7.3, 3.25, "t", r"$\varepsilon$", alpha=a, zero_line=True)
    m = _F_T <= t
    if m.sum() > 1:
        p1 = np.array([M1(tt / dur, vv) for tt, vv in zip(_F_T[m], _F_PHI[m])])
        ax.plot(p1[:, 0], p1[:, 1], color=CYAN, lw=3.0, alpha=a, zorder=6)
        ax.add_patch(Circle(tuple(p1[-1]), 0.09, facecolor=CYAN, edgecolor="none",
                            alpha=a, zorder=7))
        p2 = np.array([M2(tt / dur, vv / _F_REF) for tt, vv in zip(_F_T[m], _F_EMF[m])])
        ax.plot(p2[:, 0], p2[:, 1], color=ORANGE, lw=3.0, alpha=a, zorder=6)
        ax.add_patch(Circle(tuple(p2[-1]), 0.09, facecolor=ORANGE, edgecolor="none",
                            alpha=a, zorder=7))
    ax.text(4.15, 4.12, "flux through coil", color=CYAN, fontsize=15,
            va="center", ha="center", alpha=a, zorder=6)
    ax.text(11.85, 4.12, "induced EMF = – slope of φ–t graph", color=ORANGE, fontsize=15,
            va="center", ha="center", alpha=a, zorder=6)

    footer(ax, "EMF exists only while φ CHANGES. Flat φ–t graph ⇒ zero EMF, however large φ is.",
           alpha=a)


# ==================================================================== 4 LENZ
def scene_lenz(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Lenz's Law  —  the meaning of the minus sign", TAG, alpha=a, accent=ORANGE)

    approaching = t < 11.5
    cy = 5.15
    if approaching:
        mx = seg(t, [(1.5, 1.5), (7.5, 3.25), (11.5, 3.25)])
    else:
        mx = seg(t, [(12.5, 3.25), (18.5, 1.5), (22.0, 1.5)])

    solenoid(ax, 5.9, cy, 2.2, 0.92, n=9, color=COPPER, alpha=a, lw=3.0, z=5)
    # N-first: the leading pole faces the coil, which is what the labels below claim
    bar_magnet(ax, mx, cy, north_left=False, alpha=a, z=8)

    # induced pole on the coil face nearest the magnet
    face_pole = "N" if approaching else "S"
    fc_col = RED if approaching else BLUE
    ax.add_patch(Circle((5.02, cy), 0.34, facecolor=fc_col, edgecolor=WHITE,
                        lw=1.8, alpha=0.95 * a, zorder=9))
    ax.text(5.02, cy, face_pole, color="white", fontsize=19, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=10)

    # motion + force arrows
    vdir = 0.8 if approaching else -0.8
    arrow(ax, mx, cy + 1.05, mx + vdir, cy + 1.05, color=LIME, lw=2.8, alpha=a, head=0.26, z=9)
    ax.text(mx + vdir / 2, cy + 1.42, r"$\vec{v}$", color=LIME, fontsize=19,
            va="center", ha="center", alpha=a, zorder=9)
    fdir = -0.8 if approaching else 0.8
    arrow(ax, mx, cy - 1.05, mx + fdir, cy - 1.05, color=PINK, lw=2.8, alpha=a, head=0.26, z=9)
    ax.text(mx + fdir / 2, cy - 1.45,
            "REPULSION" if approaching else "ATTRACTION", color=PINK, fontsize=15,
            fontweight="bold", va="center", ha="center", alpha=a, zorder=9)

    # induced current sense on the coil
    spin = "anticlockwise" if approaching else "clockwise"
    ax.add_patch(Arc((5.9, cy), 2.3, 2.3, theta1=205, theta2=335,
                     edgecolor=CYAN, lw=2.6, alpha=a, zorder=6))
    tip = np.radians(335 if approaching else 205)
    arrow(ax, 5.9 + 1.15 * np.cos(tip - (0.13 if approaching else -0.13)),
          cy + 1.15 * np.sin(tip - (0.13 if approaching else -0.13)),
          5.9 + 1.15 * np.cos(tip), cy + 1.15 * np.sin(tip),
          color=CYAN, lw=2.6, alpha=a, head=0.26, z=6)
    ax.text(5.9, cy - 1.72, "induced current : " + spin, color=CYAN, fontsize=16,
            va="center", ha="center", alpha=a, zorder=6)
    ax.text(5.9, cy - 2.08, "(seen from the magnet's side)", color=MUTED, fontsize=13,
            va="center", ha="center", alpha=a, zorder=6)

    ax.text(4.3, 7.52,
            "N-pole APPROACHING" if approaching else "N-pole RECEDING",
            color=YELLOW, fontsize=23, fontweight="bold", va="center", ha="center",
            alpha=a, zorder=6)
    ax.text(4.3, 6.98,
            "φ increasing  →  coil OPPOSES it  →  pushes magnet back"
            if approaching else
            "φ decreasing  →  coil OPPOSES it  →  pulls magnet back",
            color=WHITE, fontsize=16, va="center", ha="center", alpha=a, zorder=6)

    # ---- right panel
    panel(ax, 8.9, 1.25, 6.75, 6.45, fc=PANEL, ec=ORANGE, alpha=0.95 * a, lw=1.8, z=2)
    ax.text(12.28, 7.25, "LENZ'S LAW", color=ORANGE, fontsize=26, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=4)
    ax.text(12.28, 6.45,
            "The induced current always flows in the\n"
            "direction that OPPOSES the change\nproducing it.",
            color=WHITE, fontsize=18, va="center", ha="center", alpha=a,
            zorder=4, linespacing=1.55)

    s1 = fade(t - 2.5, 0.5)
    s2 = fade(t - 4.5, 0.5)
    s3 = fade(t - 6.5, 0.5)
    s4 = fade(t - 13.0, 0.5)
    bullet(ax, 9.25, 5.42, "Step 1 : find φ and whether it ↑ or ↓",
           alpha=a * s1, fs=17, dot=LIME)
    bullet(ax, 9.25, 4.80, "Step 2 : induced φ opposes that change",
           alpha=a * s2, fs=17, dot=LIME)
    bullet(ax, 9.25, 4.18, "Step 3 : right-hand rule → current sense",
           alpha=a * s3, fs=17, dot=LIME)
    formula(ax, 12.28, 3.25, r"$\varepsilon = -N\dfrac{d\phi}{dt}$", fs=25, color=YELLOW,
            alpha=a, bw=3.2, bh=1.35, fc=PANEL_2)
    ax.text(12.28, 2.25, "the “–” sign IS Lenz's law", color=YELLOW, fontsize=17,
            va="center", ha="center", alpha=a, zorder=4)
    ax.text(12.28, 1.72, "Opposition ⇒ you do work ⇒ that work\nbecomes electrical energy.",
            color=GREEN, fontsize=16.5, va="center", ha="center", alpha=a * s4,
            zorder=4, linespacing=1.5)

    footer(ax, "Lenz's law is simply conservation of energy applied to induction.",
           alpha=a, accent=ORANGE)


# ==================================================================== 5 GENERATOR
def scene_generator(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Practical Example 1  \u2014  the AC Generator", TAG, alpha=a, accent=LIME)

    w = 2 * np.pi / 5.0                     # one revolution every 5 s
    t0 = 1.5
    th = w * max(0.0, t - t0)
    cx, cy, R = 4.05, 5.75, 1.38

    ax.add_patch(Rectangle((1.15, cy - 1.9), 0.72, 3.8, facecolor=RED,
                           edgecolor="none", alpha=0.9 * a, zorder=3))
    ax.text(1.51, cy, "N", color="white", fontsize=25, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=4)
    ax.add_patch(Rectangle((6.23, cy - 1.9), 0.72, 3.8, facecolor=BLUE,
                           edgecolor="none", alpha=0.9 * a, zorder=3))
    ax.text(6.59, cy, "S", color="white", fontsize=25, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=4)
    field_lines_h(ax, 1.95, 6.15, np.linspace(cy - 1.55, cy + 1.55, 5),
                  color=CYAN, alpha=0.38 * a, lw=1.3, nar=2)

    # rotating coil, drawn edge-on (major axis perpendicular to the normal)
    ax.add_patch(Ellipse((cx, cy), width=2 * R * 0.24, height=2 * R,
                         angle=np.degrees(th), fill=False, edgecolor=COPPER,
                         lw=4.0, alpha=a, zorder=6))
    arrow(ax, cx, cy, cx + 1.15 * np.cos(th), cy + 1.15 * np.sin(th),
          color=LIME, lw=2.6, alpha=a, head=0.26, z=7)

    # leads drop clear of the pole pieces, then run to the slip rings
    wire(ax, [(cx - 0.16, cy - 1.42), (cx - 0.16, 3.38), (7.62, 3.38)], alpha=a, z=4)
    wire(ax, [(cx + 0.16, cy - 1.42), (cx + 0.16, 2.92), (7.62, 2.92)], alpha=a, z=4)
    for yy in (3.38, 2.92):
        ax.add_patch(Circle((7.85, yy), 0.17, fill=False, edgecolor=COPPER,
                            lw=2.4, alpha=a, zorder=5))
    ax.text(7.55, 2.32, "slip rings + brushes", color=MUTED, fontsize=13.5,
            va="center", ha="center", alpha=a, zorder=5)
    ax.text(3.3, 2.32, "coil rotates with angular speed \u03c9", color=MUTED,
            fontsize=13.5, va="center", ha="center", alpha=a, zorder=5)

    # live waveform
    M = mini_axes(ax, 9.0, 3.15, 6.6, 4.05, "t", r"$\varepsilon$", alpha=a, zero_line=True)
    if t > t0:
        tt = np.linspace(0, t - t0, 420)
        pts = np.array([M(x / (dur - t0), 0.82 * np.sin(w * x)) for x in tt])
        ax.plot(pts[:, 0], pts[:, 1], color=YELLOW, lw=3.0, alpha=a, zorder=6)
        ax.add_patch(Circle(tuple(pts[-1]), 0.09, facecolor=YELLOW, edgecolor="none",
                            alpha=a, zorder=7))
    ax.text(12.3, 7.45, r"$\varepsilon = NBA\omega\sin\omega t$", color=YELLOW,
            fontsize=25, va="center", ha="center", alpha=a, zorder=6)

    b1, b2, b3 = fade(t - 3.0, 0.5), fade(t - 5.0, 0.5), fade(t - 7.0, 0.5)
    bullet(ax, 9.05, 2.55, r"Peak EMF  $\varepsilon_0 = NBA\omega$", alpha=a * b1, fs=18, dot=LIME)
    bullet(ax, 9.05, 1.95,
           r"$\varepsilon$ is MAXIMUM when the coil plane is $\parallel \vec{B}$  ($\phi=0$)",
           alpha=a * b2, fs=17, dot=ORANGE)
    bullet(ax, 9.05, 1.35,
           r"$\varepsilon$ is ZERO when the coil plane is $\perp \vec{B}$  ($\phi$ max)",
           alpha=a * b3, fs=17, dot=CYAN)

    footer(ax, "Every power station works on this: mechanical rotation \u2192 changing flux \u2192 AC.",
           alpha=a, accent=LIME)
