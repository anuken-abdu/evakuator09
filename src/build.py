# -*- coding: utf-8 -*-
"""Генератор сайта эвакуатора: python3 src/build.py → dist/"""
import html, json, pathlib, shutil, datetime
from data import *

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VER = "2610242350"
TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)
WA_URL = lambda t=WA_TEXT: f"https://wa.me/{WA}?text=" + __import__("urllib.parse").parse.quote(t)

P = {
    "car": '<path d="M3 15v-3l2-5h14l2 5v3"/><path d="M3 15h18v2H3z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/><path d="M6 12h12"/>',
    "suv": '<path d="M2.5 15v-4l1.5-4h13l3 4h1.5v4"/><path d="M2.5 15h19v2h-19z"/><circle cx="7" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/><path d="M10 7v4M2.5 11h19"/>',
    "crash": '<path d="M3 16v-3l2-4h7l2 4"/><path d="M3 16h11"/><circle cx="6.5" cy="17" r="1.6"/><path d="M17 4l1 3 3-1-2 3 3 2-3 .5.5 3-2.5-2"/>',
    "engine": '<path d="M4 10h3l1-2h6l1 2h2v2h2v4h-2v2h-3l-1 1H8l-1-1H4z"/><path d="M11 11l-1 3h2l-1 3"/>',
    "route": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "wa": '<path d="M20.5 11.7a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.4-4.3a8.5 8.5 0 1 1 15.6-4.5z"/><path d="M8.8 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .5.4l.7 1.6c0 .2 0 .4-.1.5l-.5.6c-.1.2-.1.3 0 .5.5.9 1.3 1.7 2.3 2.2.2.1.3.1.5-.1l.6-.7c.1-.2.3-.2.5-.1l1.6.8c.2.1.3.2.3.3 0 .7-.4 1.4-1 1.6-.7.3-1.6.3-3.4-.6a8.8 8.8 0 0 1-3.2-3.1c-.7-1.2-.8-2.2-.1-3.6z"/>',
    "pin": '<path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
}
def ic(n, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{P[n]}</g></svg>'

HOOK = '<svg class="logo-m" viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" fill="#ff5a14"/><text x="24" y="34" text-anchor="middle" font-family="Fira Sans Extra Condensed,Arial Narrow,sans-serif" font-weight="800" font-size="30" fill="#111">09</text></svg>'
def logo(): return f'<a class="logo" href="/" aria-label="{BRAND} — на главную"><b>Эвакуатор</b><i>09</i></a>'
def bg(key): return f' style="--ph:url(/{PHOTOS[key]}?v={VER})"'

NAV = [("/uslugi/", "Услуги"), ("/mezhgorod/", "Межгород"), ("/temirtau/", "Темиртау"), ("/voprosy/", "Вопросы"), ("/kontakty/", "Контакты")]

def cta(cls="", call_label=None):
    return f'''<div class="cta-b {cls}"><a class="btn btn-a" href="tel:{TEL}" data-ev="call" aria-label="Позвонить {PHONE_LOCAL}">{ic("phone")}<span>{call_label or PHONE_LOCAL}</span></a><a class="btn btn-w" href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">{ic("wa")}<span>WhatsApp</span></a></div>'''
def bigtel(small="Звоните диспетчеру"):
    return f'''<div class="tel-b"><a class="bigtel" href="tel:{TEL}" data-ev="call"><small>{small}</small><span>{PHONE_LOCAL}</span></a>
<a class="walink" href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">{ic("wa")}<span>Написать в WhatsApp — можно отправить геолокацию</span>{ic("arrow")}</a></div>'''

def header(cur):
    items = "".join(f'<li><a href="{h}"{" aria-current=page" if h == cur else ""}>{n}</a></li>' for h, n in NAV)
    return f'''<a class="skip" href="#main">Перейти к содержанию</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}
<nav class="nav" id="nav" aria-label="Основное меню"><ul>{items}</ul></nav>
<a class="hdr-ph" href="tel:{TEL}" data-ev="call">{PHONE_LOCAL}</a>
<button class="burger" type="button" aria-label="Меню" aria-controls="nav" aria-expanded="false">{ic("menu", "i i-o")}{ic("close", "i i-c")}</button></div></header>'''

def footer():
    svc = "".join(f'<li><a href="/uslugi/{s["slug"]}/">{s["short"]}</a></li>' for s in SERVICES)
    rts = "".join(f'<li><a href="/mezhgorod/{r[0]}/">Караганда — {r[1]}</a></li>' for r in ROUTES)
    pages = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in NAV)
    return f'''<footer class="ftr"><div class="wrap">
<div class="ftr-top"><a class="ftr-tel" href="tel:{TEL}" data-ev="call">{PHONE_LOCAL}</a><p>{HOURS}. Караганда, Темиртау, Карагандинская область, межгород по Казахстану.</p></div>
<div class="ftr-g"><div class="f-col"><h4>Услуги</h4><ul>{svc}<li><a href="/mezhgorod/">Межгород</a></li></ul></div>
<div class="f-col"><h4>Межгород</h4><ul>{rts}</ul></div>
<div class="f-col"><h4>Сайт</h4><ul>{pages}<li><a href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">WhatsApp</a></li></ul></div></div>
<div class="ftr-b">{logo()}<span>© {datetime.date.today().year} {BRAND}</span><a href="/politika/">Политика конфиденциальности</a><a href="{DEV_URL}" target="_blank" rel="noopener">Разработка сайта — {DEV_NAME}</a></div></div></footer>
<div class="mbar">{cta(call_label="Позвонить")}</div>'''

ORG = {"@context": "https://schema.org", "@type": "AutomotiveBusiness", "@id": SITE + "/#org", "name": BRAND,
       "url": SITE + "/", "telephone": PHONE, "image": SITE + "/assets/img/og/home.jpg", "logo": SITE + "/icon-512.png",
       "description": LEAD, "priceRange": "по запросу",
       "address": {"@type": "PostalAddress", "addressLocality": "Караганда", "addressRegion": "Карагандинская область", "addressCountry": "KZ"},
       "areaServed": [{"@type": "City", "name": "Караганда"}, {"@type": "City", "name": "Темиртау"}, {"@type": "Country", "name": "Казахстан"}],
       "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "contactType": "customer service", "availableLanguage": ["ru", "kk"]},
       "sameAs": [f"https://wa.me/{WA}"]}
if WORK_24:
    ORG["openingHoursSpecification"] = {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}

def ld_crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (h, n) in enumerate(items)]}
def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def ld_svc(name, desc, url, area=None):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "serviceType": "Эвакуация автомобилей",
            "provider": {"@id": SITE + "/#org"}, "url": SITE + url, "areaServed": area or [{"@type": "City", "name": "Караганда"}, {"@type": "Country", "name": "Казахстан"}]}

OG = {}   # url → (файл, заголовок)
def page(url, title, desc, body, cur="", ld=(), crumbs=None, og=None, og_title=None):
    og = og or ("home" if url == "/" else url.strip("/").replace("/", "-"))
    if url != "/404/": OG[url] = (og, og_title or title.split(" — ")[0].split(" | ")[0])
    lds = [ORG] + list(ld)
    if crumbs: lds.append(ld_crumbs([("/", "Главная")] + crumbs))
    if url == "/": lds.append({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE + "/", "inLanguage": "ru"})
    tag_id = GA_ID or GADS_ID
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={tag_id}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());'
          + "".join(f'gtag("config","{x}");' for x in (GA_ID, GADS_ID) if x) + "</script>") if tag_id else ""
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li>' + "".join(
            f'<li><a href="{h}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>' for i, (h, n) in enumerate(crumbs)) + "</ol></nav>"
    body = body.replace("<!--CRUMBS-->", cr)
    cfg = json.dumps({"ads": [GADS_ID, GADS_CALL_LABEL, GADS_WA_LABEL]})
    full = SITE + url
    return f'''<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{ga}
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{full}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#111111"><meta name="geo.region" content="KZ-KAR"><meta name="geo.placename" content="Караганда">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{full}">
<meta property="og:image" content="{SITE}/assets/img/og/{og}.jpg?v={VER}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/fira-sans-extra-condensed-cyrillic-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/fira-sans-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}
</head><body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
<script>window.EV={cfg};</script><script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''

def write(url, content):
    p = DIST / "404.html" if url == "/404/" else (DIST / url.strip("/") / "index.html" if url != "/" else DIST / "index.html")
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")

# ---------- блоки ----------
def blk(title, inner, sub="", dark=False, link=None):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ic("arrow")}</a>' if link else ""
    return f'''<section class="blk{" blk-d" if dark else ""}"><div class="wrap blk-in"><div class="blk-l"><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}{lk}</div><div class="blk-r">{inner}</div></div></section>'''
def svc_rows(exclude=None):
    li = "".join(f'<li><a href="/uslugi/{s["slug"]}/"><span class="rw-t">{s["short"]}</span><span class="rw-d">{s["text"]}</span>{ic("arrow", "i rw-a")}</a></li>' for s in SERVICES if s["slug"] != exclude)
    li += f'<li><a href="/mezhgorod/"><span class="rw-t">Межгород</span><span class="rw-d">Из Караганды в любой город Казахстана и обратно.</span>{ic("arrow", "i rw-a")}</a></li>'
    return f'<ul class="rows">{li}</ul>'
def board(exclude=None):
    rows = "".join(f'<li><a href="/mezhgorod/{r[0]}/"><span class="bd-f">Караганда</span><span class="bd-x">→</span><span class="bd-t">{r[1]}</span><span class="bd-s">и обратно</span></a></li>' for r in ROUTES if r[0] != exclude)
    return f'<div class="board"><div class="bd-h"><span>Откуда</span><span></span><span>Куда</span><span></span></div><ul>{rows}</ul></div>'
def steps():
    return '<ol class="st">' + "".join(f'<li><span class="st-n">{i+1}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(STEPS)) + "</ol>"
def call_info():
    return '<dl class="sheet">' + "".join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in CALL_INFO) + "</dl>"
def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{q}{ic("chev")}</summary><p>{a}</p></details>' for q, a in faq) + "</div>"
def ck(items):
    return '<ul class="lst">' + "".join(f'<li>{x}</li>' for x in items) + "</ul>"
def area_sec():
    d = '<span class="sl">/</span>'.join(f"<span>{x}</span>" for x in DISTRICTS)
    s = '<span class="sl">/</span>'.join(f'<a href="/temirtau/">{x}</a>' if x == "Темиртау" else f"<span>{x}</span>" for x in SUBURBS)
    return blk("Где работаем", f'<p class="ar">{d}</p><p class="ar ar-2">{s}</p>', "Вся Караганда, пригороды и трассы Карагандинской области. Межгород — по всему Казахстану.")
def call_band(title="Нужен эвакуатор?", sub="Звоните или пишите — уточним детали и назовём стоимость до выезда."):
    return f'''<section class="band"><div class="wrap band-in"><div class="band-t"><h2>{title}</h2><p>{sub}</p></div>{bigtel("Позвонить")}</div></section>'''
def ph(h1, lead, photo="uslugi"):
    return f'''<section class="ph"{bg(photo)}><div class="wrap ph-in"><!--CRUMBS--><h1>{h1}</h1><p>{lead}</p>{cta()}</div></section>'''

# ---------- страницы ----------
def build_home():
    body = f"""<section class="hero"{bg("hero")}><div class="wrap hero-in">
<h1>Эвакуатор<br>в Караганде</h1>
<p class="hero-s">По городу, пригородам и межгород по всему Казахстану. Легковые автомобили, кроссоверы и внедорожники — на платформе{", круглосуточно" if WORK_24 else ""}.</p>
{bigtel()}</div></section>
{blk("Что перевозим", svc_rows(), "Автомобиль едет на платформе, а не на тросе.")}
<section class="blk blk-d"><div class="wrap"><div class="bd-top"><h2>Межгород из Караганды</h2><a class="lnk" href="/mezhgorod/">Все направления {ic("arrow")}</a></div>{board()}
<p class="bd-more">А также {", ".join(OTHER_CITIES)} и другие города Казахстана.</p></div></section>
{blk("Как вызвать", steps(), "Три шага от звонка до доставки.")}
{blk("Что сказать при звонке", call_info(), "Так мы быстрее найдём машину и точнее назовём стоимость.")}
{area_sec()}
{blk("Вопросы", faq_html(FAQ[:6]), "", link=("Все вопросы", "/voprosy/"))}
{call_band()}"""
    write("/", page("/", f"Эвакуатор Караганда — вызов эвакуатора по городу и межгород{', круглосуточно' if WORK_24 else ''}",
                    f"Эвакуатор в Караганде: по городу, пригородам и межгород по всему Казахстану. Легковые, кроссоверы, внедорожники, после ДТП. {('Круглосуточно. ' if WORK_24 else '')}Тел. {PHONE_LOCAL}.",
                    body, "/", [ld_faq(FAQ[:6])], og_title="Эвакуатор в Караганде"))

def build_services():
    body = f"""{ph("Услуги эвакуатора в Караганде", "Перевозим автомобили на платформе по Караганде, области и всему Казахстану.")}
{blk("Что перевозим", svc_rows())}{blk("Как вызвать", steps())}{blk("Что сказать при звонке", call_info())}{call_band()}"""
    write("/uslugi/", page("/uslugi/", f"Услуги эвакуатора в Караганде — {BRAND}", "Эвакуация легковых автомобилей, кроссоверов и внедорожников, после ДТП и при поломке, межгород по Казахстану. Караганда и область.", body, "/uslugi/", crumbs=[("/uslugi/", "Услуги")]))
    for s in SERVICES:
        url = f'/uslugi/{s["slug"]}/'
        body = f"""{ph(s["name"], s["text"])}
{blk("Что входит", ck(s["points"]))}{blk("Что сказать при звонке", call_info())}{blk("Как вызвать", steps())}
{blk("Вопросы", faq_html(s["faq"] + FAQ[1:3]))}{blk("Другие услуги", svc_rows(exclude=s["slug"]))}{call_band()}"""
        write(url, page(url, f'{s["name"]} — {BRAND}', f'{s["text"]} Тел. {PHONE_LOCAL}.', body, "/uslugi/",
                        [ld_svc(s["name"], s["text"], url), ld_faq(s["faq"] + FAQ[1:3])], crumbs=[("/uslugi/", "Услуги"), (url, s["short"])], og_title=s["short"]))

def build_routes():
    rfaq = [("Как рассчитывается стоимость межгорода?", "Зависит от расстояния, типа автомобиля и его состояния. Назовите маршрут и марку машины — посчитаем стоимость до выезда."),
            ("Можно заказать перевозку заранее?", "Да. Согласуем дату и время погрузки и адрес доставки."),
            ("Перевозите в обратную сторону?", "Да, забираем автомобили из других городов и везём в Караганду.")]
    body = f"""{ph("Эвакуатор межгород из Караганды", "Перевозим автомобили на платформе из Караганды в любой город Казахстана и обратно.", "mezhgorod")}
<section class="blk blk-d"><div class="wrap"><div class="bd-top"><h2>Направления</h2></div>{board()}<p class="bd-more">А также {", ".join(OTHER_CITIES)} и другие города Казахстана.</p></div></section>
{blk("Как проходит перевозка", ck(["Согласуем маршрут, дату и время погрузки", "Грузим автомобиль на платформу и фиксируем ремнями", "Везём по трассе до города назначения", "Передаём автомобиль по адресу: дом, сервис или стоянка"]))}
{blk("Что сказать при звонке", call_info())}{blk("Вопросы о межгороде", faq_html(rfaq))}{call_band("Нужна перевозка в другой город?")}"""
    write("/mezhgorod/", page("/mezhgorod/", f"Эвакуатор межгород из Караганды по Казахстану — {BRAND}", "Перевозка автомобилей на эвакуаторе из Караганды в Астану, Алматы, Балхаш, Жезказган, Павлодар, Шымкент и другие города Казахстана.", body, "/mezhgorod/",
                              [ld_svc("Эвакуатор межгород из Караганды", "Перевозка автомобилей на эвакуаторе-платформе из Караганды по Казахстану.", "/mezhgorod/"), ld_faq(rfaq)], crumbs=[("/mezhgorod/", "Межгород")], og_title="Межгород из Караганды"))
    for slug, city, to, frm in ROUTES:
        url = f"/mezhgorod/{slug}/"
        h1 = f"Эвакуатор Караганда — {city}"
        lead = f"Перевозим автомобили на эвакуаторе-платформе из Караганды {to} и {frm} в Караганду."
        fq = [(f"Сколько стоит эвакуатор из Караганды {to}?", f"Стоимость зависит от типа автомобиля и его состояния. Позвоните или напишите в WhatsApp: «Караганда — {city}», марка автомобиля — назовём сумму до выезда."),
              (f"Можно перевезти машину {frm} в Караганду?", f"Да, забираем автомобили {frm} и доставляем в Караганду."),
              ("Можно заказать перевозку заранее?", "Да. Согласуем дату и время погрузки и адрес доставки.")]
        body = f"""{ph(h1, lead, "mezhgorod")}
{blk(f"Караганда — {city}", ck([f"Погрузка в Караганде по вашему адресу", f"Доставка {to}: до двери, сервиса или стоянки", f"Обратное направление: {frm} в Караганду", "Легковые автомобили, кроссоверы и внедорожники", "Автомобиль на ходу, после ДТП или с поломкой"]))}
{blk("Что сказать при звонке", call_info())}{blk("Вопросы", faq_html(fq))}
<section class="blk blk-d"><div class="wrap"><div class="bd-top"><h2>Другие направления</h2><a class="lnk" href="/mezhgorod/">Весь межгород {ic("arrow")}</a></div>{board(exclude=slug)}</div></section>{call_band(f"Нужен эвакуатор {to}?")}"""
        write(url, page(url, f"{h1}: перевозка авто на эвакуаторе", f"{lead} Легковые, кроссоверы, внедорожники. Тел. {PHONE_LOCAL}.", body, "/mezhgorod/",
                        [ld_svc(h1, lead, url, [{"@type": "City", "name": "Караганда"}, {"@type": "City", "name": city}]), ld_faq(fq)], crumbs=[("/mezhgorod/", "Межгород"), (url, f"Караганда — {city}")], og_title=f"Караганда — {city}"))

def build_misc():
    tfaq = [("Вы выезжаете в Темиртау?", "Да, выезжаем из Караганды в Темиртау и перевозим автомобили по Темиртау, в Караганду и в другие города."),
            ("Можно отвезти машину из Темиртау в Караганду?", "Да, доставим автомобиль в Караганду: в сервис, на стоянку или по вашему адресу.")] + FAQ[1:3]
    body = f"""{ph("Эвакуатор в Темиртау", "Выезжаем из Караганды в Темиртау: перевозим автомобили по городу, в Караганду и в другие города Казахстана.")}
{blk("Что делаем в Темиртау", ck(["Эвакуация легковых автомобилей, кроссоверов и внедорожников", "Эвакуация после ДТП и при поломке", "Перевозка Темиртау — Караганда и обратно", "Межгород из Темиртау по Казахстану"]))}
{blk("Что сказать при звонке", call_info())}{blk("Вопросы", faq_html(tfaq))}{call_band("Нужен эвакуатор в Темиртау?")}"""
    write("/temirtau/", page("/temirtau/", f"Эвакуатор Темиртау — вызов эвакуатора, перевозка в Караганду | {BRAND}", f"Эвакуатор в Темиртау: по городу, в Караганду и межгород. Легковые, кроссоверы, внедорожники, после ДТП. Тел. {PHONE_LOCAL}.", body, "/temirtau/",
                             [ld_svc("Эвакуатор в Темиртау", "Эвакуация автомобилей в Темиртау и перевозка в Караганду.", "/temirtau/", [{"@type": "City", "name": "Темиртау"}]), ld_faq(tfaq)], crumbs=[("/temirtau/", "Темиртау")], og_title="Эвакуатор в Темиртау"))
    body = f"""{ph("Вопросы об эвакуаторе", "Как вызвать эвакуатор в Караганде, от чего зависит стоимость и что сказать при звонке.")}
{blk("Частые вопросы", faq_html(FAQ))}{blk("Что сказать при звонке", call_info())}{call_band()}"""
    write("/voprosy/", page("/voprosy/", f"Вопросы об эвакуаторе в Караганде — {BRAND}", "Ответы на частые вопросы: как вызвать эвакуатор в Караганде, стоимость, межгород, работа ночью, вызов на трассу.", body, "/voprosy/", [ld_faq(FAQ)], crumbs=[("/voprosy/", "Вопросы")], og_title="Вопросы об эвакуаторе"))
    ct = f"""<dl class="sheet sheet-c"><div><dt>Телефон</dt><dd><a href="tel:{TEL}" data-ev="call">{PHONE_LOCAL}</a></dd></div>
<div><dt>WhatsApp</dt><dd><a href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">{PHONE_LOCAL}</a></dd></div>
<div><dt>Режим работы</dt><dd>{HOURS}</dd></div><div><dt>Где работаем</dt><dd>Караганда, Темиртау, Карагандинская область; межгород — по всему Казахстану</dd></div></dl>"""
    body = f"""{ph("Контакты", "Звоните или пишите в WhatsApp. Можно сразу отправить геолокацию автомобиля.")}
{blk("Связь", ct)}{blk("Что сказать при звонке", call_info())}{call_band()}"""
    write("/kontakty/", page("/kontakty/", f"Контакты эвакуатора в Караганде — {PHONE_LOCAL}", f"Эвакуатор в Караганде: {PHONE_LOCAL}, WhatsApp. {HOURS}. Караганда, Темиртау, межгород по Казахстану.", body, "/kontakty/", crumbs=[("/kontakty/", "Контакты")], og_title="Контакты"))
    S = [("Какие данные мы получаем", "Сайт не собирает персональные данные через формы. Если вы звоните или пишете в WhatsApp, мы видим номер телефона и сообщения, которые вы отправляете, в том числе геолокацию, если вы её передаёте."),
         ("Зачем", "Чтобы связаться с вами, уточнить детали перевозки и выполнить заказ."),
         ("Аналитика", "Сайт может использовать сервисы веб-аналитики Google, которые собирают обезличенные данные о посещениях и нажатиях. Их можно ограничить в настройках браузера."),
         ("Передача третьим лицам", "Мы не передаём ваши данные третьим лицам, кроме случаев, предусмотренных законодательством Республики Казахстан."),
         ("Обращения", f"По вопросам обработки данных звоните или пишите: {PHONE_LOCAL}.")]
    body = f"""<section class="ph ph-s"><div class="wrap ph-in"><!--CRUMBS--><h1>Политика конфиденциальности</h1><p>Как сайт {DOMAIN} обрабатывает данные посетителей.</p></div></section>
<section class="blk"><div class="wrap prose">{"".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in S)}</div></section>"""
    write("/politika/", page("/politika/", f"Политика конфиденциальности — {BRAND}", f"Политика обработки данных посетителей сайта {DOMAIN}.", body, crumbs=[("/politika/", "Политика конфиденциальности")], og_title="Политика конфиденциальности"))
    body = f"""<section class="ph ph-s"><div class="wrap ph-in"><h1>Страница не найдена</h1><p>Возможно, она была перемещена. Нужен эвакуатор — звоните.</p>{cta()}</div></section>{blk("Что перевозим", svc_rows())}"""
    write("/404/", page("/404/", f"Страница не найдена — {BRAND}", "Страница не найдена.", body, og="home").replace('content="index,follow,max-image-preview:large"', 'content="noindex"'))

def build_meta():
    urls = [u for u in OG if u != "/404/"]
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u == '/' else '0.8'}</priority></url>\n" for u in urls)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n', encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Bingbot", "YandexBot"]
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    ll = [f"# {BRAND}", "", f"> {LEAD}", "", "## Главное",
          f"- Город: Караганда (Карагандинская область, Казахстан); также Темиртау и пригороды", "- Межгород: перевозка автомобилей из Караганды по всему Казахстану и обратно",
          f"- Телефон: {PHONE_LOCAL} ({PHONE}), WhatsApp: https://wa.me/{WA}", f"- Режим работы: {HOURS}",
          "- Тип техники: эвакуатор-платформа; легковые автомобили, кроссоверы, внедорожники", "- Стоимость: зависит от расстояния, типа и состояния автомобиля; сумму называют по телефону или в WhatsApp до выезда",
          "", "## Услуги"] + [f"- [{s['short']}]({SITE}/uslugi/{s['slug']}/): {s['text']}" for s in SERVICES] + \
         [f"- [Межгород]({SITE}/mezhgorod/): из Караганды в любой город Казахстана и обратно", "", "## Направления межгорода"] + \
         [f"- [Караганда — {r[1]}]({SITE}/mezhgorod/{r[0]}/)" for r in ROUTES] + [f"- Также: {', '.join(OTHER_CITIES)}", "",
         "## Районы Караганды", "- " + ", ".join(DISTRICTS), "", "## Пригороды", "- " + ", ".join(SUBURBS), "", "## Как вызвать"] + \
         [f"- {t}: {d}" for t, d in CALL_INFO] + ["", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ]
    (DIST / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": BRAND, "short_name": "Эвакуатор", "start_url": "/", "display": "browser", "background_color": "#0f1115", "theme_color": "#0f1115",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    (ROOT / "src" / "og_list.json").write_text(json.dumps(OG, ensure_ascii=False, indent=1), encoding="utf-8")

def build_assets():
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    shutil.copy(ROOT / "src" / "app.js", DIST / "assets" / "app.js")
    if (ROOT / "images").exists(): shutil.copytree(ROOT / "images", DIST / "images", dirs_exist_ok=True)
    for f in ("favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        if (ROOT / "assets" / f).exists(): shutil.copy(ROOT / "assets" / f, DIST / f)

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_assets(); build_home(); build_services(); build_routes(); build_misc(); build_meta()
    print("pages:", len(OG))
