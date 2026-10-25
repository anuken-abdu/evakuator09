# Эвакуатор Караганда — сайт

Статический сайт в папке `dist/` (19 страниц + 404), Vercel отдаёт его как есть.

- `src/data.py` — все тексты и настройки: домен, телефон, режим работы, ID тегов Google.
- `src/build.py` — генератор страниц → `python3 src/build.py`.
- `src/render_art.py`, `src/render_brand.py` — иллюстрации, favicon и баннеры превью (нужен Playwright).
- `src/ads.py` — файл Google Ads для Editor → папка `google-ads/`.

После правки `src/data.py`: `python3 src/build.py` (если менялись заголовки — сначала `python3 src/render_brand.py`).

Домен (hoster.kz → DNS): `A @ 76.76.21.21`, `CNAME www cname.vercel-dns.com`. В Vercel основным сделать адрес с www.
