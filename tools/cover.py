"""Render a Reels/Shorts cover (1080x1920) in the style that wins in the kids-craft niche:
the finished craft + hands filling the frame, plain background, ONE short bold line inside the
center 1080x1080 square (so it survives the grid's 1:1 and 4:5 crops). No logo, no clutter.

Usage: python3 tools/cover.py <clip name in brand/clips> <seconds> "<3-5 word title>" <out.jpg> [y=0.30] [zoom=1.0] [cy=0.5 vertical crop position 0..1]
"""
import os, sys, subprocess, tempfile, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import B, font_css, e
W, H = 1080, 1920
def main(clip, t, title, out, y=0.30, zoom=1.0, cy=0.5):
    tmp = tempfile.mkdtemp(); frame = os.path.join(tmp, "f.jpg")
    vf = f"scale={int(W*zoom)}:{int(H*zoom)}:flags=lanczos,crop={W}:{H}:(iw-{W})/2:(ih-{H})*{cy},eq=saturation=1.18:contrast=1.06:brightness=0.02,unsharp=5:5:0.6"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", os.path.join(B, "clips", clip + ".mp4"),
                    "-frames:v", "1", "-vf", vf, "-q:v", "2", frame], check=True)
    img = "data:image/jpeg;base64," + base64.b64encode(open(frame, "rb").read()).decode()
    html = f'''<html><head><meta charset="utf-8"><style>{font_css()}
body{{margin:0}} .t{{font-family:Fredoka;font-weight:700;font-size:118px;line-height:1.02;color:#fff;text-align:center;
-webkit-text-stroke:10px #2B2A4C;paint-order:stroke fill;text-shadow:0 8px 0 #2B2A4C,0 14px 30px rgba(0,0,0,.35)}}</style></head>
<body><div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:url({img}) center/cover">
<div class="t" style="position:absolute;left:60px;right:60px;top:{int(H*y)}px">{e(title)}</div></div></body></html>'''
    from playwright.sync_api import sync_playwright
    p = os.path.join(tmp, "c.html"); open(p, "w").write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + p); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        pg.screenshot(path=out, type="jpeg", quality=92); b.close()
    print(out)
if __name__ == "__main__":
    a = sys.argv[1:]; main(a[0], float(a[1]), a[2], a[3], *(float(x) for x in a[4:]))
