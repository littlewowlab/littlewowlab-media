"""Render a week's content plan into carousel images and short videos.

Usage:  python3 tools/render.py content/<week>/plan.json

plan.json:
{
  "week": "2026-W47",
  "posts": [
    {"id": "01", "kind": "carousel", "slides": [SLIDE, ...]},
    {"id": "02", "kind": "video", "seconds_per_scene": 2.6, "scenes": [SLIDE, ...]}
  ]
}
SLIDE types:
  {"type": "hook",  "photo": "p01", "text": "Big headline", "sub": "small line"}
  {"type": "photo", "photo": "p07", "title": "Short title", "caption": "One line", "num": 1}
  {"type": "tip",   "title": "Heading", "lines": ["line", "line"], "color": 2}
  {"type": "cta",   "title": "Free 3-project sampler", "sub": "Link in bio", "photo": "p15"}
Photos are names in brand/photos (without .jpg). Colors 1-5 = chapter colors.
Outputs: content/<week>/<id>-<n>.jpg (1080x1350) or content/<week>/<id>.mp4 (1080x1920).
"""
import json, os, sys, base64, subprocess, tempfile, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "brand")
INK = "#2B2A4C"
C = {1: "#F2604E", 2: "#159F94", 3: "#E39A0B", 4: "#6E56F0", 5: "#2FA55C"}
TINT = {1: "#FDE7E3", 2: "#DDF3F1", 3: "#FDF1D6", 4: "#ECE8FE", 5: "#DFF3E6"}

def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def font_css():
    out = []
    for fam, ws in (("Fredoka", (500, 600, 700)), ("Nunito", (400, 600, 700, 800))):
        for w in ws:
            p = os.path.join(B, "fonts", f"{fam.lower()}-latin-{w}-normal.woff2")
            out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('{b64(p,'font/woff2')}') format('woff2');}}")
    return "\n".join(out)

def pos(sl):
    return sl.get("pos", "50% 50%")

def photo(name):
    return b64(os.path.join(B, "photos", name + ".jpg"), "image/jpeg")

LOGO = None
def logo():
    global LOGO
    if LOGO is None:
        LOGO = b64(os.path.join(B, "logo.png"), "image/png")
    return LOGO

e = lambda s: html.escape(str(s))

def slide_html(s, W, H, video=False):
    t = s["type"]; col = C.get(s.get("color", 1), C[1]); tint = TINT.get(s.get("color", 1), TINT[1])
    big = 1.0 if not video else 1.12
    badge = f'<img src="{logo()}" style="position:absolute;right:34px;top:34px;width:{int(118*big)}px;height:{int(118*big)}px;border-radius:50%;border:5px solid #fff;box-shadow:0 6px 18px rgba(0,0,0,.18)">'
    if t == "hook":
        ph = s.get("photo")
        bg = f'<img src="{photo(ph)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos(s)}">' if ph else f'<div style="position:absolute;inset:0;background:{tint}"></div>'
        return f'''{bg}<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(43,42,76,.05) 25%,rgba(43,42,76,.8) {"78%" if video else "100%"},rgba(43,42,76,.85) 100%)"></div>{badge}
<div style="position:absolute;left:60px;right:60px;bottom:{int(H*(0.27 if video else 0.09))}px;color:#fff">
<div class="f" style="font-size:{int(92*big)}px;font-weight:700;line-height:1.02;text-shadow:0 3px 14px rgba(0,0,0,.35)">{e(s["text"])}</div>
{f'<div class="n" style="font-size:{int(40*big)}px;font-weight:700;margin-top:22px;opacity:.95">{e(s["sub"])}</div>' if s.get("sub") else ""}</div>'''
    if t == "photo":
        ph_h = int(H * (0.66 if not video else 0.62))
        num = f'<div class="f" style="position:absolute;left:44px;top:{ph_h-58}px;width:116px;height:116px;border-radius:50%;background:{col};color:#fff;font-size:62px;font-weight:700;display:flex;align-items:center;justify-content:center;border:7px solid #fff">{e(s["num"])}</div>' if s.get("num") is not None else ""
        return f'''<div style="position:absolute;inset:0;background:#FFF7EC"></div>
<img src="{photo(s["photo"])}" style="position:absolute;left:0;top:0;width:100%;height:{ph_h}px;object-fit:cover;object-position:{pos(s)}">{badge}{num}
<div style="position:absolute;left:60px;right:60px;top:{ph_h+70}px;color:{INK}">
<div class="f" style="font-size:{int(70*big)}px;font-weight:700;line-height:1.05">{e(s["title"])}</div>
{f'<div class="n" style="font-size:{int(38*big)}px;font-weight:600;margin-top:18px;color:#55547a;line-height:1.3">{e(s["caption"])}</div>' if s.get("caption") else ""}</div>'''
    if t == "tip":
        fs, ts, top, circ = (64, 104, int(H*0.24), 92) if video else (int(42*big), int(78*big), int(H*0.16), 64)
        lines = "".join(f'<div style="display:flex;gap:26px;margin-top:{int(fs*1.1)}px;align-items:flex-start"><div class="f" style="flex:none;width:{circ}px;height:{circ}px;border-radius:50%;background:{col};color:#fff;font-size:{int(circ*.55)}px;font-weight:700;display:flex;align-items:center;justify-content:center">{i+1}</div><div class="n" style="font-size:{fs}px;font-weight:800;line-height:1.25;padding-top:{int(circ*.08)}px">{e(l)}</div></div>' for i, l in enumerate(s["lines"]))
        return f'''<div style="position:absolute;inset:0;background:{tint}"></div>{badge}
<div style="position:absolute;left:70px;right:70px;top:{top}px;color:{INK}">
<div class="f" style="font-size:{ts}px;font-weight:700;line-height:1.05;color:{col}">{e(s["title"])}</div>{lines}</div>'''
    if t == "cta":
        ph = s.get("photo", "p15")
        return f'''<div style="position:absolute;inset:0;background:#FFF7EC"></div>
<img src="{photo(ph)}" style="position:absolute;left:0;top:0;width:100%;height:{int(H*0.5)}px;object-fit:cover;object-position:{pos(s)}">
<img src="{logo()}" style="position:absolute;left:50%;top:{int(H*0.5)-120}px;transform:translateX(-50%);width:240px;height:240px;border-radius:50%;border:8px solid #fff;box-shadow:0 8px 24px rgba(0,0,0,.18)">
<div style="position:absolute;left:60px;right:60px;top:{int(H*0.5)+150}px;text-align:center;color:{INK}">
<div class="f" style="font-size:{int(76*big)}px;font-weight:700;line-height:1.05">{e(s["title"])}</div>
<div class="f" style="display:inline-block;margin-top:30px;background:{col};color:#fff;font-size:{int(44*big)}px;font-weight:600;padding:16px 44px;border-radius:60px">{e(s.get("sub","Link in bio"))}</div></div>'''
    raise ValueError(t)

def render_slides(slides, W, H, out_paths, video=False):
    from playwright.sync_api import sync_playwright
    css = font_css() + "\n.f{font-family:Fredoka}.n{font-family:Nunito}body{margin:0}"
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for s, out in zip(slides, out_paths):
            doc = f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">{slide_html(s, W, H, video)}</div></body></html>'
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
                f.write(doc); tmp = f.name
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            pg.screenshot(path=out, type="jpeg", quality=90); os.unlink(tmp)
        b.close()

def make_video(stills, out, sec):
    fps = 30; n = int(sec * fps); fade = 0.4
    inputs, filters = [], []
    for i, p in enumerate(stills):
        inputs += ["-loop", "1", "-t", str(sec), "-i", p]
        filters.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0009,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={fps},setsar=1,format=yuv420p[v{i}]")
    chain = "[v0]"; off = sec - fade
    for i in range(1, len(stills)):
        filters.append(f"{chain}[v{i}]xfade=transition=fade:duration={fade}:offset={off:.2f}[x{i}]")
        chain = f"[x{i}]"; off += sec - fade
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-stream_loop", "-1", "-i", os.path.join(B, "audio", "bed.wav"),
           "-filter_complex", ";".join(filters) + f";[{len(stills)}:a]volume=0.55,afade=t=out:st={off+fade-1.0:.2f}:d=1[a]", "-map", chain, "-map", "[a]", "-t", f"{off+fade:.2f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)

def main(plan_path):
    plan = json.load(open(plan_path)); d = os.path.dirname(os.path.abspath(plan_path))
    for p in plan["posts"]:
        if p["kind"] == "carousel":
            outs = [os.path.join(d, f'{p["id"]}-{i+1}.jpg') for i in range(len(p["slides"]))]
            render_slides(p["slides"], 1080, 1350, outs)
            print(p["id"], "carousel", len(outs))
        elif p["kind"] == "video":
            tmpd = tempfile.mkdtemp()
            stills = [os.path.join(tmpd, f"s{i}.jpg") for i in range(len(p["scenes"]))]
            render_slides(p["scenes"], 1080, 1920, stills, video=True)
            out = os.path.join(d, f'{p["id"]}.mp4')
            make_video(stills, out, p.get("seconds_per_scene", 2.6))
            render_slides([p["scenes"][0]], 1080, 1920, [os.path.join(d, f'{p["id"]}-cover.jpg')], video=True)
            print(p["id"], "video", out)

if __name__ == "__main__":
    main(sys.argv[1])
