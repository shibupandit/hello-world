"""Reviews page (/reviews/). Built from pnw-trenchless/reviews.html (approved 2026-11-09).

Rating, review count and the Google link come from the Website Settings options page.
Review cards are a Bricks query loop over the `testimonial` post type; the project strip is a
query loop over `project` (cards shared with elements_projects.py). Empty values are hidden.
"""
from elements import (N, section, container, block, h, t, span, a, svg, btn, eyebrow, attrs, link,
                      head_split, flatten, when, RATING, REVIEWS, GOOGLE_URL)
from elements_projects import project_card, q, REAL_ONLY


def hero():
    crumbs = N("block", "crumbs", [
        block("crumbs__list", [
            block("crumbs__item", [a("Home", "/", "crumbs__link")], tag="li"),
            block("crumbs__item", [span("Reviews", "text-accent-light", _attributes=attrs(aria_current="page"))], tag="li"),
        ], tag="ol"),
    ], tag="nav", _attributes=attrs(aria_label="Breadcrumb"))
    return section("section svc-hero reviews-hero section--dark grain", [
        container([
            crumbs,
            block("svc-hero__grid", [
                block("stack-l", [
                    span("Reviews", "eyebrow rise"),
                    h("h1", 'What homeowners <span class="serif">say about us.</span>', "accent-light rise rise--2"),
                    t("Real reviews from real customers, in their own words. We don't edit them, and we don't pick only the good ones: every review comes straight from Google.", "svc-hero__lede rise rise--3"),
                    block("hero__actions rise rise--4", [
                        btn("Read them on Google", link(GOOGLE_URL, True), "btn--primary", icon="icon-arrow.svg", **when(GOOGLE_URL)),
                        btn("Leave a review", "#leave", "btn--white btn--outline", icon="icon-check.svg", icon_left=True),
                    ]),
                ]),
                block("score rise rise--4", [
                    span("Google rating", "label-accent"),
                    block("score__main", [
                        span(RATING, "score__num"),
                        block("mini-stack", [
                            span("★★★★★", "score__stars", _attributes=attrs(role="img", aria_label=f"{RATING} out of 5 stars")),
                            span(f"from {REVIEWS} reviews", "text-light-muted", **when(REVIEWS)),
                            span("on Google", "text-light-muted", **when(REVIEWS, "==")),
                        ], tag="span"),
                    ]),
                ], **when(RATING)),
            ]),
        ]),
    ], label="Hero")


def review_card(query, label="Review card (loop)"):
    """One testimonial, repeated by a query loop (fields: review_text, rating, city, source)."""
    return N("block", "rv-card", [
        span("★★★★★", "stars", _attributes=attrs(role="img", aria_label="{acf_rating} out of 5 stars", data_rating="{acf_rating}")),
        t("{acf_review_text}", "rv-card__text", tag="blockquote"),
        block("rv-card__by", [
            block("review__av", [span("{post_title}", "review__initial")], tag="span", _attributes=attrs(aria_hidden="true")),
            block("id-stack", [span("{post_title}", "strong-dark"), span("{acf_city} · {acf_source}", "rv-card__meta")], tag="span"),
        ]),
    ], label=label, tag="li", hasLoop=True, query=query)


def all_reviews():
    return section("section section--white", [
        container([
            block("rv-grid", [review_card({"objectType": "post", "post_type": ["testimonial"], "orderby": "date", "order": "desc",
                                            "posts_per_page": 30, "no_found_rows": True})], tag="ul", _attributes=attrs(aria_label="All reviews")),
            block("rv-more", [btn("See every review on Google", link(GOOGLE_URL, True), "btn--base btn--outline", icon="icon-arrow.svg")], **when(GOOGLE_URL)),
        ]),
    ], sid="all", label="All reviews (loop)")


def leave():
    steps = [("Open our Google listing", "The button takes you straight to the review box."),
             ("Pick your stars", "Be honest. Every review helps us do better."),
             ("Say what we did", "Mention the service and your town, so neighbors with the same problem find it.")]
    return section("section section--dark grain", [
        container([
            block("split-even", [
                block("text-block-light rv-leave__text", [
                    eyebrow("Had work done by us?"),
                    h("h2", 'Tell your neighbors <span class="serif">how it went.</span>'),
                    t("A short Google review helps other Spokane homeowners find an honest contractor, and it helps a small family business more than you'd think."),
                    btn("Leave a Google review", link(GOOGLE_URL, True), "btn--primary", icon="icon-arrow.svg", **when(GOOGLE_URL)),
                ]),
                block("list-ruled-dark", [
                    block("rv-steps__item", [span(f"0{i + 1}", "num-row__num"),
                                             block("rv-steps__body", [span(ti, "rv-steps__title"), span(tx, "text-light-muted")], tag="span")], tag="li")
                    for i, (ti, tx) in enumerate(steps)
                ], tag="ol"),
            ]),
        ]),
    ], sid="leave", label="Leave a review")


def projects():
    return section("section section--tint", [
        container([
            head_split("The jobs behind the reviews", 'Real jobs. <span class="serif">Real yards.</span>', a("All projects", "/projects/", "link-arrow")),
            block("grid-3-2", [project_card(q(posts_per_page=3, meta_query=[REAL_ONLY]))], tag="ul"),
        ]),
    ], label="Projects (loop)")




SECTIONS = [hero, all_reviews, leave, projects]


def page():
    return {
        "key": "reviews", "post_type": "page", "title": "Reviews", "slug": "reviews",
        "excerpt": "Real Google reviews of PNW Trenchless: trenchless sewer lining, pipe bursting and water line replacement across Spokane and Stevens counties.",
        "sections": [{"key": fn.__name__, "elements": flatten([fn()], "r" + format(k, "x"))} for k, fn in enumerate(SECTIONS)],
    }
