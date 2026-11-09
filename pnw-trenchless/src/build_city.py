"""Assemble city-single.html from the service page shell + src/city-main.html + src/projects.css (pcards)
+ src/serve.css. Same approach as build_reviews.py.
Run from pnw-trenchless/: python3 src/build_city.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
ci, mi = s.index(l), s.index(lm)
conv = re.search(r"<!-- =+ 13 CONVERSION =+ -->.*?</section>", lm, re.S).group(0)
conv = conv.replace("Find out if your pipe <span class=\"serif\">can be lined.</span>", "Get a quote in <span class=\"serif\">Spokane Valley.</span>")
conv = conv.replace('value="Pipe Lining"', 'value="City: Spokane Valley"').replace("service = Pipe Lining", "source = City: Spokane Valley")
conv = conv.replace('<label for="i1"><input type="radio" name="service" id="i1" value="lining" checked><span>CIPP lining</span></label>',
                    '<label for="i1"><input type="radio" name="service" id="i1" value="lining"><span>CIPP lining</span></label>')
conv = conv.replace('<label for="i2"><input type="radio" name="service" id="i2" value="sewer"><span>Sewer line repair</span></label>',
                    '<label for="i2"><input type="radio" name="service" id="i2" value="sewer" checked><span>Sewer line repair</span></label>')
main = open("src/city-main.html").read().replace("<!--CONVERSION-->", conv)
css = l + "\n" + open("src/projects.css").read() + "\n" + open("src/serve.css").read() + "\n" + open("src/city.css").read()
out = s[:ci] + css + s[ci + len(l):mi] + main + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Trenchless Sewer Repair in Spokane Valley, WA | PNW Trenchless</title>", out, count=1)
out = re.sub(r'<meta name="description" content="Trenchless sewer and water line repair in Spokane Valley, WA: sewer lining, pipe bursting, water line pulling and point repairs. '
                       'Family-owned, camera footage you keep. Call or text 509-953-2036.">',
             lambda m: '<meta name="description" content="Trenchless sewer and water line repair for homeowners, commercial properties and industrial and municipal sites '
                       'across Spokane and Stevens counties. Small access points, camera footage, written quotes.">', out, count=1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
open("city-single.html", "w").write(out)
print("city-single.html", len(out))
