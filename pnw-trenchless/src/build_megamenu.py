"""Assemble megamenu.html: the Who We Serve design page with the Services mega menu in the header
(src/megamenu-nav.html + src/megamenu.css). Design preview only; ?open in the URL shows it open.
Run from pnw-trenchless/: python3 src/build_megamenu.py
"""
s = open("who-we-serve.html").read()
old = '      <a href="index.html#services">Services</a>\n'
assert old in s
s = s.replace(old, open("src/megamenu-nav.html").read(), 1)
for a, b in [('<a href="index.html#who">Who We Serve</a>', '<a href="who-we-serve.html">Who We Serve</a>'),
             ('<a href="index.html#mike">About</a>', '<a href="about.html">About</a>'),
             ('<a href="#estimate">Contact</a>', '<a href="contact.html">Contact</a>')]:
    assert a in s
    s = s.replace(a, b, 1)
s = s.replace("</head>", "<style>\n" + open("src/megamenu.css").read() + "</style>\n</head>", 1)
JS = """<script>
(function () {
  /* Services mega menu: hover or focus on desktop, click everywhere, Esc closes */
  var item = document.getElementById('navServices'), btn = item.querySelector('.nav__trigger'), timer;
  var desktop = function () { return window.matchMedia('(min-width: 1201px)').matches; };
  var set = function (open) { item.classList.toggle('is-open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false'); };
  btn.addEventListener('click', function () { set(!item.classList.contains('is-open')); });
  item.addEventListener('mouseenter', function () { if (desktop()) { clearTimeout(timer); set(true); } });
  item.addEventListener('mouseleave', function () { if (desktop()) { timer = setTimeout(function () { set(false); }, 180); } });
  item.addEventListener('focusout', function (e) { if (desktop() && !item.contains(e.relatedTarget)) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && item.classList.contains('is-open')) { set(false); btn.focus(); } });
  document.addEventListener('click', function (e) { if (desktop() && !item.contains(e.target)) set(false); });
  if (/[?&]open/.test(location.search)) set(true);
})();
</script>
</body>"""
s = s.replace("</body>", JS, 1)
s = s.replace("<title>Who We Serve | Homes, Businesses &amp; Industrial Sites | PNW Trenchless</title>", "<title>Services mega menu (design preview) | PNW Trenchless</title>", 1)
open("megamenu.html", "w").write(s)
print("megamenu.html", len(s))
