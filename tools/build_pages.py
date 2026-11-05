#!/usr/bin/env python3
"""Build the inner pages from index.html + partials/.

index.html is the source of truth for <head>, the icon sprite, topbar,
header, footer and scripts. Each page in PAGES wraps a partial from
partials/ with that shared shell, so a header or footer change only has
to be made once in index.html.

Usage:  python3 tools/build_pages.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = {
    "blog.html": {
        "partial": "blog.main.html",
        "title": "Insights | Hartwell &amp; Crane",
        "description": "Articles from Hartwell & Crane attorneys on Texas personal injury, employment, family, criminal, business and estate law.",
        "active": "blog.html",
        "body_class": "page-blog",
    },
    "blog-single.html": {
        "partial": "blog-single.main.html",
        "title": "What to do in the first 72 hours after a truck accident | Hartwell &amp; Crane",
        "description": "What to secure in the first 72 hours after a commercial truck crash in Texas, and the federal and state deadlines that apply.",
        "active": "blog.html",
        "body_class": "page-article",
    },
    "practice-area.html": {
        "partial": "practice-area.main.html",
        "title": "Personal Injury Lawyers | Hartwell &amp; Crane",
        "description": "Hartwell & Crane represents injured Texans in truck, car and motorcycle crashes, wrongful death, premises liability and product cases. No fee unless we win.",
        "active": "index.html#practice",
        "body_class": "page-practice",
        # Highlight this practice area in the sidebar list
        "current_practice": "Personal Injury",
    },
    "about.html": {
        "partial": "about.main.html",
        "title": "About Us | Hartwell &amp; Crane",
        "description": "Hartwell & Crane is a Texas trial firm founded in 1994 by two former prosecutors. 14 attorneys, four offices, and a partner on every case.",
        "active": "index.html#about",
        "body_class": "page-about",
        "contact_page": True,
    },
    "team.html": {
        "partial": "team.main.html",
        "title": "Our Team | Hartwell &amp; Crane",
        "description": "Meet the Hartwell & Crane team: trial attorneys, paralegals and staff across our Dallas, Houston, Austin and Fort Worth offices.",
        "active": "team.html",
        "body_class": "page-team",
        "contact_page": True,
    },
    "team-single.html": {
        "partial": "team-single.main.html",
        "title": "Eleanor Hartwell, Founding Partner | Hartwell &amp; Crane",
        "description": "Eleanor Hartwell is a founding partner of Hartwell & Crane and Board Certified in Civil Trial Law by the Texas Board of Legal Specialization.",
        "active": "team.html",
        "body_class": "page-profile",
        "contact_page": True,
    },
    "testimonials.html": {
        "partial": "testimonials.main.html",
        "title": "Client Testimonials | Hartwell &amp; Crane",
        "description": "Read what clients say about Hartwell & Crane: reviews from personal injury, employment, family, criminal defense, business and estate clients across Texas.",
        "active": "none",
        "body_class": "page-reviews",
        "contact_page": True,
    },
    "news.html": {
        "partial": "news.main.html",
        "title": "Press &amp; News | Hartwell &amp; Crane",
        "description": "Press releases, verdicts, awards and media coverage from Hartwell & Crane, a Texas trial firm.",
        "active": "none",
        "body_class": "page-news",
        "contact_page": True,
    },
    "news-single.html": {
        "partial": "news-single.main.html",
        "title": "Hartwell &amp; Crane wins $14.2 million verdict against national trucking carrier | Hartwell &amp; Crane",
        "description": "A Dallas County jury found the carrier liable after evidence showed the driver's logbook had been altered.",
        "active": "none",
        "body_class": "page-article page-news-single",
        "contact_page": True,
    },
    "contact.html": {
        "partial": "contact.main.html",
        "title": "Contact Us | Hartwell &amp; Crane",
        "description": "Contact Hartwell & Crane for a free, confidential case review. Call 24/7, email our intake team or visit our Dallas, Houston, Austin and Fort Worth offices.",
        "active": "contact.html",
        "body_class": "page-contact",
        # Contact links in the header/footer point at this page instead of the homepage section
        "contact_page": True,
    },
}

# In-page anchors on the homepage that must point back to index.html from other pages
HOME_ANCHORS = ("top", "about", "practice", "attorneys", "results", "offices", "contact", "insights")


def include(html: str) -> str:
    def repl(m):
        return (ROOT / "partials" / f"{m.group(1)}.html").read_text().rstrip("\n") + "\n"
    return re.sub(r"<!-- @include ([\w-]+) -->\n?", repl, html)


def from_index(html: str, src: str) -> str:
    """Copy a homepage section (matched by its id) into a page: <!-- @from-index offices -->"""
    def repl(m):
        name = m.group(1)
        sec = re.search(r'    <section class="[^"]*" id="%s".*?</section>\n' % name, src, re.S) or \
            re.search(r'    <section class="%s[ "].*?</section>\n' % name, src, re.S)
        return sec.group(0) if sec else ""
    return re.sub(r"    <!-- @from-index ([\w-]+) -->\n?", repl, html)


def main() -> None:
    src = (ROOT / "index.html").read_text()
    head_end = src.index("</head>")
    main_start = src.index('<main id="main">') + len('<main id="main">')
    main_end = src.index("</main>")
    head, shell_top, shell_bottom = src[:head_end], src[head_end:main_start], src[main_end:]

    for out, cfg in PAGES.items():
        h = re.sub(r"<title>.*?</title>", f"<title>{cfg['title']}</title>", head, count=1)
        h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + cfg["description"] + m.group(2), h, count=1)

        top, bottom = shell_top, shell_bottom
        for a in HOME_ANCHORS:
            top = top.replace(f'href="#{a}"', f'href="index.html#{a}"')
            bottom = bottom.replace(f'href="#{a}"', f'href="index.html#{a}"')
        top = top.replace('<body class="is-boxed">', f'<body class="{cfg["body_class"]}">')
        if cfg.get("contact_page"):
            top = top.replace('href="index.html#contact"', 'href="contact.html"')
            bottom = bottom.replace('href="index.html#contact"', 'href="contact.html"')
        top = top.replace('class="nav__link is-active"', 'class="nav__link"')
        top = top.replace(f'<a class="nav__link" href="{cfg["active"]}">',
                          f'<a class="nav__link is-active" href="{cfg["active"]}" aria-current="page">')

        body = from_index(include((ROOT / "partials" / cfg["partial"]).read_text()), src)
        body = body.replace('href="#contact"', 'href="contact.html"')
        if cfg.get("current_practice"):
            name = cfg["current_practice"]
            body = body.replace(
                f'<a class="practice-list__link" href="practice-area.html"><span class="practice-list__name">{name}</span>',
                f'<a class="practice-list__link is-current" href="practice-area.html" aria-current="page"><span class="practice-list__name">{name}</span>',
            )
        (ROOT / out).write_text(h + top + "\n\n" + body + "\n  " + bottom)
        print(f"built {out}")


if __name__ == "__main__":
    main()
