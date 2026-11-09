"""Who We Serve page (/who-we-serve/). Built from pnw-trenchless/who-we-serve.html (approved 2026-11-09).

Based on the Home "Who we work for" section. Phone, address and contact come from Website Settings;
the projects strip is a query loop over real `project` posts (cards shared with elements_projects.py).
Unknown facts stay as `tbc` placeholders.
"""
from elements import (N, section, container, block, h, t, span, a, svg, img, btn, eyebrow, attrs, link,
                      head, head_split, flatten, TEL, PHONE)
from elements_projects import project_card, q, REAL_ONLY

SERVICES = [("icon-liner.svg", "Sewer pipe lining", "/services/sewer-pipe-lining/", "A new pipe inside the old one, for cracks, leaks and roots."),
            ("icon-burst.svg", "Pipe bursting", "/services/pipe-bursting/", "A brand-new HDPE pipe pulled in, for collapsed or undersized lines."),
            ("icon-drop.svg", "Water line pulling", "/services/water-line-pulling/", "A new CTS poly water line, pressure and leak tested."),
            ("icon-patch.svg", "Point repairs", "/services/point-repairs/", "One damaged spot relined, the rest of the pipe left as it is.")]


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", "/", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Who We Serve", "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    jumps = [("icon-home.svg", "Homeowners", "Sewer &amp; water lines under your yard", "#homes"),
             ("icon-building.svg", "Commercial properties", "Stay open while we work", "#commercial"),
             ("icon-factory.svg", "Industrial &amp; municipal", "Larger lines, documented", "#industrial")]
    return section("section svc-hero serve-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("svc-hero__content", [
                    span("Who we serve", "eyebrow rise"),
                    h("h1", 'Homes, businesses <span class="serif">and industrial sites.</span>', "svc-hero__title rise rise--2"),
                    t("Trenchless repair and replacement for residential, commercial and industrial properties, from a home's sewer line to lines under parking lots, roadways and working facilities.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("Request a quote", "/contact/", "btn--primary", icon="icon-arrow.svg"),
                        btn(f"Call or text {PHONE}", TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
                    ]),
                ]),
                block("jump rise rise--4", [span("Pick your property", "jump__label")] + [
                    block("jump__item", [
                        block("jump__ico", [svg(ic)], tag="span", _attributes=attrs(aria_hidden="true")),
                        block("jump__text", [span(ti, "jump__title"), span(note, "jump__note")], tag="span"),
                        svg("icon-arrow.svg", "jump__go", _attributes=attrs(aria_hidden="true")),
                    ], href=u) for ic, ti, note, u in jumps
                ], tag="nav", _attributes=attrs(aria_label="Jump to a property type")),
            ]),
        ]),
    ], label="Hero")


def cols(left_title, left, right_title, right):
    def col(title, items, check):
        return block("who__col", [
            h("h3", title, "who__h3"),
            block("who__list" + (" who__list--check" if check else ""), [t(x, "who__item", tag="li") for x in items], tag="ul"),
        ])
    return block("who__cols", [col(left_title, left, False), col(right_title, right, True)])


def kicker(icon, text, dark=False):
    return block("who__kicker" + (" who__kicker--dark" if dark else ""), [
        block("who__ico", [svg(icon)], tag="span", _attributes=attrs(aria_hidden="true")), span(text)], tag="span")


def homes():
    return section("section section--white", [
        container([
            block("who", [
                block("who__media", [
                    block("who__img", [img("job-lawn-restored.jpg", None, alt="A front lawn after the job, with the pit backfilled and the grass back in place")]),
                    t("After a sewer repair: one small pit, backfilled, and the lawn back in place.", "who__cap", tag="figcaption"),
                ], tag="figure"),
                block("who__text", [
                    kicker("icon-home.svg", "Homeowners"),
                    h("h2", 'Your line fixed. <span class="serif">Your yard left alone.</span>'),
                    t("Sewer and water lines under lawns, driveways, patios and mature trees. Small access points instead of a torn-up yard.", "who__lede"),
                    cols("What we see at homes", ["Roots in old clay sewer lines", "Cracked, offset or collapsed pipe", "Orangeburg (fiber) sewer pipe", "Old galvanized water service, low pressure"],
                         "What you get", ["Camera footage you keep", "A written quote before any work", "Water off for hours, not days", "Mike on the job, start to finish"]),
                    block("who__links", [a(lbl, u, "who__link") for _, lbl, u, _ in SERVICES]),
                ]),
            ]),
        ]),
    ], sid="homes", label="Homeowners")


def commercial():
    return section("section section--tint", [
        container([
            block("who who--reverse", [
                block("who__media", [
                    block("who__img", [img("job-access-pit.jpg", None, alt="A shored access pit, with the camera reel and jetter beside it")]),
                    t(f"A small, shored access pit: the footprint we plan for instead of a trench. {tbc('Replace with a photo from a commercial job')}", "who__cap", tag="figcaption"),
                ], tag="figure"),
                block("who__text", [
                    kicker("icon-building.svg", "Commercial properties"),
                    h("h2", 'Keep the doors open <span class="serif">while we fix the line.</span>'),
                    t("We choose methods that keep your property open and running during the work, with less disruption to parking, landscaping and tenants.", "who__lede"),
                    cols("Where trenchless helps", ["Lines under parking lots &amp; hardscape", "Lines under landscaping and entrances", "Sites that can't close for a dig"],
                         "What you get", ["Clear schedule and budget up front", "Lower restoration costs", "Camera footage for your records"]),
                    block("who__tags", [span("Property types", "who__tags-label"), span(tbc("Mike to confirm: e.g. retail, offices, apartments, HOAs, churches, schools"))]),
                ]),
            ]),
        ]),
    ], sid="commercial", label="Commercial")


def industrial():
    facts = [("Line sizes", f"{tbc('X&quot;')} to {tbc('X&quot;')}"), ("Longest run", tbc("X ft")), ("Focus", "Code &amp; compliance")]
    steps = [("Site &amp; pipe condition evaluation", "Access, surface use, soil and nearby utilities, before anything is planned."),
             ("CCTV assessment", "The full line on camera, with defects and distances recorded."),
             ("Written recommendation", "The method that fits, with a lifecycle cost comparison against the alternatives."),
             ("The work", f"Scheduled around your operations. {tbc('Night / weekend work, traffic control, permits')}"),
             ("Final testing &amp; documentation", "Final camera run and the records you need for your files.")]
    return section("section section--dark grain", [
        container([
            block("ind", [
                block("ind__text", [
                    kicker("icon-factory.svg", "Industrial &amp; municipal", dark=True),
                    h("h2", 'Larger lines. <span class="serif">Every step documented.</span>'),
                    t("Larger lines and longer runs, with a CCTV assessment, a written recommendation, and documentation from evaluation through final testing.", "who__lede"),
                    block("ind__facts", [block("ind__fact", [span(l, "ind__fact-label"), span(v, "ind__fact-value")], tag="li") for l, v in facts], tag="ul"),
                ]),
                block("rv-steps", [
                    block("rv-steps__item", [span(f"0{i + 1}", "rv-steps__num"),
                                             block("rv-steps__body", [span(ti, "rv-steps__title"), span(tx, "rv-steps__text")], tag="span")], tag="li")
                    for i, (ti, tx) in enumerate(steps)
                ], tag="ol"),
            ]),
        ]),
    ], sid="industrial", label="Industrial &amp; municipal")


def side():
    auds = ["Homes", "Commercial", "Industrial &amp; municipal"]
    rows = [("Typical lines", ["Sewer lateral, water service", "Sewer and water lines under paved areas", "Larger lines, longer runs"]),
            ("What we plan around", ["Lawn, driveway, trees, your water use", "Parking, tenants, opening hours", "Operations, safety, compliance"]),
            ("Before the work", ["Camera inspection and a written quote", "Schedule and budget up front", "Site evaluation, CCTV assessment, written recommendation"]),
            ("After the work", ["Before and after footage", "Footage for your records", "Final testing and documentation"])]
    head_row = block("ws-row ws-row--head", [span("What changes", "eyebrow")] + [span(x, "ws-row__head") for x in auds],
                     _attributes=attrs(role="row"))
    body = [block("ws-row", [span(lbl, "ws-row__label", _attributes=attrs(role="rowheader"))] + [
        block("ws-row__cell", [span(aud, "ws-row__aud", _attributes=attrs(aria_hidden="true")), span(v)], _attributes=attrs(role="cell"))
        for aud, v in zip(auds, vals)], _attributes=attrs(role="row")) for lbl, vals in rows]
    return section("section section--white", [
        container([
            head("Side by side", 'Same honest process, <span class="serif">planned for your property.</span>',
                 "Every job starts with a camera inspection and ends with a final camera run. What changes is what we plan around."),
            block("ws-rows", [head_row] + body, _attributes=attrs(role="table", aria_label="What changes by property type")),
        ]),
    ], label="Side by side")


def services():
    return section("section section--tint", [
        container([
            head_split("Services", 'Four ways we fix it, <span class="serif">for any property.</span>',
                       t("The camera decides the method. Here's what each one is for.", "section__intro section__intro--narrow")),
            block("ws-svc", [
                block("", [block("ws-svc__item", [
                    block("ws-svc__ico", [svg(ic)], tag="span", _attributes=attrs(aria_hidden="true")),
                    span(ti, "ws-svc__title"), span(tx, "ws-svc__text"),
                    svg("icon-arrow.svg", "ws-svc__go", _attributes=attrs(aria_hidden="true")),
                ], href=u)], tag="li") for ic, ti, u, tx in SERVICES
            ], tag="ul"),
        ]),
    ], label="Services")


def projects():
    return section("section section--white", [
        container([
            head_split("Recent work", 'Real jobs. <span class="serif">Real yards.</span>', a("All projects", "/projects/", "link-arrow")),
            block("pcards", [project_card(q(posts_per_page=3, meta_query=[REAL_ONLY]))], tag="ul"),
        ]),
    ], label="Projects (loop)")


FAQ = [
    ("Do you work on commercial properties?", ["Yes. We work on residential, commercial and industrial properties, including lines under parking lots and hardscape, and we choose methods that keep your property open during the work."]),
    ("Can my business stay open during the work?", [f"In most cases, yes: trenchless work needs small access points instead of a trench across your lot. {tbc('Whether Mike schedules after-hours or weekend work.')}"]),
    ("Do you work with property managers and HOAs?", [tbc("Yes / no, and how quotes and approvals are handled.")]),
    ("Do you take municipal or public work?", [tbc("Which agencies, bidding, prevailing wage, prequalification.")]),
    ("Are you licensed, bonded and insured?", [f"Yes. PNW Trenchless is licensed, bonded and insured, WA Contractor Reg. #PNWTRT*744KQ. {tbc('Certificate of insurance on request?')}"]),
    ("What paperwork do I get at the end?", [f"The before and after camera footage on every job. Industrial and municipal jobs also get documentation from evaluation through final testing. {tbc('Report format.')}"]),
]


def faq():
    items = [block("faq__item", [
        block("", [h("h3", qu, "faq__q")], label="Title", _hidden={"_cssClasses": "accordion-title-wrapper"}),
        block("faq__answer", [t(x) for x in ans], label="Content", _hidden={"_cssClasses": "accordion-content-wrapper"}),
    ], label="Item") for qu, ans in FAQ]
    return section("section section--tint", [
        container([
            block("split split--faq", [
                block("sticky-aside", [
                    eyebrow("Questions"),
                    h("h2", 'Straight <span class="serif">answers.</span>'),
                    t("Answers come from Mike. Drafts are marked until he confirms them."),
                    btn(PHONE, TEL, "btn--base btn--outline", icon="icon-phone.svg", icon_left=True),
                ]),
                N("accordion-nested", "faq__list", items, expandItem="0", independentToggle=True),
            ]),
        ]),
    ], sid="faq", label="FAQ")




SECTIONS = [hero, homes, commercial, industrial, side, services, projects, faq]


def page():
    return {
        "key": "who-we-serve", "post_type": "page", "title": "Who We Serve", "slug": "who-we-serve",
        "excerpt": "Trenchless sewer and water line repair for homeowners, commercial properties and industrial and municipal sites across Spokane and Stevens counties.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "v" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
