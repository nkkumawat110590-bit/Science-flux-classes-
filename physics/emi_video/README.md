# Electromagnetic Induction — Faraday's & Lenz's Law (explainer video)

A narrated 3:55, 1920×1080 @ 24 fps animated explainer built entirely in Python
(matplotlib + numpy), encoded with ffmpeg. Every diagram is drawn from code —
no stock art, no AI image generation — so each frame is reproducible and
editable. A **Science Flux Classes** badge is burned into every frame.

## Contents

| File | Purpose |
|---|---|
| `core.py` | Canvas, palette, easing, brand badge, and the reusable physics primitives (solenoid, bar magnet, galvanometer, field markers, plot frames) |
| `scenes_a.py` | Scenes 1–5: title, magnetic flux, Faraday's law, Lenz's law, AC generator |
| `scenes_b.py` | Scenes 6–10: eddy currents, transformer, motional EMF, solved example, formula sheet |
| `narrate.py` | The spoken script, and the synthesiser that renders each take to `audio/NN.wav` + `timing.json` |
| `render.py` | Scene list, playout timing, and the frame renderer |
| `build_audio.py` | Lays the takes onto a silent bed and muxes them onto the video |
| `narration.md` | Generated from `narrate.py` — the script with timings |

## Scene running order

| # | Scene | Start | Length |
|---|---|---|---|
| 1 | Title | 0:00 | 8.2 s |
| 2 | Magnetic flux — φ = BA cos θ | 0:08 | 23.6 s |
| 3 | Faraday's law — live φ–t and ε–t graphs | 0:31 | 32.2 s |
| 4 | Lenz's law — opposition and energy conservation | 1:04 | 28.4 s |
| 5 | AC generator — ε = NBAω sin ωt | 1:32 | 26.4 s |
| 6 | Eddy currents — magnet in copper vs plastic pipe | 1:58 | 21.3 s |
| 7 | Transformer — mutual induction | 2:20 | 24.4 s |
| 8 | Motional EMF — ε = Bℓv | 2:44 | 24.8 s |
| 9 | Solved example — exam pattern | 3:09 | 29.5 s |
| 10 | Formula sheet | 3:38 | 17.1 s |

## How the timing works

Each scene is choreographed against a **design duration**. When a narration take
is longer than that, `render.py` stretches the scene: it renders more frames and
feeds the scene a scaled clock, so the authored animation plays slower rather
than finishing early and freezing on a still. Change the script and the video
re-times itself — you never hand-edit keyframes to match a voice track.

## The voice

Narrated with **ElevenLabs** (`eleven_multilingual_v2`, voice *Ellis - British
Modern* - a clear teaching voice built for explainer work). The ten takes are
generated per scene, so any single line can be re-recorded without touching the
others.

`narrate.py` keeps a local espeak-ng + MBROLA fallback, used before ElevenLabs
was reachable here. It is intelligible but audibly synthetic; the committed
track is the ElevenLabs one.

To re-record a line: change it in `narrate.py`, regenerate that take as
`audio/NN.wav` (16 kHz mono), then re-run `build_audio.py`. If the new take
still fits its scene the video needs no re-render at all; if it is longer,
re-run `render.py` first and the scene stretches to fit.

## Physics notes on the animation

* In scene 3 the flux is modelled as a smooth function of magnet position and the
  EMF is obtained by **numerical differentiation** of that flux, so the ε–t curve
  really is −dφ/dt of the φ–t curve rather than a hand-drawn shape.
* The galvanometer needle follows the **sign of ε as plotted**, so the graph and the
  instrument never disagree.
* In scene 8 the current direction follows from qv×B (up the rod), which puts the
  force BIℓ opposite to v — Lenz's law, shown rather than asserted.

## Layout is checked by measurement, not by eye

Text collisions are caught with a render-and-measure pass: each scene is drawn,
the window extents of the heading, the chapter tag and the golden-point line are
taken, and real clearance is required between them. Eyeballing had already let
two colliding headings through.

## Rebuilding

```bash
pip install numpy matplotlib imageio imageio-ffmpeg
apt-get install -y espeak-ng mbrola mbrola-us2
cd physics/emi_video
python3 narrate.py
python3 render.py EMI_Faraday_Lenz_silent.mp4
python3 build_audio.py
```

Renders ~5,660 frames in roughly seven minutes on a single core.
