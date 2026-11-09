"""City (service area) pages: Gutenberg content, written as plain core blocks (paragraph, heading,
list, image, buttons, links). No custom classes or inline styles in the content: the Bricks city
template (elements_city.py) styles it through the `prose` class on its Post Content element.

Only facts already on the site are used. Local facts Mike has to supply stay in <span class="tbc">
(no visual style on the live site; search the content for class="tbc" before launch).

Images: {{img:ID}} placeholders become core image blocks in import (the attachment URL is resolved
on the site). Run: python3 city_pages.py -> writes city_pages.json
"""
import json, pathlib

# Media IDs (pnw_media_ids): job-during 54, job-after 55, job-waterline 56, job-old-pipe 859,
# job-lined-pipe 860, job-access-pit 861, job-pipe-connection 862, job-lawn-restored 863.
ALT = {54: "Small access pit dug in a front lawn during a trenchless repair",
       55: "The same lawn after the repair, with the grass back in place",
       56: "Access pit with the new blue water line next to the meter box",
       859: "A section of old sewer pipe cut open, with heavy buildup inside",
       860: "An old sewer pipe cut open, with the new blue liner cured inside it",
       861: "A shored access pit in a front lawn, with the camera reel and jetter beside it",
       862: "The new sewer pipe connected in the access pit",
       863: "A front lawn after the job, with the pit backfilled and the grass back in place"}
CAPTION = {859: "What years of buildup look like inside an old sewer line.",
           860: "A new liner cured inside an old pipe: a seamless pipe within a pipe."}

# name, slug, where (from the Home service-area notes), featured image, inline image, menu order
CITIES = [
    ("Spokane", "spokane", "across the Spokane metro area", 54, 860, 1),
    ("Spokane Valley", "spokane-valley", "east of Spokane", 863, 859, 2),
    ("Deer Park", "deer-park", "north of Spokane", 861, 860, 3),
    ("Clayton", "clayton", "our home base", 862, 859, 4),
    ("Stevens County", "stevens-county", "north of Spokane County", 56, 860, 5),
    ("Spokane County", "spokane-county", "across Spokane County and nearby", 55, 859, 6),
]

SERVICES = [("Sewer pipe lining", "/services/sewer-pipe-lining/",
             "A resin liner cures inside your old pipe, creating a seamless, jointless pipe within a pipe. No trench, and no joints for roots to find."),
            ("Pipe bursting", "/services/pipe-bursting/",
             "A bursting head breaks the old pipe outward while new HDPE pipe is pulled in behind it. A completely new pipe with a 50+ year lifespan, and it can be upsized."),
            ("Water line pulling", "/services/water-line-pulling/",
             "We pull a new CTS poly line underground, reconnect it, and test it for pressure and leaks. No rust or scale buildup, and better water pressure."),
            ("Point repairs", "/services/point-repairs/",
             "When the damage is isolated to one section and the rest of the pipe is sound, we reline just that spot instead of replacing the whole line.")]


def p(html):
    return f"<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def lst(items, ordered=False):
    tag = "ol" if ordered else "ul"
    attrs = ' {"ordered":true}' if ordered else ""
    lis = "\n".join(f"<!-- wp:list-item -->\n<li>{x}</li>\n<!-- /wp:list-item -->" for x in items)
    return f'<!-- wp:list{attrs} -->\n<{tag} class="wp-block-list">{lis}</{tag}>\n<!-- /wp:list -->'


def image(mid):
    return "{{img:%d}}" % mid


def buttons(items):
    btns = "\n".join(f'<!-- wp:button -->\n<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{u}">{t}</a></div>\n<!-- /wp:button -->'
                     for t, u in items)
    return f'<!-- wp:buttons -->\n<div class="wp-block-buttons">{btns}</div>\n<!-- /wp:buttons -->'


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def content(name, where, inline):
    home = name == "Clayton"
    lead = (f"PNW Trenchless is based in Clayton, so this is home. We fix sewer and water lines for Clayton homes, businesses and industrial sites from the inside, through small access points instead of a trench across your yard."
            if home else
            f"Sewer backing up, or water pressure dropping? We fix sewer and water lines {where}, including {name}, from the inside, through small access points instead of a trench across your yard.")
    blocks = [
        p(lead),
        p("PNW Trenchless is family-owned and run by Mike Jeisma, who has spent 14+ years in sewer and water line work across the Spokane area. "
          "Every job starts with a camera inspection: you see what we see, and you get a true and honest quote in writing before any work begins."),
        h2(f"Sewer and water line problems we see in {name}"),
        p("Many older Spokane-area homes still run on clay, cast iron or Orangeburg sewer lines and galvanized water service. "
          "Add mature pines and maples, and root intrusion is one of the most common problems we see."),
        lst(["<strong>Roots in the line:</strong> backups that keep coming back after the line is cleared.",
             "<strong>Cracked or collapsed pipe:</strong> old clay and Orangeburg lines past their life.",
             "<strong>Low water pressure:</strong> often a corroded galvanized water service.",
             "<strong>One bad spot:</strong> a single crack or joint on an otherwise good line."]),
        p(tbc(f"Mike, 2–3 sentences about {name}: neighborhoods, soil, how deep lines run, what he finds most often.")),
        image(inline),
        h2(f"Our trenchless services in {name}"),
    ]
    for title, url, text in SERVICES:
        blocks += [h3(title), p(f'{text} <a href="{url}">More about {title.lower()}</a>')]
    blocks += [
        h2("How a trenchless repair works"),
        lst(["<strong>Camera inspection.</strong> We record the full line and show you the footage.",
             "<strong>Written quote.</strong> The method that fits your pipe, and the price, before any work.",
             "<strong>The repair.</strong> Lining, bursting, a new water line or a point repair, through one or two small access points.",
             "<strong>Final camera run.</strong> Proof the line is fixed. You keep the before and after footage."], ordered=True),
        h2("Trenchless or digging?"),
        p("With a traditional dig you also pay to restore everything that came out of the ground. Trenchless repair leaves your lawn, driveway and trees in place in most cases, "
          "and your water or sewer is off for hours, not days."),
        p("Trenchless isn't right for every pipe. If a section has a belly or is out of grade, digging that spot may be the better fix, and we'll tell you so."),
        h3(f"Permits and scheduling in {name}"),
        p(tbc(f"Which permits apply in {name}, whether PNW Trenchless pulls them, and how soon a camera inspection can be booked.")),
        h2(f"Get a quote in {name}"),
        p(f'Call or text <a href="tel:5099532036">509-953-2036</a>, or send us the details and a photo of the problem. Mike calls you back and books the camera. '
          f'You can also read <a href="/reviews/">what our customers say</a> or see <a href="/projects/">recent projects</a>.'),
        buttons([("Get a quote", "/contact/"), ("Call or text 509-953-2036", "tel:5099532036")]),
    ]
    return "\n\n".join(blocks)


def build():
    pages = []
    for name, slug, where, featured, inline, order in CITIES:
        pages.append({"title": name, "slug": slug, "featured": featured, "menu_order": order,
                      "excerpt": f"Trenchless sewer and water line repair in {name}: sewer lining, pipe bursting, water line pulling and point repairs. Family-owned, camera footage you keep.",
                      "content": content(name, where, inline)})
    data = {"alt": ALT, "caption": CAPTION, "pages": pages}
    pathlib.Path(__file__).with_name("city_pages.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    return data


if __name__ == "__main__":
    d = build()
    print([(x["slug"], len(x["content"])) for x in d["pages"]])
