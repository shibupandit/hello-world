"""Service page: Pipe Bursting. Built from pnw-trenchless/service-pipe-bursting.html (approved 2026-11-09).
Generated from elements_lining.py (same blocks), then rewritten for bursting.

Uses the shared helpers and global classes from elements.py. Header and footer come from the
site-wide Bricks templates (101 / 102), so this file only builds the page content.
Unknown facts stay as `tbc` placeholders; FAQ answers carry no draft label (user, 2026-11-09).
"""
from elements import (N, section, container, block, div, h, t, span, a, svg, img, btn, eyebrow, attrs, link,
                      head, head_split, flatten, review_loop, TEL, PHONE, ADDRESS)

HOME = "/"
LINING = "/services/sewer-pipe-lining/"


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", HOME, "crumbs__link")], tag="li"),
            block("crumbs__item", [a("Services", "/#services", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Pipe Bursting", "text-accent-light", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    return section("section svc-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("stack-l", [
                    span("HDPE · full replacement", "eyebrow rise"),
                    h("h1", 'Trenchless pipe <span class="serif">bursting</span> in Spokane', "accent-light rise rise--2"),
                    t("Replace a collapsed, crushed or undersized sewer line without trenching your yard. A bursting head breaks the old pipe apart underground while a brand-new HDPE pipe is pulled in right behind it, through two small access pits.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("See if bursting fits your line", "/contact/", "btn--primary", icon="icon-arrow.svg"),
                        btn(f"Call or text {PHONE}", TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
                    ]),
                    block("byline rise rise--5", [
                        span("MJ", "byline__av", _attributes=attrs(aria_hidden="true")),
                        span(f"Written &amp; reviewed by <strong>Mike Jeisma</strong>, owner, 14+ years in trenchless repair · Updated {tbc('Month YYYY')}", "grow"),
                    ]),
                ]),
                block("figure-stack rise rise--4", [
                    block("svc-hero__art", [img("job-access-pit.jpg", "cover-img", alt="A shored access pit in a front lawn, with the camera reel and jetter beside it")]),
                    t("One of the small access pits: shored, with the camera and jetter on hand.", "caption-light", tag="figcaption"),
                ], tag="figure"),
            ]),
        ]),
    ], label="Hero")


def answer():
    facts = [("Typical job time", f"{tbc('X')} day(s)"), ("Digging", "2 small access pits"),
             ("New pipe", "HDPE, 50+ yr lifespan"), ("Warranty", f"{tbc('X')} years")]
    return section("section section--tint section--tight", [
        container([
            block("answer__grid", [
                block("answer__card", [
                    eyebrow("Quick answer"),
                    h("h2", 'What is <span class="serif">pipe bursting?</span>'),
                    t("Pipe bursting is a trenchless way to replace a sewer line. A cone-shaped bursting head is pulled through the old pipe from one access pit to another. It breaks the old pipe outward into the soil, and a new, seamless HDPE pipe follows behind it in the same path. You end up with a completely new pipe, and it can be a size larger than the old one."),
                ]),
                block("facts", [block("fact", [span(l, "label-light"), span(v, "fact__value")]) for l, v in facts]),
            ]),
        ]),
    ], label="Quick answer")


def fit():
    yes = ["Collapsed or crushed sections", "Orangeburg (fiber pipe) that's deformed", "Clay pipe that's broken or badly offset",
           "Pipe too small for the household (upsize)", "Long runs under lawns, driveways and landscaping"]
    no = [("Pipe still round, with cracks or roots", "Pipe lining", LINING), ("Line under a slab or inside the house", "Pipe lining", LINING),
          ("Bellies or sags holding water", "Spot excavation", None), ("One damaged spot on a good line", "Point repair", "/services/point-repairs/")]
    return section("section section--white", [
        container([
            head("Is bursting right for your pipe?", 'When bursting works, <span class="serif">and when it doesn\'t.</span>',
                 "Bursting replaces the whole run between two pits, so it shines when the old pipe is past saving. The camera shows which fix fits, and we'll show you the footage either way."),
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
    ], label="Is bursting right")


def how():
    steps = [("Camera inspection", "We record the full line, measure its length and depth, and mark every defect and connection."),
             ("Locate &amp; dig two pits", f"Utilities are located, then we dig one small pit at each end of the run. {tbc('Typical pit size')}."),
             ("Fuse the new pipe", f"Lengths of HDPE are heat-fused into one continuous, joint-free pipe, sized for your line {tbc('or upsized')}."),
             ("Burst &amp; pull", f"The bursting head is pulled through the old line, {tbc('static / pneumatic')}, breaking it outward as the new pipe follows."),
             ("Reconnect", f"The new pipe is connected at the house and at the main or septic, {tbc('and any branch lines reopened')}."),
             ("Verify &amp; restore", "A final camera run proves the result, then the pits are backfilled and the site is cleaned up. You get the footage.")]
    return section("section section--dark grain", [
        container([
            head_split("How pipe bursting works", 'The bursting process, <span class="serif">step by step.</span>',
                       t("From the first camera run to the final one, here's what happens under your yard.", "section__intro section__intro--narrow")),
            block("stages", [svg("art-bursting-stages.svg", _attributes=attrs(role="img", aria_label="Three stages of pipe bursting: broken old pipe, bursting head splitting it as new HDPE pipe follows, new seamless HDPE pipe"))], tag="figure"),
            block("steps steps--6", [block("step", [h("h3", ti, "step__title"), t(tx)], tag="li") for ti, tx in steps], tag="ol"),
        ]),
    ], sid="how", label="How bursting works")


def inside():
    def still(mod, tag, tag_mod, right, cap_bold, label):
        # mod is the job photo file; label is its alt text (client photos, 2026-11-09).
        return block("still", [
            block("still__feed still__media", [
                img(mod, "cover-img", alt=label),
                block("feed__hud feed__hud--top", [span(tag, ("still__tag " + tag_mod).strip()), span(right)]),
            ]),
            t(f"<strong>{cap_bold}</strong>", "still__cap", tag="figcaption"),
        ], tag="figure")

    return section("section section--tint", [
        container([
            head("Before &amp; after", 'See it from <span class="serif">inside the pipe.</span>',
                 "Real photos from our jobs: the old pipe we find, and the new pipe that replaces it."),
            block("grid-2", [
                still("job-old-pipe.jpg", "Before", "", "OLD PIPE", "Before: the old line, worn out and full of buildup.", "A section of old sewer pipe cut open, with heavy buildup inside"),
                still("job-pipe-connection.jpg", "After", "tag--after", "NEW PIPE", "After: the new pipe connected in the access pit.", "The new sewer pipe connected in the access pit"),
            ]),
        ]),
    ], label="Before and after")


def specs():
    rows = [("New pipe", "HDPE (high-density polyethylene)"), ("Joints", "Heat-fused, no joints"),
            ("Sizes", f"{tbc('X&quot;')} to {tbc('X&quot;')} · upsizing {tbc('up to X&quot;')}"), ("Pipe rating", tbc("e.g. SDR 17, ASTM F714, as applicable")),
            ("Expected life", "50+ years"), ("Warranty", f"{tbc('X')} years · {tbc('transferable?')}")]
    return section("section section--white", [
        container([
            block("split", [
                block("section__head", [
                    eyebrow("What you get"),
                    h("h2", 'What goes <span class="serif">into the ground.</span>'),
                    t("Real specs from the pipe we install, not a sales sheet.", "section__intro"),
                    block("note note--tint", [svg("icon-alert.svg"), t("<strong>Straight talk:</strong> the new pipe follows the old line's path. If the old line has a sag, that spot may need fixing separately, and the camera shows us before we start.")]),
                ]),
                block("spec-table", [block("spec-table__row", [span(k, "label"), span(v, "spec-table__value")]) for k, v in rows]),
            ]),
        ]),
    ], label="Specs")


def cost():
    factors = ["Length of the run being replaced", "Depth of the pipe and the access pits", "Pipe size, and whether we upsize it",
               "Soil and rock conditions", "Reconnections and surface restoration"]
    return section("section section--tint", [
        container([
            block("split-wide", [
                block("text-block cost__text", [
                    eyebrow("Cost"),
                    h("h2", 'How much does pipe bursting <span class="serif">cost in Spokane?</span>'),
                    t(f"Most residential pipe bursting jobs we do fall between {tbc('$X,XXX and $XX,XXX')}.", "cost__range"),
                    t("Your written quote comes after the camera inspection, so it's based on your actual line, not a guess. Compare it against a dig-and-replace quote plus the cost to restore your lawn, driveway or landscaping."),
                    t(f"<strong>Included:</strong> {tbc('inspection video, pits, new HDPE pipe, reconnections, permit, final video, warranty')}", "cost__incl"),
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
                    h("h2", f'Mike Jeisma has replaced {tbc("hundreds of")} <span class="serif">Inland Northwest</span> sewer lines.', "accent-light"),
                    t(tbc("Mike, 2–3 sentences: when he chooses bursting over lining, what he checks before he pulls the head, why he does the final video."), "owner__quote", tag="blockquote"),
                    block("owner__creds", [
                        block("owner__cred", [svg("icon-shield.svg"), span(tbc("Bursting system certification"))], tag="li"),
                        block("owner__cred", [svg("icon-check.svg"), span("WA Reg. #PNWTRT*744KQ")], tag="li"),
                        block("owner__cred", [svg("icon-home.svg"), span(f"Family-owned, {ADDRESS}")], tag="li"),
                    ], tag="ul"),
                    a("About Mike", "/about/", "link-arrow"),
                ]),
            ]),
        ]),
    ], sid="mike", label="Who does the work")


def jobs():
    items = [("job-access-pit.jpg", "A shored access pit in a front lawn, with the camera reel and jetter beside it", "The access pit", "One small, shored pit instead of a trench across the yard."),
             ("job-old-pipe.jpg", "A section of old sewer pipe cut open, with heavy buildup inside", "The old pipe", "What years of buildup look like inside an old line."),
             ("job-lawn-restored.jpg", "A front lawn after the job, with the pit backfilled and the grass back in place", "The yard afterwards", "Pit backfilled and the lawn back in place.")]
    return section("section section--white", [
        container([
            head_split("On the job", 'One job, <span class="serif">start to finish.</span>', a("All projects", "/projects/", "link-arrow")),
            block("grid-3", [
                block("job", [
                    block("job__media", [img(f, "cover-img", alt=alt)], tag="figure"),
                    block("job__body", [span(title, "job__title"), t(text, "caption")]),
                ], tag="li") for f, alt, title, text in items
            ], tag="ul"),
        ]),
    ], label="Bursting projects")


def quotes():
    return section("section section--dark grain", [
        container([
            head("Reviews that mention bursting", 'What bursting customers <span class="serif">say.</span>'),
            block("quotes__grid", [review_loop({"posts_per_page": 2, "meta_query": [{"id": "service", "key": "services", "value": '"__POST_ID__"', "compare": "LIKE"}]}, label="Bursting reviews (loop)")]),
        ]),
    ], label="Reviews")


FAQ = [
    ("How long does an HDPE pipe last?", [f"HDPE pipe has an expected lifespan of 50+ years, and its heat-fused joints leave nothing for roots to get into. {tbc('PNW warranty terms.')}"], True),
    ("Can you make my pipe bigger?", [f"Often, yes. Because the old pipe is broken outward, bursting can pull in a larger pipe than the one you have. {tbc('Typical upsizing limits.')}"], True),
    ("How much digging is there?", [f"Two small access pits, one at each end of the run, instead of a trench along the whole line. {tbc('Typical pit size and depth.')}"], True),
    ("Can I use my water and toilets during the job?", [tbc("How long the line is out of service during bursting and reconnection.")], False),
    ("Is it safe for nearby gas, water and other lines?", [f"All utilities are located and marked before we dig, and the camera and locator show where your line runs. {tbc('Mike to describe his clearance checks.')}"], True),
    ("Is pipe bursting or pipe lining better?", ["It depends on the pipe. Lining needs a host pipe that still holds its shape. For collapsed or deformed pipe, or to upsize, bursting pulls in a brand-new HDPE pipe."], True),
    ("Do I need a permit in Spokane for pipe bursting?", [tbc("Yes / no, which jurisdictions, and how it's handled.")], False),
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
                    eyebrow("Pipe bursting FAQ"),
                    h("h2", 'Straight <span class="serif">answers.</span>'),
                    t("Answers come from Mike. Drafts are marked until he confirms them."),
                    btn(PHONE, TEL, "btn--base btn--outline", icon="icon-phone.svg", icon_left=True),
                ]),
                N("accordion-nested", "faq__list", items, expandItem="0", independentToggle=True),
            ]),
        ]),
    ], sid="faq", label="FAQ")


def more():
    rel = [("icon-liner.svg", "Sewer pipe lining", LINING), ("icon-drop.svg", "Water line pulling", "/services/water-line-pulling/"),
           ("icon-camera.svg", f"Sewer camera inspection {tbc('standalone?')}", "/#services"), ("icon-yard.svg", "Trenchless vs. digging: full comparison", "/#how")]
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
                    eyebrow("Pipe bursting near you"),
                    h("h2", 'We replace sewer pipes <span class="serif">across Spokane &amp; Stevens counties.</span>', "near__title"),
                    block("chip-row", [a(c, "/#areas", "near__city") for c in cities]),
                ]),
            ]),
        ]),
    ], label="Related + near you")




SECTIONS = [hero, answer, fit, how, inside, specs, cost, owner, jobs, quotes, faq, more]


def page():
    return {
        "key": "pipe-bursting", "post_type": "service", "title": "Pipe Bursting", "slug": "pipe-bursting",
        "excerpt": "Trenchless pipe bursting in Spokane: replace a collapsed, crushed or undersized sewer line with new seamless HDPE pipe through two small access pits.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "b" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
