"""Assemble reviews.html from the service page shell + src/reviews-main.html + src/projects.css (pcards)
+ src/reviews.css. Same approach as build_projects.py.
Run from pnw-trenchless/: python3 src/build_reviews.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
ci, mi = s.index(l), s.index(lm)
conv = re.search(r"<!-- =+ 13 CONVERSION =+ -->.*?</section>", lm, re.S).group(0)
conv = conv.replace("Find out if your pipe <span class=\"serif\">can be lined.</span>", "Ready to be <span class=\"serif\">our next review?</span>")
conv = conv.replace('value="Pipe Lining"', 'value="Reviews"').replace("service = Pipe Lining", "source = Reviews")
conv = conv.replace('<label for="i1"><input type="radio" name="service" id="i1" value="lining" checked><span>CIPP lining</span></label>',
                    '<label for="i1"><input type="radio" name="service" id="i1" value="lining"><span>CIPP lining</span></label>')
conv = conv.replace('<label for="i2"><input type="radio" name="service" id="i2" value="sewer"><span>Sewer line repair</span></label>',
                    '<label for="i2"><input type="radio" name="service" id="i2" value="sewer" checked><span>Sewer line repair</span></label>')
main = open("src/reviews-main.html").read().replace("<!--CONVERSION-->", conv)
css = l + "\n" + open("src/projects.css").read() + "\n" + open("src/reviews.css").read()
out = s[:ci] + css + s[ci + len(l):mi] + main + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Reviews | What Spokane Homeowners Say | PNW Trenchless</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="Read real Google reviews of PNW Trenchless: trenchless sewer lining, pipe bursting and '
                       'water line replacement across Spokane and Stevens counties. 4.9 stars on Google.">', out, count=1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
open("reviews.html", "w").write(out)
print("reviews.html", len(out))
