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
      // "#about" or "/#about" (no backslashes: WordPress strips them from saved scripts)
      var href = l.getAttribute("href") || "";
      var k = href.indexOf("#");
      if (k > -1 && href.length > k + 1 && (k === 0 || href.slice(0, k) === "/")) byId[href.slice(k + 1)] = l;
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
  // 8. Blog archive: category chips + search (Bricks: Query Filters)
  var grid = document.querySelector(".js-blog-grid");
  if (grid) {
    var chips = document.querySelectorAll(".chip[data-filter]");
    var featured = document.querySelector(".post-featured");
    var empty = document.querySelector(".js-blog-empty");
    var searchForm = document.querySelector(".js-blog-search");
    var searchInput = searchForm && searchForm.querySelector("input");
    var state = { cat: "all", q: "" };
    var apply = function () {
      var shown = 0;
      var items = Array.prototype.slice.call(grid.children);
      if (featured) items.push(featured);
      items.forEach(function (el) {
        var okCat = state.cat === "all" || el.getAttribute("data-category") === state.cat;
        var okQ = !state.q || el.textContent.toLowerCase().indexOf(state.q) !== -1;
        el.hidden = !(okCat && okQ);
        if (!el.hidden) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.classList.remove("is-active"); c.setAttribute("aria-pressed", "false"); });
        chip.classList.add("is-active");
        chip.setAttribute("aria-pressed", "true");
        state.cat = chip.getAttribute("data-filter");
        apply();
      });
    });
    if (searchForm && searchInput) {
      searchForm.addEventListener("submit", function (e) { e.preventDefault(); apply(); });
      searchInput.addEventListener("input", function () { state.q = searchInput.value.trim().toLowerCase(); apply(); });
    }
  }

  // 9. Single post: table of contents, scroll spy, reading progress, copy link
  var prose = document.querySelector(".js-prose");
  var toc = document.querySelector(".js-toc");
  if (prose && toc) {
    var heads = Array.prototype.slice.call(prose.querySelectorAll("h2[id]"));
    // WordPress: the "In this article" box sits outside the post content; move it under the lead paragraph
    var tocBox = toc.closest(".toc");
    var lead = prose.querySelector(".prose__lead") || prose.querySelector("p");
    if (tocBox && !prose.contains(tocBox) && lead) lead.parentNode.insertBefore(tocBox, lead.nextSibling);
    if (tocBox && heads.length < 2) tocBox.hidden = true;
    heads.forEach(function (h) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.className = "toc__link";
      a.href = "#" + h.id;
      a.textContent = h.textContent.replace(/^[0-9]+[.][ ]*/, "");
      li.appendChild(a);
      toc.appendChild(li);
    });
    var tocLinks = toc.querySelectorAll(".toc__link");
    var spy = function () {
      var current = 0;
      heads.forEach(function (h, i) { if (h.getBoundingClientRect().top < 160) current = i; });
      tocLinks.forEach(function (l, i) { l.classList.toggle("is-active", i === current); });
    };
    spy();
    window.addEventListener("scroll", spy, { passive: true });
  }
  if (prose && header) {
    var bar = document.createElement("div");
    bar.className = "read-progress";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML = '<span class="read-progress__bar"></span>';
    header.appendChild(bar);
    var fill = bar.firstChild;
    var progress = function () {
      var r = prose.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.5;
      var p = total > 0 ? Math.min(1, Math.max(0, (-r.top + window.innerHeight * 0.25) / total)) : 0;
      fill.style.transform = "scaleX(" + p.toFixed(3) + ")";
    };
    progress();
    window.addEventListener("scroll", progress, { passive: true });
    window.addEventListener("resize", progress);
  }
  var copyBtn = document.querySelector(".js-copy-link");
  if (copyBtn) {
    copyBtn.addEventListener("click", function (e) {
      if (e) e.preventDefault();
      var done = function (msg) {
        copyBtn.textContent = msg;
        setTimeout(function () { copyBtn.textContent = "Copy link"; }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(location.href).then(function () { done("Link copied"); }, function () { done("Press Ctrl+C to copy"); });
      } else {
        done("Press Ctrl+C to copy");
      }
    });
  }
  // 10. Highlight the current category chip / practice area link (WordPress archive + sidebar)
  var here = location.pathname.replace(/[/]+$/, "");
  document.querySelectorAll(".blog-filter a.chip, .practice-list__link").forEach(function (a) {
    var path = a.pathname.replace(/[/]+$/, "");
    if (path && path === here) {
      a.classList.add(a.classList.contains("chip") ? "is-active" : "is-current");
      a.setAttribute("aria-current", "page");
      if (a.classList.contains("chip")) {
        document.querySelectorAll(".blog-filter a.chip.is-active").forEach(function (o) { if (o !== a) o.classList.remove("is-active"); });
      }
    }
  });
})();
