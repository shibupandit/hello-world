"""City pages template (Bricks "content" template, condition: the 6 city pages).
Built from pnw-trenchless/city-single.html (user's reference layout, 2026-11-09).

The city text is each page's Gutenberg content (plain core blocks, see city_pages.py), rendered by
the Post Content element and styled by the `prose` class. Everything else is template: hero
({post_title}), featured image, "why" points, recent projects (loop), sidebar (services, recent
projects loop, other city pages loop, local contractor from Website Settings, call card), reviews loop.
City pages carry the meta `pnw_city = 1`, which the "Other areas" loop uses.
"""
from elements import (N, section, container, block, h, t, span, a, svg, btn, eyebrow, attrs, link, head,
                      head_split, flatten, review_loop, when, TEL, PHONE, MAIL, EMAIL, ADDRESS, HOURS)
from elements_projects import project_card, q, REAL_ONLY

SERVICES = [("icon-liner.svg", "Sewer pipe lining", "/services/sewer-pipe-lining/"),
            ("icon-burst.svg", "Pipe bursting", "/services/pipe-bursting/"),
            ("icon-drop.svg", "Water line pulling", "/services/water-line-pulling/"),
            ("icon-patch.svg", "Point repairs", "/services/point-repairs/")]
CITY = "{post_title}"


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", "/", "crumbs__link")], tag="li"),
            block("crumbs__item", [a("Service areas", "/#areas", "crumbs__link")], tag="li"),
            block("crumbs__item", [span(CITY, "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    return section("section city-hero section--dark grain", [
        container([
            crumbs,
            h("h1", f"Trenchless Sewer &amp; Water Line Repair in {CITY}", "city-hero__title"),
            block("hero__actions", [
                btn("Get a quote", "/contact/", "btn--primary", icon="icon-arrow.svg"),
                btn(PHONE, TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
            ]),
        ]),
    ], label="Hero")


def main_col():
    why = [("The owner on the job.", "Mike Jeisma, 14+ years in sewer and water line work."),
           ("You see the pipe first.", "Camera footage before and after, yours to keep."),
           ("A true and honest quote.", "In writing, before any work starts."),
           ("Less digging.", "Small access points instead of a trench across your yard.")]
    return block("city-main", [
        block("city-cover", [N("image", None, image={"useDynamicData": "{featured_image}", "size": "large"}, altText=f"{CITY}")],
              tag="figure", **when("{featured_image}")),
        N("post-content", "prose", label="Gutenberg content"),
        block("city-block", [
            h("h2", f"Why {CITY} homeowners choose PNW Trenchless", "city-block__title"),
            block("why", [t(f"<strong>{b}</strong> {x}", "why__item", tag="li") for b, x in why], tag="ul"),
        ]),
        block("city-block", [
            block("city-block__head", [h("h2", "Recent projects", "city-block__title"), a("All projects", "/projects/", "link-arrow")]),
            block("pcards pcards--two", [project_card(q(posts_per_page=2, meta_query=[REAL_ONLY]))], tag="ul"),
        ]),
    ], tag="article")


def aside():
    return block("city-aside", [
        block("widget", [
            h("h2", "Services", "widget__title"),
            block("widget__svc", [block("widget__svc-row", [block("widget__svc-item", [svg(ic), span(lbl)], href=u)], tag="li")
                                  for ic, lbl, u in SERVICES], tag="ul"),
        ], tag="section"),
        block("widget", [
            h("h2", "Recent projects", "widget__title"),
            block("widget__list", [
                N("block", "widget__list-item", [span("{post_title}", "widget__list-title"), span("{acf_service}", "widget__list-meta")],
                  label="Project (loop)", tag="a", link=link("{post_url}"), hasLoop=True, query=q(posts_per_page=4, meta_query=[REAL_ONLY])),
            ]),
        ], tag="section"),
        block("widget widget--tint", [
            h("h2", "Other areas we serve", "widget__title"),
            block("widget__areas", [
                N("block", "", [a("{post_title}", link("{post_url}"), "widget__area")], label="City page (loop)", tag="li", hasLoop=True,
                  query={"objectType": "post", "post_type": ["page"], "orderby": "menu_order", "order": "asc", "posts_per_page": 10,
                         "no_found_rows": True, "post__not_in": ["{post_id}"], "meta_query": [{"id": "city", "key": "pnw_city", "value": "1", "compare": "="}]}),
            ], tag="ul"),
        ], tag="section"),
        block("widget", [
            h("h2", "Your local contractor", "widget__title"),
            span("PNW Trenchless", "widget__name"),
            span(f"{ADDRESS} · serving {CITY}", "widget__muted", **when(ADDRESS)),
            block("widget__contact", [
                block("widget__contact-item", [svg("icon-phone.svg"), span(PHONE)], href=TEL),
                block("widget__contact-item", [svg("icon-mail.svg"), span(EMAIL)], href=MAIL, **when(EMAIL)),
            ]),
            span(HOURS, "widget__hours", **when(HOURS)),
            a("Contact us", "/contact/", "link-arrow"),
        ], tag="section"),
        block("widget widget--dark", [
            h("h2", "Talk to Mike today", "widget__title"),
            t("Tell us what's going on. Send a photo or video of the problem if you can."),
            block("widget__phone", [svg("icon-phone.svg"), span(PHONE)], href=TEL),
            btn("Get a quote", "/contact/", "btn--primary", icon="icon-arrow.svg"),
        ], tag="section"),
    ], tag="aside")


def article():
    return section("section section--white", [
        container([block("city-layout", [main_col(), aside()])]),
    ], label="Article + sidebar")


def reviews():
    return section("section section--dark grain", [
        container([
            head("Reviews", 'What customers <span class="serif">say.</span>'),
            block("quotes__grid", [review_loop({"posts_per_page": 2}, label="Reviews (loop)")]),
        ]),
    ], label="Reviews")


SECTIONS = [hero, article, reviews]


def template():
    els = []
    for k, fn in enumerate(SECTIONS):
        els += flatten([fn()], "k" + format(k, "x"))
    return {"key": "city_single", "area": "content", "elements": els}
