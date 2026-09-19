"""Lay each narration take onto a silent bed matching the rendered playout."""
import json
import subprocess
import wave

import numpy as np
import imageio_ffmpeg

from render import playout

T = json.load(open("timing.json"))
RATE, LEAD = T["rate"], T["lead_in"]


def read(path):
    with wave.open(path) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


plan = playout()
total = sum(a for *_, a in plan)
bed = np.zeros(int(round(total * RATE)), dtype=np.int16)

cursor = 0.0
for i, (name, _fn, _design, actual) in enumerate(plan):
    take = read(f"audio/{i:02d}.wav")
    start = int(round((cursor + LEAD) * RATE))
    end = min(start + len(take), len(bed))
    bed[start:end] = take[:end - start]
    print(f"  {name:16s} at {cursor + LEAD:7.2f}s  take {len(take)/RATE:6.2f}s  "
          f"scene {actual:6.2f}s")
    cursor += actual

with wave.open("narration.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
    w.writeframes(bed.tobytes())
print(f"narration.wav  {len(bed)/RATE:.1f}s")

ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, "-y", "-loglevel", "error",
                "-i", "EMI_Faraday_Lenz_silent.mp4", "-i", "narration.wav",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-ac", "2", "-ar", "44100", "-shortest",
                "EMI_Faraday_Lenz.mp4"], check=True)
print("muxed -> EMI_Faraday_Lenz.mp4")
