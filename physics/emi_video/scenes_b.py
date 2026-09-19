"""Scenes 6-10: Eddy currents, Transformer, Motional EMF, Worked example, Formula sheet."""
import numpy as np
from matplotlib.patches import Rectangle, Circle, Ellipse, Arc
from core import *
from scenes_a import seg, TAG


def vmagnet(ax, cx, cy, w=0.44, h=0.86, alpha=1.0, z=8):
    ax.add_patch(Rectangle((cx - w / 2, cy), w, h / 2, facecolor=RED,
                           edgecolor="#0B1026", lw=1.2, alpha=alpha, zorder=z))
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h / 2, facecolor=BLUE,
                           edgecolor="#0B1026", lw=1.2, alpha=alpha, zorder=z))
    ax.text(cx, cy + h / 4, "N", color="white", fontsize=12, fontweight="bold",
            va="center", ha="center", alpha=alpha, zorder=z + 1)
    ax.text(cx, cy - h / 4, "S", color="white", fontsize=12, fontweight="bold",
            va="center", ha="center", alpha=alpha, zorder=z + 1)


def pipe(ax, cx, y0, y1, hw, color, label, alpha=1.0):
    ax.add_patch(Rectangle((cx - hw, y0), 2 * hw, y1 - y0, facecolor=color,
                           edgecolor="none", alpha=0.13 * alpha, zorder=2))
    for s in (-1, 1):
        ax.plot([cx + s * hw, cx + s * hw], [y0, y1], color=color, lw=3.0,
                alpha=alpha, zorder=3)
    ax.text(cx, y1 + 0.3, label, color=color, fontsize=17, fontweight="bold",
            va="center", ha="center", alpha=alpha, zorder=4)


# ==================================================================== 6 EDDY
def scene_eddy(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Practical Example 2  —  Eddy Currents & Magnetic Braking",
              TAG, alpha=a, accent=PINK)

    y_top, y_bot = 7.05, 2.15
    pipe(ax, 2.15, 1.75, 7.35, 0.52, MUTED, "PLASTIC pipe", alpha=a)
    pipe(ax, 5.35, 1.75, 7.35, 0.52, COPPER, "COPPER pipe", alpha=a)

    # free fall (plastic) vs eddy-braked terminal velocity (copper)
    tp = np.clip((t - 1.5) / 1.8, 0, 1)
    yp = y_top - (y_top - y_bot) * tp ** 2
    tc = np.clip((t - 1.5) / 12.0, 0, 1)
    yc = y_top - (y_top - y_bot) * tc

    vmagnet(ax, 2.15, yp, alpha=a)
    vmagnet(ax, 5.35, yc, alpha=a)

    if 0 < tc < 1:
        for dy, col in ((0.78, CYAN), (-0.78, ORANGE)):
            yy = yc + dy
            if y_bot - 0.3 < yy < y_top + 0.3:
                ax.add_patch(Ellipse((5.35, yy), 1.58, 0.46, fill=False,
                                     edgecolor=col, lw=2.2, alpha=0.9 * a, zorder=6))
                arrow(ax, 5.35 + 0.6, yy + 0.16, 5.35 + 0.78, yy,
                      color=col, lw=2.0, alpha=0.9 * a, head=0.2, z=6)
        arrow(ax, 4.42, yc + 0.32, 4.42, yc - 0.32, color=LIME, lw=2.4,
              alpha=a, head=0.24, z=7)
        ax.text(4.12, yc, r"$\vec{v}$", color=LIME, fontsize=17, va="center",
                ha="center", alpha=a, zorder=7)
        arrow(ax, 6.35, yc - 0.3, 6.35, yc + 0.3, color=PINK, lw=2.6,
              alpha=a, head=0.26, z=7)
        ax.text(6.95, yc, "retarding\nforce", color=PINK, fontsize=13,
                va="center", ha="center", alpha=a, zorder=7, linespacing=1.4)

    ax.text(2.15, 1.42, "lands in ~0.4 s", color=MUTED, fontsize=14.5,
            va="center", ha="center", alpha=a * fade(t - 3.4, 0.5), zorder=5)
    ax.text(5.35, 1.42, "takes ~8 s to fall", color=COPPER, fontsize=14.5,
            va="center", ha="center", alpha=a * fade(t - 13.6, 0.5), zorder=5)
    ax.text(3.75, 1.06, "same magnet  ·  same height", color=MUTED, fontsize=13.5,
            va="center", ha="center", alpha=a, zorder=5)

    # ---- right panel
    panel(ax, 8.2, 1.25, 7.45, 6.45, fc=PANEL, ec=PINK, alpha=0.95 * a, lw=1.8, z=2)
    ax.text(11.92, 7.25, "EDDY CURRENTS", color=PINK, fontsize=25, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=4)
    ax.text(11.92, 6.68,
            "A changing flux through a SOLID conductor drives\nclosed loops of current inside its bulk.",
            color=WHITE, fontsize=16.5, va="center", ha="center", alpha=a,
            zorder=4, linespacing=1.5)

    b = [fade(t - k, 0.5) for k in (2.0, 3.4, 4.8)]
    bullet(ax, 8.55, 5.85, "By Lenz's law they OPPOSE the motion", alpha=a * b[0],
           fs=17, dot=LIME)
    bullet(ax, 8.55, 5.28, "Copper: high σ → huge eddy currents → strong braking",
           alpha=a * b[1], fs=16, dot=COPPER)
    bullet(ax, 8.55, 4.71, "Plastic: insulator → no current → free fall",
           alpha=a * b[2], fs=16, dot=MUTED)

    panel(ax, 8.55, 1.75, 6.75, 2.72, fc="#241A44", ec=YELLOW, alpha=0.92 * a, lw=1.5, z=3)
    ax.text(11.92, 4.12, "WHERE YOU SEE THEM", color=YELLOW, fontsize=17,
            fontweight="bold", va="center", ha="center", alpha=a * fade(t - 6.2, 0.5),
            zorder=4)
    apps = ["Induction cooktop & induction furnace (heating)",
            "Electromagnetic brakes in trains",
            "Damping in moving-coil galvanometers",
            "Speedometers, energy meters, metal detectors"]
    for k, s in enumerate(apps):
        bullet(ax, 8.85, 3.62 - 0.5 * k, s, alpha=a * fade(t - (7.0 + 0.9 * k), 0.5),
               fs=15.5, dot=YELLOW, dotr=0.06)

    footer(ax, "Eddy currents are minimised by LAMINATING the core — that is why transformer cores are thin sheets.",
           alpha=a, accent=PINK)


# ==================================================================== 7 TRANSFORMER
def scene_transformer(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Practical Example 3  —  the Transformer (Mutual Induction)",
              TAG, alpha=a, accent=VIOLET)

    s = np.sin(2 * np.pi * max(0.0, t - 1.2) / 3.0)
    cy = 5.15

    # laminated iron core drawn as a ring
    ax.add_patch(Rectangle((1.9, cy - 2.15), 4.4, 4.3, facecolor="#3A4570",
                           edgecolor="#5A67A0", lw=1.6, alpha=0.95 * a, zorder=3))
    ax.add_patch(Rectangle((2.8, cy - 1.35), 2.6, 2.7, facecolor=BG,
                           edgecolor="#5A67A0", lw=1.6, alpha=a, zorder=4))
    ax.text(4.1, 7.58, "laminated iron core", color="#C7D2FE", fontsize=13,
            va="center", ha="center", alpha=a, zorder=6)

    for yy in np.linspace(cy - 1.0, cy + 1.0, 5):          # primary, few turns
        ax.add_patch(Ellipse((2.35, yy), 1.15, 0.36, fill=False, edgecolor=COPPER,
                             lw=2.6, alpha=a, zorder=6))
    for yy in np.linspace(cy - 1.25, cy + 1.25, 9):        # secondary, many turns
        ax.add_patch(Ellipse((5.85, yy), 1.15, 0.28, fill=False, edgecolor=LIME,
                             lw=2.4, alpha=a, zorder=6))
    ax.text(2.35, 2.58, r"$N_p$ turns", color=COPPER, fontsize=16,
            va="center", ha="center", alpha=a, zorder=6)
    ax.text(5.85, 2.58, r"$N_s$ turns", color=LIME, fontsize=16,
            va="center", ha="center", alpha=a, zorder=6)

    # alternating flux circulating in the core
    for (px, py, dx, dy) in ((4.1, cy + 1.75, 1, 0), (4.1, cy - 1.75, -1, 0)):
        d = dx * (1 if s >= 0 else -1)
        arrow(ax, px - 0.45 * d, py, px + 0.45 * d, py, color=CYAN, lw=2.8,
              alpha=a * (0.35 + 0.65 * abs(s)), head=0.26, z=7)
    ax.text(4.1, cy, r"$\phi$", color=CYAN, fontsize=26, va="center", ha="center",
            alpha=a * (0.35 + 0.65 * abs(s)), zorder=7)

    # AC source and lamp
    ax.add_patch(Circle((0.95, cy), 0.42, fill=False, edgecolor=YELLOW, lw=2.4,
                        alpha=a, zorder=6))
    ax.text(0.95, cy, "~", color=YELLOW, fontsize=25, va="center", ha="center",
            alpha=a, zorder=7)
    ax.text(0.95, cy - 0.85, "AC", color=YELLOW, fontsize=15, va="center",
            ha="center", alpha=a, zorder=6)
    wire(ax, [(0.95, cy + 0.42), (0.95, cy + 1.15), (1.85, cy + 1.15)], alpha=a, z=5)
    wire(ax, [(0.95, cy - 0.42), (0.95, cy - 1.15), (1.85, cy - 1.15)], alpha=a, z=5)

    g = 0.28 + 0.72 * abs(s)
    for rr, al in ((0.78, 0.13), (0.62, 0.2), (0.48, 0.32)):
        ax.add_patch(Circle((7.45, cy), rr, facecolor=YELLOW, edgecolor="none",
                            alpha=al * g * a, zorder=5))
    ax.add_patch(Circle((7.45, cy), 0.36, facecolor="#FEF3C7", edgecolor=YELLOW,
                        lw=2.0, alpha=(0.3 + 0.7 * g) * a, zorder=6))
    wire(ax, [(6.42, cy + 1.15), (7.45, cy + 1.15), (7.45, cy + 0.36)], color=LIME,
         alpha=a, z=5)
    wire(ax, [(6.42, cy - 1.15), (7.45, cy - 1.15), (7.45, cy - 0.36)], color=LIME,
         alpha=a, z=5)
    ax.text(7.45, cy - 1.62, "load", color=LIME, fontsize=15, va="center",
            ha="center", alpha=a, zorder=6)

    # ---- right panel
    panel(ax, 8.55, 1.25, 7.1, 6.45, fc=PANEL, ec=VIOLET, alpha=0.95 * a, lw=1.8, z=2)
    ax.text(12.1, 7.25, "MUTUAL INDUCTION", color=VIOLET, fontsize=24,
            fontweight="bold", va="center", ha="center", alpha=a, zorder=4)
    ax.text(12.1, 6.65,
            "Changing current in the primary → changing flux\nin the core → induced EMF in the secondary.",
            color=WHITE, fontsize=16, va="center", ha="center", alpha=a,
            zorder=4, linespacing=1.5)
    formula(ax, 12.1, 5.55, r"$\varepsilon_2 = -M\dfrac{dI_1}{dt}$", fs=24, color=YELLOW,
            alpha=a * fade(t - 2.0, 0.5), bw=4.2, bh=1.25, fc=PANEL_2)
    formula(ax, 12.1, 4.05, r"$\dfrac{\varepsilon_s}{\varepsilon_p}=\dfrac{N_s}{N_p}=\dfrac{I_p}{I_s}$",
            fs=24, color=LIME, alpha=a * fade(t - 4.0, 0.5), bw=5.4, bh=1.4, fc=PANEL_2)
    bullet(ax, 8.9, 2.92, r"$N_s>N_p$ : step-UP (V rises, I falls)",
           alpha=a * fade(t - 6.0, 0.5), fs=16.5, dot=LIME)
    bullet(ax, 8.9, 2.35, r"Ideal transformer : $\varepsilon_p I_p=\varepsilon_s I_s$",
           alpha=a * fade(t - 7.5, 0.5), fs=16.5, dot=CYAN)
    bullet(ax, 8.9, 1.78, "Works on AC ONLY — steady DC gives dφ/dt = 0",
           alpha=a * fade(t - 9.0, 0.5), fs=16.5, dot=ORANGE)

    footer(ax, "A transformer changes voltage, never power — and it can never work on steady DC.",
           alpha=a, accent=VIOLET)


# ==================================================================== 8 MOTIONAL EMF
def scene_motional(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Motional EMF  —  a rod sliding on rails", TAG, alpha=a, accent=CYAN)

    y1, y2 = 4.55, 6.75
    x_r = seg(t, [(1.5, 3.0), (7.5, 7.6), (9.0, 7.6), (14.0, 3.0), (20.0, 3.0)])
    moving = (1.5 < t < 7.5) or (9.0 < t < 14.0)
    vsign = 1.0 if t < 8.0 else -1.0

    field_into_page(ax, 1.55, 8.15, y1 + 0.28, y2 - 0.28, nx=9, ny=4,
                    color=CYAN, alpha=0.5 * a, fs=14)
    ax.text(4.85, y2 + 0.72, r"$\vec{B}$  into the page", color=CYAN, fontsize=17,
            va="center", ha="center", alpha=a, zorder=4)

    ax.plot([1.3, 8.4], [y1, y1], color=COPPER, lw=3.2, alpha=a, zorder=5)
    ax.plot([1.3, 8.4], [y2, y2], color=COPPER, lw=3.2, alpha=a, zorder=5)
    ax.add_patch(Rectangle((1.18, y1 + 0.62), 0.42, 0.96, facecolor=PANEL_2,
                           edgecolor=WHITE, lw=2.0, alpha=a, zorder=6))
    ax.plot([1.39, 1.39], [y1, y1 + 0.62], color=COPPER, lw=3.2, alpha=a, zorder=5)
    ax.plot([1.39, 1.39], [y1 + 1.58, y2], color=COPPER, lw=3.2, alpha=a, zorder=5)
    ax.text(0.82, y1 + 1.1, "R", color=WHITE, fontsize=19, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=6)

    ax.plot([x_r, x_r], [y1, y2], color=LIME, lw=6.0, alpha=a,
            solid_capstyle="round", zorder=7)
    ax.text(x_r + 0.34, (y1 + y2) / 2, r"$\ell$", color=LIME, fontsize=19,
            va="center", ha="center", alpha=a, zorder=7)

    if moving:
        arrow(ax, x_r, y2 + 0.38, x_r + 0.95 * vsign, y2 + 0.38, color=LIME,
              lw=2.8, alpha=a, head=0.26, z=8)
        ax.text(x_r + 0.5 * vsign, y2 + 0.74, r"$\vec{v}$", color=LIME, fontsize=19,
                va="center", ha="center", alpha=a, zorder=8)
        arrow(ax, x_r, y1 - 0.38, x_r - 0.95 * vsign, y1 - 0.38, color=PINK,
              lw=2.8, alpha=a, head=0.26, z=8)
        ax.text(x_r - 0.52 * vsign, y1 - 0.76, r"$F=BI\ell$", color=PINK, fontsize=16,
                va="center", ha="center", alpha=a, zorder=8)
        # induced current: up the rod, left along the top rail, back along the bottom
        arrow(ax, x_r - 0.34, 5.32, x_r - 0.34, 5.98, color=YELLOW, lw=2.6,
              alpha=a, head=0.24, z=8)
        for xx in (2.6, 3.9, 5.2):
            if xx < x_r - 0.55:
                arrow(ax, xx + 0.34, y2 + 0.16, xx, y2 + 0.16, color=YELLOW, lw=2.2,
                      alpha=a, head=0.2, z=8)
                arrow(ax, xx, y1 - 0.16, xx + 0.34, y1 - 0.16, color=YELLOW, lw=2.2,
                      alpha=a, head=0.2, z=8)
        ax.text(x_r - 0.72, 5.65, "I", color=YELLOW, fontsize=17, fontweight="bold",
                va="center", ha="center", alpha=a, zorder=8)

    ax.text(4.85, 3.35,
            "Free charges in the rod feel  qv×B  → they pile up → an EMF appears",
            color=MUTED, fontsize=15.5, va="center", ha="center", alpha=a, zorder=5)

    # ---- right panel
    panel(ax, 9.0, 1.25, 6.65, 6.45, fc=PANEL, ec=CYAN, alpha=0.95 * a, lw=1.8, z=2)
    ax.text(12.32, 7.25, "MOTIONAL EMF", color=CYAN, fontsize=25, fontweight="bold",
            va="center", ha="center", alpha=a, zorder=4)
    ax.text(12.32, 6.6, r"$\phi = B\ell x$      $\Rightarrow$      $\dfrac{d\phi}{dt}=B\ell\dfrac{dx}{dt}$",
            color=WHITE, fontsize=20, va="center", ha="center", alpha=a * fade(t - 1.5, 0.5),
            zorder=4)
    formula(ax, 12.32, 5.3, r"$|\varepsilon| = B\ell v$", fs=30, color=YELLOW,
            alpha=a * fade(t - 3.5, 0.5), bw=4.0, bh=1.3, fc=PANEL_2)
    bullet(ax, 9.35, 4.15, r"Induced current  $I = \dfrac{B\ell v}{R}$",
           alpha=a * fade(t - 5.5, 0.5), fs=17, dot=ORANGE)
    bullet(ax, 9.35, 3.4, r"Retarding force  $F = \dfrac{B^2\ell^2 v}{R}$",
           alpha=a * fade(t - 7.0, 0.5), fs=17, dot=PINK)
    bullet(ax, 9.35, 2.65, r"Power dissipated  $P = \dfrac{B^2\ell^2v^2}{R}$",
           alpha=a * fade(t - 8.5, 0.5), fs=17, dot=LIME)
    ax.text(12.32, 1.78, "Reverse v  →  the current and the force both reverse.",
            color=MUTED, fontsize=15.5, va="center", ha="center",
            alpha=a * fade(t - 10.0, 0.5), zorder=4)

    footer(ax, "The retarding force is Lenz's law again: you must do work to keep the rod moving.",
           alpha=a, accent=CYAN)


# ==================================================================== 9 EXAMPLE
def scene_example(ax, t, dur):
    a = fade(t, 0.5, 0.4, dur)
    title_bar(ax, "Solved Example  —  exam pattern", TAG, alpha=a, accent=ORANGE)

    panel(ax, 0.6, 5.75, 14.8, 2.05, fc=PANEL, ec=ORANGE, alpha=0.95 * a, lw=1.8, z=2)
    ax.text(0.95, 7.42, "QUESTION", color=ORANGE, fontsize=15, fontweight="bold",
            va="center", ha="left", alpha=a, zorder=4)
    ax.text(0.95, 6.82,
            "A circular coil of 200 turns and radius 5 cm lies with its plane perpendicular to a uniform field.",
            color=WHITE, fontsize=17.5, va="center", ha="left", alpha=a, zorder=4)
    ax.text(0.95, 6.28,
            "The field falls steadily from 0.60 T to 0.20 T in 0.10 s.  Find the induced EMF and the current if R = 4 Ω.",
            color=WHITE, fontsize=17.5, va="center", ha="left", alpha=a, zorder=4)

    steps = [
        (r"Area :   $A=\pi r^{2}=\pi(0.05)^{2}=7.85\times10^{-3}\ \mathrm{m^{2}}$", CYAN),
        (r"Rate :   $\left|\dfrac{dB}{dt}\right|=\dfrac{0.60-0.20}{0.10}=4\ \mathrm{T\,s^{-1}}$", LIME),
        (r"EMF :   $|\varepsilon|=NA\left|\dfrac{dB}{dt}\right|=200\times7.85\times10^{-3}\times4$", YELLOW),
        (r"Current :   $I=\dfrac{|\varepsilon|}{R}=\dfrac{6.28}{4}$", VIOLET),
    ]
    for k, (s, c) in enumerate(steps):
        al = a * fade(t - (1.6 + 2.5 * k), 0.6)
        y = 5.05 - 0.95 * k
        panel(ax, 0.6, y - 0.4, 9.4, 0.82, fc="#131A3A", ec=c, alpha=0.9 * al, lw=1.4, z=3)
        ax.text(0.95, y, s, color=c, fontsize=19, va="center", ha="left",
                alpha=al, zorder=4)

    al = a * fade(t - 11.2, 0.7)
    panel(ax, 10.35, 1.35, 5.05, 3.7, fc="#24194A", ec=YELLOW, alpha=0.95 * al, lw=2.0, z=3)
    ax.text(12.87, 4.55, "ANSWER", color=YELLOW, fontsize=17, fontweight="bold",
            va="center", ha="center", alpha=al, zorder=4)
    ax.text(12.87, 3.75, r"$|\varepsilon| = 6.28\ \mathrm{V}$", color=WHITE, fontsize=27,
            va="center", ha="center", alpha=al, zorder=4)
    ax.text(12.87, 2.95, r"$I = 1.57\ \mathrm{A}$", color=WHITE, fontsize=27,
            va="center", ha="center", alpha=al, zorder=4)
    ax.text(12.87, 2.05,
            "By Lenz's law the current flows so as\nto MAINTAIN the decreasing flux.",
            color=LIME, fontsize=14.5, va="center", ha="center", alpha=al,
            zorder=4, linespacing=1.45)

    footer(ax, "Always convert cm → m before substituting; a radius slip costs the whole question.",
           alpha=a, accent=ORANGE)


# ==================================================================== 10 FORMULAE
def scene_formulae(ax, t, dur):
    a = fade(t, 0.5, 0.5, dur)
    title_bar(ax, "Formula Sheet  —  Electromagnetic Induction", TAG, alpha=a, accent=YELLOW)

    cards = [
        ("Magnetic flux", r"$\phi=\vec{B}\cdot\vec{A}=BA\cos\theta$", CYAN),
        ("Faraday's law", r"$\varepsilon=-N\dfrac{d\phi}{dt}$", YELLOW),
        ("Induced charge", r"$q=\dfrac{N\Delta\phi}{R}$   (time-independent)", LIME),
        ("Motional EMF", r"$\varepsilon=B\ell v$ ,   $F=\dfrac{B^{2}\ell^{2}v}{R}$", ORANGE),
        ("Rotating coil", r"$\varepsilon=NBA\omega\sin\omega t$ ,  $\varepsilon_0=NBA\omega$", PINK),
        ("Rotating rod", r"$\varepsilon=\frac{1}{2}B\omega\ell^{2}$", VIOLET),
        ("Self induction", r"$\varepsilon=-L\dfrac{dI}{dt}$ ,   $U=\frac{1}{2}LI^{2}$", GREEN),
        ("Mutual induction", r"$\varepsilon_2=-M\dfrac{dI_1}{dt}$ ,  $M=k\sqrt{L_1L_2}$", CYAN),
    ]
    for k, (name, tex, c) in enumerate(cards):
        col, row = k % 2, k // 2
        x = 0.55 + col * 7.75
        y = 6.28 - row * 1.62
        al = a * fade(t - (0.9 + 0.42 * k), 0.5)
        panel(ax, x, y, 7.3, 1.45, fc=PANEL, ec=c, alpha=0.93 * al, lw=1.6, z=2)
        ax.text(x + 0.3, y + 1.14, name.upper(), color=c, fontsize=13.5,
                fontweight="bold", va="center", ha="left", alpha=al, zorder=4)
        ax.text(x + 0.3, y + 0.5, tex, color=WHITE, fontsize=20, va="center",
                ha="left", alpha=al, zorder=4)

    footer(ax, "Learn the SIGN, the RATE and the OPPOSITION — every EMI question is built from these three ideas.",
           alpha=a, accent=YELLOW)
