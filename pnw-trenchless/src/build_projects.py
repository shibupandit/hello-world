"""Assemble projects.html from the service page shell + src/projects-main.html + src/projects.css.

Same approach as build_about.py / build_contact.py. The quote section is the lining page's
conversion section with Projects wording.
Run from pnw-trenchless/: python3 src/build_projects.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
ci, mi = s.index(l), s.index(lm)
conv = re.search(r"<!-- =+ 13 CONVERSION =+ -->.*?</section>", lm, re.S).group(0)
conv = conv.replace("Find out if your pipe <span class=\"serif\">can be lined.</span>", "Want a result <span class=\"serif\">like these?</span>")
conv = conv.replace('value="Pipe Lining"', 'value="Projects"').replace("service = Pipe Lining", "source = Projects")
conv = conv.replace('<label for="i1"><input type="radio" name="service" id="i1" value="lining" checked><span>CIPP lining</span></label>',
                    '<label for="i1"><input type="radio" name="service" id="i1" value="lining"><span>CIPP lining</span></label>')
conv = conv.replace('<label for="i2"><input type="radio" name="service" id="i2" value="sewer"><span>Sewer line repair</span></label>',
                    '<label for="i2"><input type="radio" name="service" id="i2" value="sewer" checked><span>Sewer line repair</span></label>')
main = open("src/projects-main.html").read().replace("<!--CONVERSION-->", conv)
out = s[:ci] + l + "\n" + open("src/projects.css").read() + s[ci + len(l):mi] + main + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Projects | Real Trenchless Sewer &amp; Water Line Jobs | PNW Trenchless</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="Real PNW Trenchless jobs: small access pits instead of trenches, the old pipe we pull out, '
                       'what goes in its place, and the yard after. Spokane and Stevens counties.">', out, count=1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
open("projects.html", "w").write(out)
print("projects.html", len(out))
