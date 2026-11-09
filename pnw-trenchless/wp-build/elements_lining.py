"""Service page: Sewer Pipe Lining (CIPP). Built from pnw-trenchless/service-sewer-pipe-lining.html.

Uses the shared helpers and global classes from elements.py. Header and footer come from the
site-wide Bricks templates (101 / 102), so this file only builds the page content.
Unknown facts stay as `tbc` placeholders; FAQ answers carry no draft label (user, 2026-11-09).
"""
from elements import (N, section, container, block, div, h, t, span, a, svg, img, btn, eyebrow, attrs, link,
                      head, head_split, flatten, review_loop, TEL, PHONE, ADDRESS)

HOME = "/"
BURSTING = "/services/pipe-bursting/"


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", HOME, "crumbs__link")], tag="li"),
            block("crumbs__item", [a("Services", "/#services", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Sewer Pipe Lining", "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    return section("section svc-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("svc-hero__content", [
                    span("CIPP · pipe in a pipe", "eyebrow rise"),
                    h("h1", 'Sewer pipe <span class="serif">lining</span> in Spokane', "svc-hero__title rise rise--2"),
                    t("Fix a cracked, leaking or root-filled sewer line from the inside, without trenching your yard. We build a new, seamless pipe inside your old one through one or two small access points.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("See if lining works for your pipe", "#estimate", "btn--primary", icon="icon-arrow.svg"),
                        btn(f"Call or text {PHONE}", TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
                    ]),
                    block("byline rise rise--5", [
                        span("MJ", "byline__av", _attributes=attrs(aria_hidden="true")),
                        span(f"Written &amp; reviewed by <strong>Mike Jeisma</strong>, owner, 14+ years in trenchless repair · Updated {tbc('Month YYYY')}", "byline__text"),
                    ]),
                ]),
                block("svc-hero__media rise rise--4", [
                    block("svc-hero__art", [img("job-lined-pipe.jpg", "cover-img", alt="An old sewer pipe cut open, with the new blue liner cured inside it")]),
                    t("A cut section of an old pipe with the new liner cured inside.", "svc-hero__cap", tag="figcaption"),
                ], tag="figure"),
            ]),
        ]),
    ], label="Hero")


def answer():
    facts = [("Typical job time", f"{tbc('X')} day(s)"), ("Digging", "0–2 small access points"),
             ("Pipe sizes", f"{tbc('X&quot;')} to {tbc('X&quot;')}"), ("Warranty", f"{tbc('X')} years")]
    return section("section section--tint section--tight", [
        container([
            block("answer__grid", [
                block("answer__card", [
                    eyebrow("Quick answer"),
                    h("h2", 'What is CIPP <span class="serif">pipe lining?</span>'),
                    t("Cured-in-place pipe (CIPP) lining is a trenchless sewer repair. A resin-saturated liner is pulled or inverted into the cleaned host pipe, inflated against the walls and cured until it hardens into a jointless new pipe. Most residential jobs need little or no digging."),
                ]),
                block("facts", [block("fact", [span(l, "fact__label"), span(v, "fact__value")]) for l, v in facts]),
            ]),
        ]),
    ], label="Quick answer")


def fit():
    yes = ["Cracks and pinhole leaks", "Root intrusion at joints", "Offset or separated joints (minor)",
           "Corroded cast iron that's still round", "Lines under driveways, trees, patios or slabs"]
    no = [("Collapsed or crushed sections", "Pipe bursting", True), ("Orangeburg (fiber pipe) that's deformed", "Pipe bursting", True),
          ("Bellies or sags holding water", "Spot excavation", False), ("Pipe too small for the household", "Bursting to upsize", True)]
    return section("section section--white", [
        container([
            head("Is lining right for your pipe?", 'When lining works, <span class="serif">and when it doesn\'t.</span>',
                 "Lining needs a host pipe that still holds its shape. The camera tells us which side of the line yours is on, and we'll show you the footage either way."),
            block("fit__grid", [
                block("fit-card fit-card--yes", [
                    block("fit-card__head", [block("fit-card__ico", [svg("icon-check.svg")], tag="span"), h("h3", "Good candidates", "fit-card__title")]),
                    block("fit-card__list", [t(x, "fit-card__item", tag="li") for x in yes], tag="ul"),
                ]),
                block("fit-card fit-card--no", [
                    block("fit-card__head", [block("fit-card__ico", [svg("icon-alert.svg")], tag="span"), h("h3", "Usually a different fix", "fit-card__title")]),
                    block("fit-card__list", [
                        block("fit-card__item", [span(x), a(alt, BURSTING, "fit-card__alt") if linked else span(alt, "fit-card__alt fit-card__alt--static")], tag="li")
                        for x, alt, linked in no
                    ], tag="ul"),
                ]),
            ]),
        ]),
    ], label="Is lining right")


def how():
    steps = [("Camera inspection", "We record the full line, measure its length and mark every defect and connection."),
             ("Clean the pipe", f"Roots, scale and debris come out with {tbc('hydro jetting / descaling')} so the liner bonds to a clean wall."),
             ("Wet out the liner", f"The liner is cut to length and saturated with {tbc('resin type')} on site."),
             ("Install", f"We {tbc('invert / pull')} it into place through the cleanout or a small access pit and inflate it against the old pipe."),
             ("Cure", f"The resin hardens ({tbc('ambient / hot water / steam / UV')}) into a rigid new pipe in {tbc('X')} hours."),
             ("Reopen &amp; verify", "Branch connections are reinstated and a final camera run proves the result. You get the footage.")]
    return section("section section--dark grain", [
        container([
            head_split("How CIPP lining works", 'The lining process, <span class="serif">step by step.</span>',
                       t("From the first camera run to the final one, here's what happens inside your pipe.", "section__intro section__intro--narrow")),
            block("stages", [svg("art-lining-stages.svg", _attributes=attrs(role="img", aria_label="Three stages of CIPP lining: cracked host pipe, liner inverted and inflated, cured jointless new pipe"))], tag="figure"),
            block("steps steps--6", [block("step", [h("h3", ti, "step__title"), t(tx)], tag="li") for ti, tx in steps], tag="ol"),
        ]),
    ], sid="how", label="How lining works")


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
                 "Real photos from our jobs: the old pipe we find, and the liner that goes inside it."),
            block("inside__grid", [
                still("job-old-pipe.jpg", "Before", "", "OLD PIPE", "Before: an old line choked with buildup.", "A section of old sewer pipe cut open, with heavy buildup inside"),
                still("job-lined-pipe.jpg", "After", "still__tag--after", "NEW LINER", "After: the new liner cured inside the old pipe.", "An old sewer pipe cut open, with the new blue liner cured inside it"),
            ]),
        ]),
    ], label="Before and after")


def specs():
    rows = [("Liner system", tbc("Manufacturer / system name")), ("Resin", tbc("Epoxy / polyester / vinyl ester")),
            ("Wall thickness", f"{tbc('X')} mm"), ("Design life", f"{tbc('X')}+ years (per manufacturer)"),
            ("Standards", tbc("e.g. ASTM F1216 / F1743, as applicable")), ("Warranty", f"{tbc('X')} years · {tbc('transferable?')}")]
    return section("section section--white", [
        container([
            block("specs__grid", [
                block("section__head", [
                    eyebrow("What you get"),
                    h("h2", 'What goes <span class="serif">into your pipe.</span>'),
                    t("Real specs from the system we install, not a sales sheet.", "section__intro"),
                    block("note note--tint", [svg("icon-alert.svg"), t("<strong>Straight talk:</strong> a liner slightly reduces the inside diameter, but its smooth, jointless wall usually flows as well as or better than the rough old pipe.")]),
                ]),
                block("spec-table", [block("spec-table__row", [span(k, "spec-table__term"), span(v, "spec-table__value")]) for k, v in rows]),
            ]),
        ]),
    ], label="Specs")


def cost():
    factors = ["Length of pipe being lined", "Pipe diameter and material", "Number of branch connections to reopen",
               "Access: cleanout vs. new access pit", "How much root and scale cleaning is needed"]
    return section("section section--tint", [
        container([
            block("cost__grid", [
                block("cost__text", [
                    eyebrow("Cost"),
                    h("h2", 'How much does pipe lining <span class="serif">cost in Spokane?</span>'),
                    t(f"Most residential sewer lining jobs we do fall between {tbc('$X,XXX and $XX,XXX')}.", "cost__range"),
                    t("Your written quote comes after the camera inspection, so it's based on your actual pipe, not a guess. Compare it against a dig-and-replace quote plus the cost to restore your lawn, driveway or landscaping."),
                    t(f"<strong>Included:</strong> {tbc('inspection video, cleaning, permit, final video, warranty')}", "cost__incl"),
                ]),
                block("cost-card", [
                    h("h3", "What affects the price", "cost-card__title"),
                    block("cost-card__list", [block("cost-card__item", [span(f"0{i + 1}", "cost-card__num"), span(x)], tag="li") for i, x in enumerate(factors)], tag="ul"),
                    btn("Get my written quote", "#estimate", "btn--primary form__submit", icon="icon-arrow.svg"),
                ]),
            ]),
        ]),
    ], label="Cost")


def owner():
    return section("section section--dark grain", [
        container([
            block("owner__grid", [
                block("owner__photo", [img("trailer.jpg", "cover-img", alt="The PNW Trenchless equipment trailer")]),
                block("owner__content", [
                    eyebrow("Who does the work"),
                    h("h2", f'Mike Jeisma has lined {tbc("hundreds of")} <span class="serif">Inland Northwest</span> sewer lines.', "owner__title"),
                    t(tbc("Mike, 2–3 sentences: what he looks for on the camera, the mistake he sees other companies make with lining, why he does the final video."), "owner__quote", tag="blockquote"),
                    block("owner__creds", [
                        block("owner__cred", [svg("icon-shield.svg"), span(tbc("Liner manufacturer certification"))], tag="li"),
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
            block("jobs__grid", [
                block("job", [
                    block("job__media", [img(f, "cover-img", alt=alt)], tag="figure"),
                    block("job__body", [span(title, "job__title"), t(text, "job__spec")]),
                ], tag="li") for f, alt, title, text in items
            ], tag="ul"),
        ]),
    ], label="Lining projects")


def quotes():
    return section("section section--dark grain", [
        container([
            head("Reviews that mention lining", 'What lining customers <span class="serif">say.</span>'),
            block("quotes__grid", [review_loop({"posts_per_page": 2, "meta_query": [{"id": "service", "key": "services", "value": '"__POST_ID__"', "compare": "LIKE"}]}, label="Lining reviews (loop)")]),
        ]),
    ], label="Reviews")


FAQ = [
    ("How long does a lined pipe last?", [tbc("Design life per the liner manufacturer + PNW warranty terms.")], False),
    ("Can roots grow through a liner?", ["A cured liner forms a seamless, jointless pipe, so roots have no joints to get back in through. We clear the roots first, then line the pipe."], True),
    ("Can I use my water and toilets during the job?", [tbc("How long the line is out of service during lining and curing.")], False),
    ("Will lining make my pipe smaller?", ["Slightly, by the liner's wall thickness. Its smooth, jointless wall usually flows as well as or better than the rough old pipe."], True),
    ("Can you line a pipe that has a belly in it?", ["A belly (sag) that holds water is usually better fixed by digging that one spot. The camera shows us, and we'll tell you before we start."], True),
    ("Can you line cast iron under my house or slab?", [f"Corroded cast iron that's still round is a good lining candidate, including under slabs."], True),
    ("Is pipe lining or pipe bursting better?", ["It depends on the pipe. Lining needs a host pipe that still holds its shape. For collapsed or deformed pipe, or to upsize, pipe bursting pulls in a brand-new HDPE pipe."], True),
    ("Do I need a permit in Spokane for sewer lining?", [tbc("Yes / no, which jurisdictions, and how it's handled.")], False),
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
                    eyebrow("Pipe lining FAQ"),
                    h("h2", 'Straight <span class="serif">answers.</span>'),
                    t("Answers come from Mike. Drafts are marked until he confirms them."),
                    btn(PHONE, TEL, "btn--base btn--outline", icon="icon-phone.svg", icon_left=True),
                ]),
                N("accordion-nested", "faq__list", items, expandItem="0", independentToggle=True),
            ]),
        ]),
    ], sid="faq", label="FAQ")


def more():
    rel = [("icon-burst.svg", "Pipe bursting", BURSTING), ("icon-drop.svg", "Water line pulling", "/services/water-line-pulling/"),
           ("icon-camera.svg", f"Sewer camera inspection {tbc('standalone?')}", "/#services"), ("icon-yard.svg", "Trenchless vs. digging: full comparison", "/#how")]
    cities = ["Spokane", "Spokane Valley", "Deer Park", "Clayton", "Stevens County", "Spokane County"]
    return section("section section--tint", [
        container([
            block("more__grid", [
                block("", [
                    eyebrow("Related services"),
                    block("related", [
                        block("", [block("related__link", [block("related__ico", [svg(ic)], tag="span"), span(lbl, "related__label"), svg("icon-arrow.svg", "related__go")], href=u)], tag="li")
                        for ic, lbl, u in rel
                    ], tag="ul"),
                ], label="Related services"),
                block("near", [
                    eyebrow("Pipe lining near you"),
                    h("h2", 'We line sewer pipes <span class="serif">across Spokane &amp; Stevens counties.</span>', "near__title"),
                    block("near__cities", [a(c, "/#areas", "near__city") for c in cities]),
                ]),
            ]),
        ]),
    ], label="Related + near you")




SECTIONS = [hero, answer, fit, how, inside, specs, cost, owner, jobs, quotes, faq, more]


def page():
    return {
        "key": "sewer-pipe-lining", "post_type": "service", "title": "Sewer Pipe Lining", "slug": "sewer-pipe-lining",
        "excerpt": "Trenchless sewer pipe lining (CIPP) in Spokane: a new, seamless pipe inside your old one through one or two small access points.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "l" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
