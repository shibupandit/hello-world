"""Assemble service-water-line-pulling.html from the Sewer Pipe Lining page + src/water-main.html.

Same shell, tokens and blocks as the lining page (src/lining.css is kept as is); only the
page content, title, description and JSON-LD change. The content was first generated from
src/lining-main.html and then rewritten for water line pulling.
Run from pnw-trenchless/: python3 src/build_water.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
lm = open("src/lining-main.html").read()
mi = s.index(lm)
out = s[:mi] + open("src/water-main.html").read() + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Water Line Pulling in Spokane | Trenchless Water Line Replacement | PNW Trenchless</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="Trenchless water line replacement in Spokane: a new CTS poly line pulled underground through small access pits, '
                       'reconnected and tested for pressure and leaks. Free estimate. Call or text 509-953-2036.">', out, count=1)
# Swap the service JSON-LD if the lining page has one; otherwise add one.
out = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", out, flags=re.S)
LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","name":"Water line pulling (trenchless water line replacement)",
 "serviceType":"Water line replacement","provider":{"@type":"LocalBusiness","name":"PNW Trenchless","telephone":"+1-509-953-2036"},
 "areaServed":["Spokane","Spokane Valley","Deer Park","Clayton","Stevens County","Spokane County"]}
</script>
"""
out = out.replace("</head>", LD + "</head>", 1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
open("service-water-line-pulling.html", "w").write(out)
print("service-water-line-pulling.html", len(out))
