/* Эвакуатор 09: меню, «назад/наверх», онлайн-помощник, учёт звонков и WhatsApp в Google Ads */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var CFG = window.EV || {}, body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- меню ---------- */
  var burger = $(".burger");
  function setNav(o) { body.classList.toggle("nav-open", o); if (burger) burger.setAttribute("aria-expanded", o ? "true" : "false"); }
  if (burger) burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  window.addEventListener("resize", function () { if (window.innerWidth > 900) setNav(false); });

  /* ---------- конверсии ---------- */
  var ADS = CFG.ads || [], last = {};
  function conv(ev) {
    if (!window.gtag) return;
    var now = Date.now(); if (last[ev] && now - last[ev] < 1500) return; last[ev] = now;
    try {
      window.gtag("event", ev === "call" ? "phone_click" : "whatsapp_click");
      var label = ev === "call" ? ADS[1] : ADS[2];
      if (ADS[0] && label) window.gtag("event", "conversion", { send_to: ADS[0] + "/" + label });
    } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-ev]"); if (a) conv(a.getAttribute("data-ev"));
  });

  /* ---------- назад / наверх ---------- */
  var bBack = $(".fl-back"), bTop = $(".fl-top");
  var inner = location.pathname !== "/";
  if (bBack) {
    bBack.hidden = !inner;
    bBack.addEventListener("click", function () {
      var same = false; try { same = document.referrer && new URL(document.referrer).host === location.host; } catch (e) {}
      if (same && history.length > 1) { history.back(); return; }
      var cr = $$(".crumbs a"); location.href = cr.length ? cr[cr.length - 1].getAttribute("href") : "/";
    });
  }
  if (bTop) bTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });
  var tick = false;
  function onScroll() {
    tick = false;
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (bTop) bTop.hidden = y < 600;
    var end = y + window.innerHeight >= document.documentElement.scrollHeight - 160;
    body.classList.toggle("at-end", end && y > 300);
  }
  window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ================= онлайн-помощник ================= */
  var chat = $("#chat"), fab = $(".fl-chat"), cb = $("#chatB"), cq = $("#chatQ"), cf = $("#chatF"), ci = $("#chatI"), waBtn = $("#chatWa");
  if (!chat) return;
  var hist = [], started = false, busy = false, apiOk = true;
  var ROUTES = CFG.routes || [];
  var PH = CFG.phone || "", H24 = !!CFG.h24;

  function openChat() {
    chat.hidden = false; body.classList.add("chat-open"); fab.setAttribute("aria-expanded", "true");
    if (!started) { started = true; say("Здравствуйте! Я онлайн-помощник эвакуатора в Караганде. Подскажу по вызову, межгороду и стоимости. Что случилось с машиной и где она сейчас?", QUICK); }
    if (window.innerWidth > 767) setTimeout(function () { ci.focus(); }, 50);
  }
  function closeChat() { if (chat.hidden) return; chat.hidden = true; body.classList.remove("chat-open"); fab.setAttribute("aria-expanded", "false"); fab.focus(); }
  fab.addEventListener("click", function () { chat.hidden ? openChat() : closeChat(); });
  $(".chat-x").addEventListener("click", closeChat);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { setNav(false); closeChat(); } });

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function linkify(s) {
    return esc(s).replace(/(\/(?:mezhgorod|uslugi|temirtau|voprosy|kontakty)[a-z0-9\-\/]*)/g, '<a href="$1">$1</a>')
      .replace(/(8 700 180 01 90)/g, '<a href="tel:' + CFG.tel + '" data-ev="call">$1</a>');
  }
  function add(role, text) {
    var m = document.createElement("div"); m.className = "msg " + (role === "u" ? "msg-u" : "msg-b");
    m.innerHTML = role === "u" ? esc(text) : linkify(text); cb.appendChild(m); cb.scrollTop = cb.scrollHeight;
  }
  function dots() { var t = document.createElement("div"); t.className = "msg msg-b dots"; t.innerHTML = "<i></i><i></i><i></i>"; cb.appendChild(t); cb.scrollTop = cb.scrollHeight; return t; }
  function say(text, quick) {
    var t = dots();
    setTimeout(function () { t.remove(); add("b", text); hist.push({ role: "assistant", content: text }); setQuick(quick); updWa(); }, Math.min(1300, 350 + text.length * 5));
  }
  var QUICK = ["Нужен эвакуатор сейчас", "Сколько стоит?", "Межгород", "Грузовой эвакуатор", "После ДТП", "Работаете ночью?"];
  function setQuick(list) {
    cq.innerHTML = "";
    (list || QUICK).forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { ask(q); }); cq.appendChild(b); });
  }
  // WhatsApp из чата — с текстом разговора, чтобы диспетчер сразу видел детали
  function updWa() {
    var u = hist.filter(function (h) { return h.role === "user"; }).map(function (h) { return h.content; }).join(". ");
    var t = "Здравствуйте! Нужен эвакуатор." + (u ? " " + u.slice(0, 600) : "");
    waBtn.href = "https://wa.me/" + CFG.wa + "?text=" + encodeURIComponent(t);
  }
  function ask(text) {
    text = String(text || "").trim(); if (!text || busy) return;
    add("u", text); hist.push({ role: "user", content: text }); cq.innerHTML = ""; updWa();
    var local = kb(text);
    if (local && local.instant) return say(local.a, local.q);
    if (!apiOk) return say((local || FALLBACK).a, (local || FALLBACK).q);
    busy = true; var t = dots();
    var ctrl = window.AbortController ? new AbortController() : null, timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 12000);
    fetch("/api/chat", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-12), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) { if (!j.reply) throw new Error("empty"); clearTimeout(timer); t.remove(); add("b", j.reply); hist.push({ role: "assistant", content: j.reply }); setQuick(local && local.q); updWa(); busy = false; })
      .catch(function () { clearTimeout(timer); t.remove(); apiOk = false; busy = false; var r = local || FALLBACK; say(r.a, r.q); });
  }
  cf.addEventListener("submit", function (e) { e.preventDefault(); var v = ci.value; ci.value = ""; ask(v); });

  /* ---------- база ответов (работает и без ИИ) ---------- */
  var CALL = "Позвоните " + PH + " или нажмите «В WhatsApp» под чатом — там можно отправить геолокацию.";
  var FALLBACK = { a: "Точный ответ даст диспетчер. " + CALL + " Назовите адрес, марку машины и куда её везти.", q: ["Сколько стоит?", "Межгород", "Что сказать при звонке?"] };
  var routeList = ROUTES.map(function (r) { return r[1]; }).join(", ");
  var KB = [
    { k: ["привет", "здравств", "добрый", "салем", "сәлем"], instant: 1, a: "Здравствуйте! Чем помочь? Расскажите, что с машиной и где она находится." },
    { k: ["спасибо", "рахмет"], instant: 1, a: "Пожалуйста! Если нужен эвакуатор — " + CALL },
    { k: ["бот", "робот", "живой", "человек"], instant: 1, a: "Я онлайн-помощник сайта. Машину отправляет диспетчер — " + CALL },
    { k: ["сейчас", "срочно", "нужен эвакуатор", "вызвать", "вызов", "приехать", "приедет", "быстро"], a: "Звоните прямо сейчас: " + PH + ". Скажите адрес или ориентир, марку и модель машины, что случилось и куда везти. В WhatsApp можно отправить геолокацию — так найдём быстрее.", q: ["Сколько стоит?", "Что сказать при звонке?"] },
    { k: ["стоим", "цена", "сколько стоит", "почем", "почём", "прайс", "тариф", "тенге", "₸", "дорого"], a: "Стоимость зависит от расстояния, типа машины и её состояния — на ходу, после ДТП или с заблокированными колёсами. Диспетчер назовёт точную сумму до выезда: " + PH + ".", q: ["Межгород", "Нужен эвакуатор сейчас"] },
    { k: ["межгород", "другой город", "в астану", "в алматы", "из караганды", "перевез", "по казахстану", "междугор"].concat(ROUTES.map(function (r) { return r[1].toLowerCase().slice(0, 5); })), a: "Да, возим машины из Караганды по всему Казахстану и обратно. Основные направления: " + routeList + ". Подробнее — /mezhgorod/. Назовите маршрут и марку машины — посчитаем стоимость.", q: ["Сколько стоит?", "Можно заранее?"] },
    { k: ["заранее", "на завтра", "дату", "запланир"], a: "Да, перевозку можно заказать заранее — согласуем дату, время погрузки и адрес доставки. " + CALL },
    { k: ["дтп", "авари", "разбит", "удар"], a: "Заберём машину после ДТП, когда документы оформлены и её разрешили убрать. Если колёса не крутятся или заблокирован руль — скажите при звонке. Отвезём на стоянку, в сервис, домой или в другой город. Подробнее — /uslugi/evakuaciya-posle-dtp/.", q: ["Сколько стоит?", "Нужен эвакуатор сейчас"] },
    { k: ["не завод", "сломал", "поломк", "заглох", "аккумулятор", "сел"], a: "Если машина не заводится или сломалась в пути — отвезём её в автосервис, гараж или домой. Ремонт на месте не делаем. Подробнее — /uslugi/evakuaciya-pri-polomke/." },
    { k: ["ночь", "ночью", "круглосуточ", "выходн", "праздник", "график", "время работы", "до скольки"], a: H24 ? "Работаем круглосуточно, без выходных и праздников. " + CALL : "Режим работы уточните у диспетчера: " + PH + "." },
    { k: ["трасс", "дорог", "километр", "км", "геолок", "за городом"], a: "Да, выезжаем на трассы. Назовите трассу и ближайший километровый знак или отправьте геолокацию в WhatsApp — кнопка «В WhatsApp» под чатом." },
    { k: ["темиртау", "шахтинск", "сарань", "абай", "топар", "пригород", "област"], a: "Работаем по Караганде, Темиртау, Шахтинску, Сарани, Абаю, Топару и другим населённым пунктам области. Про Темиртау — /temirtau/." },
    { k: ["внедорож", "кроссовер", "джип", "полный привод", "4х4", "4x4", "микроавтобус", "минивэн", "габарит"], a: "Возим легковые автомобили, кроссоверы и внедорожники на платформе, а грузовики, автобусы и спецтехнику — на грузовом эвакуаторе — для полного привода это безопаснее. Если машина крупная, назовите марку и модель — диспетчер скажет, подойдёт ли эвакуатор." },
    { pri: 3, k: ["грузов", "камаз", "автобус", "газель", "спецтехник", "трактор", "фура", "фуру", "тягач", "маз", "ман ", "вольво", "погрузчик", "экскаватор"], a: "Да, есть грузовой эвакуатор: перевозим грузовики, микроавтобусы, автобусы и спецтехнику по Караганде, области и межгород. Назовите марку, модель и примерную массу — диспетчер скажет, подойдёт ли эвакуатор, и назовёт стоимость: " + PH + ". Подробнее — /uslugi/gruzovoy-evakuator/." },
    { k: ["мотоцикл", "мото", "скутер", "квадроцикл"], a: "Про перевозку мототехники уточните у диспетчера: " + PH + "." },
    { k: ["поехать с", "пассажир", "сесть в", "со мной"], a: "Можно ли поехать вместе с машиной — зависит от эвакуатора, который приедет. Уточните при звонке: " + PH + "." },
    { k: ["что сказать", "что нужно", "какие данные", "что сообщить"], a: "Скажите четыре вещи: где машина (адрес, ориентир или километр трассы), какая машина (марка, модель, тип кузова), что случилось и куда везти. Так подача будет быстрее, а цена — точнее." },
    { k: ["оплат", "kaspi", "каспи", "наличн", "перевод", "карт"], a: "Способ оплаты уточните у диспетчера при вызове: " + PH + "." },
    { k: ["штрафстоян", "спецстоян", "забрали", "эвакуировали"], a: "Мы не работаем со штрафстоянками — машины туда отправляет полиция. Если нужно перевезти машину после того, как вы её забрали, звоните: " + PH + "." },
    { k: ["инста", "instagram", "соцсет"], instant: 1, a: "Наш Instagram — @evakuator.krg. Там фото и видео работ." },
    { k: ["номер", "телефон", "контакт", "whatsapp", "ватсап", "позвон"], instant: 1, a: "Телефон и WhatsApp: " + PH + ". Кнопки «Позвонить» и «В WhatsApp» — прямо под чатом." },
  ];
  function kb(text) {
    var t = " " + text.toLowerCase().replace(/ё/g, "е") + " ", best = null, sc = 0;
    KB.forEach(function (it) { var s = 0; it.k.forEach(function (k) { if (t.indexOf(k.replace(/ё/g, "е")) > -1) s += k.length; }); s *= it.pri || 1; if (s > sc) { sc = s; best = it; } });
    if (best && !best.a) return null;
    return best ? { a: best.a, q: best.q, instant: best.instant } : null;
  }
})();
