"""Render Pinterest pins (1000x1500). Usage: python3 tools/pins.py pins/<batch>.json
Spec: {"pins":[{"id":"flower","photo":"p07","pos":"50% 50%","kicker":"FREE PRINTABLE","title":"...","sub":"...","color":2}]}"""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import C, INK, e, font_css, photo, logo
W, H = 1000, 1500
def html(p):
    col = C.get(p.get("color", 1), C[1]); ph = 930
    return f'''<div style="position:absolute;inset:0;background:#FFF7EC"></div>
<img src="{photo(p["photo"])}" style="position:absolute;left:0;top:0;width:100%;height:{ph}px;object-fit:cover;object-position:{p.get("pos","50% 50%")}">
<div class="f" style="position:absolute;left:50px;top:{ph-36}px;background:{col};color:#fff;font-size:34px;font-weight:700;letter-spacing:2px;padding:14px 30px;border-radius:40px">{e(p["kicker"])}</div>
<div style="position:absolute;left:50px;right:50px;top:{ph+70}px;color:{INK}">
<div class="f" style="font-size:{p.get("size",82)}px;font-weight:700;line-height:1.04">{e(p["title"])}</div>
<div class="n" style="font-size:38px;font-weight:700;color:#55547a;margin-top:20px;line-height:1.25">{e(p["sub"])}</div></div>
<img src="{logo()}" style="position:absolute;right:40px;bottom:36px;width:120px;height:120px;border-radius:50%">
<div class="n" style="position:absolute;left:50px;bottom:60px;font-size:30px;font-weight:800;color:{col}">Little WOW Lab · ages 5–10</div>'''
def main(path):
    from playwright.sync_api import sync_playwright
    spec = json.load(open(path)); d = os.path.dirname(os.path.abspath(path))
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for p in spec["pins"]:
            doc = f'<html><head><meta charset="utf-8"><style>{font_css()}\n.f{{font-family:Fredoka}}.n{{font-family:Nunito}}body{{margin:0}}</style></head><body><div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">{html(p)}</div></body></html>'
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f: f.write(doc); tmp = f.name
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(d, p["id"] + ".jpg"), type="jpeg", quality=90); os.unlink(tmp); print(p["id"])
        b.close()
if __name__ == "__main__": main(sys.argv[1])
