/* Эвакуатор Караганда: меню и учёт звонков/WhatsApp в Google Ads */
(function () {
  "use strict";
  var body = document.body, burger = document.querySelector(".burger");
  function setNav(o) { body.classList.toggle("nav-open", o); if (burger) burger.setAttribute("aria-expanded", o ? "true" : "false"); }
  if (burger) burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  document.querySelectorAll(".nav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 960) setNav(false); });

  // конверсии: «Звонок» — клик по номеру, «WhatsApp» — клик по WhatsApp (номер переадресации Google в Казахстане недоступен)
  var ADS = (window.EV && window.EV.ads) || [], last = {};
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-ev]"); if (!a || !window.gtag) return;
    var ev = a.getAttribute("data-ev"), now = Date.now();
    if (last[ev] && now - last[ev] < 1500) return; last[ev] = now;
    try {
      window.gtag("event", ev === "call" ? "phone_click" : "whatsapp_click");
      var label = ev === "call" ? ADS[1] : ADS[2];
      if (ADS[0] && label) window.gtag("event", "conversion", { send_to: ADS[0] + "/" + label });
    } catch (err) {}
  });
})();
