"""Favicon и баннеры превью (assets/img/og/*.jpg) в стиле сайта. Запуск после build.py, затем build.py ещё раз."""
import base64, hashlib, json, pathlib, html
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; A = ROOT / "assets"; OUT = A / "img" / "og"; OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
F = "".join(f'@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64(A/"fonts"/f)})}}' for n, w, f in [
    ("H", 800, "fira-sans-extra-condensed-cyrillic-800-normal.woff2"), ("HL", 800, "fira-sans-extra-condensed-latin-800-normal.woff2"),
    ("M", 500, "ibm-plex-mono-cyrillic-500-normal.woff2"), ("ML", 500, "ibm-plex-mono-latin-500-normal.woff2")])
def og_html(t):
    size = 150 if len(t) <= 14 else 118 if len(t) <= 24 else 92
    return f'''<html><head><style>{F}body{{margin:0}}.b{{width:1200px;height:630px;position:relative;background:#141414;color:#f1efe9;font-family:HL,H;overflow:hidden}}
.l{{position:absolute;left:64px;top:56px;display:flex;font-family:H,HL;font-size:40px;text-transform:uppercase}}.l b{{padding:8px 10px 6px 0}}.l i{{font-style:normal;background:#ff5a14;color:#111;padding:8px 10px 6px}}
h1{{position:absolute;left:64px;right:64px;bottom:150px;margin:0;font-family:H,HL;font-size:{size}px;line-height:.9;text-transform:uppercase}}
.s{{position:absolute;left:0;right:0;bottom:0;height:96px;background:#ff5a14;color:#111;font-family:M,ML;font-size:26px;letter-spacing:.06em;text-transform:uppercase;display:flex;align-items:center;padding:0 64px}}
</style></head><body><div class="b"><div class="l"><b>Эвакуатор</b><i>09</i></div><h1>{html.escape(t)}</h1><div class="s">Караганда · пригороды · межгород по Казахстану</div></div></body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 512, "height": 512})
    pg.set_content(f'<html><head><style>{F}</style></head><body style="margin:0"><div style="width:512px;height:512px;background:#ff5a14;display:flex;align-items:center;justify-content:center;font-family:HL,H;font-size:330px;color:#111;line-height:1;padding-top:20px">09</div></body></html>')
    pg.wait_for_timeout(200); pg.screenshot(path=str(A / "icon-512.png"))
    im = Image.open(A / "icon-512.png").convert("RGB")
    im.resize((192, 192), Image.LANCZOS).save(A / "icon-192.png"); im.resize((180, 180), Image.LANCZOS).save(A / "apple-touch-icon.png")
    im.resize((48, 48), Image.LANCZOS).save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    OG = json.loads((ROOT / "src" / "og_list.json").read_text()); man_p = OUT / "manifest.json"
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    pg2 = b.new_page(viewport={"width": 1200, "height": 630}); n = 0
    for url, (slug, title) in OG.items():
        key = hashlib.md5(("v4" + title).encode()).hexdigest()
        if man.get(slug) == key and (OUT / f"{slug}.jpg").exists(): continue
        pg2.set_content(og_html(title)); pg2.wait_for_timeout(120); pg2.screenshot(path=str(OUT / f"{slug}.jpg"), type="jpeg", quality=86); man[slug] = key; n += 1
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1)); b.close()
print("og rendered", n)
