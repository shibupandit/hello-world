"""Service page: Water Line Pulling. Built from pnw-trenchless/service-water-line-pulling.html (2026-11-09).
Generated from elements_bursting.py (same blocks), then rewritten for water lines. No "inside the pipe"
section (there are no camera stills for water lines); the projects strip is a query loop over
`project` posts whose service is "Water line".

Uses the shared helpers and global classes from elements.py. Header and footer come from the
site-wide Bricks templates (101 / 102), so this file only builds the page content.
Unknown facts stay as `tbc` placeholders; FAQ answers carry no draft label (user, 2026-11-09).
"""
from elements import (N, section, container, block, div, h, t, span, a, svg, img, btn, eyebrow, attrs, link,
                      head, head_split, flatten, review_loop, TEL, PHONE, ADDRESS)
from elements_projects import project_card, q, REAL_ONLY

HOME = "/"
LINING = "/services/sewer-pipe-lining/"
BURSTING = "/services/pipe-bursting/"


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", HOME, "crumbs__link")], tag="li"),
            block("crumbs__item", [a("Services", "/#services", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Water Line Pulling", "text-accent-light", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    return section("section svc-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("stack-l", [
                    span("CTS poly · pressure tested", "eyebrow rise"),
                    h("h1", 'Trenchless water line <span class="serif">pulling</span> in Spokane', "accent-light rise rise--2"),
                    t("Replace an old, leaking or corroded water service line without trenching your yard. We pull a new CTS poly line underground, reconnect it, and test it for pressure and leaks.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("Get a water line quote", "/contact/", "btn--primary", icon="icon-arrow.svg"),
                        btn(f"Call or text {PHONE}", TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
                    ]),
                    block("byline rise rise--5", [
                        span("MJ", "byline__av", _attributes=attrs(aria_hidden="true")),
                        span(f"Written &amp; reviewed by <strong>Mike Jeisma</strong>, owner, 14+ years in sewer &amp; water line work · Updated {tbc('Month YYYY')}", "grow"),
                    ]),
                ]),
                block("figure-stack rise rise--4", [
                    block("svc-hero__art", [img("job-waterline.jpg", "cover-img", alt="Access pit with the new blue water line in place next to the meter box")]),
                    t("A small access pit at the meter, with the new line pulled in.", "caption-light", tag="figcaption"),
                ], tag="figure"),
            ]),
        ]),
    ], label="Hero")


def answer():
    facts = [("Typical job time", f"{tbc('X')} day(s)"), ("Digging", "Small access pits"),
             ("New line", "CTS poly, no rust or scale"), ("Warranty", f"{tbc('X')} years")]
    return section("section section--tint section--tight", [
        container([
            block("answer__grid", [
                block("answer__card", [
                    eyebrow("Quick answer"),
                    h("h2", 'What is <span class="serif">water line pulling?</span>'),
                    t("Water line pulling is a trenchless way to replace the water service line that feeds your home. Instead of digging a trench the whole length of the line, we open small access pits and pull a new CTS poly line underground. Then we reconnect it and test it for pressure and leaks. The new line doesn't rust or build up scale, so you get your water pressure back."),
                ]),
                block("facts", [block("fact", [span(l, "label-light"), span(v, "fact__value")]) for l, v in facts]),
            ]),
        ]),
    ], label="Quick answer")


def fit():
    yes = ["Old galvanized service line", "Rusty or discolored water at the tap", "Low water pressure through the whole house",
           "Repeated leaks or a wet spot in the yard", "Lines under lawns, driveways and landscaping"]
    no = [("Low pressure at one faucet only", "A plumber", None), ("Leak on the city side of the meter", "Your water utility", None),
          ("Slow drains, backups or sewer smell", "Sewer lining", LINING), ("Collapsed or broken sewer pipe", "Pipe bursting", BURSTING)]
    return section("section section--white", [
        container([
            head("Is a new water line right for you?", 'When a new line fixes it, <span class="serif">and when it won\'t.</span>',
                 "A new service line fixes problems that start in the line itself. If the trouble is somewhere else, we'll tell you before anything is dug."),
            block("grid-2", [
                block("fit-card fit-card--yes", [
                    block("fit-card__head", [block("fit-card__ico", [svg("icon-check.svg")], tag="span"), h("h3", "Good candidates", "title-card")]),
                    block("list-ruled", [t(x, "fit-card__item", tag="li") for x in yes], tag="ul"),
                ]),
                block("fit-card fit-card--no", [
                    block("fit-card__head", [block("fit-card__ico", [svg("icon-alert.svg")], tag="span"), h("h3", "Usually a different fix", "title-card")]),
                    block("list-ruled", [
                        block("fit-card__item", [span(x), a(alt, url, "fit-card__alt") if url else span(alt, "fit-card__alt fit-card__alt--static")], tag="li")
                        for x, alt, url in no
                    ], tag="ul"),
                ]),
            ]),
        ]),
    ], label="Is a new line right")


def how():
    steps = [("Find the line", "We find where your service line runs, from the meter to the house, and check what it's made of and why it's failing."),
             ("Locate &amp; dig small pits", f"Utilities are located, then we dig small access pits instead of a trench. {tbc('Where the pits go and typical size')}."),
             ("Pull the new line", f"A new CTS poly line is pulled underground along the path, {tbc('method Mike uses')}."),
             ("Reconnect", f"The new line is connected at the meter and at the house, {tbc('fittings and shutoff details')}."),
             ("Pressure &amp; leak test", "We test the new line for pressure and leaks before the job is done."),
             ("Restore", "The pits are backfilled and the site is cleaned up. Your water is off for hours, not days.")]
    return section("section section--dark grain", [
        container([
            head_split("How water line pulling works", 'The water line pull, <span class="serif">step by step.</span>',
                       t("From finding the line to the pressure test, here's what happens under your yard.", "section__intro section__intro--narrow")),
            block("stages", [svg("art-water-stages.svg", _attributes=attrs(role="img", aria_label="Three stages of a water line pull: old line with rust and scale, new CTS poly line pulled in between two small pits, the line reconnected and pressure tested"))], tag="figure"),
            block("steps steps--6", [block("step", [h("h3", ti, "step__title"), t(tx)], tag="li") for ti, tx in steps], tag="ol"),
        ]),
    ], sid="how", label="How water line pulling works")


def specs():
    rows = [("New line", "CTS poly (polyethylene, copper tube size)"), ("Inside the pipe", "No rust or scale buildup"),
            ("Sizes", f"{tbc('X&quot;')} to {tbc('X&quot;')}"), ("Pipe rating", tbc("e.g. pressure class, standard, as applicable")),
            ("Testing", "Pressure and leak tested"), ("Warranty", f"{tbc('X')} years · {tbc('transferable?')}")]
    return section("section section--white", [
        container([
            block("split", [
                block("section__head", [
                    eyebrow("What you get"),
                    h("h2", 'What goes <span class="serif">into the ground.</span>'),
                    t("Real specs from the line we install, not a sales sheet.", "section__intro"),
                    block("note note--tint", [svg("icon-alert.svg"), t("<strong>Straight talk:</strong> a new service line fixes pressure lost in a corroded or leaking line. If the low pressure comes from the city main or your house plumbing, a new line won't fix it, and we'll tell you that before we start.")]),
                ]),
                block("spec-table", [block("spec-table__row", [span(k, "label"), span(v, "spec-table__value")]) for k, v in rows]),
            ]),
        ]),
    ], label="Specs")


def cost():
    factors = ["Length of the line, meter to house", "How deep the line is buried", "What's on top: lawn, driveway, trees",
               "Soil and rock conditions", "Connections at the meter and the house"]
    return section("section section--tint", [
        container([
            block("split-wide", [
                block("text-block cost__text", [
                    eyebrow("Cost"),
                    h("h2", 'How much does a new water line <span class="serif">cost in Spokane?</span>'),
                    t(f"Most residential water line pulls we do fall between {tbc('$X,XXX and $X,XXX')}.", "cost__range"),
                    t("You get a written quote after we've looked at your line, so it's based on your actual job, not a guess. Compare it against a dig-and-replace quote plus the cost to restore your lawn, driveway or landscaping."),
                    t(f"<strong>Included:</strong> {tbc('pits, new CTS poly line, reconnections, pressure test, permit, warranty')}", "cost__incl"),
                ]),
                block("card-dark cost-card", [
                    h("h3", "What affects the price", "cost-card__title"),
                    block("list-ruled-dark", [block("num-row", [span(f"0{i + 1}", "num-row__num"), span(x)], tag="li") for i, x in enumerate(factors)], tag="ul"),
                    btn("Get my written quote", "/contact/", "btn--primary btn-block", icon="icon-arrow.svg"),
                ]),
            ]),
        ]),
    ], label="Cost")


def owner():
    return section("section section--dark grain", [
        container([
            block("owner__grid", [
                block("owner__photo", [img("trailer.jpg", "cover-img", alt="The PNW Trenchless equipment trailer")]),
                block("stack-l", [
                    eyebrow("Who does the work"),
                    h("h2", f'Mike Jeisma has replaced {tbc("dozens of")} <span class="serif">Inland Northwest</span> water lines.', "accent-light"),
                    t(tbc("Mike, 2–3 sentences: what he sees in old galvanized lines around Spokane, how he keeps water downtime short, why he pressure tests every line."), "owner__quote", tag="blockquote"),
                    block("owner__creds", [
                        block("owner__cred", [svg("icon-shield.svg"), span(tbc("Licensing or certification for water service work"))], tag="li"),
                        block("owner__cred", [svg("icon-check.svg"), span("WA Reg. #PNWTRT*744KQ")], tag="li"),
                        block("owner__cred", [svg("icon-home.svg"), span(f"Family-owned, {ADDRESS}")], tag="li"),
                    ], tag="ul"),
                    a("About Mike", "/about/", "link-arrow"),
                ]),
            ]),
        ]),
    ], sid="mike", label="Who does the work")


def jobs():
    return section("section section--white", [
        container([
            head_split("Water line projects", 'Recent water <span class="serif">line jobs.</span>', a("All projects", "/projects/", "link-arrow")),
            block("grid-3-2", [project_card(q(posts_per_page=3, meta_query=[REAL_ONLY, {"id": "svc", "key": "service", "value": "water_line", "compare": "="}]),
                                          label="Water line projects (loop)")], tag="ul"),
        ]),
    ], label="Water line projects (loop)")


def quotes():
    return section("section section--dark grain", [
        container([
            head("Reviews that mention water lines", 'What water line customers <span class="serif">say.</span>'),
            block("quotes__grid", [review_loop({"posts_per_page": 2, "meta_query": [{"id": "service", "key": "services", "value": '"__POST_ID__"', "compare": "LIKE"}]}, label="Water line reviews (loop)")]),
        ]),
    ], label="Reviews")


FAQ = [
    ("How long will my water be off?", [f"Hours, not days. The old line keeps working while the new one goes in, and we tell you exactly when the water goes off for the reconnection. {tbc('Typical shutoff time.')}"], True),
    ("What is CTS poly pipe?", ["It's polyethylene water pipe made to copper tube size (CTS), so it connects to standard fittings. It doesn't rust or build up scale inside like old galvanized pipe does."], True),
    ("Will a new line fix my low water pressure?", ["If the pressure is lost in a corroded or leaking service line, yes. If the cause is the city main or your house plumbing, a new line won't fix it, and we'll tell you before you spend the money."], True),
    ("How much digging is there?", [f"Small access pits instead of a trench along the whole line. {tbc('Where the pits usually go and typical size.')}"], True),
    ("Is the water line my responsibility or the city's?", [tbc("Where the homeowner's part of the line starts in Spokane and the surrounding areas.")], False),
    ("How long does a poly water line last?", [tbc("Expected life and PNW warranty terms.")], False),
    ("Do I need a permit to replace my water line?", [tbc("Yes / no, which jurisdictions, and how it's handled.")], False),
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
                    eyebrow("Water line FAQ"),
                    h("h2", 'Straight <span class="serif">answers.</span>'),
                    t("Answers come from Mike. Drafts are marked until he confirms them."),
                    btn(PHONE, TEL, "btn--base btn--outline", icon="icon-phone.svg", icon_left=True),
                ]),
                N("accordion-nested", "faq__list", items, expandItem="0", independentToggle=True),
            ]),
        ]),
    ], sid="faq", label="FAQ")


def more():
    rel = [("icon-liner.svg", "Sewer pipe lining", LINING), ("icon-burst.svg", "Pipe bursting", BURSTING),
           ("icon-patch.svg", "Point repairs", "/services/point-repairs/"), ("icon-yard.svg", "Trenchless vs. digging: full comparison", "/#how")]
    cities = ["Spokane", "Spokane Valley", "Deer Park", "Clayton", "Stevens County", "Spokane County"]
    return section("section section--tint", [
        container([
            block("more__grid", [
                block("", [
                    eyebrow("Related services"),
                    block("related", [
                        block("", [block("related__link", [block("related__ico", [svg(ic)], tag="span"), span(lbl, "grow"), svg("icon-arrow.svg", "related__go")], href=u)], tag="li")
                        for ic, lbl, u in rel
                    ], tag="ul"),
                ], label="Related services"),
                block("stack-m", [
                    eyebrow("Water line pulling near you"),
                    h("h2", 'We replace water lines <span class="serif">across Spokane &amp; Stevens counties.</span>', "near__title"),
                    block("chip-row", [a(c, "/#areas", "near__city") for c in cities]),
                ]),
            ]),
        ]),
    ], label="Related + near you")




SECTIONS = [hero, answer, fit, how, specs, cost, owner, jobs, quotes, faq, more]


def page():
    return {
        "key": "water-line-pulling", "post_type": "service", "title": "Water Line Pulling", "slug": "water-line-pulling",
        "excerpt": "Trenchless water line replacement in Spokane: a new CTS poly line pulled underground through small access pits, reconnected and tested for pressure and leaks.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "w" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
