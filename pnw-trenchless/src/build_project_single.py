"""Assemble project-single.html (single project template) from the service page shell +
src/project-single-main.html + src/projects.css (pcards) + src/project-single.css.

Same approach as build_projects.py. Sample content is the front-lawn job.
Run from pnw-trenchless/: python3 src/build_project_single.py
"""
import re

s = open("service-sewer-pipe-lining.html").read()
l = open("src/lining.css").read()
lm = open("src/lining-main.html").read()
ci, mi = s.index(l), s.index(lm)
conv = re.search(r"<!-- =+ 13 CONVERSION =+ -->.*?</section>", lm, re.S).group(0)
conv = conv.replace("Find out if your pipe <span class=\"serif\">can be lined.</span>", "Want a result <span class=\"serif\">like this one?</span>")
conv = conv.replace('value="Pipe Lining"', 'value="Project page"').replace("service = Pipe Lining", "source = Project page")
main = open("src/project-single-main.html").read().replace("<!--CONVERSION-->", conv)
css = l + "\n" + open("src/projects.css").read() + "\n" + open("src/project-single.css").read()
out = s[:ci] + css + s[ci + len(l):mi] + main + s[mi + len(lm):]
out = re.sub(r"<title>.*?</title>", "<title>Front-Lawn Sewer Line Project | PNW Trenchless</title>", out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*">',
             lambda m: '<meta name="description" content="A PNW Trenchless sewer line job: one shored access pit instead of a trench, '
                       'the new pipe connected, and the lawn put back. Photos from the job site.">', out, count=1)
out = out.replace('<span><span class="tbc">Address or service-area business</span>, Clayton, WA</span>', '<span>North Spokane County</span>')
out = out.replace("photo.addEventListener('change'", "if (photo) photo.addEventListener('change'", 1)
open("project-single.html", "w").write(out)
print("project-single.html", len(out))
