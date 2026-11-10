"""Assemble megamenu.html: the Who We Serve design page with the Services and Who We Serve mega menus in the
header (src/megamenu-nav.html, src/megamenu-serve-nav.html + src/megamenu.css). Design preview only;
?open = Services, ?serve = Who We Serve, ?about = About, ?areas = Service Areas.
Run from pnw-trenchless/: python3 src/build_megamenu.py
"""
s = open("who-we-serve.html").read()
old = '      <a href="index.html#services">Services</a>\n'
assert old in s
s = s.replace(old, open("src/megamenu-nav.html").read(), 1)
old = '      <a href="index.html#who">Who We Serve</a>\n'
assert old in s
s = s.replace(old, open("src/megamenu-serve-nav.html").read(), 1)
old = '      <a href="index.html#how">How It Works</a>\n'
assert old in s
s = s.replace(old, "", 1)
old = '      <a href="index.html#mike">About</a>\n'
assert old in s
s = s.replace(old, open("src/megamenu-about-nav.html").read(), 1)
old = '      <a href="index.html#areas">Service Areas</a>\n'
assert old in s
s = s.replace(old, open("src/megamenu-areas-nav.html").read(), 1)
for a, b in [
             ('<a href="#estimate">Contact</a>', '<a href="contact.html">Contact</a>')]:
    assert a in s
    s = s.replace(a, b, 1)
s = s.replace("</head>", "<style>\n" + open("src/megamenu.css").read() + "</style>\n</head>", 1)
JS = """<script>
(function () {
  /* mega menus: hover or focus on desktop, click everywhere, Esc closes; one open at a time */
  var items = [].slice.call(document.querySelectorAll('.nav__item'));
  var desktop = function () { return window.matchMedia('(min-width: 1201px)').matches; };
  var set = function (item, open) { item.classList.toggle('is-open', open); item.querySelector('.nav__trigger').setAttribute('aria-expanded', open ? 'true' : 'false'); };
  items.forEach(function (item) {
    var btn = item.querySelector('.nav__trigger'), timer;
    btn.addEventListener('click', function () { var o = !item.classList.contains('is-open'); items.forEach(function (i) { set(i, false); }); set(item, o); });
    item.addEventListener('mouseenter', function () { if (desktop()) { clearTimeout(timer); items.forEach(function (i) { if (i !== item) set(i, false); }); set(item, true); } });
    item.addEventListener('mouseleave', function () { if (desktop()) { timer = setTimeout(function () { set(item, false); }, 180); } });
    item.addEventListener('focusout', function (e) { if (desktop() && !item.contains(e.relatedTarget)) set(item, false); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') items.forEach(function (i) { if (i.classList.contains('is-open')) { set(i, false); i.querySelector('.nav__trigger').focus(); } }); });
  document.addEventListener('click', function (e) { if (desktop()) items.forEach(function (i) { if (!i.contains(e.target)) set(i, false); }); });
  if (/[?&]open/.test(location.search)) set(document.getElementById('navServices'), true);
  if (/[?&]serve/.test(location.search)) set(document.getElementById('navServe'), true);
  if (/[?&]about/.test(location.search)) set(document.getElementById('navAbout'), true);
  if (/[?&]areas/.test(location.search)) set(document.getElementById('navAreas'), true);
})();
</script>
</body>"""
s = s.replace("</body>", JS, 1)
s = s.replace("<title>Who We Serve | Homes, Businesses &amp; Industrial Sites | PNW Trenchless</title>", "<title>Services mega menu (design preview) | PNW Trenchless</title>", 1)
open("megamenu.html", "w").write(s)
print("megamenu.html", len(s))
