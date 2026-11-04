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
        sec = re.search(r'    <section class="[^"]*" id="%s".*?</section>\n' % m.group(1), src, re.S)
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
