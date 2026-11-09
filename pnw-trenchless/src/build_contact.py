"""Assemble contact.html from the service page shell + src/contact-main.html + src/contact.css.

Same approach as build_about.py. The service-area map is copied from the homepage design.
Run from pnw-trenchless/: python3 src/build_contact.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
home = open("index.html").read()
ci, mi = s.index(l), s.index(lm)
main = open("src/contact-main.html").read()
a = home.index('<figure class="map">')
b = home.index("</figure>", a) + len("</figure>")
mp = home[a:b].replace("CLAYTON TO SPOKANE METRO", "SPOKANE &amp; STEVENS COUNTIES")
# The office is in North Spokane County (Website Settings), so Clayton is not labelled as home base here.
mp = re.sub(r'<text[^>]*>HOME BASE</text>', '', mp)
main = main.replace("<!--MAP-->", mp)
out = s[:ci] + l + "\n" + open("src/contact.css").read() + s[ci + len(l):mi] + main + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Contact PNW Trenchless | Call or Text Mike, Spokane Trenchless Sewer Repair</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="Call or text Mike at 509-953-2036, email info@pnwtrenchless.com or request a free camera '
                       'estimate. PNW Trenchless serves Spokane, Spokane Valley, Deer Park, Clayton and Stevens County.">', out, count=1)
LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ContactPage","name":"Contact PNW Trenchless",
 "mainEntity":{"@type":"LocalBusiness","name":"PNW Trenchless","telephone":"+1-509-953-2036","email":"info@pnwtrenchless.com",
  "areaServed":["Spokane","Spokane Valley","Deer Park","Clayton","Stevens County","Spokane County"]}}
</script>
"""
out = out.replace("</head>", LD + "</head>", 1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
# The Contact form has no upload field (Fluent free has none), so guard the shared upload script.
out = out.replace("photo.addEventListener('change'", "if (photo) photo.addEventListener('change'", 1)
open("contact.html", "w").write(out)
print("contact.html", len(out))
