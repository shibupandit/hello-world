"""About page: Meet Mike. Built from pnw-trenchless/about.html (approved 2026-11-09).

Uses the shared helpers and global classes from elements.py. Header and footer come from the
site-wide Bricks templates, so this file only builds the page content. Contact details come
from the Website Settings options page; reviews come from the Testimonials post type.
Unknown facts stay as `tbc` placeholders.
"""
from elements import (N, section, container, block, div, h, t, span, a, svg, img, btn, eyebrow, attrs, link,
                      head, head_split, estimate, flatten, review_loop, when, TEL, PHONE, ADDRESS)

HOME = "/"
RATING = "{acf_site_google_rating}"
REVIEWS = "{acf_site_google_review_count}"


def tbc(x):
    return f'<span class="tbc">{x}</span>'


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", HOME, "crumbs__link")], tag="li"),
            block("crumbs__item", [span("About", "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    portrait = block("portrait rise rise--4", [
        block("portrait__frame", [
            svg("art-silhouette.svg", "mike__silhouette", _attributes=attrs(aria_hidden="true")),
            block("owner__ph", [svg("icon-photo.svg"), span(tbc("Portrait: Mike in work gear, trailer behind him. Real, not a stock smile"))], tag="span"),
            block("portrait__plate", [
                block("portrait__id", [span("Mike Jeisma", "portrait__name"), span("Owner &amp; lead technician", "portrait__role")], tag="span"),
                span(f"Est. {tbc('2025')}", "portrait__est"),
            ]),
        ]),
    ], tag="figure")
    return section("section svc-hero about-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("svc-hero__content", [
                    span("About PNW Trenchless", "eyebrow rise"),
                    h("h1", 'Meet Mike Jeisma, <span class="serif">the owner who shows up</span> to your job.', "svc-hero__title rise rise--2"),
                    t(f"PNW Trenchless is a family-owned sewer and water line company based in {ADDRESS}. Mike has spent 14+ years fixing underground pipes across the Spokane area. When you call, you talk to him. When the trailer pulls up, he's on it.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("Talk to Mike about your line", "#estimate", "btn--primary", icon="icon-arrow.svg"),
                        btn(PHONE, TEL, "btn--white btn--outline", icon="icon-phone.svg", icon_left=True),
                    ]),
                ]),
                portrait,
            ]),
        ]),
    ], label="Hero")


def numbers():
    tiles = [
        block("stat", [span("14<small>+ yrs</small>", "stat__num"), span("in sewer &amp; water line repair", "stat__label")], tag="li"),
        block("stat", [span(f"{tbc('N')}<small>+</small>", "stat__num"), span("trenchless jobs completed in his career", "stat__label")], tag="li"),
        block("stat", [span(f"{tbc('N')}<small> ft</small>", "stat__num"), span("of pipe lined or burst", "stat__label")], tag="li"),
        block("stat", [
            span(f"{RATING}<small>★</small>", "stat__num"),
            span(f"on Google from {REVIEWS} reviews", "stat__label", **when(REVIEWS)),
            span("average rating on Google", "stat__label", **when(REVIEWS, "==")),
        ], tag="li", **when(RATING)),
    ]
    return section("section section--tint section--tight", [
        container([
            block("stats__grid", tiles, tag="ul"),
            t(tbc("Only numbers Mike can stand behind go live. Drop any tile he can't verify."), "stats__note"),
        ]),
    ], label="Numbers", _attributes=attrs(aria_label="Mike in numbers"))


def story():
    steps = [
        ("2 years", "Starts in plumbing", f"Learns residential plumbing from the ground up at {tbc('company or &quot;a local plumbing shop&quot;')}.", False),
        ("5 years", f"Sewer repair, {tbc('Gold Seal Plumbing')}", f"Five years focused on sewer line diagnosis and repair. {tbc('Confirm OK to name.')}", False),
        ("7 years", "Trenchless specialist", "Seven years doing lining and bursting full-time with a Spokane trenchless contractor.", False),
        ("today", "Founds PNW Trenchless", f"Family-owned, based in {ADDRESS}, serving Spokane and Stevens counties.", True),
    ]
    years = [tbc("20XX–20XX"), tbc("20XX–20XX"), tbc("20XX–20XX"), tbc("2025")]
    return section("section section--white", [
        container([
            block("story__grid", [
                block("story__aside", [
                    eyebrow("The story"),
                    h("h2", 'Why I started <span class="serif">PNW Trenchless.</span>'),
                    span("In Mike's own words", "story__meta"),
                ]),
                block("story__body", [
                    block("story__quote", [
                        t(tbc("Mike, 3–4 short paragraphs from an interview: how he got into sewer work, the first trenchless job that sold him on it, what he saw homeowners go through with big digs and vague quotes, and why in 2025 he decided to put his own name on the work."), "story__text"),
                        t(tbc("Closing line in his words: what he wants every customer to say after the job."), "story__close"),
                    ], tag="blockquote"),
                    block("signature", [
                        span("Mike Jeisma", "signature__mark", _attributes=attrs(aria_hidden="true")),
                        block("signature__id", [span("Mike Jeisma", "signature__name"), span("Owner, PNW Trenchless", "signature__role")], tag="span"),
                    ]),
                ]),
            ]),
            block("timeline", [
                block("timeline__head", [
                    h("h3", "14 years, one trade", "timeline__title"),
                    span(tbc("Confirm years and order with Mike"), "timeline__note"),
                ]),
                block("timeline__bar", [div(f"timeline__seg timeline__seg--{m}", tag="span") if m else div("timeline__seg", tag="span") for m in ("", "5", "7", "now")],
                      _attributes=attrs(aria_hidden="true")),
                block("timeline__list", [
                    block("milestone" + (" milestone--now" if now else ""), [
                        span(f"{yr} · {dur}", "milestone__when"),
                        h("h4", ti, "milestone__title"),
                        t(tx, "milestone__text"),
                    ], tag="li")
                    for yr, (dur, ti, tx, now) in zip(years, steps)
                ], tag="ol"),
            ]),
        ]),
    ], label="The story")


def promises():
    items = [("icon-camera.svg", "You see what we see", "Every recommendation starts with camera footage you watch with us."),
             ("icon-check.svg", "A straight answer", "If digging, a spot repair or doing nothing yet is the better call, we'll say so."),
             ("icon-home.svg", "The owner on the job", "Mike runs the work himself. No handoff to a crew you've never met."),
             ("icon-card.svg", "Written price first", "A clear scope and price before any work starts."),
             ("icon-film.svg", "Proof at the end", "A final camera video of the finished pipe, for your records and warranty."),
             ("icon-yard.svg", "Your property, respected", "Small footprint, access points restored, site cleaned before we leave.")]
    return section("section section--tint", [
        container([
            head("How we work", 'What you can <span class="serif">expect from us.</span>', "Six promises Mike makes on every job, big or small."),
            block("promises__grid", [
                block("promise", [
                    block("promise__ico", [svg(ic)], tag="span"),
                    span(f"0{i + 1}", "promise__num"),
                    h("h3", ti, "promise__title"),
                    t(tx, "promise__text"),
                ], tag="li")
                for i, (ic, ti, tx) in enumerate(items)
            ], tag="ol"),
        ]),
    ], label="How we work")


def rig():
    kit = [("icon-camera.svg", "Sewer camera &amp; locator", "Brand / model"), ("icon-liner.svg", "Lining system", "Brand / system"),
           ("icon-burst.svg", "Bursting rig", "Brand / model"), ("icon-drop.svg", "Pipe cleaning", "Hydro jetter / descaler")]
    return section("section section--dark grain", [
        container([
            block("rig__grid", [
                block("rig__media", [
                    block("rig__main", [img("trailer.jpg", alt="The PNW Trenchless equipment trailer"), t("The trailer", "rig__tag", tag="figcaption")], tag="figure"),
                    block("rig__ph", [svg("icon-photo.svg"), span(tbc("Photo: wrapped truck"))], tag="figure"),
                    block("rig__ph", [svg("icon-photo.svg"), span(tbc("Photo: inside the trailer / gear"))], tag="figure"),
                ]),
                block("rig__text", [
                    eyebrow("Equipment"),
                    h("h2", 'Built for trenchless <span class="serif">from day one.</span>'),
                    t("PNW Trenchless runs a fully outfitted trailer for sewer lining, pipe bursting and water line replacement, so most jobs start and finish in one visit."),
                    block("kit", [
                        block("kit__row", [block("kit__term", [svg(ic), span(term)], tag="dt"), t(tbc(val), "kit__value", tag="dd")])
                        for ic, term, val in kit
                    ], tag="dl"),
                ]),
            ]),
        ]),
    ], label="Equipment")


def verify():
    return section("section section--white", [
        container([
            head("Credentials", 'Licensed, insured <span class="serif">and verifiable.</span>', "Don't take our word for it. Each one links to its public record."),
            block("verify__grid", [
                block("verify-card verify-card--primary", [
                    block("verify-card__ico", [svg("icon-shield.svg")], tag="span"),
                    h("h3", "WA Contractor Registration", "verify-card__title"),
                    t("#PNWTRT*744KQ", "verify-card__value"),
                    a("Verify on WA L&amp;I", link("https://secure.lni.wa.gov/verify/", True), "link-arrow"),
                ], tag="li"),
                block("verify-card", [
                    block("verify-card__ico", [svg("icon-check.svg")], tag="span"),
                    h("h3", "Bonded &amp; insured", "verify-card__title"),
                    t(f"{tbc('Bond amount')} · {tbc('General liability carrier')}", "verify-card__value"),
                    t("Certificate available on request", "verify-card__fine"),
                ], tag="li"),
                block("verify-card", [
                    block("verify-card__ico", [svg("icon-liner.svg")], tag="span"),
                    h("h3", "Manufacturer certified", "verify-card__title"),
                    t(tbc("Liner system certification"), "verify-card__value"),
                    t(tbc("Bursting system certification"), "verify-card__value"),
                ], tag="li"),
                block("verify-card", [
                    block("verify-card__ico", [svg("icon-building.svg")], tag="span"),
                    h("h3", "Memberships", "verify-card__title"),
                    t(tbc("BBB · NASSCO · local chamber, if any"), "verify-card__value"),
                ], tag="li"),
            ], tag="ul"),
        ]),
    ], label="Credentials")


def local():
    cities = ["Spokane", "Spokane Valley", "Deer Park", "Clayton", "Stevens County", "Spokane County"]
    return section("section section--tint", [
        container([
            block("local__grid", [
                block("local__text", [
                    eyebrow("Local &amp; family"),
                    h("h2", 'Built for the <span class="serif">Pacific Northwest.</span>'),
                    t(f"We live here. {tbc('Family detail Mike is comfortable sharing: who&#39;s part of the business, how long in the area, community involvement.')}"),
                    t("We serve Spokane, Spokane Valley, Deer Park, Clayton and Stevens County."),
                    block("near__cities", [a(c, "/#areas", "near__city") for c in cities]),
                    a("See our service areas", "/#areas", "link-arrow"),
                ]),
                block("local__photo", [
                    block("local__mtn", [svg("art-local-mountains.svg")], _attributes=attrs(aria_hidden="true")),
                    block("owner__ph", [svg("icon-photo.svg"), span(tbc("Photo: Mike and family, or Mike at a local community event"))], tag="span"),
                ], tag="figure"),
            ]),
        ]),
    ], label="Local &amp; family")


def reviews():
    return section("section section--dark grain", [
        container([
            head_split("Reviews that mention Mike", 'What customers say <span class="serif">about Mike.</span>', a("All reviews", "/#reviews", "link-arrow")),
            block("quotes__grid quotes__grid--3", [review_loop({"posts_per_page": 3}, label="Reviews (loop)")]),
        ]),
    ], label="Reviews")


def quote():
    return estimate(kicker="Talk to the owner", title='Got a sewer problem? <span class="serif">Talk to Mike directly.</span>',
                    intro="Call or text with a photo or video of the problem. He'll tell you honestly whether you need a camera inspection.",
                    contact_ways=False)


SECTIONS = [hero, numbers, story, promises, rig, verify, local, reviews, quote]


def page():
    return {
        "key": "about",
        "post_type": "page",
        "title": "About",
        "slug": "about",
        "excerpt": "Meet Mike Jeisma, owner of PNW Trenchless: 14+ years fixing sewer and water lines across the Spokane area.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "a" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
