"""Core canvas, palette and reusable physics-diagram primitives for the EMI explainer."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Circle, Ellipse, FancyBboxPatch,
                                FancyArrow, Arc, Polygon, Wedge)

# ----------------------------------------------------------------- palette
BG        = "#0B1026"
PANEL     = "#151C3F"
PANEL_2   = "#1E2755"
CYAN      = "#22D3EE"
ORANGE    = "#FB923C"
LIME      = "#A3E635"
PINK      = "#F472B6"
YELLOW    = "#FDE047"
RED       = "#EF4444"
BLUE      = "#3B82F6"
COPPER    = "#E8944A"
WHITE     = "#F1F5F9"
MUTED     = "#94A3B8"
GREEN     = "#34D399"
VIOLET    = "#A78BFA"

W, H = 16.0, 9.0
FPS = 24
DPI = 120

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "dejavusans",
})


def new_canvas():
    fig = plt.figure(figsize=(W, H), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    return fig, ax


def reset(ax):
    ax.clear()
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_facecolor(BG)
    ax.axis("off")


def grab(fig):
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    return buf[:, :, :3].copy()


# ----------------------------------------------------------------- easing
def ease(t):
    """smoothstep 0..1"""
    t = float(np.clip(t, 0.0, 1.0))
    return t * t * (3 - 2 * t)


def fade(t, tin=0.4, tout=None, dur=None):
    """alpha ramp-in (and optional ramp-out)."""
    a = ease(t / tin) if tin > 0 else 1.0
    if tout and dur and t > dur - tout:
        a *= 1.0 - ease((t - (dur - tout)) / tout)
    return float(np.clip(a, 0, 1))


# ----------------------------------------------------------------- chrome
def panel(ax, x, y, w, h, fc=PANEL, ec=None, alpha=1.0, r=0.16, lw=1.6, z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, facecolor=fc,
                       edgecolor=ec if ec else fc, alpha=alpha, zorder=z)
    ax.add_patch(p)
    return p


def title_bar(ax, title, tag, alpha=1.0, accent=CYAN):
    panel(ax, 0.35, 8.05, 15.3, 0.78, fc=PANEL, ec=accent, alpha=0.95 * alpha, lw=1.8, z=2)
    ax.add_patch(Rectangle((0.35, 8.05), 0.14, 0.78, facecolor=accent,
                           edgecolor="none", alpha=alpha, zorder=3))
    ax.text(0.72, 8.44, title, color=WHITE, fontsize=27, fontweight="bold",
            va="center", ha="left", alpha=alpha, zorder=3)
    ax.text(15.45, 8.44, tag, color=accent, fontsize=15.5, fontweight="bold",
            va="center", ha="right", alpha=0.95 * alpha, zorder=3)


# The footer bar stops at x=12.45 so the brand badge drawn by watermark()
# always has clear space; nothing in the golden-point line may run into it.
FOOTER_W = 12.1
WM_X = 12.65


def footer(ax, text, alpha=1.0, accent=YELLOW, label="GOLDEN POINT"):
    panel(ax, 0.35, 0.22, FOOTER_W, 0.7, fc="#22194A", ec=accent,
          alpha=0.95 * alpha, lw=1.6, z=2)
    ax.text(0.62, 0.57, label, color=accent, fontsize=12.5, fontweight="bold",
            va="center", ha="left", alpha=alpha, zorder=3)
    ax.text(2.72, 0.57, text, color=WHITE, fontsize=15.5, va="center", ha="left",
            alpha=alpha, zorder=3)


def watermark(ax, alpha=1.0, accent=CYAN):
    """Brand badge, drawn on every frame in its own reserved strip."""
    panel(ax, WM_X, 0.22, 3.0, 0.7, fc="#16204A", ec=accent,
          alpha=0.92 * alpha, lw=1.5, z=2)
    ax.add_patch(Rectangle((WM_X, 0.22), 0.1, 0.7, facecolor=accent,
                           edgecolor="none", alpha=alpha, zorder=3))
    ax.text(14.2, 0.70, "SCIENCE FLUX", color=accent, fontsize=13.5,
            fontweight="bold", va="center", ha="center", alpha=alpha, zorder=3)
    ax.text(14.2, 0.42, "C L A S S E S", color=WHITE, fontsize=11,
            fontweight="bold", va="center", ha="center", alpha=0.9 * alpha, zorder=3)


def formula(ax, x, y, tex, fs=25, color=YELLOW, alpha=1.0, box=True,
            bw=None, bh=0.95, fc=PANEL_2, ec=None, ha="center"):
    if box:
        bw = bw if bw else 5.2
        x0 = x - bw / 2 if ha == "center" else x
        panel(ax, x0, y - bh / 2, bw, bh, fc=fc, ec=ec if ec else color,
              alpha=0.92 * alpha, lw=1.7, z=3)
    ax.text(x, y, tex, color=color, fontsize=fs, va="center", ha=ha,
            alpha=alpha, zorder=4)


def bullet(ax, x, y, text, alpha=1.0, color=WHITE, fs=17, dot=CYAN, dotr=0.075):
    ax.add_patch(Circle((x, y), dotr, facecolor=dot, edgecolor="none",
                        alpha=alpha, zorder=4))
    ax.text(x + 0.3, y, text, color=color, fontsize=fs, va="center", ha="left",
            alpha=alpha, zorder=4)


def arrow(ax, x1, y1, x2, y2, color=CYAN, lw=2.6, alpha=1.0, head=0.22, z=4, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=f"-|>,head_width={head*0.62},head_length={head}",
                                color=color, lw=lw, alpha=alpha, linestyle=ls,
                                shrinkA=0, shrinkB=0),
                zorder=z)


# ----------------------------------------------------------------- physics bits
def solenoid(ax, cx, cy, length, radius, n=9, color=COPPER, lw=3.0, alpha=1.0, z=5):
    """Side-on solenoid: evenly spaced turns drawn as narrow ellipses."""
    xs = np.linspace(cx - length / 2, cx + length / 2, n)
    for x in xs:
        ax.add_patch(Ellipse((x, cy), width=length / (n * 1.55), height=2 * radius,
                             fill=False, edgecolor=color, lw=lw, alpha=alpha, zorder=z))
    return xs


def bar_magnet(ax, cx, cy, w=1.9, h=0.62, north_left=True, alpha=1.0, z=7, fs=19):
    nc, sc = (RED, BLUE) if north_left else (BLUE, RED)
    nl, sl = ("N", "S") if north_left else ("S", "N")
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w / 2, h, facecolor=nc,
                           edgecolor="#0B1026", lw=1.4, alpha=alpha, zorder=z))
    ax.add_patch(Rectangle((cx, cy - h / 2), w / 2, h, facecolor=sc,
                           edgecolor="#0B1026", lw=1.4, alpha=alpha, zorder=z))
    ax.text(cx - w / 4, cy, nl, color="white", fontsize=fs, fontweight="bold",
            va="center", ha="center", alpha=alpha, zorder=z + 1)
    ax.text(cx + w / 4, cy, sl, color="white", fontsize=fs, fontweight="bold",
            va="center", ha="center", alpha=alpha, zorder=z + 1)


def galvanometer(ax, cx, cy, r=0.78, defl=0.0, alpha=1.0, z=6, label="G"):
    """defl in -1..1 -> needle angle +-62 deg (right = positive)."""
    ax.add_patch(Circle((cx, cy), r, facecolor="#F8FAFC", edgecolor=CYAN,
                        lw=2.4, alpha=alpha, zorder=z))
    ax.add_patch(Wedge((cx, cy), r * 0.94, 30, 150, width=r * 0.1,
                       facecolor="#CBD5E1", edgecolor="none", alpha=alpha, zorder=z + 1))
    for a in range(30, 151, 15):
        ra = np.radians(a)
        ax.plot([cx + r * 0.72 * np.cos(ra), cx + r * 0.86 * np.cos(ra)],
                [cy + r * 0.72 * np.sin(ra), cy + r * 0.86 * np.sin(ra)],
                color="#64748B", lw=1.2, alpha=alpha, zorder=z + 1)
    d = float(np.clip(defl, -1, 1))
    ang = np.radians(90 - 62 * d)
    ncol = ORANGE if abs(d) > 0.03 else "#475569"
    ax.plot([cx, cx + r * 0.78 * np.cos(ang)], [cy, cy + r * 0.78 * np.sin(ang)],
            color=ncol, lw=3.4, solid_capstyle="round", alpha=alpha, zorder=z + 2)
    ax.add_patch(Circle((cx, cy), r * 0.1, facecolor="#1E293B", edgecolor="none",
                        alpha=alpha, zorder=z + 3))
    ax.text(cx, cy - r * 0.52, label, color="#334155", fontsize=15,
            fontweight="bold", va="center", ha="center", alpha=alpha, zorder=z + 2)
    ax.text(cx - r * 0.66, cy + r * 0.45, "–", color="#64748B", fontsize=14,
            va="center", ha="center", alpha=alpha, zorder=z + 2)
    ax.text(cx + r * 0.66, cy + r * 0.45, "+", color="#64748B", fontsize=13,
            va="center", ha="center", alpha=alpha, zorder=z + 2)


def wire(ax, pts, color=COPPER, lw=2.6, alpha=1.0, z=4):
    p = np.asarray(pts, dtype=float)
    ax.plot(p[:, 0], p[:, 1], color=color, lw=lw, alpha=alpha,
            solid_capstyle="round", zorder=z)


def field_into_page(ax, x0, x1, y0, y1, nx=7, ny=5, color=CYAN, alpha=0.75, fs=13, z=2):
    for x in np.linspace(x0, x1, nx):
        for y in np.linspace(y0, y1, ny):
            ax.text(x, y, "×", color=color, fontsize=fs, alpha=alpha,
                    va="center", ha="center", zorder=z)


def field_out_page(ax, x0, x1, y0, y1, nx=7, ny=5, color=CYAN, alpha=0.75, r=0.075, z=2):
    for x in np.linspace(x0, x1, nx):
        for y in np.linspace(y0, y1, ny):
            ax.add_patch(Circle((x, y), r, fill=False, edgecolor=color,
                                lw=1.3, alpha=alpha, zorder=z))
            ax.add_patch(Circle((x, y), r * 0.3, facecolor=color,
                                edgecolor="none", alpha=alpha, zorder=z))


def field_lines_h(ax, x0, x1, ys, color=CYAN, alpha=0.5, lw=1.5, nar=3, z=2):
    """Horizontal uniform-field lines with arrowheads pointing +x."""
    for y in ys:
        ax.plot([x0, x1], [y, y], color=color, lw=lw, alpha=alpha, zorder=z)
        for xa in np.linspace(x0 + (x1 - x0) * 0.22, x1 - (x1 - x0) * 0.12, nar):
            ax.annotate("", xy=(xa + 0.2, y), xytext=(xa, y),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.14,head_length=0.2",
                                        color=color, lw=lw, alpha=alpha,
                                        shrinkA=0, shrinkB=0), zorder=z)


def mini_axes(ax, x, y, w, h, xlabel, ylabel, ac=MUTED, alpha=1.0, z=3,
              fs=13, zero_line=True):
    """Draw a small plot frame in canvas coords. Returns mapper (u,v in 0..1)->canvas."""
    panel(ax, x, y, w, h, fc="#101736", ec="#2A3563", alpha=0.95 * alpha, lw=1.4, z=z)
    x0, y0 = x + 0.62, y + 0.5
    pw, ph = w - 0.9, h - 0.85
    ax.plot([x0, x0], [y0, y0 + ph], color=ac, lw=1.6, alpha=alpha, zorder=z + 1)
    ax.plot([x0, x0 + pw], [y0 + ph / 2, y0 + ph / 2] if zero_line else [y0, y0],
            color=ac, lw=1.6, alpha=alpha, zorder=z + 1)
    ax.text(x0 + pw + 0.1, (y0 + ph / 2) if zero_line else y0, xlabel, color=ac,
            fontsize=fs, va="center", ha="left", alpha=alpha, zorder=z + 1)
    ax.text(x0 - 0.12, y0 + ph + 0.06, ylabel, color=ac, fontsize=fs + 1,
            va="bottom", ha="center", alpha=alpha, zorder=z + 1)

    def M(u, v):
        """u: 0..1 along x; v: -1..1 (if zero_line) else 0..1 along y."""
        cx = x0 + u * pw
        cy = (y0 + ph / 2 + v * ph / 2) if zero_line else (y0 + v * ph)
        return cx, cy
    return M
