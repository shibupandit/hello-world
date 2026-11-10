"""Service page: Point Repairs. Built from pnw-trenchless/service-point-repairs.html (approved 2026-11-09).
Generated from elements_bursting.py (same blocks), then rewritten for point repairs. The projects strip
is a query loop over real `project` posts whose service is Point repair or Sewer lining.

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
WATER = "/services/water-line-pulling/"


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", HOME, "crumbs__link")], tag="li"),
            block("crumbs__item", [a("Services", "/#services", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Point Repairs", "text-accent-light", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    return section("section svc-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("stack-l", [
                    span("Spot repair · localized relining", "eyebrow rise"),
                    h("h1", 'Sewer <span class="serif">point repairs</span> in Spokane', "accent-light rise rise--2"),
                    t("When the damage is isolated to one section and the rest of the pipe is sound, we reline just that spot instead of replacing the whole line. One crack, one bad joint, one root problem: fixed from inside the pipe.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("See if a spot fix will do", "/contact/", "btn--primary", icon="icon-arrow.svg"),
                        btn(f"Call or text {PHONE}", TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
                    ]),
                    block("byline rise rise--5", [
                        span("MJ", "byline__av", _attributes=attrs(aria_hidden="true")),
                        span(f"Written &amp; reviewed by <strong>Mike Jeisma</strong>, owner, 14+ years in trenchless repair · Updated {tbc('Month YYYY')}", "grow"),
                    ]),
                ]),
                block("figure-stack rise rise--4", [
                    block("svc-hero__art", [svg("art-point-hero.svg")], _attributes=attrs(aria_hidden="true")),
                    t("Illustration: a spot liner sealing one damaged section, with the sound pipe on either side left as it is.", "caption-light", tag="figcaption"),
                ], tag="figure"),
            ]),
        ]),
    ], label="Hero")


def answer():
    facts = [("Typical job time", f"{tbc('X')} hours"), ("Digging", f"Usually none {tbc('confirm')}"),
             ("Repair length", f"{tbc('X')} ft per patch"), ("Warranty", f"{tbc('X')} years")]
    return section("section section--tint section--tight", [
        container([
            block("answer__grid", [
                block("answer__card", [
                    eyebrow("Quick answer"),
                    h("h2", 'What is a <span class="serif">point repair?</span>'),
                    t("A point repair fixes one damaged section of a sewer line from the inside. The camera finds the exact spot, then a short liner is carried to it on an inflatable packer, pressed against the old pipe and left to cure. The result is a sealed, jointless patch over the damage, while the rest of the line, which is still sound, stays as it is."),
                ]),
                block("facts", [block("fact", [span(l, "label-light"), span(v, "fact__value")]) for l, v in facts]),
            ]),
        ]),
    ], label="Quick answer")


def fit():
    yes = ["One cracked or broken section", "One leaking or separated joint", "Roots getting in at a single joint",
           "A small hole or damaged spot", "The rest of the line still sound on camera"]
    no = [("Cracks or roots along the whole line", "Pipe lining", LINING), ("Collapsed or crushed pipe", "Pipe bursting", BURSTING),
          ("Bellies or sags holding water", "Spot excavation", None), ("Problem is the water line", "Water line pulling", WATER)]
    return section("section section--white", [
        container([
            head("Is a point repair right for your pipe?", 'When one fix is enough, <span class="serif">and when it isn\'t.</span>',
                 "A point repair only makes sense if the rest of the line is in good shape. The camera shows us the whole pipe, and we'll show you the footage either way."),
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
    ], label="Is a point repair right")


def how():
    steps = [("Camera inspection", "We record the full line, check that the rest of the pipe is sound, and measure the exact distance to the damage."),
             ("Clean the spot", f"Roots, scale and debris come out with {tbc('hydro jetting / cutting')} so the patch bonds to a clean wall."),
             ("Wet out the patch", f"A liner is cut to the length of the damage and saturated with {tbc('resin type')} on site."),
             ("Position the packer", f"The patch rides in on an inflatable packer through the cleanout {tbc('or a small access point')}, guided by the camera footage."),
             ("Inflate &amp; cure", f"The packer presses the patch against the old pipe while the resin hardens, {tbc('X')} hours. Then it's deflated and pulled out."),
             ("Verify", "A final camera run proves the spot is sealed. You get the before and after footage.")]
    return section("section section--dark grain", [
        container([
            head_split("How a point repair works", 'The spot repair, <span class="serif">step by step.</span>',
                       t("From the first camera run to the final one, here's what happens inside your pipe.", "section__intro section__intro--narrow")),
            block("stages", [svg("art-point-stages.svg", _attributes=attrs(role="img", aria_label="Three stages of a point repair: one damaged section, a packer carrying the patch liner to the spot, the cured patch sealing the pipe"))], tag="figure"),
            block("steps steps--6", [block("step", [h("h3", ti, "step__title"), t(tx)], tag="li") for ti, tx in steps], tag="ol"),
        ]),
    ], sid="how", label="How a point repair works")


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
                 "Real photos from our jobs: the old pipe we find, and a liner cured inside it. A point repair puts the same kind of liner over just the damaged spot."),
            block("grid-2", [
                still("job-old-pipe.jpg", "Before", "", "OLD PIPE", "Before: the old line, worn out and full of buildup.", "A section of old sewer pipe cut open, with heavy buildup inside"),
                still("job-lined-pipe.jpg", "After", "tag--after", "NEW LINER", "After: a new liner cured inside the old pipe.", "An old sewer pipe cut open, with the new blue liner cured inside it"),
            ]),
        ]),
    ], label="Before and after")


def specs():
    rows = [("Patch system", tbc("Manufacturer / system name")), ("Resin", tbc("Epoxy / silicate / other")),
            ("Patch length", f"{tbc('X')} to {tbc('X')} ft"), ("Pipe sizes", f"{tbc('X&quot;')} to {tbc('X&quot;')}"),
            ("Joints", "Seamless patch, no joint over the damage"), ("Warranty", f"{tbc('X')} years · {tbc('transferable?')}")]
    return section("section section--white", [
        container([
            block("split", [
                block("section__head", [
                    eyebrow("What you get"),
                    h("h2", 'What goes <span class="serif">into the pipe.</span>'),
                    t("Real specs from the patch we install, not a sales sheet.", "section__intro"),
                    block("note note--tint", [svg("icon-alert.svg"), t("<strong>Straight talk:</strong> a point repair fixes one spot, not the whole line. If the camera shows damage in several places, lining the full run is often the better deal, and we'll show you why on the footage.")]),
                ]),
                block("spec-table", [block("spec-table__row", [span(k, "label"), span(v, "spec-table__value")]) for k, v in rows]),
            ]),
        ]),
    ], label="Specs")


def cost():
    factors = ["How long the damaged section is", "Pipe size and material", "How far the spot is from the cleanout",
               "How much cleaning the spot needs", "How many spots need a patch"]
    return section("section section--tint", [
        container([
            block("split-wide", [
                block("text-block cost__text", [
                    eyebrow("Cost"),
                    h("h2", 'How much does a point repair <span class="serif">cost in Spokane?</span>'),
                    t(f"Most residential point repairs we do fall between {tbc('$X,XXX and $X,XXX')}.", "cost__range"),
                    t("Because only one section is repaired, a point repair usually costs less than lining or replacing the whole line. Your written quote comes after the camera inspection, so it's based on your actual pipe, not a guess."),
                    t(f"<strong>Included:</strong> {tbc('inspection video, cleaning, patch, final video, warranty')}", "cost__incl"),
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
                    h("h2", f'Mike Jeisma has repaired {tbc("hundreds of")} <span class="serif">Inland Northwest</span> sewer lines.', "accent-light"),
                    t(tbc("Mike, 2–3 sentences: when a spot repair is the honest answer, when it isn't, and why he shows every customer the footage."), "owner__quote", tag="blockquote"),
                    block("owner__creds", [
                        block("owner__cred", [svg("icon-shield.svg"), span(tbc("Spot repair system certification"))], tag="li"),
                        block("owner__cred", [svg("icon-check.svg"), span("WA Reg. #PNWTRT*744KQ")], tag="li"),
                        block("owner__cred", [svg("icon-home.svg"), span(f"Family-owned, {ADDRESS}")], tag="li"),
                    ], tag="ul"),
                    a("About Mike", "/about/", "link-arrow"),
                ]),
            ]),
        ]),
    ], sid="mike", label="Who does the work")


def jobs():
    svc = {"id": "svc", "key": "service", "value": "^(point_repair|sewer_lining)$", "compare": "REGEXP"}
    return section("section section--white", [
        container([
            head_split("Repair projects", 'Recent <span class="serif">repair jobs.</span>', a("All projects", "/projects/", "link-arrow")),
            block("grid-3-2", [project_card(q(posts_per_page=3, meta_query=[REAL_ONLY, svc]), label="Repair projects (loop)")], tag="ul"),
        ]),
    ], label="Repair projects (loop)")


def quotes():
    return section("section section--dark grain", [
        container([
            head("Reviews that mention a spot repair", 'What point repair customers <span class="serif">say.</span>'),
            block("quotes__grid", [review_loop({"posts_per_page": 2, "meta_query": [{"id": "service", "key": "services", "value": '"__POST_ID__"', "compare": "LIKE"}]}, label="Point repair reviews (loop)")]),
        ]),
    ], label="Reviews")


FAQ = [
    ("Is a point repair a permanent fix?", [f"For the spot it covers, yes: the patch seals the damage with a jointless liner. It doesn't fix the rest of the line, which is why we check the whole pipe on camera first. {tbc('Expected life and PNW warranty terms.')}"], True),
    ("Why not just line the whole pipe?", ["If the rest of the line is sound, you don't need to pay for it. If the camera shows damage in several places, we'll tell you, and lining the whole run may be the better deal."], True),
    ("Do you have to dig?", [f"Usually not. The patch goes in through a cleanout. {tbc('When a small access point is needed.')}"], True),
    ("How long does it take?", [tbc("Typical time on site, and how long the line is out of service.")], False),
    ("Will roots come back at that joint?", [f"The patch covers the joint the roots got in through, so there's no gap left at that spot. {tbc('Mike&#039;s experience with roots at other joints.')}"], True),
    ("Can you fix more than one spot?", [f"Yes, each damaged spot can get its own patch. Past {tbc('X')} spots, lining the whole line often costs about the same, and we'll show you both options."], True),
    ("Do I need a permit in Spokane for a point repair?", [tbc("Yes / no, which jurisdictions, and how it's handled.")], False),
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
                    eyebrow("Point repair FAQ"),
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
           ("icon-drop.svg", "Water line pulling", WATER), ("icon-yard.svg", "Trenchless vs. digging: full comparison", "/#how")]
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
                    eyebrow("Point repairs near you"),
                    h("h2", 'We repair sewer lines <span class="serif">across Spokane &amp; Stevens counties.</span>', "near__title"),
                    block("chip-row", [a(c, "/#areas", "near__city") for c in cities]),
                ]),
            ]),
        ]),
    ], label="Related + near you")




SECTIONS = [hero, answer, fit, how, inside, specs, cost, owner, jobs, quotes, faq, more]


def page():
    return {
        "key": "point-repairs", "post_type": "service", "title": "Point Repairs", "slug": "point-repairs",
        "excerpt": "Sewer point repairs in Spokane: when the damage is in one spot, we reline just that section from inside the pipe instead of replacing the whole line.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "p" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
