"""Cut a short vertical video from motion clips with timed text.

Usage: python3 tools/cut.py content/<week>/<id>.cut.json
Spec:
{"out": "02.mp4", "music": 0.3,
 "segments": [
  {"clip": "flower-bloom", "ss": 0, "t": 10, "speed": 1.15, "layout": "full",
   "texts": [{"text": "Write a secret inside.", "from": 0, "to": 2.4, "y": 0.6, "size": 88}]},
  {"clip": "flower-bloom", "ss": 3, "t": 6, "speed": 1.0, "layout": "top", "color": 2,
   "title": "How to make it", "steps": [{"text": "Cut a flower from paper", "at": 0.3}, ...],
   "cta": {"text": "Free template in bio", "at": 4.5}}
 ]}
Clips are names in brand/clips (without .mp4). Times in "texts"/"steps" are seconds of OUTPUT time within the segment.
layout "full": clip fills the frame. layout "top": clip fills the top 50%, steps appear below on cream (top half).
Output: 1080x1920 mp4 next to the spec, plus <id>-cover.jpg.
"""
import json, os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from render import B, C, INK, e, font_css

W, H = 1080, 1920
TOP = int(H * 0.5)

def pill(text, y, size):
    return (f'<div style="position:absolute;left:50px;right:50px;top:{int(H*y)}px;text-align:center">'
            f'<span class="f" style="display:inline;font-size:{size}px;font-weight:700;line-height:1.38;color:#fff;'
            f'background:rgba(43,42,76,.82);padding:10px 26px;border-radius:22px;box-decoration-break:clone;-webkit-box-decoration-break:clone">{e(text)}</span></div>')

def step_html(i, text, col):
    y = TOP + 160 + i * 122
    return (f'<div style="position:absolute;left:64px;right:50px;top:{y}px;display:flex;gap:24px;align-items:center;color:{INK}">'
            f'<div class="f" style="flex:none;width:84px;height:84px;border-radius:50%;background:{col};color:#fff;font-size:48px;font-weight:700;display:flex;align-items:center;justify-content:center">{i+1}</div>'
            f'<div class="n" style="font-size:56px;font-weight:800;line-height:1.15">{e(text)}</div></div>')

def png(pg, body, path):
    doc = f'<html><head><meta charset="utf-8"><style>{font_css()}\n.f{{font-family:Fredoka}}.n{{font-family:Nunito}}html,body{{margin:0;background:transparent}}</style></head><body><div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">{body}</div></body></html>'
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(doc); tmp = f.name
    pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
    pg.screenshot(path=path, omit_background=True); os.unlink(tmp)

def build_segment(pg, seg, idx, tmpd):
    clip = os.path.join(B, "clips", seg["clip"] + ".mp4")
    sp = seg.get("speed", 1.0); dur = seg["t"] / sp
    col = C.get(seg.get("color", 1), C[1])
    overlays = []  # (png, from, to)
    if seg.get("layout", "full") == "full":
        for j, t in enumerate(seg.get("texts", [])):
            p = os.path.join(tmpd, f"s{idx}t{j}.png"); png(pg, pill(t["text"], t.get("y", 0.6), t.get("size", 84)), p)
            overlays.append((p, t["from"], t["to"]))
        base = f"[0:v]trim={seg['ss']}:{seg['ss']+seg['t']},setpts=(PTS-STARTPTS)/{sp},scale={W}:{H}:flags=lanczos,setsar=1,fps=30[b0]"
    else:
        p = os.path.join(tmpd, f"s{idx}title.png")
        png(pg, f'<div class="f" style="position:absolute;left:64px;top:{TOP+40}px;font-size:80px;font-weight:700;color:{col}">{e(seg.get("title",""))}</div>', p)
        overlays.append((p, 0, dur))
        for j, s in enumerate(seg.get("steps", [])):
            p = os.path.join(tmpd, f"s{idx}st{j}.png"); png(pg, step_html(j, s["text"], col), p)
            overlays.append((p, s["at"], dur))
        if seg.get("cta"):
            p = os.path.join(tmpd, f"s{idx}cta.png")
            png(pg, f'<div style="position:absolute;left:0;right:0;top:{TOP-150}px;text-align:center"><span class="f" style="background:{col};color:#fff;font-size:64px;font-weight:700;padding:20px 48px;border-radius:70px;box-shadow:0 8px 26px rgba(0,0,0,.3)">{e(seg["cta"]["text"])}</span></div>', p)
            overlays.append((p, seg["cta"]["at"], dur))
        cy = seg.get("crop_y", 0.2)
        base = (f"color=c=0xFFF7EC:s={W}x{H}:r=30:d={dur:.3f}[bg];"
                f"[0:v]trim={seg['ss']}:{seg['ss']+seg['t']},setpts=(PTS-STARTPTS)/{sp},scale={W}:{H}:flags=lanczos,crop={W}:{TOP}:0:{int(H*cy)},setsar=1,fps=30[c];"
                f"[bg][c]overlay=0:0:shortest=1[b0]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", clip]
    fc = [base]; cur = "b0"
    for k, (p, a, b_) in enumerate(overlays):
        cmd += ["-i", p]
        fc.append(f"[{cur}][{k+1}:v]overlay=0:0:enable='between(t,{a},{b_})'[b{k+1}]"); cur = f"b{k+1}"
    at = f"[0:a]atrim={seg['ss']}:{seg['ss']+seg['t']},asetpts=PTS-STARTPTS,atempo={sp},volume={seg.get('clip_volume',0.8)}[a]"
    out = os.path.join(tmpd, f"seg{idx}.mp4")
    cmd += ["-filter_complex", ";".join(fc + [at]), "-map", f"[{cur}]", "-map", "[a]", "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "44100", "-ac", "2", out]
    subprocess.run(cmd, check=True)
    return out, dur

def main(spec_path):
    from playwright.sync_api import sync_playwright
    spec = json.load(open(spec_path)); d = os.path.dirname(os.path.abspath(spec_path)); tmpd = tempfile.mkdtemp()
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        segs = [build_segment(pg, s, i, tmpd) for i, s in enumerate(spec["segments"])]
        b.close()
    total = sum(x[1] for x in segs); n = len(segs)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for p, _ in segs: cmd += ["-i", p]
    cmd += ["-stream_loop", "-1", "-i", os.path.join(B, "audio", spec.get("bed", "bed2") + ".wav")]
    cat = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][ca]"
    mv = spec.get("music", 0.3)
    fc = f"{cat};[{n}:a]volume={mv},afade=t=out:st={total-1:.2f}:d=1[m];[ca][m]amix=inputs=2:duration=first:normalize=0[a]"
    out = os.path.join(d, spec["out"])
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    cover = out[:-4] + "-cover.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(spec.get("cover_at", 1.0)), "-i", out, "-frames:v", "1", "-q:v", "3", cover], check=True)
    print(out, f"{total:.1f}s")

if __name__ == "__main__":
    main(sys.argv[1])
