# Electromagnetic Induction — Faraday's & Lenz's Law (explainer video)

A 3:01, 1920×1080 @ 24 fps animated explainer built entirely in Python
(matplotlib + numpy), encoded with ffmpeg. Every diagram is drawn from code —
no stock art, no AI image generation — so each frame is reproducible and
editable.

## Contents

| File | Purpose |
|---|---|
| `core.py` | Canvas, colour palette, easing, and the reusable physics primitives (solenoid, bar magnet, galvanometer, field markers, plot frames) |
| `scenes_a.py` | Scenes 1–5: title, magnetic flux, Faraday's law, Lenz's law, AC generator |
| `scenes_b.py` | Scenes 6–10: eddy currents, transformer, motional EMF, solved example, formula sheet |
| `render.py` | Scene list + durations; renders the whole film to MP4 |
| `narration.md` | Timed voiceover script (≈2.5 words/s) matched to the scene boundaries |

## Scene running order

| # | Scene | Start | Length |
|---|---|---|---|
| 1 | Title | 0:00 | 5 s |
| 2 | Magnetic flux — φ = BA cos θ | 0:05 | 18 s |
| 3 | Faraday's law — live φ–t and ε–t graphs | 0:23 | 26 s |
| 4 | Lenz's law — opposition and energy conservation | 0:49 | 22 s |
| 5 | AC generator — ε = NBAω sin ωt | 1:11 | 22 s |
| 6 | Eddy currents — magnet in copper vs plastic pipe | 1:33 | 18 s |
| 7 | Transformer — mutual induction | 1:51 | 18 s |
| 8 | Motional EMF — ε = Bℓv | 2:09 | 20 s |
| 9 | Solved example — exam pattern | 2:29 | 18 s |
| 10 | Formula sheet | 2:47 | 14 s |

## Physics notes on the animation

* In scene 3 the flux is modelled as a smooth function of magnet position and the
  EMF is obtained by **numerical differentiation** of that flux, so the ε–t curve
  really is −dφ/dt of the φ–t curve rather than a hand-drawn shape.
* The galvanometer needle follows the **sign of ε as plotted**, so the graph and the
  instrument never disagree.
* In scene 8 the current direction follows from qv×B (up the rod), which puts the
  force BIℓ opposite to v — Lenz's law, shown rather than asserted.

## Rebuilding

```bash
pip install numpy matplotlib imageio imageio-ffmpeg
cd physics/emi_video
python3 render.py EMI_Faraday_Lenz.mp4
```

Renders ~4,300 frames in roughly 5 minutes on a single core. To change the
running order or timings, edit the `SCENES` list in `render.py`.
