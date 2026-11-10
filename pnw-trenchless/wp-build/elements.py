"""PNW Trenchless: native Bricks element trees (header, footer, Home sections).

Placeholders resolved on the site by the import script:
- "_cls": [class names]          -> "_cssGlobalClasses": [ids]
- {"__media": "file.ext", ...}   -> {"id": <attachment id>, "url": "<url>", ...}

Run: python3 elements.py -> writes elements.json
"""
import json, pathlib

# Contact details come from the ACF options page "Website Settings" (Bricks dynamic data),
# so editing them there updates the whole site.
TEL = "tel:{acf_site_phone}"
SMS = "sms:{acf_site_phone}"
MAIL = "mailto:{acf_site_email}"
EMAIL = "{acf_site_email}"
ADDRESS = "{acf_site_address}"
RATING = "{acf_site_google_rating}"
REVIEWS = "{acf_site_google_review_count}"
GOOGLE_URL = "{acf_site_google_url}"
HOURS = "{acf_site_hours}"
MAP_IFRAME = "{acf_site_google_map_iframe}"
FB = "https://www.facebook.com/profile.php?id=61589495076554"
PHONE = "{acf_site_phone}"
QUOTE_FORM_ID = 3  # Fluent Forms "Request a quote"
CONTACT_ID = 785  # Contact page: has its own form, so the footer quote section is hidden there
NAV_LINKS = [("Services", "/#services"), ("Who We Serve", "/who-we-serve/"), ("How It Works", "/#how"),
             ("About", "/about/"), ("Service Areas", "/#areas"), ("Contact", "/contact/")]


def M(f, **extra):
    d = {"__media": f}
    d.update(extra)
    return d


def when(tag, compare="!="):
    """Bricks element condition: show only when the dynamic tag is (not) empty."""
    key = tag.strip("{}").replace("acf_site_", "")
    return {"_conditions": [[{"id": f"c{key[:4]}{'n' if compare == '!=' else 'e'}", "key": "dynamic_data", "compare": compare, "value": "", "dynamic_data": tag}]]}


def link(url, new_tab=False, aria=None):
    d = {"type": "external", "url": url}
    if new_tab:
        d["newTab"] = True
        d["rel"] = "noopener"
    if aria:
        d["ariaLabel"] = aria
    return d


def attrs(**kv):
    return [{"name": k.replace("_", "-"), "value": v} for k, v in kv.items()]


TAGS = {
    "text-basic": {"div", "p", "span", "figcaption", "address", "figure"},
    "block": {"div", "section", "a", "article", "nav", "ol", "ul", "li", "aside", "address", "figure"},
    "div": {"div", "section", "a", "article", "nav", "ol", "ul", "li", "aside", "address", "figure"},
    "heading": {"h1", "h2", "h3", "h4", "h5", "h6"},
    "section": {"section"},
}


class N:
    def __init__(self, name, cls=None, children=None, label=None, **settings):
        self.name, self.children, self.settings = name, list(children or []), dict(settings)
        tag = self.settings.get("tag")
        if tag and name in TAGS and tag not in TAGS[name]:
            self.settings["tag"] = "custom"
            self.settings["customTag"] = tag
        if cls:
            self.settings["_cls"] = cls.split() if isinstance(cls, str) else list(cls)
        self.label = label or (self.settings.get("_cls") or [None])[0]


# --- element helpers ------------------------------------------------------
def section(cls, children, sid=None, label=None, tag=None, **s):
    if sid:
        s["_cssId"] = sid
    if tag:
        s["tag"] = tag
    return N("section", cls, children, label=label, **s)


def container(children, cls=None, **s):
    return N("container", cls, children, **s)


def block(cls, children=(), tag=None, href=None, **s):
    if tag:
        s["tag"] = tag
    if href:
        s["tag"] = "a"
        s["link"] = href if isinstance(href, dict) else link(href)
    return N("block", cls, children, **s)


def div(cls, children=(), tag=None, **s):
    if tag:
        s["tag"] = tag
    return N("div", cls, children, **s)


def h(tag, text, cls=None, **s):
    return N("heading", cls, text=text, tag=tag, **s)


def t(text, cls=None, tag="p", **s):
    return N("text-basic", cls, text=text, tag=tag, **s)


def span(text, cls=None, **s):
    return t(text, cls, tag="span", **s)


def a(text, href, cls=None, **s):
    return N("text-link", cls, text=text, link=href if isinstance(href, dict) else link(href), **s)


def svg(f, cls=None, **s):
    return N("svg", cls, file=M(f), **s)


def img(f, cls=None, alt=None, **s):
    st = {"image": M(f, size="full")}
    if alt is not None:
        st["altText"] = alt
    st.update(s)
    return N("image", cls, **st)


def btn(text, href, cls="btn--primary", icon=None, icon_left=False, **s):
    st = {"text": text, "link": href if isinstance(href, dict) else link(href)}
    if icon:
        st["icon"] = {"library": "svg", "svg": M(icon)}
        st["iconPosition"] = "left" if icon_left else "right"
    st.update(s)
    return N("button", cls, **st)


def mode_switch(mode, pfx):
    """Bricks interactions for the cross-section toggle (no custom JS)."""
    other = "trenchless" if mode == "dig" else "dig"
    def ia(n, sel, key, val):
        return {"id": f"{pfx}{n:04d}", "trigger": "click", "action": "setAttribute", "target": "custom",
                "targetSelector": sel, "actionAttributeKey": key, "actionAttributeValue": val}
    return [ia(1, "#xsec", "data-mode", mode), ia(2, f"#xsec-{mode}", "aria-pressed", "true"), ia(3, f"#xsec-{other}", "aria-pressed", "false")]


def eyebrow(text):
    return span(text, "eyebrow")


# --------------------------------------------------------------------------
# HEADER TEMPLATE
# --------------------------------------------------------------------------
def services_menu():
    """"Services" in the header: a Bricks nav dropdown with the mega menu option (design: megamenu.html).
    Bricks handles hover, click, keyboard, Esc and the mobile menu; the panel is as wide as .header__inner.
    The service cards are a query loop (user, 2026-11-10): add a service post and it appears here."""
    hide = attrs(aria_hidden="true")
    # One card, repeated by a query loop over the `service` post type (ordered by menu_order).
    # Fields per service: card_image, card_label, card_text (ACF group "Service card (menu)").
    cards = [N("block", "", [block("mega-card", [
        block("mega-card__art", [N("image", None, image={"useDynamicData": "{acf_card_image}", "size": "medium"}, altText="")],
              tag="span", _attributes=hide, **when("{acf_card_image}")),
        span("{acf_card_label}", "mega-card__spec", **when("{acf_card_label}")),
        block("mega-card__title", [span("{post_title}"), svg("icon-arrow.svg", _attributes=hide)], tag="span"),
        span("{acf_card_text}", "mega-card__text", **when("{acf_card_text}")),
    ], href=link("{post_url}"))], label="Service card (loop)", tag="li", hasLoop=True,
        query={"objectType": "post", "post_type": ["service"], "orderby": "menu_order", "order": "asc", "posts_per_page": 8, "no_found_rows": True})]
    panel = block("mega__panel", [
        block("mega__grid", [
            block("mega__main", [
                span("Four ways we fix it, without the trench", "mega__label"),
                block("mega__cards", cards, tag="ul"),
            ]),
            block("mega__aside", [
                block("mega__aside-ico", [svg("icon-camera.svg")], tag="span", _attributes=hide),
                span("Not sure which one you need?", "mega__aside-title"),
                t("Every job starts with a camera inspection. You see the footage, and the camera decides the method.", "mega__aside-text"),
                block("mega__phone", [svg("icon-phone.svg"), span(PHONE)], href=TEL),
                btn("Get a quote", "/contact/", "btn--primary btn-block", icon="icon-arrow.svg"),
            ]),
        ]),
        block("mega__foot", [
            block("mega__note", [svg("icon-film.svg"), span("You keep the before and after footage on every job.")], tag="span"),
            block("mega__links", [a("Who we serve", "/who-we-serve/", "mega__link"), a("Recent projects", "/projects/", "mega__link"), a("Reviews", "/reviews/", "mega__link")]),
        ]),
    ])
    return N("dropdown", "nav__drop", [
        N("div", "mega", [panel], tag="div", _hidden={"_cssClasses": "brx-dropdown-content"}, label="Mega menu content"),
    ], text="Services", tag="li", megaMenu=True, megaMenuSelector=".header__inner", megaMenuSelectorVertical=".header__inner", ariaLabel="Toggle services menu", label="Services (mega menu)")


def header():
    topbar = block("topbar", [
        block("topbar__inner", [
            span("Serving Spokane, Spokane Valley, Deer Park, Clayton, Stevens &amp; Spokane County", "topbar__area"),
            block("topbar__links", [
                span("WA Reg. #PNWTRT*744KQ"),
                block("topbar__link", [svg("icon-mail.svg", "ico"), span(EMAIL)], href=MAIL),
                block("topbar__link", [svg("icon-fb.svg", "ico"), span("Facebook")], href=link(FB, True)),
            ]),
        ]),
    ])
    head = block("header", [
        block("header__inner", [
            block("logo", [img("logo.png", alt="PNW Trenchless")], href=link("/", aria="PNW Trenchless home")),
            N("nav-nested", "nav", [
                block("nav__items", [
                    services_menu(),
                ] + [a(t, u, "nav__link") for t, u in NAV_LINKS[1:]] + [
                    block("nav__extras", [
                        block("nav__phone", [
                            block("header__phone-ico", [svg("icon-phone.svg")], tag="span"),
                            block("header__phone-text", [span("Call or text", "header__phone-label"), span(PHONE, "header__phone-num")], tag="span"),
                        ], href=link(TEL, aria=f"Call or text {PHONE}")),
                        btn("Get a Quote", "/contact/", "btn--primary btn-block", icon="icon-arrow.svg"),
                        block("nav__contact", [
                            block("topbar__link", [svg("icon-mail.svg", "ico"), span(EMAIL)], href=MAIL),
                            block("topbar__link", [svg("icon-fb.svg", "ico"), span("Facebook")], href=link(FB, True)),
                        ]),
                        span("Serving Spokane, Spokane Valley, Deer Park, Clayton, Stevens &amp; Spokane County", "nav__area"),
                    ], tag="li"),
                ], tag="ul", _hidden={"_cssClasses": "brx-nav-nested-items"}, label="Nav items"),
                N("toggle", "nav__open", animation="squeeze", ariaLabel="Open menu", label="Toggle (Open: Mobile)"),
            ], ariaLabel="Main", mobileMenu="custom", mobileMenuCustomBreakpoint=1200),
            block("header__cta", [
                block("header__phone", [
                    block("header__phone-ico", [svg("icon-phone.svg")], tag="span"),
                    block("header__phone-text", [span("Call or text", "header__phone-label"), span(PHONE, "header__phone-num")], tag="span"),
                ], href=link(TEL, aria=f"Call or text {PHONE}")),
                btn("Get a Quote", "/contact/", "btn--primary btn--s"),
            ]),
        ]),
    ], tag="div")
    return [topbar, head]


# --------------------------------------------------------------------------
# FOOTER TEMPLATE (+ mobile call bar)
# --------------------------------------------------------------------------
def footer():
    def col(title, links):
        return block("footer__col", [h("h2", title, "footer__heading")] + [a(x, u) for x, u in links])

    foot = section("footer section--deep", [
        container([
            block("footer__grid", [
                block("footer__col", [
                    block("logo logo--footer", [img("logo.png", alt="PNW Trenchless")], href=link("/", aria="PNW Trenchless home")),
                    span("Less digging. Less disruption. Built to last."),
                    span(ADDRESS, **when(ADDRESS)),
                    a(PHONE, TEL, "footer__phone"),
                    a(EMAIL, MAIL),
                    block("social", [
                        block("social__link", [svg("icon-fb.svg")], href=link(FB, True, "PNW Trenchless on Facebook")),
                        block("social__link", [svg("icon-mail.svg")], href=link(MAIL, aria="Email PNW Trenchless")),
                        block("social__link", [svg("icon-chat.svg")], href=link(SMS, aria="Text PNW Trenchless")),
                    ]),
                ]),
                col("Services", [("Sewer Pipe Lining", "/services/sewer-pipe-lining/"), ("Pipe Bursting", "/services/pipe-bursting/"), ("Water Line Pulling", "/services/water-line-pulling/"), ("Point Repairs", "/services/point-repairs/")]),
                col("Service Areas", [(x, "/" + x.lower().replace(" ", "-") + "/") for x in ["Spokane", "Spokane Valley", "Deer Park", "Clayton", "Stevens County", "Spokane County"]]),
                block("footer__col", [h("h2", "Company", "footer__heading"), a("About", "/about/"), a("Who We Serve", "/who-we-serve/"), a("Projects", "/projects/"), a("Reviews", "/reviews/"), a("Contact", "/contact/"), span(HOURS, "text-light-muted", **when(HOURS))]),
            ]),
            t("TRENCHLESS", "footer__word", tag="div", _attributes=attrs(aria_hidden="true")),
            block("footer__bottom", [
                span("© 2026 PNW Trenchless · WA Contractor Reg. #PNWTRT*744KQ · Licensed, bonded &amp; insured"),
                block("footer__legal", [a("Privacy", "/privacy-policy/"), span("·"), a("Accessibility", "#")], tag="span"),
            ]),
        ]),
    ], tag="footer", label="Footer")
    callbar = block("callbar", [
        btn("Call / Text", SMS, "btn--white btn--outline btn--s", icon="icon-chat.svg", icon_left=True),
        btn("Free Estimate", "#estimate", "btn--primary btn--s"),
    ], _attributes=attrs(aria_label="Quick contact"))
    # Site-wide quote section (user, 2026-11-09): lives in the footer template, above the footer,
    # on every page except Contact (which has its own form section with id="estimate").
    quote = estimate()
    quote.settings["_conditions"] = [[{"id": "nocnt", "key": "post_id", "compare": "!=", "value": str(CONTACT_ID)}]]
    return [quote, foot, callbar]


# --------------------------------------------------------------------------
# HOME SECTIONS
# --------------------------------------------------------------------------
def head_split(eyebrow_text, title, right):
    return block("section__head section__head--split", [
        block("section__head-main", [eyebrow(eyebrow_text), h("h2", title)]),
        right,
    ])


def head(eyebrow_text, title, intro=None):
    kids = [eyebrow(eyebrow_text), h("h2", title)]
    if intro:
        kids.append(t(intro, "section__intro"))
    return block("section__head", kids)


def hero():
    # Real job photo (client, 2026-11-09) in place of the drawn camera screen.
    feed = block("hero-feed hero-photo", [img("job-access-pit.jpg", "cover-img", alt="A small, shored access pit in a front lawn on a PNW Trenchless job")], tag="figure")
    proof = [("icon-liner.svg", "Pipe bursting, CIPP lining, water line pulling &amp; point repairs"),
             ("icon-yard.svg", "Two small access points instead of a trench across your property"),
             ("icon-film.svg", "Camera footage before and after, yours to keep")]
    return section("section hero section--dark grain", [
        block("hero__bg", [img("trailer.jpg", alt="")]),
        container([
            block("hero__inner", [
                block("stack-l", [
                    block("hero__kicker rise", [
                        span(f"{RATING} ★★★★★ on Google", "chip", **when(RATING)),
                        span("Family-owned · 14+ years · Residential, commercial &amp; industrial"),
                    ]),
                    t("Trenchless sewer &amp; water line repair · Spokane, WA", "label-wide rise rise--2"),
                    h("h1", 'Fix the pipe. <span class="serif">Keep the yard.</span>', "hero__title rise rise--3"),
                    t("Family-owned and led by Mike Jeisma, with 14+ years in trenchless sewer and water line work. We camera the line, show you exactly what we see, and give you a true and honest quote.", "hero__lede rise rise--4"),
                    block("hero__actions rise rise--5", [
                        btn("Get a True &amp; Honest Quote", "/contact/", "btn--primary", icon="icon-arrow.svg"),
                        btn("Text a Photo of the Problem", SMS, "btn--white btn--outline", icon="icon-camera.svg", icon_left=True),
                    ]),
                ]),
                block("stack-s rise rise--5", [
                    feed,
                    t("<strong>One small pit, not a trench.</strong> A real access pit from one of our jobs.", "hero-feed__cap"),
                ]),
            ]),
            block("hero__proof", [block("hero__proof-item", [svg(i), span(x)], tag="li") for i, x in proof], tag="ul"),
        ]),
    ], label="Hero")


def ticker():
    items = [("icon-liner.svg", "Sewer pipe lining", "CIPP"), ("icon-burst.svg", "Pipe bursting", "HDPE"),
             ("icon-drop.svg", "Water line replacement", "CTS POLY"), ("icon-patch.svg", "Point repairs", "SPOT LINER")]

    def group(hidden):
        kids = []
        for n, (ic, name, spec) in enumerate(items):
            cls = "ticker__item" + (" ticker__item--outline" if n % 2 == 1 else "")
            extra = {"_attributes": attrs(tabindex="-1")} if hidden else {}
            kids.append(block(cls, [block("ticker__ico", [svg(ic)], tag="span"), span(name, "ticker__name"), span(spec, "ticker__spec")], href="#services", **extra))
            kids.append(div("ticker__joint", tag="span", _attributes=attrs(aria_hidden="true")))
        return block("ticker__group", kids, **({"_attributes": attrs(aria_hidden="true")} if hidden else {}))

    words = [("less digging", "Spokane"), ("less disruption", "Spokane Valley"), ("built to last", "Deer Park"),
             ("no trench", "Clayton"), ("yard intact", "Stevens County"), ("honest pricing", "Spokane County")]

    def sub():
        kids = []
        for w, city in words:
            kids += [span(w, "ticker__word"), div("ticker__dot", tag="i"), span(city, "label-wide"), div("ticker__dot", tag="i")]
        return block("ticker__group ticker__group--sub", kids)

    return section("ticker", [
        block("ticker__row", [block("ticker__track", [group(False), group(True)])]),
        block("ticker__row", [block("ticker__track ticker__track--reverse", [sub(), sub()])], _attributes=attrs(aria_hidden="true")),
    ], label="Service ticker", _attributes=attrs(aria_label="Our trenchless services"))


def stats():
    data = [("14<small>+ yrs</small>", "repairing sewer &amp; water lines in the Inland NW"),
            ("2", "small access pits instead of one long trench"),
            ("50<small>+ yrs</small>", "expected lifespan of new HDPE pipe"),
            ('<span class="tbc">X</span><small>-yr</small>', "workmanship warranty on every repair")]
    return section("section section--tint section--tight", [
        container([block("stats__grid", [block("stat", [span(n, "stat__num"), span(l, "stat__label")], tag="li") for n, l in data], tag="ul")]),
    ], label="Stats", _attributes=attrs(aria_label="At a glance"))


def signs():
    rows = [("icon-sign-recurring-clogs.svg", "Recurring clogs", "Drains back up again weeks after clearing.", "Most common"),
            ("icon-sign-gurgling-drains.svg", "Gurgling drains", "Toilets bubble when the tub drains.", "Blockage"),
            ("icon-sign-sewer-odor.svg", "Sewer odor", "A smell in the basement or the yard.", "Crack or break"),
            ("icon-yard.svg", "Soggy or extra-green patches", "Lush strips of lawn over the line's path.", "Leak"),
            ("icon-sign-tree-roots.svg", "Tree roots", "Roots pulled out on your plumber's snake.", "Joint intrusion"),
            ("icon-sign-low-water-pressure.svg", "Low water pressure", "Often corroded galvanized water service.", "Water line")]
    return section("section section--tint section--flush-top", [
        container([
            block("split", [
                block("sticky-aside", [
                    eyebrow("Warning signs"),
                    h("h2", 'Is your sewer line <span class="serif">failing?</span>'),
                    t("Most homeowners call us after the third snake job in a year. If any of these sound familiar, a camera inspection will tell you what's actually happening underground."),
                    btn("Book a camera inspection", "/contact/", "btn--base btn--outline", icon="icon-camera.svg", icon_left=True),
                ]),
                block("list-ruled-strong", [
                    block("sign", [block("sign__ico", [svg(ic)], tag="span"), block("sign__body", [h("h3", ti, "title-l"), t(tx, "caption")]), span(tag, "sign__tag")], tag="li")
                    for ic, ti, tx, tag in rows
                ], tag="ul"),
            ]),
        ]),
    ], label="Warning signs")


def explain():
    facts = [("Digging", "Trench the full length", "1–2 small access points"),
             ("Lawn, driveway, trees", "Removed, then rebuilt", "Left intact in most cases"),
             ("Restoration", "Landscaping, concrete, paving extra", "Minimal"),
             ("Disruption", "Yard torn up for the duration", "Water off for hours, not days")]
    video = block("explain__media", [
        img("job-during.jpg", alt="A small access pit dug in a front lawn during a trenchless sewer repair"),
        block("explain__caption", [span("On the job", "explain__caption-label"), span("One small access pit instead of a trench across the yard", "explain__caption-title")], tag="figcaption"),
    ], tag="figure")
    xsec = block("xsec", [
        block("xsec__bar", [
            h("h3", "See the difference in your yard", "xsec__title"),
            block("xsec__toggle", [
                div("xsec__toggle-btn", [span("Traditional dig")], tag="button", _cssId="xsec-dig", _attributes=attrs(type="button", aria_pressed="true"), _interactions=mode_switch("dig", "xd")),
                div("xsec__toggle-btn", [span("Trenchless")], tag="button", _cssId="xsec-trenchless", _attributes=attrs(type="button", aria_pressed="false"), _interactions=mode_switch("trenchless", "xt")),
            ], _attributes=attrs(role="group", aria_label="Repair method")),
        ]),
        block("xsec__art", [svg("art-cross-section.svg", _attributes=attrs(role="img", aria_label="Cross-section of a yard from house to street, showing either a full trench or two small access pits"))]),
        block("xsec__facts", [
            block("xsec__fact", [span(lbl, "xsec__fact-label"), t(f'<span data-show="dig">{d}</span><span data-show="trenchless">{tr}</span>', "xsec__fact-value", tag="span")])
            for lbl, d, tr in facts
        ]),
    ], _cssId="xsec", _attributes=attrs(data_mode="dig"))
    return section("section section--white", [
        container([
            block("split split--center", [
                block("text-block explain__text", [
                    eyebrow("The basics"),
                    h("h2", 'What is trenchless <span class="serif">pipe repair?</span>'),
                    t("Instead of digging a trench the full length of your sewer or water line, we open one or two small access points and repair or replace the pipe underground. Your lawn, driveway, trees and landscaping stay where they are."),
                    t("There are two main ways to do it. <strong>Pipe lining</strong> builds a new pipe inside the old one. <strong>Pipe bursting</strong> pulls a brand-new pipe through while breaking the old one apart. The camera tells us which one you need."),
                ]),
                video,
            ]),
            xsec,
        ]),
    ], sid="how", label="What is trenchless")


def services():
    cards = [
        ("", "/services/sewer-pipe-lining/", "art-service-lining.svg", "CIPP · pipe in a pipe", "Sewer pipe lining",
         "A resin liner cures inside your old pipe, creating a seamless, jointless pipe within a pipe. No trench, and no joints for roots to find.",
         ["Cracks", "Leaks", "Root intrusion"]),
        ("svc-card--accent", "/services/pipe-bursting/", "art-service-burst.svg", "HDPE · full replacement", "Pipe bursting",
         "A bursting head breaks the old pipe outward while new HDPE pipe is pulled in behind it. A completely new pipe with a 50+ year lifespan, and it can be upsized for better flow.",
         ["Collapsed lines", "Orangeburg", "Clay", "Upsizing"]),
        ("svc-card--water", "/services/water-line-pulling/", "art-service-water.svg", "CTS poly · pressure tested", "Water line replacement",
         "We pull a new CTS poly line underground, reconnect it, and test it for pressure and leaks. No rust or scale buildup, and better water pressure.",
         ["Old galvanized", "Leaks", "Low pressure"]),
        ("svc-card--accent", "/services/point-repairs/", "art-service-spot.svg", "Spot repair · localized relining", "Point repairs",
         "When the damage is isolated to one section and the rest of the pipe is sound, we reline just that spot instead of replacing the whole line.",
         ["One bad joint", "A single crack", "Localized roots"]),
    ]

    def card(mod, url, art, spec, title, text, tags):
        # Image, arrow and heading all link to the service page. The image and arrow are hidden
        # from screen readers and skipped by Tab, so each card has one announced link (the heading).
        quiet = attrs(aria_hidden="true", tabindex="-1")
        return block(("svc-card " + mod).strip(), [
            block("svc-card__art", [svg(art)], href=url, _attributes=quiet),
            block("svc-card__body", [
                block("svc-card__top", [span(spec, "svc-card__spec"), block("svc-card__go", [svg("icon-arrow.svg")], href=url, _attributes=quiet)]),
                h("h3", title, "svc-card__title", link=link(url)),
                t(text),
                block("svc-card__foot", [span("Best for", "svc-card__foot-label")] + [span(x, "pill-tag") for x in tags]),
            ]),
        ], tag="li")

    return section("section section--tint", [
        container([
            head_split("Services", 'Four ways we fix it, <span class="serif">without the trench.</span>',
                       t("Every job starts with a CCTV camera inspection. We match the method to your pipe, not the other way around.", "section__intro section__intro--narrow")),
            block("svc-grid", [card(*c) for c in cards], tag="ul"),
            block("svc-strip", [
                block("svc-strip__text", [svg("icon-film.svg"), span("Every job starts with a CCTV inspection, and you keep the before and after footage.")], tag="span"),
                btn("Request a quote", "/contact/", "btn--primary", icon="icon-arrow.svg"),
            ]),
        ]),
    ], sid="services", label="Services")


def audience():
    cards = [("icon-home.svg", "Homeowners", "Sewer and water lines under lawns, driveways, patios and mature trees. Small access points instead of a torn-up yard.",
              ["Sewer lateral lining &amp; bursting", "Water service line pulls", "Camera footage you keep"]),
             ("icon-building.svg", "Commercial properties", "We choose methods that keep your property open and running during the work, with less disruption to parking, landscaping and tenants.",
              ["Lines under parking lots &amp; hardscape", "Clear schedule and budget up front", "Lower restoration costs"]),
             ("icon-factory.svg", "Industrial &amp; municipal", "Larger lines and longer runs, with a CCTV assessment, a written recommendation, and documentation from evaluation through final testing.",
              ["Site and pipe condition evaluation", "Lifecycle cost comparison", "Code and compliance focused"])]
    return section("section section--white", [
        container([
            head_split("Who we work for", 'Homes, businesses <span class="serif">and industrial sites.</span>',
                       t("Trenchless repair and replacement for residential, commercial and industrial properties, from a home's sewer line to lines under parking lots, roadways and working facilities.", "section__intro section__intro--narrow")),
            block("grid-3", [
                block("aud-card", [
                    block("aud-card__ico", [svg(ic)], tag="span"),
                    h("h3", ti, "title-card"),
                    t(tx),
                    block("checklist", [block("checklist__item", [svg("icon-check.svg"), span(x)], tag="li") for x in items], tag="ul"),
                ], tag="li") for ic, ti, tx, items in cards
            ], tag="ul"),
        ]),
    ], sid="who", label="Who we serve")


def compare():
    rows = [("Digging", "1–2 small access points", "Trench the full length of the pipe"),
            ("Lawn, driveway, trees", "Left intact in most cases", "Removed, then rebuilt"),
            ("Typical timeline", 'Faster in most cases (<span class="tbc">X</span> day typical)', '<span class="tbc">X</span> days to weeks'),
            ("Restoration costs", "Minimal", "Landscaping, concrete, paving extra"),
            ("Finished pipe", "Seamless, root- and corrosion-resistant. HDPE rated 50+ years", "New pipe, with joints"),
            ("Disruption to your home", "Water off for hours, not days", "Yard torn up for the duration")]
    cells = [
        block("compare__cell compare__cell--head", [span("Factor", "eyebrow")], _attributes=attrs(role="columnheader")),
        block("compare__cell compare__cell--head compare__cell--us", [span("PNW Trenchless", "compare__kicker"), span("Trenchless")], _attributes=attrs(role="columnheader")),
        block("compare__cell compare__cell--head", [span("The old way", "compare__kicker"), span("Traditional excavation")], _attributes=attrs(role="columnheader")),
    ]
    for i, (lbl, us, them) in enumerate(rows):
        last = " compare__cell--last" if i == len(rows) - 1 else ""
        cells += [
            t(lbl, "compare__cell compare__cell--label", tag="div", _attributes=attrs(role="rowheader")),
            t(us, "compare__cell compare__cell--us" + last, tag="div", _attributes=attrs(role="cell")),
            t(them, "compare__cell text-muted", tag="div", _attributes=attrs(role="cell")),
        ]
    return section("section section--tint", [
        container([
            head("Trenchless vs. traditional", 'The repair price is <span class="serif">only part of the cost.</span>',
                 "With a traditional dig you also pay to restore everything that came out of the ground."),
            block("compare", [block("compare__table", cells, _attributes=attrs(role="table", aria_label="Trenchless compared with traditional excavation"))]),
            block("note", [svg("icon-alert.svg"), t("<strong>Trenchless isn't right for every pipe.</strong> If a section has a belly (sag) or is out of grade, digging that spot may be the better fix, and we'll tell you so.")]),
        ]),
    ], label="Comparison")


def decide():
    outs = [("", "If the camera shows", "The pipe still holds its shape", "Cracks, joint gaps and roots, but structurally intact.", "Pipe lining"),
            ("outcome--burst", "If the camera shows", "It's collapsed or deformed", "Orangeburg, crushed clay, or you need a bigger diameter.", "Pipe bursting"),
            ("outcome--spot", "If the damage is", "Isolated to one spot", "One bad joint or crack, and the rest of the pipe is sound.", "Point repair"),
            ("outcome--water", "If the problem is", "Your water service", "Rusty galvanized pipe, repeated leaks, weak pressure.", "Water line pull")]
    return section("section section--white", [
        container([
            head("Which repair do I need?", 'Lining or bursting? <span class="serif">The camera decides.</span>'),
            block("flow", [
                block("flow__start", [
                    block("feed flow__feed", [
                        div("feed__cross", tag="span"),
                        block("feed__hud feed__hud--top", [span("INSPECT", "feed__rec")]),
                        block("feed__hud", [span("STEP 1", "feed__ft")]),
                    ], _attributes=attrs(role="img", aria_label="Camera inspection view")),
                    t("Every recommendation starts with what the camera actually shows."),
                ]),
                block("flow__lines", [svg("art-flow-lines.svg")], _attributes=attrs(aria_hidden="true")),
                block("flow__outcomes", [
                    block(("outcome " + mod).strip(), [span(i, "label outcome__if"), h("h3", ti, "outcome__title"), t(tx), span(pill, "outcome__pill")], tag="article")
                    for mod, i, ti, tx, pill in outs
                ]),
            ]),
        ]),
    ], label="Decision flow")


def process():
    steps = [("Camera inspection", "We run a camera through the line and locate the problem."),
             ("You see the footage", "Mike walks you through what's wrong and your options."),
             ("Written quote", "Clear scope and price. No pressure."),
             ("Trenchless repair", "Small access points, repair done, area restored."),
             ("Final camera proof", "A post-repair video for your records and warranty.")]
    return section("section section--dark grain", [
        container([
            head_split("Our process", 'Start to finish, <span class="serif">on camera.</span>',
                       btn("Start with step 01", "/contact/", "btn--primary", icon="icon-arrow.svg")),
            block("steps", [block("step", [h("h3", ti, "step__title"), t(tx)], tag="li") for ti, tx in steps], tag="ol"),
        ]),
    ], sid="process", label="Process")


def mike():
    creds = [("icon-check.svg", "14+ years in trenchless sewer &amp; water line repair"),
             ("icon-check.svg", '<span class="tbc">Manufacturer certifications</span>'),
             ("icon-shield.svg", "WA Reg. #PNWTRT*744KQ, licensed, bonded &amp; insured"),
             ("icon-home.svg", f"Lives and works locally in {ADDRESS}")]
    return section("section section--tint", [
        container([
            block("split split--center split--mike", [
                block("mike__media", [
                    block("mike__photo", [
                        img("job-access-pit.jpg", "cover-img", alt="A shored access pit in a front lawn on a PNW Trenchless job"),
                        block("mike__plate", [
                            block("mike__id", [span("Mike Jeisma", "mike__name"), span("Owner &amp; lead technician", "caption-light")], tag="span"),
                            span(f'{ADDRESS} · Est. <span class="tbc">2025</span>', "mike__est"),
                        ]),
                    ]),
                    img("trailer.jpg", "mike__inset", alt="PNW Trenchless equipment trailer"),
                ]),
                block("stack-l", [
                    eyebrow("Family-owned · meet the owner"),
                    t("We treat every project like it’s for our own family. Our customers deserve honest work, fair pricing, and results built to last.", "mike__quote", tag="blockquote"),
                    t('PNW Trenchless is a family-owned company built on honesty, quality workmanship and customer care. Mike has spent 14+ years in sewer and water line work across the Spokane area, the last decade-plus focused on trenchless lining and bursting. In <span class="tbc">2025</span> he started PNW Trenchless to do it his way: show customers the footage, give them a straight answer, and do the work himself.', "mike__bio"),
                    block("creds", [block("creds__item", [svg(ic), span(tx)], tag="li") for ic, tx in creds], tag="ul"),
                    block("mike__sign", [
                        block("mini-stack", [span("Mike Jeisma", "mike__sig-name"), span("Owner, PNW Trenchless", "caption-neutral")], tag="span"),
                        a("Read Mike's full story", "/about/", "link-arrow"),
                    ]),
                ]),
            ]),
        ]),
    ], sid="mike", label="About Mike")


def projects():
    return section("section section--white", [
        container([
            head_split("Recent projects", 'Real jobs. <span class="serif">Real yards.</span>', a("See all projects", "/projects/", "link-arrow")),
            # Bricks query loops over the `project` post type (elements_projects.py).
            block("", [__import__("elements_projects").project_feature(
                {"objectType": "post", "post_type": ["project"], "orderby": "date", "order": "desc", "no_found_rows": True, "posts_per_page": 1,
                 "meta_query": [{"id": "feat", "key": "featured", "value": "1", "compare": "="}]}, label="Featured project (loop)", cta=False)], label="Featured project"),
            block("projects__more", [__import__("elements_projects").project_mini(
                {"objectType": "post", "post_type": ["project"], "orderby": "date", "order": "desc", "no_found_rows": True, "posts_per_page": 2, "offset": 1,
                 "meta_query": [{"id": "real", "key": "is_placeholder", "value": "1", "compare": "!="}]})]),
        ]),
    ], sid="projects", label="Projects")


def review_loop(query, label="Review (query loop)"):
    """One review card, repeated by a Bricks query loop over the Testimonials post type.
    Content comes from ACF fields: review_text, rating, city, source; the name is the post title."""
    q = {"objectType": "post", "post_type": ["testimonial"], "orderby": "date", "order": "desc", "no_found_rows": True}
    q.update(query)
    return N("block", "review", [
        span("★★★★★", "stars", _attributes=attrs(role="img", aria_label="{acf_rating} out of 5 stars", data_rating="{acf_rating}")),
        t("{acf_review_text}", "review__quote", tag="blockquote"),
        block("review__by", [
            block("review__av", [span("{post_title}", "review__initial")], tag="span", _attributes=attrs(aria_hidden="true")),
            block("id-stack", [span("{post_title}", "review__author"), span("{acf_city} · {acf_source}", "fine-light")], tag="span"),
        ], tag="figcaption"),
    ], label=label, tag="figure", hasLoop=True, query=q)


def reviews():
    return section("section section--dark grain", [
        container([
            head("Reviews", 'What Spokane homeowners <span class="serif">say.</span>'),
            block("reviews__grid", [
                block("rating", [
                    span(RATING, "rating__num", **when(RATING)),
                    span('<span class="tbc">X.X</span>', "rating__num", **when(RATING, "==")),
                    span("★★★★★", "stars", _attributes=attrs(aria_label="5 stars")),
                    t(f"Average from {REVIEWS} Google reviews", **when(REVIEWS)),
                    t("Average Google rating", **when(REVIEWS, "==")),
                    a("Read them on Google", link(GOOGLE_URL, True), "link-arrow", **when(GOOGLE_URL)),
                ]),
                block("review-row", [
                    review_loop({"posts_per_page": 3, "meta_query": [{"id": "featured", "key": "featured", "value": "1", "compare": "="}]},
                                label="Featured reviews (loop)"),
                ]),
            ]),
            block("assure", [
                block("assure__item", [svg("icon-shield.svg"), h("h3", '<span class="tbc">X</span>-year warranty on every repair', "assure__title"), t('<span class="tbc">What\'s covered: materials and workmanship, transferable if you sell?</span>')]),
                block("assure__item", [svg("icon-card.svg"), h("h3", "Sewer emergencies don't wait for payday", "assure__title"), t('<span class="tbc">Financing partner, terms and apply link (if offered).</span>')]),
            ]),
        ]),
    ], sid="reviews", label="Reviews")


def areas():
    cities = [("Spokane", "Metro"), ("Spokane Valley", "East"), ("Deer Park", "North"), ("Clayton", "Home base"), ("Stevens County", "North"), ("Spokane County", "+ nearby")]
    return section("section section--tint", [
        container([
            block("split split--center split--areas", [
                block("text-block", [
                    eyebrow("Local expertise"),
                    h("h2", 'Built for <span class="serif">Inland Northwest</span> sewer lines.'),
                    t('Many older Spokane-area homes still run on clay, cast iron or Orangeburg sewer lines and galvanized water service. Add mature pines and maples, and root intrusion is one of the most common problems we see. <span class="tbc">Mike to add 2–3 sentences from his own experience: neighborhoods, soil, depth.</span>'),
                    block("chip-row", [span(x, "material") for x in ["Clay", "Cast iron", "Orangeburg", "Galvanized"]], _attributes=attrs(aria_label="Pipe materials common in the area")),
                    block("list-ruled-strong", [block("", [block("city", [span(c), span(n, "city__note")], href="/contact/")], tag="li") for c, n in cities], tag="ul"),
                ]),
                block("map", [
                    # The Google map embed (Website Settings) replaces the illustrated map when it is filled in.
                    t(MAP_IFRAME, "map__embed", tag="div", **when(MAP_IFRAME)),
                    svg("art-service-map.svg", _attributes=attrs(role="img", aria_label="Service area map from Clayton south to Spokane and Spokane Valley"), **when(MAP_IFRAME, "==")),
                    t("APPROXIMATE SERVICE AREA · CLAYTON TO SPOKANE METRO", "map__caption", tag="figcaption", **when(MAP_IFRAME, "==")),
                ], tag="figure"),
            ]),
        ]),
    ], sid="areas", label="Service areas")


FAQ = [
    ("How much does trenchless sewer repair cost in Spokane?", ["It depends on the length of the line, how deep it is, how easy it is to reach, and whether it needs lining or bursting. After a camera inspection you get a written quote with a fixed scope, so there are no surprises.", '<span class="tbc">Honest price range from Mike.</span>'], True),
    ("Is a lined pipe as strong as a new one?", ['A cured-in-place liner forms a seamless, jointless pipe inside the old one. With no joints, roots have nowhere to get in. <span class="tbc">Design life and liner spec.</span>'], True),
    ("Will you have to dig at all?", ["Usually one or two small access points, not a trench. If the camera shows a sag or a section that's out of grade, digging that one spot may be the better fix, and we'll tell you before we start."], True),
    ("How long does the job take, and can I use my plumbing?", ['Most jobs take <span class="tbc">X</span> day(s). Your water or sewer is off for hours, not days, and we\'ll tell you exactly when.'], True),
    ("Can you fix a pipe full of tree roots?", ["Yes. We clear the roots, then line the pipe so there are no joints for them to grow back through."], True),
    ("What if my pipe has collapsed?", ["Lining needs a pipe that still holds its shape. For a collapsed or crushed line, pipe bursting pulls a brand-new HDPE pipe through the old path."], True),
    ("Do you work on commercial and industrial properties?", ["Yes. Along with homes, we repair and replace lines for commercial and industrial properties, and we choose methods that keep your property running during the work."], False),
    ("How do you decide which method to use?", ["We look at the pipe on camera, plus access points, soil, surface use and nearby utilities. Then we recommend the method that fits: bursting for full replacement, lining for sound host pipes, or a point repair when damage is isolated. You get the reasoning, schedule and budget in writing."], False),
    ("Does homeowners insurance cover sewer line repair?", ['It depends on your policy and any service-line coverage you carry. We can provide camera footage and a written report for your insurer. <span class="tbc">Mike to add what he typically sees.</span>'], True),
    ("Do you handle permits?", ['<span class="tbc">Yes / which jurisdictions, and how it\'s billed.</span>'], True),
]


def faq():
    items = []
    for q, answers, draft in FAQ:
        content = [t(x) for x in answers]
        items.append(block("faq__item", [
            block("", [h("h3", q, "faq__q")], label="Title", _hidden={"_cssClasses": "accordion-title-wrapper"}),
            block("faq__answer", content, label="Content", _hidden={"_cssClasses": "accordion-content-wrapper"}),
        ], label="Item"))
    # FAQ schema stays off until Mike confirms the draft answers.
    return section("section section--white", [
        container([
            block("split split--faq", [
                block("sticky-aside", [
                    eyebrow("FAQ"),
                    h("h2", 'Straight <span class="serif">answers.</span>'),
                    t("Don't see your question? Call or text Mike and he'll give you a straight answer."),
                    btn(PHONE, TEL, "btn--base btn--outline", icon="icon-phone.svg", icon_left=True),
                ]),
                N("accordion-nested", "faq__list", items, expandItem="0", independentToggle=True),
            ]),
        ]),
    ], sid="faq", label="FAQ")


def quote_form(title_tag="h3", extra_cls=""):
    """The white quote card around Fluent Forms "Request a quote" (one form for every page;
    Fluent stores the page URL with each entry)."""
    return block(("form " + extra_cls).strip(), [
        block("form__head", [h(title_tag, "Request a quote", "form__title"), span("Takes about a minute", "caption-neutral")]),
        N("shortcode", "form__fluent", shortcode=f'[fluentform id="{QUOTE_FORM_ID}"]'),
        t('No obligation. We reply personally, usually <span class="tbc">same day</span>.', "form__fine"),
    ], label=f"Quote form (Fluent Forms #{QUOTE_FORM_ID})")


def estimate(kicker="Request a quote", title='Get a <span class="serif">true and honest</span> quote.',
             intro="Give us some details and we'll reach out right away. Homes, businesses and industrial sites across Spokane and Stevens County.",
             contact_ways=True):
    ways = [("icon-phone.svg", "Call", PHONE, TEL, False), ("icon-chat.svg", "Text", "Send a photo", SMS, False),
            ("icon-mail.svg", "Email", "Write to us", MAIL + "?subject=Quote%20request", False), ("icon-fb.svg", "Facebook", "Message us", FB, True)]

    form = quote_form()
    return section("section section--dark estimate", [
        div("estimate__glow", _attributes=attrs(aria_hidden="true")),
        container([
            block("split split--center", [
                block("text-block-light estimate__text", [
                    eyebrow(kicker),
                    h("h2", title),
                    t(intro),
                    block("bigphone", [span("Call or text now", "bigphone__label"), span(PHONE, "bigphone__num"), span("Send a photo or video of the problem if you can.", "caption-light")], href=TEL),
                ] + ([block("contact-ways", [block("contact-way", [svg(ic), span(lbl), span(note, "contact-way__note")], href=link(u, nt)) for ic, lbl, note, u, nt in ways])] if contact_ways else []) + [
                    block("list-ruled-dark", [block("num-row", [span(f"0{i + 1}", "num-row__num"), span(x)], tag="li") for i, x in enumerate(["You send the details or a photo", "Mike calls you back and books the camera", "You see the footage and get a written quote"])], tag="ol"),
                ]),
                form,
            ]),
        ]),
    ], sid="estimate", label="Quote")


SECTIONS = [hero, ticker, stats, signs, explain, services, audience, compare, decide, process, mike, projects, reviews, areas, faq]


# --------------------------------------------------------------------------
def flatten(nodes, prefix):
    out, counter = [], [0]

    def nid():
        counter[0] += 1
        return (prefix + format(counter[0], "x").rjust(6 - len(prefix), "0"))[:6]

    def walk(n, parent):
        i = nid()
        e = {"id": i, "name": n.name, "parent": parent, "settings": n.settings}
        if n.label:
            e["label"] = n.label
        out.append(e)
        for ch in n.children:
            walk(ch, i)

    for n in nodes:
        walk(n, 0)
    return out


def build():
    data = {
        "header": flatten(header(), "h"),
        "footer": flatten(footer(), "f"),
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "s" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
        "pages": [],
    }
    import elements_lining
    data["pages"].append(elements_lining.page())
    import elements_about
    data["pages"].append(elements_about.page())
    import elements_contact
    data["pages"].append(elements_contact.page())
    import elements_bursting
    data["pages"].append(elements_bursting.page())
    import elements_projects
    data["pages"].append(elements_projects.page())
    import elements_reviews
    data["pages"].append(elements_reviews.page())
    import elements_water
    data["pages"].append(elements_water.page())
    import elements_point
    data["pages"].append(elements_point.page())
    import elements_serve
    data["pages"].append(elements_serve.page())
    import elements_city
    data["templates"] = [elements_projects.single_template(), elements_city.template()]
    pathlib.Path(__file__).with_name("elements.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    return data


if __name__ == "__main__":
    d = build()
    print("header", len(d["header"]), "footer", len(d["footer"]), "sections", [(s["key"], len(s["elements"])) for s in d["sections"]])
