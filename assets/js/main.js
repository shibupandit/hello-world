/* Hartwell & Crane — small progressive enhancements.
   In Bricks: paste into Settings → Custom code → Body (footer) scripts,
   or a Code element on the template. Bricks' native Nav Menu, Accordion
   and Slider elements can replace parts 1, 3 and 4. */
(function () {
  "use strict";

  // 1. Sticky header shadow
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // 2. Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  // Active nav link follows the section in view
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav__link"));
  if ("IntersectionObserver" in window && links.length) {
    var byId = {};
    links.forEach(function (l) {
      var id = l.getAttribute("href").slice(1);
      if (id) byId[id] = l;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var link = byId[entry.target.id];
        if (!link) return;
        links.forEach(function (l) { l.classList.remove("is-active"); });
        link.classList.add("is-active");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  // 3. FAQ: keep one item open at a time
  var faqs = document.querySelectorAll(".faq-item");
  faqs.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      faqs.forEach(function (other) { if (other !== item) other.open = false; });
    });
  });

  // 4. Testimonial slider (native scroll-snap + buttons)
  var track = document.querySelector(".js-slider");
  if (track) {
    var step = function (dir) {
      var card = track.firstElementChild;
      if (!card) return;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      var amount = (card.getBoundingClientRect().width + gap) * dir;
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      var atStart = track.scrollLeft <= 4;
      if (dir > 0 && atEnd) track.scrollTo({ left: 0 });
      else if (dir < 0 && atStart) track.scrollTo({ left: track.scrollWidth });
      else track.scrollBy({ left: amount });
    };
    var prev = document.querySelector(".js-slide-prev");
    var next = document.querySelector(".js-slide-next");
    if (prev) prev.addEventListener("click", function () { step(-1); });
    if (next) next.addEventListener("click", function () { step(1); });
  }

  // 5. Forms: client-side validation and a confirmation message.
  //    In WordPress the Bricks Form element (or your form plugin) handles submission.
  document.querySelectorAll(".js-form").forEach(function (form) {
    var status = form.querySelector(".form__status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstInvalid = null;
      form.querySelectorAll("[required]").forEach(function (field) {
        var ok = field.checkValidity() && field.value.trim() !== "";
        field.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !firstInvalid) firstInvalid = field;
      });
      if (!status) return;
      status.hidden = false;
      if (firstInvalid) {
        status.classList.add("is-error");
        status.textContent = "Please complete the highlighted fields so we can reach you.";
        firstInvalid.focus();
        return;
      }
      status.classList.remove("is-error");
      status.textContent = "Thank you. A member of our intake team will contact you within one business day.";
      form.reset();
    });
    form.addEventListener("input", function (e) {
      if (e.target.getAttribute("aria-invalid") === "true" && e.target.checkValidity() && e.target.value.trim() !== "") {
        e.target.setAttribute("aria-invalid", "false");
      }
    });
  });

  // 6. Footer year
  var year = document.querySelector(".js-year");
  if (year) year.textContent = String(new Date().getFullYear());
  // 7. Footer offices: open boxes on desktop, closed accordions at <= 640px
  var officeItems = document.querySelectorAll(".footer-office");
  if (officeItems.length && window.matchMedia) {
    var mq = window.matchMedia("(max-width: 640px)");
    var syncOffices = function () {
      officeItems.forEach(function (d) { d.open = !mq.matches; });
    };
    syncOffices();
    if (mq.addEventListener) mq.addEventListener("change", syncOffices);
    else if (mq.addListener) mq.addListener(syncOffices);
    // Desktop: keep boxes open even if a summary is activated by keyboard
    officeItems.forEach(function (d) {
      d.addEventListener("toggle", function () { if (!mq.matches && !d.open) d.open = true; });
    });
  }
})();
