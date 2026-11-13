"""Generate the brand music bed (original, synthesized). Usage: python3 tools/music.py brand/audio/bed2.wav
Upbeat ukulele strum + glockenspiel melody + bass + claps/shaker, 116 bpm, C major, 8 bars (loops cleanly)."""
import numpy as np, sys, wave
SR = 44100; BPM = 116; BEAT = 60 / BPM; BARS = 8; N = int(SR * BEAT * 4 * BARS)
rng = np.random.default_rng(7)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def put(buf, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR) % N; n = len(sig); l = gain * (1 - max(pan, 0)); r = gain * (1 + min(pan, 0))
    idx = (i + np.arange(n)) % N
    np.add.at(buf[0], idx, sig * l); np.add.at(buf[1], idx, sig * r)
def pluck(m, dur=1.2, bright=0.5):  # Karplus-Strong nylon string
    f = hz(m); p = int(SR / f); n = int(SR * dur); x = rng.uniform(-1, 1, p)
    k = np.ones(3) / 3; x = np.convolve(x, k, 'same') * (1 - bright) + x * bright
    out = np.empty(n); bufk = x.copy(); j = 0
    for i in range(n):
        out[i] = bufk[j]; nx = bufk[(j + 1) % p]; bufk[j] = 0.996 * 0.5 * (bufk[j] + nx); j = (j + 1) % p
    return out * np.exp(-np.arange(n) / (SR * dur * 0.6))
def glock(m, dur=0.9):
    t = np.arange(int(SR * dur)) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.45*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*9) + 0.2*np.sin(2*np.pi*5.4*f*t)*np.exp(-t*16)
    return s * np.exp(-t * 5.5) * np.minimum(t * 400, 1)
def bass(m, dur):
    t = np.arange(int(SR * dur)) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t) + 0.12*np.sin(2*np.pi*3*f*t)
    return s * np.exp(-t * 3.2) * np.minimum(t * 200, 1)
def kick():
    t = np.arange(int(SR * 0.28)) / SR; f = 110 * np.exp(-t * 22) + 48
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t * 13)
def clap():
    n = int(SR * 0.16); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    x = np.convolve(x, np.r_[1, -0.92], 'same'); env = sum(np.exp(-np.maximum(t - d, 0) * 55) * (t >= d) for d in (0, 0.011, 0.023))
    return x * env * 0.35
def shaker(a=1.0):
    n = int(SR * 0.07); t = np.arange(n) / SR; x = np.diff(rng.normal(0, 1, n + 1))
    return x * np.exp(-t * 60) * 0.22 * a
buf = np.zeros((2, N))
CH = [(48, [60, 64, 67, 72]), (55, [59, 62, 67, 71]), (57, [60, 64, 69, 72]), (53, [60, 65, 69, 72])]  # C G Am F
MEL = [  # (beat offset in bar, midi) x 8 bars, a bouncy hook that resolves
 [(0,76),(0.5,79),(1,84),(2,79),(2.5,76),(3,79)], [(0,74),(0.5,79),(1,83),(2,79),(3,74),(3.5,76)],
 [(0,76),(0.5,81),(1,84),(2,81),(2.5,76),(3,72)], [(0,77),(1,81),(1.5,84),(2,81),(3,79),(3.5,77)],
 [(0,76),(0.5,79),(1,84),(1.5,88),(2,84),(3,79)], [(0,74),(0.5,79),(1,83),(1.5,86),(2,83),(3,79)],
 [(0,76),(0.5,81),(1,84),(2,88),(2.5,84),(3,81)], [(0,77),(0.5,81),(1,84),(1.5,83),(2,84),(3,79),(3.5,74)]]
STRUM = [(0, 1, 1.0), (1, 1, 0.8), (1.5, -1, 0.55), (2.5, -1, 0.6), (3, 1, 0.8), (3.5, -1, 0.5)]  # d d u u d u
for bar in range(BARS):
    root, notes = CH[bar % 4]; t0 = bar * 4 * BEAT
    for b, d, a in STRUM:
        order = notes if d > 0 else notes[::-1]
        for k, m in enumerate(order):
            put(buf, pluck(m, 0.9, 0.55), t0 + b * BEAT + k * 0.012, 0.16 * a, pan=-0.25)
    for b in (0, 2): put(buf, bass(root - 12, BEAT * 1.6), t0 + b * BEAT, 0.42)
    put(buf, bass(root - 5, BEAT * 0.8), t0 + 3.5 * BEAT, 0.3)
    for b in (0, 2): put(buf, kick(), t0 + b * BEAT, 0.5)
    for b in (1, 3): put(buf, clap(), t0 + b * BEAT, 0.5, pan=0.1)
    if bar % 4 == 3: put(buf, clap(), t0 + 3.5 * BEAT, 0.4, pan=-0.2)
    for e in range(8): put(buf, shaker(1.0 if e % 2 else 0.6), t0 + e * 0.5 * BEAT + (0.012 if e % 2 else 0), 1.0, pan=0.35)
    for b, m in MEL[bar]: put(buf, glock(m), t0 + b * BEAT, 0.2, pan=0.2)
# light stereo room: a few feedback-free early reflections (wraps, so the loop stays seamless)
wet = np.zeros_like(buf)
for d, g, sw in ((0.031, 0.22, 0), (0.047, 0.18, 1), (0.071, 0.13, 0), (0.113, 0.09, 1)):
    s = np.roll(buf, int(d * SR), axis=1) * g; wet += s[::-1] if sw else s
mix = buf + wet; mix = np.tanh(mix * 1.15); mix /= np.abs(mix).max() / 0.89
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print(sys.argv[1], round(N / SR, 2), 's')
