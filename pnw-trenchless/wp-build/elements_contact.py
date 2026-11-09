"""Contact page. Built from pnw-trenchless/contact.html (approved 2026-11-09).

Uses the shared helpers and global classes from elements.py. Header and footer come from the
site-wide Bricks templates. Phone, email, address, hours and the Google map embed come from the
Website Settings options page; the form is Fluent Forms "Request a quote".
Unknown facts stay as `tbc` placeholders; FAQ answers carry no draft label (user, 2026-11-09).
"""
from elements import (N, section, container, block, div, h, t, span, a, svg, btn, eyebrow, attrs, link,
                      flatten, when, quote_form, TEL, SMS, MAIL, FB, PHONE, EMAIL, ADDRESS, HOURS, MAP_IFRAME)

HOME = "/"


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", HOME, "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Contact", "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))

    def way(ic, label, value, href, primary=False, new_tab=False):
        return block("reach__item" + (" reach__item--primary" if primary else ""), [
            block("reach__ico", [svg(ic)], tag="span"),
            block("reach__body", [span(label, "reach__label"), span(value, "reach__value")], tag="span"),
            svg("icon-arrow.svg", "reach__go", _attributes=attrs(aria_hidden="true")),
        ], href=link(href, new_tab))

    return section("section svc-hero contact-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("svc-hero__content", [
                    span("Contact", "eyebrow rise"),
                    h("h1", 'Talk to Mike. <span class="serif">Get a straight answer.</span>', "svc-hero__title rise rise--2"),
                    t("Call, text or send the form. You reach Mike Jeisma, the owner, not a call center. Send a photo or video of the problem and he'll tell you what he sees and what it's likely to need.", "svc-hero__lede rise rise--3"),
                    block("owner__creds rise rise--4", [
                        block("owner__cred", [svg("icon-home.svg"), span(ADDRESS)], tag="li", **when(ADDRESS)),
                        block("owner__cred", [svg("icon-shield.svg"), span("WA Reg. #PNWTRT*744KQ")], tag="li"),
                        block("owner__cred", [svg("icon-camera.svg"), span("Free camera estimate")], tag="li"),
                    ], tag="ul"),
                ]),
                block("reach rise rise--4", [
                    way("icon-phone.svg", "Call Mike", PHONE, TEL, primary=True),
                    way("icon-chat.svg", "Text a photo or video", PHONE, SMS),
                    way("icon-mail.svg", "Email", EMAIL, MAIL + "?subject=Quote%20request"),
                    way("icon-fb.svg", "Facebook", "Message us", FB, new_tab=True),
                    block("reach__hours", [
                        span(f"Hours: {HOURS}", **when(HOURS)),
                        span(f"· {tbc('Emergency calls?')}"),
                    ], tag="p"),
                ], _attributes=attrs(aria_label="Ways to reach us")),
            ]),
        ]),
    ], label="Hero")


def connect():
    steps = [("You reach out", "Form, call or text. A photo or short video of the problem helps a lot."),
             ("Mike calls you back", "He asks a few questions and books the camera inspection."),
             ("You see the footage", "You watch the camera run with him and see exactly what's wrong."),
             ("Written quote", "A clear scope and price before any work starts. No pressure.")]
    rows = [("Based in", ADDRESS, ADDRESS), ("Hours", HOURS, HOURS), ("Reply time", tbc("Usually same day"), None),
            ("Licensed", "WA Reg. #PNWTRT*744KQ · bonded &amp; insured", None)]
    return section("section section--tint", [
        container([
            block("connect__grid", [
                quote_form(title_tag="h2", extra_cls="connect__form"),
                block("connect__side", [
                    block("connect__block", [
                        eyebrow("What happens next"),
                        h("h3", 'From your message to a <span class="serif">written quote.</span>', "connect__title"),
                        block("steps-mini", [
                            block("steps-mini__item", [
                                span(f"0{i + 1}", "steps-mini__num"),
                                block("steps-mini__body", [span(ti, "steps-mini__title"), span(tx, "steps-mini__text")], tag="span"),
                            ], tag="li")
                            for i, (ti, tx) in enumerate(steps)
                        ], tag="ol"),
                    ]),
                    block("info-card", [
                        block("info-card__row", [t(term, "info-card__term", tag="dt"), t(val, "info-card__value", tag="dd")], **(when(cond) if cond else {}))
                        for term, val, cond in rows
                    ], tag="dl"),
                ]),
            ]),
        ]),
    ], sid="estimate", label="Form + details")


def urgent():
    return section("section urgent section--white", [
        container([
            block("urgent__card", [
                block("urgent__ico", [svg("icon-alert.svg")], tag="span"),
                block("urgent__text", [
                    h("h2", 'Sewer backing up <span class="serif">right now?</span>', "urgent__title"),
                    t(f"Stop running water in the house, then call or text Mike. He'll tell you what to do next. {tbc('Confirm emergency / after-hours availability.')}"),
                ]),
                block("urgent__actions", [
                    btn(f"Call {PHONE}", TEL, "btn--primary", icon="icon-phone.svg", icon_left=True),
                    btn("Text a photo", SMS, "btn--base btn--outline", icon="icon-chat.svg", icon_left=True),
                ]),
            ]),
        ]),
    ], label="Urgent")


def area():
    cities = [("Spokane", "Metro"), ("Spokane Valley", "East"), ("Deer Park", "North"), ("Clayton", "North"), ("Stevens County", "North"), ("Spokane County", "+ nearby")]
    return section("section section--tint", [
        container([
            block("split split--center split--areas", [
                block("areas__text", [
                    eyebrow("Where we work"),
                    h("h2", 'Serving Spokane &amp; <span class="serif">Stevens counties.</span>'),
                    t(f"Based in {ADDRESS}. Not on the list? Call or text anyway. If you're nearby, we'll usually come out."),
                    block("city-list", [block("", [block("city", [span(c), span(n, "city__note")], href="/#areas")], tag="li") for c, n in cities], tag="ul"),
                ]),
                block("map", [
                    # The Google map embed (Website Settings) replaces the illustrated map when it is filled in.
                    t(MAP_IFRAME, "map__embed", tag="div", **when(MAP_IFRAME)),
                    svg("art-service-map-area.svg", _attributes=attrs(role="img", aria_label="Service area map: Spokane, Spokane Valley, Deer Park and Clayton"), **when(MAP_IFRAME, "==")),
                    t("APPROXIMATE SERVICE AREA · SPOKANE &amp; STEVENS COUNTIES", "map__caption", tag="figcaption", **when(MAP_IFRAME, "==")),
                ], tag="figure"),
            ]),
        ]),
    ], label="Service area")


FAQ = [
    ("Is the camera estimate really free?", [f"Yes. Mike runs the camera, shows you the footage and gives you a written quote. {tbc('Confirm what&#39;s included and any travel limits.')}"], True),
    ("How fast will I hear back?", [f"{tbc('Typical reply time, e.g. same day on weekdays.')} If it's urgent, call or text instead of using the form."], True),
    ("What should I send with my message?", ["Your address or city, what you've noticed (slow drains, backups, wet spots, smells) and, if you can, a photo or short video. That's enough for Mike to tell you what's likely going on."], False),
    ("Do you work outside the listed areas?", [f"We serve Spokane, Spokane Valley, Deer Park, Clayton, Stevens County and Spokane County. If you're nearby, ask."], False),
]


def faq():
    items = []
    for q, answers, draft in FAQ:
        content = [t(x) for x in answers]
        items.append(block("faq__item", [
            block("", [h("h3", q, "faq__q")], label="Title", _hidden={"_cssClasses": "accordion-title-wrapper"}),
            block("faq__answer", content, label="Content", _hidden={"_cssClasses": "accordion-content-wrapper"}),
        ], label="Item"))
    return section("section section--white", [
        container([
            block("split split--faq", [
                block("sticky-aside", [
                    eyebrow("Before you call"),
                    h("h2", 'Quick <span class="serif">answers.</span>'),
                    t("Anything else? Call or text Mike and he'll give you a straight answer."),
                    btn(PHONE, TEL, "btn--base btn--outline", icon="icon-phone.svg", icon_left=True),
                ]),
                N("accordion-nested", "faq__list", items, expandItem="0", independentToggle=True),
            ]),
        ]),
    ], label="FAQ")


SECTIONS = [hero, connect, urgent, area, faq]


def page():
    return {
        "key": "contact",
        "post_type": "page",
        "title": "Contact",
        "slug": "contact",
        "excerpt": "Call or text Mike, email, or request a free camera estimate. PNW Trenchless serves Spokane, Spokane Valley, Deer Park, Clayton and Stevens County.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "c" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
