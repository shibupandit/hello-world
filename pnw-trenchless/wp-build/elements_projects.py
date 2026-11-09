"""Projects: the /projects/ page, the single project template, and the shared query-loop cards.

Built from pnw-trenchless/projects.html and project-single.html (2026-11-09). Projects are the
ACF post type `project` (fields: title_accent, service, setting, summary, featured, is_placeholder,
location, completed, time_on_site, problem, method, yard, digging, old_pipe, new_pipe, length,
story_problem, story_work, story_result, cover_image, before_image, after_image, work_image,
work_caption, gallery). Every card and detail is Bricks dynamic data; empty fields are hidden
with element conditions, so nothing unconfirmed is shown.
"""
from elements import (N, section, container, block, div, h, t, span, a, svg, img, btn, eyebrow, attrs, link,
                      head, head_split, estimate, flatten, review_loop, when, TEL, PHONE)

PROJECTS = "/projects/"
BASE_Q = {"objectType": "post", "post_type": ["project"], "orderby": "date", "order": "desc", "no_found_rows": True}


def q(**extra):
    d = dict(BASE_Q)
    d.update(extra)
    return d


def dimg(tag, cls="cover-img", size="large"):
    """Image element filled from an ACF image field (attachment ID)."""
    return N("image", cls, image={"useDynamicData": tag, "size": size})


def any_of(*tags):
    """Bricks conditions: show when at least one of the dynamic tags is not empty (OR between sets)."""
    return {"_conditions": [[{"id": f"o{i}{t.strip('{}')[4:8]}", "key": "dynamic_data", "compare": "!=", "value": "", "dynamic_data": t}] for i, t in enumerate(tags)]}


def title_html(cls_serif="serif"):
    return f'{{post_title}} <span class="{cls_serif}">{{acf_title_accent}}</span>'


# --- shared loop cards ------------------------------------------------------
def project_feature(query, label="Project feature (loop)", cta=True):
    """The dark 'Real jobs. Real yards.' card: during/after photos + details. One per project."""
    rows = [("Location", "{acf_location}"), ("Problem", "{acf_problem}"), ("Method", "{acf_method}"), ("Yard", "{acf_yard}")]
    spec = []
    for term, tag in rows:
        spec += [t(term, "spec__term", tag="dt", **when(tag)), t(tag, "spec__value", tag="dd", **when(tag))]
    info = [
        eyebrow("{acf_service} · {acf_setting}"),
        span(title_html(), "project__title"),
        block("spec", spec, tag="dl", **any_of(*[x for _, x in rows])),
    ]
    if cta:
        info.append(a("View project", link("{post_url}"), "link-arrow project__link"))
    return N("block", "project", [
        block("job-pair", [
            block("job-pair__fig", [dimg("{acf_before_image}", None), span("DURING", "job-pair__tag")], tag="figure"),
            block("job-pair__fig", [dimg("{acf_after_image}", None), span("AFTER", "job-pair__tag job-pair__tag--after")], tag="figure"),
        ]),
        block("project__info", info),
    ], label=label, tag="article", hasLoop=True, query=query)


def project_card(query, label="Project card (loop)"):
    return N("block", "pcard", [
        block("pcard__media", [dimg("{acf_cover_image}")], tag="figure"),
        block("pcard__body", [
            span("{acf_service}", "pcard__tag"),
            h("h3", "{post_title}", "pcard__title"),
            t("{acf_summary}", "pcard__text", **when("{acf_summary}")),
        ]),
    ], label=label, tag="a", link=link("{post_url}"), hasLoop=True, query=query)


def project_mini(query, label="Project mini card (loop)"):
    return N("block", "mini", [
        dimg("{acf_cover_image}", None, "medium"),
        block("mini__body", [span("{post_title}", "mini__title"), span("{acf_summary}", "mini__text")], tag="span"),
    ], label=label, tag="a", link=link("{post_url}"), hasLoop=True, query=query)


REAL_ONLY = {"id": "real", "key": "is_placeholder", "value": "1", "compare": "!="}
WITH_PAIR = [{"id": "hasb", "key": "before_image", "value": "", "compare": "!="}, {"id": "hasa", "key": "after_image", "value": "", "compare": "!="}]


# --- /projects/ page -----------------------------------------------------------
def p_hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", "/", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Projects", "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))

    def tile(f, alt, tag, cls="mosaic__item", after=False):
        return block(cls, [img(f, "cover-img", alt=alt), t(tag, "mosaic__tag" + (" mosaic__tag--after" if after else ""), tag="figcaption")], tag="figure")

    return section("section svc-hero projects-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("svc-hero__content", [
                    span("Projects", "eyebrow rise"),
                    h("h1", 'Real jobs. <span class="serif">Real yards.</span>', "svc-hero__title rise rise--2"),
                    t("Every job starts with a camera and ends with one. Here's what our work actually looks like: the small pits, the pipe we pull out, what goes in its place, and the yard after we leave.", "svc-hero__lede rise rise--3"),
                    block("owner__creds rise rise--4", [
                        block("owner__cred", [svg("icon-camera.svg"), span("Camera before &amp; after")], tag="li"),
                        block("owner__cred", [svg("icon-yard.svg"), span("Small pits, not trenches")], tag="li"),
                        block("owner__cred", [svg("icon-home.svg"), span("Yard put back")], tag="li"),
                    ], tag="ul"),
                ]),
                block("mosaic rise rise--4", [
                    tile("job-access-pit.jpg", "A shored access pit in a front lawn", "Access pit", "mosaic__item mosaic__item--tall"),
                    tile("job-lined-pipe.jpg", "An old sewer pipe cut open, with the new liner cured inside", "New liner"),
                    tile("job-lawn-restored.jpg", "A front lawn after the job", "Lawn after", after=True),
                ], _attributes=attrs(aria_label="Photos from our jobs")),
            ]),
        ]),
    ], label="Hero")


def p_list():
    return section("section section--white", [
        container([
            head_split("Recent projects", 'Before, during <span class="serif">and after.</span>',
                       t("Photos straight from the job site. Details are added once the homeowner is happy for us to share them.", "section__intro section__intro--narrow")),
            block("project-list", [project_feature(q(posts_per_page=2, meta_query=WITH_PAIR + [REAL_ONLY]), cta=True)]),
            block("pcards pcards--spaced", [project_card(q(posts_per_page=12, offset=2))], tag="ul"),
        ]),
    ], sid="list", label="Projects (loops)")


def p_docs():
    steps = [("icon-camera.svg", "Camera before", "We run the camera first and show you exactly what's wrong."),
             ("icon-photo.svg", "Photos during", "Pits, old pipe and new pipe, photographed as the work happens."),
             ("icon-film.svg", "Camera after", "A final camera run proves the new line is clear and sound."),
             ("icon-check.svg", "Yours to keep", "You keep the footage for your records, warranty and resale.")]
    return section("section section--tint", [
        container([
            head_split("How we document every job", 'You see it all, <span class="serif">start to finish.</span>',
                       t("The same record you see here, you get for your own line.", "section__intro section__intro--narrow")),
            block("docs__grid", [
                block("docs__item", [block("docs__ico", [svg(ic)], tag="span"), span(f"0{i + 1}", "docs__num"), h("h3", ti, "docs__title"), t(tx, "docs__text")], tag="li")
                for i, (ic, ti, tx) in enumerate(steps)
            ], tag="ol"),
        ]),
    ], label="How we document")


def p_reviews():
    return section("section section--dark grain", [
        container([
            head_split("Reviews", 'What homeowners <span class="serif">say after.</span>', a("All reviews", "/#reviews", "link-arrow")),
            block("quotes__grid quotes__grid--3", [review_loop({"posts_per_page": 3}, label="Reviews (loop)")]),
        ]),
    ], label="Reviews")


def p_quote():
    return estimate(kicker="Free camera estimate", title='Want a result <span class="serif">like these?</span>',
                    intro="Start with a camera inspection. You'll see what we see before you decide anything.", contact_ways=False)


PAGE_SECTIONS = [p_hero, p_list, p_docs, p_reviews, p_quote]


def page():
    return {
        "key": "projects", "post_type": "page", "title": "Projects", "slug": "projects",
        "excerpt": "Real PNW Trenchless jobs: small access pits instead of trenches, the old pipe we pull out, what goes in its place, and the yard after.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "p" + format(k, "x"))} for k, fn in enumerate(PAGE_SECTIONS)],
    }


# --- single project template ---------------------------------------------------
def s_hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", "/", "crumbs__link")], tag="li"),
            block("crumbs__item", [a("Projects", PROJECTS, "crumbs__link")], tag="li"),
            block("crumbs__item", [span("{post_title}", "crumbs__current", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    meta = [("Location", "{acf_location}"), ("Service", "{acf_service}"), ("Completed", "{acf_completed}"), ("Time on site", "{acf_time_on_site}")]
    return section("section pj-hero section--dark grain", [
        container([
            crumbs,
            block("pj-hero__head", [
                block("pj-hero__title", [
                    span("{acf_service} · {acf_setting}", "eyebrow rise"),
                    h("h1", title_html(), "pj-hero__h1 rise rise--2"),
                ]),
                block("pj-meta rise rise--3", [
                    block("pj-meta__item", [t(term, "pj-meta__term", tag="dt"), t(tag, "pj-meta__value", tag="dd")], **when(tag))
                    for term, tag in meta
                ], tag="dl"),
            ]),
            block("pj-cover rise rise--4", [dimg("{acf_cover_image}", "cover-img", "full"), t("{acf_service}", "pj-cover__tag", tag="figcaption")], tag="figure"),
        ]),
    ], label="Hero")


def s_glance():
    items = [("Old pipe", "{acf_old_pipe}"), ("New pipe", "{acf_new_pipe}"), ("Length", "{acf_length}"), ("Digging", "{acf_digging}")]
    return section("section pj-glance section--tint", [
        container([
            block("pj-glance__grid", [
                block("pj-glance__item", [span(lab, "pj-glance__label"), span(tag, "pj-glance__value")], tag="li", **when(tag))
                for lab, tag in items
            ], tag="ul"),
        ]),
    ], label="At a glance", **any_of(*[x for _, x in items]))


def s_story():
    def blk(num, title, tag, extra=()):
        return block("pj-block", [span(num, "pj-block__num"), h("h2", title, "pj-block__title"), t(tag, "pj-block__text")] + list(extra), **when(tag))

    work_photo = block("pj-inline", [dimg("{acf_work_image}", None, "medium"), t("{acf_work_caption}", "pj-inline__cap", tag="figcaption")],
                       tag="figure", **when("{acf_work_image}"))
    card_rows = [("Service", "{acf_service}"), ("Location", "{acf_location}"), ("Problem", "{acf_problem}"), ("Method", "{acf_method}"), ("Yard", "{acf_yard}")]
    return section("section section--white", [
        container([
            block("pj-story__grid", [
                block("pj-story__body", [
                    # Shown until the story fields are filled in.
                    block("pj-block", [span("01", "pj-block__num"), h("h2", "About this job", "pj-block__title"), t("{acf_summary}", "pj-block__text"), work_photo],
                          **when("{acf_story_problem}", "==")),
                    blk("01", "The problem", "{acf_story_problem}"),
                    blk("02", "What we did", "{acf_story_work}", [block("pj-inline", [dimg("{acf_work_image}", None, "medium"), t("{acf_work_caption}", "pj-inline__cap", tag="figcaption")], tag="figure", **when("{acf_work_image}"))]),
                    blk("03", "The result", "{acf_story_result}"),
                ]),
                block("pj-aside", [
                    block("pj-card", [
                        eyebrow("This job"),
                        block("pj-card__list", [
                            block("pj-card__row", [t(term, "pj-card__term", tag="dt"), t(tag, "pj-card__value", tag="dd")], **when(tag))
                            for term, tag in card_rows
                        ], tag="dl"),
                        btn("Get a quote like this", "#estimate", "btn--primary form__submit", icon="icon-arrow.svg"),
                        block("pj-card__phone", [svg("icon-phone.svg"), span(f"Or call / text {PHONE}")], href=TEL),
                    ]),
                ], tag="aside"),
            ]),
        ]),
    ], label="The story")


def s_ba():
    return section("section section--dark grain", [
        container([
            head_split("Before &amp; after", 'Same yard, <span class="serif">before and after.</span>',
                       t("One small pit instead of a trench across the yard.", "section__intro section__intro--narrow")),
            block("job-pair pj-ba", [
                block("job-pair__fig", [dimg("{acf_before_image}", None), span("DURING", "job-pair__tag")], tag="figure"),
                block("job-pair__fig", [dimg("{acf_after_image}", None), span("AFTER", "job-pair__tag job-pair__tag--after")], tag="figure"),
            ]),
        ]),
    ], label="Before and after", _conditions=[[{"id": "bab", "key": "dynamic_data", "compare": "!=", "value": "", "dynamic_data": "{acf_before_image}"},
                                                 {"id": "baa", "key": "dynamic_data", "compare": "!=", "value": "", "dynamic_data": "{acf_after_image}"}]])


def s_gallery():
    return section("section section--white", [
        container([
            head("Job photos", 'From the <span class="serif">job site.</span>'),
            N("image-gallery", "pj-gallery", items={"useDynamicData": "{acf_gallery}"}, layout="grid", columns=3, imageSize="large", link="lightbox"),
        ]),
    ], label="Gallery", **when("{acf_gallery}"))


def s_reviews():
    return section("section section--dark grain", [
        container([
            head_split("Reviews", 'What homeowners <span class="serif">say.</span>', a("All reviews", "/#reviews", "link-arrow")),
            block("quotes__grid quotes__grid--3", [review_loop({"posts_per_page": 3}, label="Reviews (loop)")]),
        ]),
    ], label="Reviews")


def s_more():
    return section("section section--white", [
        container([
            head_split("More projects", 'Other jobs <span class="serif">like this one.</span>', a("All projects", PROJECTS, "link-arrow")),
            block("pcards", [project_card(q(posts_per_page=3, post__not_in=["{post_id}"], excludeCurrentPost=True))], tag="ul"),
        ]),
    ], label="More projects")


def s_quote():
    return estimate(kicker="Free camera estimate", title='Want a result <span class="serif">like this one?</span>',
                    intro="Start with a camera inspection. You'll see what we see before you decide anything.", contact_ways=False)


SINGLE_SECTIONS = [s_hero, s_glance, s_story, s_ba, s_gallery, s_reviews, s_more, s_quote]


def single_template():
    els = []
    for k, fn in enumerate(SINGLE_SECTIONS):
        els += flatten([fn()], "j" + format(k, "x"))
    return {"key": "project_single", "area": "content", "elements": els}
