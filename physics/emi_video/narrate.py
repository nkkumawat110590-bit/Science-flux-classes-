"""Synthesise the scene narration and report how long each take runs.

Voice: espeak-ng driving an MBROLA diphone voice. The neural options were not
reachable from this environment (huggingface.co and translate.google.com are
both refused by the egress policy), so this is the best offline voice available.
Text is written for the ear: symbols are spelled out, because the synthesiser
reads "phi" and "epsilon" but not the glyphs.
"""
import json
import subprocess
import wave
from pathlib import Path

VOICE = "mb-us2"
SPEED = 145          # words per minute
PITCH = 46
GAP = 4              # 10 ms units between words

OUT = Path("audio")
LEAD_IN = 0.6        # silence before the take starts
TAIL = 0.9           # silence after it ends

NARRATION = [
    ("Title",
     "Electromagnetic induction. Faraday's law, Lenz's law, "
     "and the machines they run."),
    ("Magnetic Flux",
     "Everything starts with magnetic flux: B, times A, times cosine theta. "
     "Theta is the angle between the field and the area vector, the normal to the loop, "
     "never the plane. Turn the normal along B and the flux is maximum. "
     "Turn it ninety degrees and the flux falls to zero."),
    ("Faraday's Law",
     "Faraday's law. The E M F equals minus N, d phi by d t. "
     "Push the magnet in: the flux climbs, and the needle kicks. "
     "Stop it inside the coil, and the flux is large but no longer changing, "
     "so the needle drops to zero. "
     "Pull it out and the E M F flips sign. Move it faster and the deflection grows. "
     "The E M F curve is just the negative slope of the flux curve."),
    ("Lenz's Law",
     "So what is that minus sign doing there? That is Lenz's law. "
     "The induced current always opposes the change that produced it. "
     "Bring a north pole in: the coil's near face becomes north, and pushes back. "
     "Pull it away: that face turns south, and pulls it back. "
     "If the coil helped you, you would get free energy. "
     "Lenz's law is conservation of energy."),
    ("AC Generator",
     "Spin a coil in a magnetic field. The flux varies as cosine omega t, "
     "so the E M F is N B A omega, sine omega t. The peak is N B A omega. "
     "Notice the timing: the E M F is zero when the flux is largest, "
     "and maximum when the flux is zero. "
     "Slip rings carry it out, and that is every power station."),
    ("Eddy Currents",
     "Drop the same magnet down two pipes. Through plastic it falls. "
     "Through copper it crawls. The moving magnet drives closed loops of current "
     "in the copper wall, and by Lenz's law they oppose the motion. "
     "That is induction cooking, and the brakes on a train."),
    ("Transformer",
     "Mutual induction. Alternating current in the primary makes an alternating flux "
     "in the core, which induces an E M F in the secondary. "
     "The voltages follow the turns ratio, and the currents go the other way. "
     "A transformer changes voltage, never power. "
     "And on steady D C, nothing happens at all."),
    ("Motional EMF",
     "Slide a conducting rod along rails, in a field into the page. "
     "The enclosed area grows, the flux is B l x, so the E M F is B l v. "
     "Current flows up the rod, and that current, sitting in the same field, "
     "pushes the rod backwards. You must keep pushing, "
     "and that work becomes heat in the resistor."),
    ("Solved Example",
     "Two hundred turns, radius five centimetres, and a field falling "
     "from zero point six, to zero point two tesla, in a tenth of a second. "
     "The area is pi r squared: seven point eight five, times ten to the minus three. "
     "The rate is four tesla per second. So the E M F is six point two eight volts, "
     "and the current is one point five seven amperes."),
    ("Formula Sheet",
     "Everything in one frame. Flux, Faraday, induced charge, motional E M F, "
     "the rotating coil and the rotating rod, self and mutual induction. "
     "Learn the sign, the rate, and the opposition."),
]


def synth(text, path):
    subprocess.run(
        ["espeak-ng", "-v", VOICE, "-s", str(SPEED), "-p", str(PITCH),
         "-g", str(GAP), "-w", str(path), text],
        check=True, capture_output=True)
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate(), w.getframerate()


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    timing, rates = {}, set()
    for i, (name, text) in enumerate(NARRATION):
        p = OUT / f"{i:02d}.wav"
        dur, rate = synth(text, p)
        rates.add(rate)
        timing[name] = {"audio": round(dur, 2),
                        "scene": round(LEAD_IN + dur + TAIL, 2),
                        "words": len(text.split())}
        print(f"  {i:02d} {name:16s} {dur:6.2f}s audio -> {timing[name]['scene']:6.2f}s scene "
              f"({timing[name]['words']} words)")
    print("sample rates:", rates)
    json.dump({"lead_in": LEAD_IN, "tail": TAIL, "rate": rates.pop(), "scenes": timing},
              open("timing.json", "w"), indent=2)
    print("total narrated scene time:",
          round(sum(v["scene"] for v in timing.values()), 1), "s")
