import sys, time
import numpy as np
import imageio.v2 as iio
from core import new_canvas, reset, grab, FPS
import scenes_a as A
import scenes_b as B

SCENES = [
    ("Title",              A.scene_title,       5),
    ("Magnetic Flux",      A.scene_flux,       18),
    ("Faraday's Law",      A.scene_faraday,    26),
    ("Lenz's Law",         A.scene_lenz,       22),
    ("AC Generator",       A.scene_generator,  22),
    ("Eddy Currents",      B.scene_eddy,       18),
    ("Transformer",        B.scene_transformer,18),
    ("Motional EMF",       B.scene_motional,   20),
    ("Solved Example",     B.scene_example,    18),
    ("Formula Sheet",      B.scene_formulae,   14),
]

def main():
    OUT = sys.argv[1] if len(sys.argv) > 1 else "EMI_Faraday_Lenz.mp4"
    total = sum(d for _, _, d in SCENES)
    nframes = int(total * FPS)
    print(f"scenes={len(SCENES)} duration={total}s frames={nframes} fps={FPS}", flush=True)

    fig, ax = new_canvas()
    w = iio.get_writer(OUT, fps=FPS, codec="libx264", quality=None, macro_block_size=1,
                       ffmpeg_params=["-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p"])
    t0 = time.time()
    done = 0
    for name, fn, dur in SCENES:
        n = int(dur * FPS)
        for k in range(n):
            reset(ax)
            fn(ax, k / FPS, dur)
            w.append_data(grab(fig))
            done += 1
            if done % 120 == 0:
                el = time.time() - t0
                print(f"  {done}/{nframes} ({100*done/nframes:.1f}%) {el:.0f}s "
                      f"eta {el/done*(nframes-done):.0f}s  [{name}]", flush=True)
    w.close()
    print(f"DONE {OUT} in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
