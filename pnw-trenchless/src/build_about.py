"""Assemble about.html from the service page shell + src/about-main.html + src/about.css.

The service page (service-sewer-pipe-lining.html) supplies the shared head, tokens, header,
footer and scripts; src/lining.css stays in (the About page reuses its blocks).
Run from pnw-trenchless/: python3 src/build_about.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
ci, mi = s.index(l), s.index(lm)
out = s[:ci] + l + "\n" + open("src/about.css").read() + s[ci + len(l):mi] + open("src/about-main.html").read() + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>About Mike Jeisma | PNW Trenchless, Spokane Trenchless Sewer Repair</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="Meet Mike Jeisma, owner of PNW Trenchless. 14+ years fixing sewer and water lines '
                       'across the Spokane area. When you call, you talk to him; when the trailer pulls up, he\'s on it.">', out, count=1)
LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AboutPage","name":"About Mike Jeisma | PNW Trenchless",
 "mainEntity":{"@type":"Person","name":"Mike Jeisma","jobTitle":"Owner & lead technician",
  "worksFor":{"@type":"LocalBusiness","name":"PNW Trenchless","telephone":"+1-509-953-2036","email":"info@pnwtrenchless.com",
   "areaServed":["Spokane","Spokane Valley","Deer Park","Clayton","Stevens County","Spokane County"]}}}
</script>
"""
out = out.replace("</head>", LD + "</head>", 1)
# Footer address: the user set the office address to North Spokane County (Website Settings).
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
open("about.html", "w").write(out)
print("about.html", len(out))
