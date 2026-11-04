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
        "body_class": "is-boxed page-blog",
    },
    "blog-single.html": {
        "partial": "blog-single.main.html",
        "title": "What to do in the first 72 hours after a truck accident | Hartwell &amp; Crane",
        "description": "What to secure in the first 72 hours after a commercial truck crash in Texas, and the federal and state deadlines that apply.",
        "active": "blog.html",
        "body_class": "is-boxed page-article",
    },
}

# In-page anchors on the homepage that must point back to index.html from other pages
HOME_ANCHORS = ("top", "about", "practice", "attorneys", "results", "offices", "contact", "insights")


def include(html: str) -> str:
    def repl(m):
        return (ROOT / "partials" / f"{m.group(1)}.html").read_text().rstrip("\n") + "\n"
    return re.sub(r"<!-- @include ([\w-]+) -->\n?", repl, html)


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
        top = top.replace('class="nav__link is-active"', 'class="nav__link"')
        top = top.replace(f'<a class="nav__link" href="{cfg["active"]}">',
                          f'<a class="nav__link is-active" href="{cfg["active"]}" aria-current="page">')

        body = include((ROOT / "partials" / cfg["partial"]).read_text())
        (ROOT / out).write_text(h + top + "\n\n" + body + "\n  " + bottom)
        print(f"built {out}")


if __name__ == "__main__":
    main()
