"""Render the EMI explainer to MP4.

Each scene is choreographed against a DESIGN duration. When narration is
present the scene is stretched to cover its take: we render more frames and
feed the scene a scaled clock, so the authored choreography simply plays
slower instead of finishing early and freezing.
"""
import json
import sys
import time
from pathlib import Path

import imageio.v2 as iio

from core import new_canvas, reset, grab, watermark, FPS
import scenes_a as A
import scenes_b as B

# (name, function, design duration)
SCENES = [
    ("Title",          A.scene_title,        5),
    ("Magnetic Flux",  A.scene_flux,        18),
    ("Faraday's Law",  A.scene_faraday,     26),
    ("Lenz's Law",     A.scene_lenz,        22),
    ("AC Generator",   A.scene_generator,   22),
    ("Eddy Currents",  B.scene_eddy,        18),
    ("Transformer",    B.scene_transformer, 18),
    ("Motional EMF",   B.scene_motional,    20),
    ("Solved Example", B.scene_example,     18),
    ("Formula Sheet",  B.scene_formulae,    14),
]


def playout():
    """[(name, fn, design_dur, actual_dur)] — stretched to the narration if timed."""
    timing = {}
    if Path("timing.json").exists():
        timing = json.load(open("timing.json"))["scenes"]
    out = []
    for name, fn, design in SCENES:
        actual = max(design, timing.get(name, {}).get("scene", 0))
        out.append((name, fn, design, actual))
    return out


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "EMI_Faraday_Lenz.mp4"
    plan = playout()
    total = sum(a for _, _, _, a in plan)
    nframes = int(round(total * FPS))
    print(f"scenes={len(plan)} duration={total:.1f}s frames={nframes} fps={FPS}", flush=True)

    fig, ax = new_canvas()
    w = iio.get_writer(out, fps=FPS, codec="libx264", quality=None, macro_block_size=1,
                       ffmpeg_params=["-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p"])
    t0, done = time.time(), 0
    for name, fn, design, actual in plan:
        n = int(round(actual * FPS))
        scale = design / actual          # feed the scene its own clock
        for k in range(n):
            reset(ax)
            fn(ax, (k / FPS) * scale, design)
            watermark(ax)
            w.append_data(grab(fig))
            done += 1
            if done % 240 == 0:
                el = time.time() - t0
                print(f"  {done}/{nframes} ({100*done/nframes:.1f}%) {el:.0f}s "
                      f"eta {el/done*(nframes-done):.0f}s  [{name}]", flush=True)
    w.close()
    print(f"DONE {out} in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
