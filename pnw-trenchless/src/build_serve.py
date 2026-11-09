"""Assemble who-we-serve.html from the service page shell + src/serve-main.html + src/projects.css (pcards)
+ src/serve.css. Same approach as build_reviews.py.
Run from pnw-trenchless/: python3 src/build_serve.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
ci, mi = s.index(l), s.index(lm)
conv = re.search(r"<!-- =+ 13 CONVERSION =+ -->.*?</section>", lm, re.S).group(0)
conv = conv.replace("Find out if your pipe <span class=\"serif\">can be lined.</span>", "Tell us about <span class=\"serif\">your property.</span>")
conv = conv.replace('value="Pipe Lining"', 'value="Who We Serve"').replace("service = Pipe Lining", "source = Who We Serve")
conv = conv.replace('<label for="i1"><input type="radio" name="service" id="i1" value="lining" checked><span>CIPP lining</span></label>',
                    '<label for="i1"><input type="radio" name="service" id="i1" value="lining"><span>CIPP lining</span></label>')
conv = conv.replace('<label for="i2"><input type="radio" name="service" id="i2" value="sewer"><span>Sewer line repair</span></label>',
                    '<label for="i2"><input type="radio" name="service" id="i2" value="sewer" checked><span>Sewer line repair</span></label>')
main = open("src/serve-main.html").read().replace("<!--CONVERSION-->", conv)
css = l + "\n" + open("src/projects.css").read() + "\n" + open("src/serve.css").read()
out = s[:ci] + css + s[ci + len(l):mi] + main + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Who We Serve | Homes, Businesses &amp; Industrial Sites | PNW Trenchless</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="Trenchless sewer and water line repair for homeowners, commercial properties and industrial and municipal sites '
                       'across Spokane and Stevens counties. Small access points, camera footage, written quotes.">', out, count=1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
open("who-we-serve.html", "w").write(out)
print("who-we-serve.html", len(out))
