// Vercel Function: ИИ-помощник сайта evakuator09.kz.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и чат на сайте автоматически отвечает по встроенной базе.
const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";
const H24 = (process.env.WORK_24 || "1") === "1";

const SYSTEM = `Ты — онлайн-помощник сайта эвакуатора «Эвакуатор 09» в Караганде (evakuator09.kz). Пишешь в чате на сайте.
Факты: эвакуатор-платформа; легковые автомобили, кроссоверы, внедорожники; по Караганде (все районы: Казыбек би, Әлихан Бөкейхан, Майкудук, Пришахтинск, Юго-Восток, Федоровка и др.), Темиртау, Шахтинск, Сарань, Абай, Топар и трассы Карагандинской области; межгород из Караганды по всему Казахстану и обратно (Астана, Алматы, Балхаш, Жезказган, Павлодар, Шымкент, Костанай, Усть-Каменогорск и другие). Эвакуация после ДТП и при поломке. ${H24 ? "Работают круглосуточно, без выходных." : ""}
Телефон и WhatsApp: 8 700 180 01 90. Instagram: @evakuator.krg. Под чатом есть кнопки «Позвонить» и «В WhatsApp» (в WhatsApp можно отправить геолокацию).
Страницы: /mezhgorod/ (межгород), /uslugi/evakuaciya-posle-dtp/, /uslugi/evakuaciya-pri-polomke/, /temirtau/, /voprosy/, /kontakty/.
При вызове нужно сообщить: где машина (адрес, ориентир или километр трассы), марку и модель, что случилось, куда везти.
Правила:
- Отвечай на языке посетителя (русский или казахский), коротко: 1–3 предложения, без markdown, списков и эмодзи.
- Цель — чтобы человек позвонил или написал в WhatsApp. Если ситуация срочная — сразу дай номер.
- Не называй цены, время подачи, гарантии, скидки, способы оплаты и технику, которых нет в фактах. Стоимость зависит от расстояния, типа и состояния машины; диспетчер называет её до выезда.
- Не давай советов по ремонту и юридических консультаций по ДТП; при ДТП с пострадавшими — сначала 112.
- Если спрашивают, бот ли ты, честно скажи, что ты онлайн-помощник, а машину отправляет диспетчер.`;

const hits = new Map();
function limited(ip) {
  const now = Date.now(), arr = (hits.get(ip) || []).filter((t) => now - t < 600000);
  arr.push(now); hits.set(ip, arr); if (hits.size > 5000) hits.clear();
  return arr.length > 30;
}
module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }
  let body = req.body; if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const clean = [];
  for (const m of (Array.isArray(body && body.messages) ? body.messages : []).slice(-12)) {
    if (!m || (m.role !== "user" && m.role !== "assistant") || typeof m.content !== "string" || !m.content.trim()) continue;
    const x = { role: m.role, content: m.content.slice(0, 800) };
    if (!clean.length && x.role !== "user") continue;
    if (clean.length && clean[clean.length - 1].role === x.role) clean[clean.length - 1].content += "\n" + x.content; else clean.push(x);
  }
  if (!clean.length || clean[clean.length - 1].role !== "user") { res.status(400).json({ error: "bad_request" }); return; }
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST", headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: MODEL, max_tokens: 300, system: SYSTEM + `\nСтраница посетителя: ${String(body.page || "/").slice(0, 100)}`, messages: clean }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    const j = await r.json();
    const reply = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim();
    if (!reply) { res.status(502).json({ error: "empty" }); return; }
    res.status(200).json({ reply });
  } catch (e) { res.status(502).json({ error: "fail" }); }
};
