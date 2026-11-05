# Hartwell & Crane: Bricks Builder + ACSS v3 handoff

This guide covers moving the static prototype (`index.html`, `assets/`) into WordPress with **Bricks Builder** and **Automatic.css 3.x**.

The firm name, people, numbers and case results are placeholder content. Replace them with the client's real details before launch. Attorney-advertising rules (Texas Rule 7.04, or the rules of the client's state) apply to results, testimonials and award claims.

---

## 1. How the prototype is organised

| File | Role | In WordPress |
|---|---|---|
| `assets/css/acss-shim.css` | Defines ACSS v3 variables (`--primary`, `--space-m`, `--h2` …) so the prototype runs without ACSS | **Delete.** Enter the values in the ACSS dashboard instead (section 2) |
| `assets/css/style.css` | All component styles, written only with ACSS variables and BEM classes | Paste into Bricks global classes, or keep as one stylesheet (section 4) |
| `assets/js/main.js` | Sticky header, mobile menu, FAQ, slider, form messages | Mostly replaced by native Bricks elements (section 6) |
| `index.html` | Page markup; each `<!-- ===== X ===== -->` block is one Bricks section | Rebuild as Bricks sections/components (section 5) |

Class names follow BEM (`block__element--modifier`), the same convention ACSS and Bricks' "BEM class generator" use. One block maps to one Bricks component.

---

## 2. ACSS settings (applied and verified on the site)

These settings are **already applied** on whitecrowtemplate.kinsta.cloud (ACSS 3.3.8). They were checked against the CSS that ACSS generated on 2026-11-04. `assets/css/acss-shim.css` is a copy of that output for the prototype.

### Colours (ACSS → Colors)

| Colour | Hex | Switched on | Shades set (H/S/L per shade, matching the design) |
|---|---|---|---|
| Primary | `#123a31` | yes | ultra-light `#eef4f1` · light `#c9dbd4` · dark `#0b241e` · ultra-dark `#061512` · hover `#0d2c25` |
| Accent | `#b08a4f` | **yes (was off)** | ultra-light `#f7f1e6` · light `#e6d6bb` · dark `#6f5430` · hover `#977341` |
| Base | `#1a2421` | yes | ultra-light `#f4f6f4` · light `#d8dedb` · semi-dark `#55615d` (secondary text) |
| Danger | `#b3261e` | **yes (was off)** | ultra-light, light and dark are used for form errors |
| Neutral | `#000` | yes | white and black |
| Secondary, Tertiary | — | off | secondary buttons switched off too |

**ACSS shade names:** `ultra-light`, `light`, `semi-light`, `semi-dark`, `dark`, `ultra-dark`, `hover`, plus `-trans-10 … -trans-90`. There is **no `-medium` shade** for primary or base. Secondary text uses `--base-semi-dark`.

**Why the shades were set by hand:** ACSS builds each shade at a fixed lightness. Its default "dark" is 25%, which is lighter than this primary green (15%), so the default `--primary-dark` would have been lighter than the brand colour.

**Contrast:** `--accent` on white is about 3:1. Use it for large text, icons and button backgrounds. Small text on white uses `--accent-dark`.

### Typography (ACSS → Typography)
- **Root font size:** 62.5% (was 100%). Fonts: heading **Libre Caslon Display**, text **Public Sans**, both self-hosted as Bricks custom fonts. Google Fonts stays disabled.
- **Body text:** 16 → 18px.
- **Text sizes:** `text-s` 15px · `text-xs` 13px · `text-l` 18 → 21 · `text-xl` 20 → 26 · `text-xxl` 24 → 32.
- **Headings:** h1 40 → 72 · h2 32 → 52 · h3 24 → 32 · h4 20 → 24 · h5 16 → 18 · h6 14 → 16.

### Spacing and layout
- **Content width** (`vp-max`): 1240px (was 1366). `vp-min` 360px.
- **Space:** base-space 18 → 24, scale 1.5. **Section spacing:** adjust 4.5 desktop / 3.5 mobile (were 3 / 2), so `--section-space-m` runs 63 → 108px.
- **Gutter** (`section-padding-x`): 16 → 48px.
- **Radius:** ACSS defaults (`--radius` 5px, `--radius-s` 3.3px).

### Buttons (ACSS → Buttons)
- **Style:** font-weight 600, radius `var(--radius-s)`, 2px border. Primary, accent and white buttons are on, all with outline variants.
- **Classes used in the markup:** `btn--primary`, `btn--accent`, `btn--white`, combined with `btn--outline`; sizes `btn--s` (normal, 15px) and `btn--m` (large, 16–18px); `width--full` for full-width buttons.
- **Base `.btn` class:** ACSS has none. Don't add one.
- **"Use Bricks UI for Buttons":** keep it **off**. It changes how the Bricks Button element's own style controls work.

### Breakpoints (ACSS = Bricks)
**xl 1366 · l 992 · m 768 · s 480.** The CSS uses only these, plus two content-specific extras:
- **1520px:** hides the phone label in the header.
- **1500px:** adds a margin around the boxed layout.

The nav collapses at **xl (1366)**, because seven links, the phone and the CTA need about 1200px.

### ACSS must recompile in "Bricks mode"
ACSS turns on its Bricks output only during **wp-admin** requests. If ACSS settings are saved any other way (REST, WP-CLI, an MCP or PHP script), the files compile without the Bricks layer:
- `automatic-bricks.css` is about 140 bytes instead of about 50 KB
- the `btn--*` classes are missing
- ACSS classes aren't imported into Bricks

**After any scripted change:**
- Either click **Save** once in the ACSS dashboard,
- or run this in PHP before saving:
  ```php
  add_filter('automaticcss_framework_variables', fn($v) => $v + ['option-bricks' => 'on']);
  ```
  then call `(new \Automatic_CSS\Framework\Platforms\Bricks($settings))->update_globals()`.

That `update_globals()` call is also what adds ACSS's utility classes (currently 2,248) and its palettes to Bricks.

### Project custom tokens
Add these under ACSS → Custom CSS. They are the only variables not generated by ACSS:

```css
:root {
  --pc-font-display: var(--heading-font-family), "Libre Caslon Text", Georgia, serif;
  --pc-font-serif: "Libre Caslon Text", Georgia, serif;
  --pc-font-body: var(--text-font-family), Arial, sans-serif;
  --pc-boxed-width: 144rem;
  --pc-page-bg: #dfe4e1;
  --pc-shadow-s: 0 1px 2px rgb(10 15 13 / .06), 0 2px 8px rgb(10 15 13 / .05);
  --pc-shadow-m: 0 2px 4px rgb(10 15 13 / .05), 0 12px 32px rgb(10 15 13 / .08);
  --pc-shadow-l: 0 30px 80px rgb(6 21 18 / .18);
  --pc-ease: cubic-bezier(.2, .7, .2, 1);
}
```
Hairlines use ACSS variables directly: `--base-trans-10` on light backgrounds and `--white-trans-20` on dark ones.

---

## 3. Bricks global settings

1. **Bricks → Settings → General**: enable *Disable default Bricks styles* is optional; ACSS v3 handles base styles.
2. **Theme Styles**: *Site layout* stays at the default (**wide / full-width**). Coloured bands run edge to edge and content is centred at `--content-width` (1240px). The original design was boxed. To bring that back, set Site layout to Boxed (1440px) and add the `body.is-boxed` rules from `style.css`.
3. **Theme Styles → Typography**: point heading font to `var(--pc-font-display)` and body to `var(--pc-font-body)` if ACSS is not already setting them.
4. **Theme Styles → Links**: color `inherit`, no underline in nav. Keep underlines in body copy for accessibility.
5. **Breakpoints:** keep Bricks at its defaults. They match ACSS (992 / 768 / 480). Set the Nav Menu's mobile-menu breakpoint to a custom 1366px one (Bricks → Settings → Breakpoints → add "Laptop" at 1366).

---

## 4. Global classes

Two workable options:

**A. Fastest:** paste the whole of `style.css` (without the "Base" and "Container" blocks, which ACSS covers) into *Bricks → Settings → Custom code → Custom CSS*, then type the class names onto elements in the builder. Every element gets its look from the stylesheet.

**B. Native Bricks:** create each BEM class as a Bricks global class and move its rules into the class's style panel or its *Custom CSS* box (`%root%` = the class). Slower, but editors can then restyle visually.

Most teams use A for the build and move high-traffic components (buttons, cards) to B later.

### ACSS utilities that replace prototype CSS

| Prototype class | Use in Bricks instead |
|---|---|
| `.container` | Bricks **Container** element (ACSS sets width and gutter) |
| `.section` + padding | Bricks **Section** element (ACSS adds section padding) |
| Buttons | Already ACSS classes in the markup: `btn--primary` / `btn--accent` / `btn--white` (+ `btn--outline`), sizes `btn--s` / `btn--m`, `width--full` |
| 3/4-column grids | ACSS `grid--3`, `grid--4` with `grid--l-2`, `grid--s-1` for breakpoints, `gap--l` |
| `.section--tint` | ACSS `bg--primary-ultra-light` |
| `.section--dark` | ACSS `bg--primary` (text turns white automatically with ACSS dark-bg settings) |
| `.eyebrow` | Keep as global class (custom) |
| Visually hidden text | ACSS `hidden-accessible` |

---

## 5. Section-by-section build

Element names are Bricks elements. Classes are in `code`. Build each block once, then save it as a **Bricks Component** (Bricks 1.12+) or a template.

### Header template (Templates → Header)

```
Section  .topbar  (hidden at s / 480)
└ Container .topbar__inner  (flex row, space-between, wrap)
  ├ Icon list / Text: address, hours
  └ Text-link: email, "Se habla español"
Section  .header  (Sticky: Bricks header "Sticky on scroll", add class .is-scrolled via Bricks interaction or main.js)
└ Container .header__inner  (flex row, align center, space-between)
  ├ Logo element (or Div .brand with .brand__mark + .brand__text)
  ├ Nav Menu element  .nav   (Bricks native: mobile menu toggle at 1366px)
  └ Div .header__actions
    ├ Icon + text link .header__phone
    └ Button .btn--primary "Free Case Review"
```

The Bricks Nav Menu (or Nav Nestable) element provides the mobile menu, so `main.js` sections 1–2 are not needed. Style its mobile panel to match `.nav` at the 1366 breakpoint.

### Hero (component: `Hero – Consultation`)

```
Section .hero   (bg: gradient from CSS; ::before ampersand stays in custom CSS)
└ Container .hero__inner   (grid 1.25fr / 1fr; stack at 992)
  ├ Block .hero__content
  │ ├ Text  .eyebrow .eyebrow--light
  │ ├ Heading h1 .hero__title   (wrap "goes to trial" in <em>)
  │ ├ Text  .hero__lede
  │ ├ Block .hero__actions → 2 Buttons (btn--accent btn--m, btn--white btn--outline btn--m)
  │ └ Block .hero__proof → 3 × (Heading-like number + label)
  └ Block .hero__card
    ├ Heading h2 .hero__card-title + Text
    └ Form element   (fields: name, phone, select, textarea; class .form)
```

Component properties to expose: eyebrow, title, lede, button labels/links, three proof figures.

### Recognition strip
Section `.recognition` → Container `.recognition__inner` → Text label + **Icon list** or Div list `.recognition__list`. If the client has real award badges, swap to an Image gallery / logo row.

### About
```
Section .about → Container .about__inner (grid 1fr/1.1fr)
├ Block .about__media
│ ├ Image .about__frame   (founder/office photo, object-fit cover, aspect 4/5)
│ │   + Block .about__figure with quote + cite (absolute, bottom)
│ └ Block .about__seal (32 / Years in Texas courtrooms)
└ Block .about__content
  ├ eyebrow, Heading h2 .section__title, Text .about__lede
  ├ Icon list .checklist  (Bricks Icon List element works well)
  └ Block .about__footer → Button + Div .signature
```
Remove the gradient `background` on `.about__frame` once a real photo is in place.

### Practice areas (query loop)
Create CPT **Practice Area** (ACF or Meta Box / Bricks' native CPT via plugin) with fields `icon`, `excerpt`.

```
Section .practice .bg--primary-ultra-light
└ Container
  ├ Block .section__head .section__head--split
  └ Block .practice__grid   (grid 3 cols, 1px gap on a line color = hairline grid)
    └ Block .practice-card  ← Query loop: post type Practice Area, 6 posts
      ├ Icon .practice-card__icon  (dynamic icon field)
      ├ Heading h3 .practice-card__title {post_title}
      ├ Text .practice-card__text {post_excerpt}
      └ Text-link .practice-card__link → {post_url}
```

### Process (static)
Four `.process-step` blocks in an `ol` list `.process__steps`. The dashed connector is a `::after` in the CSS; keep it in custom CSS.

### Stats band
Section `.stats` → `dl.stats__grid` with 4 `.stat`. Bricks **Counter** element can replace the number if you want a count-up; set it to start from the final value on reduced motion.

### Attorneys (query loop)
CPT **Attorney** with fields `role`, `education`, `admitted_year`, featured image.

```
Block .attorneys__grid (grid--4 grid--l-2 grid--s-1)
└ Block .attorney-card  ← Query loop: Attorney, order by menu_order, 4 posts
  ├ Image .attorney-card__photo  {featured_image}  aspect 4/5, object-fit cover
  └ Block .attorney-card__body → name {post_title}, role {acf_role}, meta {acf_education} · Admitted {acf_admitted_year}
```
The initials placeholder (`data-initials` + `::before`) is only for the prototype; remove it when images exist.

### Case results (query loop)
CPT **Case Result** with fields `amount`, `result_type`, `court`, `year`.

```
Section .results .bg--primary
└ ul .results__list
  └ li .result  ← Query loop
    ├ Text .result__amount {acf_amount}
    ├ Block .result__body → .result__type, .result__text
    └ Text .result__docket {acf_court} · {acf_year}
```
Keep the disclaimer sentence next to the list. Most state bars require it.

### Testimonials
Use Bricks **Slider (Nestable)** with 3 per page / 2 at 992 / 1 at 480, gap `var(--grid-gap)`, custom arrows placed in `.slider-controls`. Each slide = `.testimonial` card. Or keep the CSS scroll-snap track and `main.js` section 4; both work.

### FAQ
Use Bricks **Accordion (Nestable)** with *Independent toggle* off (one open at a time), title class `.faq-item__q`, content `.faq-item__a`. Add the **FAQPage schema** via your SEO plugin.

### Insights
Query loop on Posts, 3 items, `.post-card` with featured image in `.post-card__media` (aspect 16/10). Category and date via dynamic data `{post_terms_category}`, `{post_date}`.

### Our Offices (query loop)
Card layout: a green header band with region label, city name in uppercase and a pin icon, finished with a brass bottom border. Below it is a white, centred body with the address, "Maps and Directions", the phone number, and a "Learn more" link to the office page.

CPT **Office** with fields `region_label` (e.g. "Headquarters"), `street`, `suite`, `city_line`, `phone`, `map_url`, and optionally `email`, `hours`. Reuse the same CPT in the footer so both lists stay in sync. Each Office post can have its own single page (template: Single → Office), which "Learn more" links to.

```
Section .offices
└ Container
  ├ Block .section__head .section__head--split
  └ ul .offices__grid   (grid--4, grid--l-2, grid--s-1)
    └ li .office-card  ← Query loop: Office, order by menu_order
      ├ Block .office-card__head   (bg primary, border-bottom 3px accent, text centred)
      │ ├ Text .office-card__tag {acf_region_label}
      │ ├ Heading h3 .office-card__city {post_title}
      │ └ Icon .office-card__pin (map pin, accent-light)
      └ Block .office-card__body   (flex column, centred)
        ├ Text .office-card__address {acf_street}<br>{acf_suite}<br>{acf_city_line}
        ├ ul .office-card__links
        │ ├ Text-link .office-card__link "Maps and Directions" → {acf_map_url} (new tab)
        │ └ Text-link .office-card__link--phone {acf_phone} → tel:
        └ Text-link .office-card__more "Learn more" → {post_url}
```
Avoid embedding a Google Map iframe on every card. Put one Map element on each Office single page instead.

### Contact / CTA
Section `.contact` → grid with contact details (Icon + Text) and a Bricks **Form** element with class `.contact__form .form`. In the Form element:
- Actions: Email + (optional) webhook to the firm's intake CRM (Clio Grow, Lawmatics …)
- Success message: "Thank you. A member of our intake team will contact you within one business day."
- Enable reCAPTCHA / Turnstile.
Form fields inherit `.form__input` styling if you add this to custom CSS:
```css
.form .form-group input, .form .form-group select, .form .form-group textarea { /* copy .form__input rules */ }
```

### Footer template (Templates → Footer)
Section `.footer .bg--primary-ultra-dark` → Container `.footer__inner` (grid 1.4fr repeat(3,1fr)) → brand, two Nav Menus (vertical), "Talk to Us" column (24/7 phone, intake email, CTA button).

**Footer offices row** (sits above the link columns):
```
Container .footer__offices
├ Heading h2 .footer__title "Our Offices"
└ Accordion (Nestable) .footer__offices-grid   ← items from a Query loop on CPT Office
  └ Item .footer-office
    ├ Title .footer-office__head → {post_title} + .footer-office__tag {acf_region_label} + icon .footer-office__chevron
    └ Content .footer-office__body → address, phone, email, "Get directions"
```
Behaviour: on desktop all four are open boxes in a 4-column grid (2 columns at 992) and can't be collapsed. At 480px and below they become closed accordions with a +/× toggle.
- In the prototype this is native `<details>` and `main.js` part 7 opens or closes them on breakpoint change.
- In Bricks Accordion (Nestable), turn on *Independent toggle*. Add the CSS from the "Footer offices" block in `style.css`, mapping `.footer-office[open]` to Bricks' `.brx-open` class. Add this small snippet so items start open on desktop:
```js
document.querySelectorAll('.footer-office').forEach(function (el) {
  if (!matchMedia('(max-width: 480px)').matches) el.classList.add('brx-open');
});
```

Second Container `.footer__legal` with copyright `{current_date:Y}`, the attorney-advertising disclaimer, and legal links.

---

## 6. JavaScript in WordPress

| `main.js` part | Replace with |
|---|---|
| Sticky header shadow | Bricks header template → *Sticky on scroll* + style the sticky state |
| Mobile nav | Nav Menu / Nav Nestable element |
| Active link on scroll | Bricks Nav Menu "scroll spy" is not built in; keep this snippet if wanted |
| FAQ one-open | Accordion (Nestable) setting |
| Testimonial slider | Slider (Nestable) |
| Form validation | Bricks Form element |
| Footer year | Dynamic tag `{current_date:Y}` |
| Footer offices desktop/mobile switch | Accordion (Nestable) + snippet in section 5 (footer) |

If you keep any of it, load it via Bricks → Settings → Custom code → Body (footer) scripts.

---

## 7. Launch checklist

- [ ] Replace all placeholder names, numbers, results, testimonials and addresses with verified client data
- [ ] Real photos: founder/office (4:5), attorney portraits (4:5, same lighting and crop), blog images (16:10)
- [ ] Attorney-advertising disclaimer and "responsible attorney" line reviewed by the client
- [ ] Schema: `LegalService` / `Attorney` on the homepage, `FAQPage` on the FAQ
- [ ] Contrast check on accent text (use `accent-dark` for small text on white)
- [ ] Keyboard test: skip link, nav, accordion, slider buttons, form errors
- [ ] Forms deliver to the intake inbox; spam protection on

---

## 8. Blog templates

Two Bricks templates: `blog.html` → **Archive** and `blog-single.html` → **Single Post**. Both reuse the header and footer templates.

In the prototype, `tools/build_pages.py` wraps `partials/blog.main.html` and `partials/blog-single.main.html` with the header and footer from `index.html`. **Edit the partials, then run `python3 tools/build_pages.py`.** Don't edit `blog.html` or `blog-single.html` directly; the script overwrites them.

### Shared components
| Component | Class | Bricks |
|---|---|---|
| Post card | `.post-card` (+ `__media--{category}`, `__footer`) | Block in a query loop. Media = Image `{featured_image}`; drop the gradient and icon once real images exist |
| Avatar | `.avatar`, `--s`, `--l`, `--xl` | Image `{author_avatar}`, round. Initials are placeholders |
| Breadcrumb | `.breadcrumb`, `--dark` on light backgrounds | Bricks **Breadcrumbs** element, or Rank Math / Yoast breadcrumbs |
| CTA band | `.cta-band` | Save as a component; used on both blog templates |

### Archive template (Templates → Archive, condition: Blog / post archive, categories, tags, search)
```
Section .page-hero
└ Container .page-hero__inner
  ├ Breadcrumbs .breadcrumb
  └ Block .page-hero__grid
    ├ Block .page-hero__content → eyebrow, h1 {archive_title}, lede {archive_description}
    └ Search element (or Filter – Search) .search-form
Section .blog
└ Container
  ├ Filter – Checkbox/Radio as buttons  .blog-filter / .chip   (Bricks 1.9+ query filters, source: Categories, show counts)
  ├ Block .post-featured  ← Query loop: posts, 1 item, "Sticky posts" or ACF "featured" = true
  ├ ul .blog__grid  ← Query loop: posts, 9 per page, exclude featured (grid--3 grid--l-2 grid--s-1)
  │ └ li .post-card
  ├ Text .blog__empty  (Query loop "No results" text)
  └ Pagination element .pagination   (style links like .pagination__link)
CTA band component
```
In the prototype, the chips and search filter the grid in the browser (`main.js` part 8). In WordPress, Bricks query filters do this with AJAX, so drop that part.

### Single post template (Templates → Single, condition: Post type = Post)
```
article .article
├ Section .article-hero (bg primary-ultra-light)
│ └ Container .article-hero__inner
│   ├ Breadcrumbs .breadcrumb .breadcrumb--dark
│   ├ Text-link .article-hero__cat {post_terms_category}
│   ├ Heading h1 .article-hero__title {post_title}
│   ├ Text .article-hero__dek {post_excerpt}
│   └ Block .article-meta → avatar {author_avatar}, {author_name}, ACF author role, dl: {post_date}, ACF "reviewed_by", reading time
├ Container .article-cover → Image {featured_image} .article-cover__image + caption {featured_image_caption}
└ Container .article-layout  (grid: 1fr / 360px; stacks at 992)
  ├ Block .article-layout__main
  │ ├ Post Content element .prose      ← all article styling lives on .prose
│ │   ("In this article" box: Table of Contents element .toc placed after the first paragraph, or in the template above Post Content)
  │ └ Block .article-footer → tags {post_terms_post_tag}, share links, author box
  └ Block .article-aside   (sidebar; see below)
```

### Single post sidebar
Four cards, each saved as a Bricks component with the class `.widget`. They sit right of the article on desktop (sidebar 360px wide). Between 769 and 992px they form a 2-column grid under the article, with the form spanning both columns. At 768px and below they stack in one column.

```
Block .article-aside  (flex column, gap --space-l, align-self stretch)
├ Section .widget  "Recent posts"
│ ├ Heading h2 .widget__title
│ └ ul .recent-posts ← Query loop: posts, 4, exclude current (post__not_in {post_id})
│   └ li .recent-post → .recent-post__title {post_title} + .recent-post__date {post_date}   (text only, no image)
├ Section .widget  "Categories"
│ └ ul .cat-list ← Query loop: Terms, taxonomy category, hide empty
│   └ li → a .cat-list__link {term_name} + span .cat-list__count {term_count}
├ Section .widget .widget--tint  "Practice areas"
│ └ ul .practice-list ← Query loop: CPT Practice Area
│   └ li → a .practice-list__link → .practice-list__name {post_title} + chevron   (text only; add .is-current on the current practice area)
└ Section .widget .widget--form  "Free case review"
  ├ .widget__eyebrow, h2 .widget__title, .widget__text
  ├ Form element .form .form--dark   (name, phone, practice area, message)
  └ a .widget__phone
```
- **Pinned form:** the form card stays pinned while scrolling only when the screen is at least 993px wide and 900px tall, so the whole card always fits. In Bricks, add the sticky rule as custom CSS inside that media query. Don't use the element's sticky setting, because it can't check screen height.
- **Field styles:** `.form--dark` restyles the fields for the green background. Map `.form__input` to Bricks' `.form-group input, select, textarea`.
- **Reuse:** the same `.widget` cards work on the blog archive too, if you add a sidebar there later.

**Content blocks editors can use inside posts.** Add these as Gutenberg block styles or reusable patterns so they get the class:
- `.prose__lead`: opening paragraph
- `.callout` with `.callout__title`: a "Key point" box
- `.pull-quote`: Quote block with the Pull Quote style
- `.table-wrap`: wrap every table so it scrolls on phones
- `.prose__checklist`: list with checkbox markers
- `.prose__disclaimer`: legal disclaimer at the end of each article. Better: put it in the template under Post Content so editors can't forget it.

**Script replacements** (`main.js` part 9):
| Prototype | Bricks |
|---|---|
| "In this article" box from `h2[id]` | Table of Contents element |
| Reading progress bar | Progress bar via a small script, or keep part 9 |
| Copy link | Keep part 9, or use a share plugin |

**Fields to add:** ACF on Post → `reviewed_by` (relationship to Attorney), `reading_time` (number, or calculate it). ACF on User → `role_title`, `bio`.

**SEO:** `Article` schema with `author` and `reviewedBy`; `BreadcrumbList` from the breadcrumbs.

---

## 9. Practice area single template

File: `practice-area.html`, built from `partials/practice-area.main.html`. Bricks: **Templates → Single**, condition *Post type = Practice Area*. The sample content is Personal Injury.

The sidebar has three cards: **Recent posts, Practice areas and the form**. There is no Categories card on this template. The sidebar cards are shared partials (`partials/widget-*.html`), so blog posts and practice pages always use identical cards. In Bricks, save each one as a component and drop the components you need into each template.

```
Section .page-hero .page-hero--practice
└ Container .page-hero__inner
  ├ Breadcrumbs .breadcrumb   (Home / Practice Areas / {post_title})
  └ Block .page-hero__grid
    ├ Block .page-hero__content → eyebrow "Practice Area", h1 {post_title}, lede {acf_hero_lede}, .page-hero__actions (2 buttons)
    └ dl .hero-stats → 3 × .hero-stats__item  (ACF repeater: label, value)
Container .article-layout
├ Block .article-layout__main
│ ├ Post Content .prose                         (overview)
│ ├ Section .practice-block "Cases we handle"   → ul .case-types > li .case-type (ACF repeater: title, text)
│ ├ Section .practice-block "What you can recover" → .damages (2 × .damages__col) + .callout
│ ├ Section .practice-block "How your case moves"  → ol .timeline > li .timeline__item (ACF repeater: step label, title, text)
│ ├ Section .practice-block "Recent results"    → ul .mini-results ← Query loop: Case Result where practice = current, 4
│ ├ Section .practice-block "Your legal team"   → ul .team-mini ← Query loop: Attorney where practice = current
│ ├ Section .practice-block FAQ                 → Accordion (Nestable) .faq-item, ACF repeater; FAQPage schema
│ └ Text .practice-disclaimer
└ Block .article-aside
  ├ Component: Recent posts   (query: posts in the category linked to this practice area, 4)
  ├ Component: Practice areas (current item gets .is-current)
  └ Component: Form box       (id="case-review" so the hero button scrolls to it)
Section .related → Query loop: posts in the linked category, 3
CTA band component
```

**Fields on the Practice Area CPT (ACF):**

| Field | Type |
|---|---|
| `hero_lede` | Textarea |
| `hero_stats` | Repeater: label, value |
| `case_types` | Repeater: title, text |
| `economic_damages`, `non_economic_damages` | Textarea, one item per line |
| `law_note` | Textarea, for the callout |
| `timeline` | Repeater: step, title, text |
| `faqs` | Repeater: question, answer |
| `blog_category` | Taxonomy, used to link related posts |

Add a relationship field `practice_areas` on both the Attorney and Case Result post types.

**Current item in the sidebar list:** in Bricks, add a condition on the link: *{post_id} equals {query_post_id}* → add class `is-current`. In the prototype, `tools/build_pages.py` sets it with `current_practice`.

**Links:** homepage practice cards and footer practice links now point to the practice template. To add another practice area, add one entry to `PAGES` in `tools/build_pages.py`, or in WordPress, add a Practice Area post.

---

## 10. Build status on whitecrowtemplate.kinsta.cloud

Built natively in Bricks on 2026-11-04 with the HTML/CSS → Bricks converter. The input is `build/bricks/`.

| Item | Where | Notes |
|---|---|---|
| Header | Bricks template **Header** (#346), condition: entire site | Topbar and main bar. Sticky: the topbar scrolls away and the bar stays. The menu collapses at 1366px using the project's own nav (links point to `/#section`). |
| Footer | Bricks template **Footer** (#347), condition: entire site | Offices row (accordions at 480px and below), link columns, legal bar |
| Homepage | Page **Home** (#348), set as the front page | 13 sections, about 450 native elements |
| Classes | 162 Bricks global classes (BEM names, uncategorised) | Alongside the 2,248 ACSS classes |
| Variables | `pc-shadow-s/m/l`, `pc-ease`, `pc-page-bg` | Category "Hartwell & Crane" |
| Global CSS | Theme style **Global → Custom CSS** | Base rules, rules that use an element selector or target classes inside SVG icons, sticky header, Fluent Forms styling |
| JavaScript | Bricks → Settings → Custom code → Body (footer) scripts | Copy of `assets/js/main.js`. **Keep it free of backslashes**: WordPress strips them when the setting is saved. |
| Forms | Fluent Forms **#3** "Free Case Review (short)" (hero), **#4** "Free Case Review (full)" (contact) | Embedded with Shortcode elements. Confirmation: "Thank you. A member of our intake team…" |
| Layout | Full-width (theme style Site layout = default) | Switched from boxed at the client's request |

**Content is still static.** Practice areas, attorneys, case results, testimonials, insights and offices are typed in. Turning them into query loops on the CPTs comes with the content step.

**Known follow-ups:**
- Set the Fluent Forms email notifications to the intake inbox.
- Make the header phone number and email dynamic (ACF Business Details options page).
- Replace the placeholder initials and gradients with real photos (HappyFiles → Images › …).

### Templates added (blog and practice areas)

| Template | Bricks ID | Conditions | Dynamic parts |
|---|---|---|---|
| **Blog Archive** | #461 | Any archive · Posts archive · Insights page (#460, the posts page) · Search | Category chips (term loop), featured article (sticky post), main-query grid of 9 cards, native Search and Pagination elements |
| **Blog Single** | #462 | Post type = Post | Title, excerpt, category, date, reading time, *Written by* / *Legally reviewed by* (loops over the linked Team posts), Post Content (`.prose`), tags, share links, author box, sidebar (recent posts, categories, practice areas, Fluent form #3), 3 related articles |
| **Practice Area Single** | #463 | Post type = Practice Area | Hero intro and figures, overview (Post Content), case types, damages, Texas-law note, timeline, results, legal team, FAQs: all ACF. Sidebar and related articles. |

**Content model:**
- **Practice Areas** post type (`practice-area`, URL `/practice-areas/<slug>/`) with the "Practice Area Details" field group:
  - `hero_lede`, `hero_stats`, `case_types`, `damages_economic`, `damages_non_economic`, `law_note`, `timeline`, `results`, `faqs` (repeaters where they repeat)
  - `legal_team`, a relationship to Team
- **Posts:** the "Article Details" field group with `written_by`, `reviewed_by` (both Team) and `reading_time`.
- **Team:** a new `team_initials` field, used in the round avatars until photos exist.
- **Empty sections hide themselves.** On a practice area with no results, damages, timeline or FAQs, Bricks conditions hide that block (repeater count `!= 0`, law note `!= ""`).

**Featured article:** the sandbox snippet `wp-content/novamira-sandbox/hc-blog-featured-post.php` makes the featured card show the **sticky** post. It also keeps that post out of the grid and sets 9 posts per page. To feature a different article, tick *Stick to the top of the blog* on it. Turn the snippet off under Novamira → Sandbox.

**How they were built:** `build/bricks/tpl-*.html` were converted with marker classes. `loop-*` became a query loop, `dyn-*` a dynamic tag, `cond-*` an element condition, and `slot-*` a native element (Post Content, Search, Pagination, Fluent Forms shortcode). Dummy content seed: `build/content/seed.json`.

### Where the CSS lives now (no global stylesheet)

The theme style's **Custom CSS is empty**. All styling is native to Bricks and ACSS:

| What | Where |
|---|---|
| Body font, size, line-height, colour | Theme style → Typography → Body |
| Container alignment and max-width | Theme style → Container (`align-items: stretch`, max-width 100%) |
| Paragraph, heading and list margins, focus outlines, anchor offset under the sticky header | ACSS resets (ACSS → Typography / Accessibility). Smooth scrolling is **on** in ACSS. |
| Component styles | Each BEM class (`hero`, `post-card`, `office-card`, …): typed controls first, the rest in that class's **Custom CSS** using `%root%`. |
| Gutters on the header, topbar and footer; zero section padding on thin bands; row direction on flex-row containers | Typed class controls (`_padding`, `_direction`, `_alignItems`) |
| List bullets off for `role="list"` | The list's own class (23 classes), or the parent class for `footer__col` and `breadcrumb` |
| SVG icon size | Global class `icon`, attached to every SVG element |
| Sticky header (`#brx-header`) | Custom CSS on the `topbar` class (used by the Header template, so it loads on every page) |
| Fluent Forms styling | Custom CSS on the `form` class (on every form shortcode element). The dark sidebar variant is on `widget--form`. |
| Article body extras (pull quote, table wrapper, checklist, lead) | Custom CSS on the `prose` class (on the Post Content element) |
| Featured card visible only on the blog home | Custom CSS on `post-featured` |

**Font families** in class typography must be **bare names** (`Libre Caslon Display`) with the fallback in *Font fallback*. A quoted stack gets double-quoted by Bricks and falls back to Times.

### Header navigation: Bricks Nav (Nestable) with mega menu

The hand-built menu was replaced with a native **Nav (Nestable)** element (`#brxe-mnav01`, class `main-nav`) in the Header template:

```
Nav (Nestable) .main-nav   mobileMenu: custom, breakpoint 1279px
├ Block ul.brx-nav-nested-items
│ ├ Text-link .nav__link  Home
│ ├ Dropdown "The Firm" (no link)
│ │ └ ul.brx-dropdown-content .nav-dropdown  About Us (/#about) · Attorneys (/#attorneys)
│ ├ Dropdown "Practice Areas" → /#practice   megaMenu ✓ (width = #brx-header .header__inner)
│ │ └ Div ul.brx-dropdown-content .mega-menu
│ │   └ li
│ │     ├ .mega-menu__grid ← query loop: Practice Areas (menu order) → .mega-menu__item (title + excerpt)
│ │     └ .mega-menu__aside  "Free case review" panel: Start my review, phone
│ ├ Dropdown "Areas We Serve" (no link)   megaMenu ✓
│ │ └ ul.brx-dropdown-content .areas-menu
│ │   └ li > .areas-menu__grid
│ │     └ .areas-menu__city ← query loop: City posts (menu order, max 6)
│ │       ├ Text-link .areas-menu__city-name  {post_title} → {post_url}
│ │       └ ul.areas-menu__services > li ← ACF repeater loop city_services → {name} → {link}
│ ├ Dropdown "Resources" (no link)
│ │ └ ul.brx-dropdown-content .nav-dropdown  Insights · Case Results (/#results) · Press & News (/category/press-news/) · Testimonials (/#testimonials)
│ ├ Text-link .nav__link  Contact
│ ├ li .main-nav__cta  "Free Case Review" (mobile overlay only)
│ └ Toggle (close, brx-toggle-div)
└ Toggle (open)
```

**Areas We Serve data:** "Areas We Serve" itself has no page or URL (the toggle is a `<span>`).

- **Cities** post type (`cities`, admin `edit.php?post_type=cities`): one post per city, URL `/<city>/` (e.g. `/dallas/`). The ACF group "City Details" → repeater `city_services` (`name`, `link`) feeds the 10 service links under each city in the mega menu.
- **One ACF post type per city** (`city-dallas`, `city-fort-worth`, `city-houston`, `city-austin`, `city-plano`, `city-arlington`), each with rewrite slug = the city slug, so pages live at `/dallas/truck-accidents/`. Each is set to *Admin Menu Parent* `edit.php?post_type=cities`, so they appear as sub-items under Cities rather than as top-level menus. Each holds 10 blank pages.
- **Short city URLs** come from `wp-content/novamira-sandbox/hc-city-urls.php`: it rewrites the Cities permalink to `/<slug>/`, adds a top rewrite rule from the option `hc_city_slugs`, and refreshes that list (and the rewrite rules) whenever a city is saved or deleted.
- **Adding a city:** add a Cities post, then add an ACF post type `city-<slug>` (rewrite slug `<slug>`, Admin Menu Parent `edit.php?post_type=cities`), create its pages, and fill the city's `city_services` repeater with their URLs. Avoid page slugs that match a city slug.

- **Breakpoint:** the custom breakpoint must stay **at or below the base Bricks breakpoint (1279px)**. A larger value makes Bricks generate the mobile menu as `min-width` (inverted). Between 1280 and 1366px the header "Free Case Review" button hides, so the full menu fits.
- **Mobile overlay:** dropdown toggles without a link render as a `<span>`. The `main-nav` custom CSS gives them the same size and padding as the links. Write selectors as `.main-nav …` in CSS saved outside the builder; `%root%` is only expanded when the class is saved in the Bricks editor.
- **Adding menu items:** add a Text-link (class `nav__link`) or a Dropdown inside the items block. New practice areas appear in the mega menu automatically.
- **Perfmatters:** "Remove Unused CSS" now excludes `themes/bricks/assets/css/`. Without that, Perfmatters strips the dropdown, mega menu and mobile overlay styles, because they only apply after a hover or tap.
- The old menu classes (`nav`, `nav__list`, `nav-toggle`, `nav__mobile-cta`) were deleted.

## 11. Contact Us page (`/contact/`, page ID 610)

Built from `build/bricks/tpl-contact.html` + `build/bricks/templates/contact.css` (generated from `partials/contact.main.html`) with the Bricks HTML→Bricks converter. New global classes have native settings plus small custom CSS: `page-hero--contact`, `contact-promise`, `contact-methods*`, `contact-method*`, `contact-main*`, `contact-card*`, `contact-aside`, `next-step*`, `hours*`.

- **Sections:** hero with promise box → three contact-method cards (pulled up over the hero with `margin-top: -6rem`) → form card + sidebar (What happens next, Office hours, Urgent call box) → Our Offices (copied from the homepage section, same Our Offices query loop) → FAQ.
- **Form:** Fluent Forms **#5 "Contact Page: Free Case Review"** (a copy of #4, so the homepage form is unchanged). Extra fields: `contact_method` radio (styled as pill buttons by the `hc-chips` container class), `nearest_office` select, and a required acknowledgement checkbox (`hc-consent`). The `contact-card` class styles them, plus the gold submit button.
- **Root sections and padding:** Bricks/ACSS adds default section padding, so the hero and the contact-method strip set `_padding` top/bottom 0 on their classes.
- **Links:** the header "Contact" item goes to `/contact/`; the header, mega menu and footer "Free Case Review" buttons go to `/contact/#case-review`.

## 12. About Us page (`/about/`, page ID 616)

Built from `build/bricks/tpl-about.html` + `build/bricks/templates/about.css` (generated from `partials/about.main.html`), the same way as the Contact page. New global classes: `story*`, `values__grid`, `value-card*`, `milestones__list`, `milestone*`, `community*`.

- **Sections:** hero with stats → Recognition strip, copied from the homepage → Our Story (sticky intro and quote, story text, checklist, signature) → What We Stand For (4 value cards) → Milestones timeline (horizontal on desktop, vertical below 992px) → Stats band and Our Attorneys, both copied from the homepage (same Team query loop) → Beyond the Courtroom → CTA band.
- **Links:** The Firm → About Us in the header and footer now goes to `/about/`.
- **Converter notes:** `dt`/`dd` children become divs, so I set them back to custom tags `dt`/`dd` on the hero stats here and on the Contact page's office hours. List classes (`values__grid`, `community__list`, `milestones__list`, `next-steps`) need `padding-left: 0` and `list-style: none`. Hero sections need `_padding` top/bottom 0 to override the default section padding.
- **Mobile grid fix:** below 767px Bricks sets `flex-wrap: wrap` on column containers, and Chrome then sizes the attorneys grid (4:5 photos) too short, so the cards spilled into the next section. The `attorneys__grid` class now includes `.brxe-container:has(> .attorneys__grid) { flex-wrap: nowrap; }`. This also fixes the homepage.

## 13. Team (archive `/team/` and profiles `/team/<name>/`)

**Data**
- **Team post type** (`team`): has an archive at `/team/`, and single profiles at `/team/<slug>/`. Order is set with Page Attributes → Order (menu_order).
- **Team Category** taxonomy (`team-category`): Attorneys (33), Paralegals (34) and Staff (35). There are 4 posts in each.
- **ACF group "Team"** (`group_68b5352c3fd58`):
  - `team_position`: role line
  - `team_job_designation`: card meta line and the attorney badge
  - `team_initials`: placeholder portrait
  - `team_label`: Attorney / Paralegal / Staff, shown above the name
  - `team_email`, `team_phone`, `team_office`, `team_since`, `team_languages`, `team_quote`
  - repeaters `team_education` / `team_admissions` / `team_honors` (`title`, `detail`) and `team_results` (`amount`, `type`)
  - relationship `team_practice_areas` → Practice Areas
  - The biography is the post content; the excerpt is its first paragraph.

**Templates**
- **Team Archive** (ID 654, condition: post type archive → Team):
  - hero
  - three groups, each a query loop on Team with a simple term filter (`tax_query: ["team-category::33"]`, ordered by menu order)
  - careers band
  - CTA band

  The Bricks simple tax query is a flat list of `taxonomy::term_id` strings. A WP-style array is ignored silently.
- **Team Single** (ID 653, condition: post type → Team):
  - profile hero: initials portrait via `data-initials="{acf_team_initials}"`, label, name, role, contact row
  - credential badge: shown only when `team_label` is Attorney
  - Post Content biography and quote
  - practice areas (relationship loop)
  - education / admissions / honors / results (repeater loops)
  - At a glance box and the free case review form (Fluent Forms #3)
  - "Meet more of the team" (4 others)

  Each section has a condition, so paralegal and staff profiles only show what they have.

**Links:** the header (The Firm → Our Team), the footer, and the homepage and About "Meet the whole team" buttons all go to `/team/`. There is no separate Attorneys page.

**Converter notes:**
- `<section>`/`<aside>` blocks become Bricks sections. Zero their padding (including the side gutter) on the class.
- A root-level layout container needs a section wrapper to get the mobile gutter.
- Inline `<a>`/`<span>` markers inside headings or text are not converted. Set the dynamic text or link on the parent element instead.

### Team portraits (Image element + `team-photo` class)

Every team portrait is a native Bricks **Image** element with the global class **`team-photo`**: Display block, Width 100%, Aspect ratio 4 / 5, Object fit cover. These are set as native class settings. The class's custom CSS only adds the hover zoom inside `.attorney-card`.

- **Where:** the Team Archive cards (3 loops), the Team Single hero and "Meet more of the team" cards, and the homepage and About attorney cards.
- **Image source:** everywhere the image is `{featured_image}` (size Large).
- **Placeholders:** each team member's featured image is a generated 800×1000 monogram portrait (`assets/img/team/<slug>.jpg`), in the HappyFiles folder **Team**. Replace it by setting a new featured image on the Team post. Any photo is cropped to 4:5 by `object-fit: cover`.
- **CSS cleanup:** the old CSS initials overlay (`.attorney-card__photo::before` / `.profile-hero__photo::before`) was removed. The frame classes keep the radius, gradient fallback and the gold hover bar.
- **Lazy-loading:** Perfmatters lazy-loads these images (`data-src`).

### Homepage and About "Our Attorneys" (query loop)

The attorney grid on the homepage (`6ouoru`) and About (`8ce895`) is now one query-loop card:
- **Query:** Team, `tax_query: ["team-category::33"]` (Attorneys), 4 per page, ordered by menu order.
- **Card content:**
  - Image `{featured_image}` with `team-photo`
  - name `{post_title}` linked to `{post_url}`
  - role `{acf_team_position}`
  - credential `{acf_team_job_designation}`
  - a "View profile →" link

The photo frame links to the profile too. The static cards were removed. To change who appears, edit the Attorneys category or the Team order.

## 14. Testimonials page (`/testimonials/`, page ID 694)

**Data:** the **Testimonial** post type, with ACF group "Testimonials" (`group_68c12b7182f2d`):
- `testimonials_body_text`: the quote
- `testimonials_rating`, `testimonials_initials`, `testimonials_practice`, `testimonials_location`
- `testimonials_attorney` + `testimonials_attorney_url`
- `testimonials_featured` (true/false)
- for the featured story only: `testimonials_result_amount`, `testimonials_result_type`, `testimonials_court`

The client name is the post title. Order is set with Page Attributes → Order. There are 10 testimonials; the 4 old dummy posts are in the trash.

**Page (built from `build/bricks/tpl-testimonials.html`):**
- **Hero** with a static rating card (4.9, Google / Avvo / Martindale). Edit these numbers on the page.
- **Featured story:** query loop, 1 post, `meta_query testimonials_featured = 1`. It shows the quote, client, the result card, and a link to the lead attorney's profile. To change it, switch "Featured story" on another testimonial and off the current one.
- **Wall:** query loop, all posts with `testimonials_featured != 1`, as masonry cards (`reviews__wall`: CSS columns 3 → 2 → 1). Card content:
  - practice tag
  - quote: the `testimonial__quote` class adds the curly quotes
  - initials avatar, name
  - "{city} · Represented by {attorney}"

  The stars are static (5).
- **"Share your experience"** band: the Google and Avvo buttons link to `#` until the review URLs are known.
- **CTA band.**

**Menu:** Resources → Testimonials now goes to `/testimonials/`. The homepage testimonial slider is still static markup (not connected to the post type).

## 15. Pagination (Blog archive + Testimonials)

Both use the native Bricks **Pagination** element with the global class **`pagination`**:
- **Blog Archive** (template 461): element `dnt2ei`, `queryId` = the main posts loop `ozzbps`.
- **Testimonials** (page 694): element `tmpag1`, placed after the wall, `queryId` = the wall loop.

**Styling (native class settings in the Pagination style panel):**
- justify center, gap 0.8rem
- item height and width 4.6rem
- white background, 1px `--base-trans-20` border, `--radius-s` corners
- text `--text-s` / 600 / `--base`
- active item: `--primary` background and border, white text
- margin-top `--space-xl`

The class's custom CSS holds only what the panel lacks: the hover state (primary border and text), a colour transition, and the icon size.

The prev/next icons (Ionicons `ion-ios-arrow-back` / `-forward`), end size and mid size are content settings. They are set on each element, because Bricks ignores content settings on a class.

**Posts per page:**
- **Blog:** 6, set on the loop `ozzbps`. With "is archive main query", Bricks applies the loop's posts_per_page to the main query, so set it there and not in a `pre_get_posts` filter. The sandbox filter in `hc-blog-featured-post.php` was changed to 6 to match.
- **Testimonials wall:** 6.

Bricks hides the pagination automatically when there is only one page (e.g. small categories).

**Featured testimonial:** Bricks applies the page number to every post loop on the page, so `hc-testimonials-featured.php` (Novamira sandbox) pins the featured loop to page 1. That way it also shows on `/testimonials/page/2/`.

## 16. Paper texture (site-wide default)

**File:** `paper-texture.webp`.
- **Format:** a 320×320 seamless tile, 37 KB. It is a single warm-brown colour with ~3% average transparency, so it never changes the colour underneath.
- **Media library:** attachment 700, in the HappyFiles folder "Site".
- **Source:** `assets/img/paper-texture.svg` (an feTurbulence recipe). Re-export a tile from it to adjust the texture.
- **v2 (2026-11-05):** the low-frequency mottling layer was removed because it made dark patches. The texture is now an even fine grain plus faint fibres: peak opacity 5% (was 11%) and local density uniform across the tile. It is a 256px tile, lossless WebP with alpha quantised to 5 levels, **12KB** (was 37KB). The URL in `--pc-paper` carries `?v=2` to bust browser caches. Bump the number whenever you replace the file.
- **Why WebP, not SVG:** the browser has to generate the SVG's noise on every page load, which measured ~9 ms on a normal screen and ~31 ms on retina, several times more on phones. Browsers also render it slightly differently. The WebP decodes in ~2 ms, looks identical everywhere, and is cached by the CDN.

**One switch, one rule.** Everything lives in **Bricks > Theme Styles > Global > CSS**:
1. **Site variables block:** `:root { --pc-paper: url(".../paper-texture.webp"); … }`.
   - The Bricks **Variables Manager is disabled** on this site, because ACSS manages its own variables.
   - So variables saved in Bricks > Variables are *not* output. All project `--pc-*` variables are defined here instead: `--pc-shadow-s/m/l`, `--pc-ease`, `--pc-page-bg`, `--pc-paper`.
   - The `--pc-shadow-*` and `--pc-ease` variables had been missing on the live site until this block was added, which restored the card shadows and the transition easing.
2. **Paper texture rule:** applies `background-image: var(--pc-paper, none)` with repeat, top left and size auto. It targets `html, .header, .section--tint, .stats, .cta-band, .article-hero, .has-paper` and the open mobile menu (`#brxe-mnav01.brx-open .brx-nav-nested-items`).

**Colours stay native.** Theme Style > General > Site background, and the Background setting on `header`, `section--tint`, `stats`, `cta-band` and `article-hero`, hold only the colour. There is no image in those settings.

**How to…**
- **Change the texture:** edit `--pc-paper` in the variables block, or replace the media file paper-texture.webp (keep the same file name).
- **Turn it off everywhere:** set `--pc-paper: none;`.
- **Add it to another light surface:** add the global class **`has-paper`** to the element. The element keeps its own background colour.
- **Remove it from one surface type:** delete that selector from the rule.

**Not textured on purpose:** cards, sidebar boxes and quote boxes stay plain white or tinted, so they stand out on the paper. Dark sections (hero, results, page heroes, footer) keep their solid colour or gradient.

## 17. Press & News (`/news/`)

**Data**
- **Post type `news`** ("Press & News", ACF, archive at `/news/`, singles at `/news/<slug>/`). The old empty blog category "Press & News" was deleted. Resources → Press & News now links to `/news/`.
- **ACF group "News Details"** (`group_hcnews01`):
  - `news_type`: select. Press Release / In the Media / Award / Firm News / Community.
  - `news_featured`: true/false.
  - `news_publication` + `news_url`: for In the Media items, the card button becomes "Read on {publication}" and opens the outside article.
  - `news_location`, `news_release`.
  - `news_figure` + `news_figure_caption`: the big number on the featured card.
  - `news_people`: relationship → Team.
- **Content:** the summary is the post excerpt; the body is the post content. There are 9 items, and the $14.2M verdict release is featured.

**Templates**
- **News Archive** (721, condition: post type archive → news):
  - hero with a media contact card
  - "As seen in" strip
  - featured loop (`news_featured = 1`, 1 post)
  - grid: the main archive query, 6 per page
  - Bricks Pagination (class `pagination`)
  - media CTA band
- **News Single** (722, condition: post type → news):
  - light article hero with type tag, title, excerpt and a Published / Location / Release / Publication row (each hidden when empty)
  - Post Content
  - "Read the full story on {publication}" button (only when `news_url` is set)
  - "About Hartwell & Crane" boilerplate
  - share buttons
  - sidebar: media contact, Attorneys in this story (relationship loop with `team-photo` images), Latest news
  - More from the firm (3 cards)
- **Tag colours:** come from `data-type="{acf_news_type}"` on the `.news-tag` element (custom CSS on the `news-tag` class).
- **Sandbox `hc-news-archive.php`:** removes the featured item from the main archive query, and pins the featured loop to page 1, so it stays on `/news/page/2/`.
- **`article-hero` class:** now has left/right padding `var(--gutter)`. It is used as a root section on news singles, and it fixes the mobile gutter there.
- **Press-release formatting in the editor:** add the class `news-dateline` to a `<strong>` at the start of the release, and `news-end` to a final `###` paragraph. Styled via the `news-boilerplate` class CSS.

### Mobile menu: only the close button while open (fix)

On phones, after scrolling, the browser's collapsing address bar could offset the full-screen menu. The header's logo, phone button and hamburger then showed above the overlay, next to the close X. The `main-nav` class custom CSS now has a "Mobile menu open" block (≤1279px):
- hides the open toggle (`.main-nav.brx-open > .brxe-toggle`)
- hides the rest of the header row (`.header:has(.main-nav.brx-open) .header__inner > :not(.main-nav)`)
- pins the overlay to `top: 0; height: 100dvh`

Everything returns when the menu closes.

## 18. Case Results (`/case-results/`)

**Data**
- **Post type `case-result`** ("Case Results", archive `/case-results/`, singles `/case-results/<slug>/`, ordered by menu_order).
- **Taxonomy `result-area`** ("Practice Areas"): Personal Injury, Employment, Family Law, Criminal Defense, Business Litigation, Estate & Probate. Filter pages live at `/case-results/area/<slug>/`.
- **ACF group "Case Result Details"** (`group_hcresult1`):
  - `result_amount`: the amount or outcome text, e.g. "Not guilty".
  - `result_type`: select. Jury Verdict / Settlement / Acquittal / Dismissal / Arbitration Award / Court Order.
  - `result_featured`.
  - `result_case_type`, `result_court`, `result_year`.
  - `result_offer`, `result_trial_length`, `result_office`.
  - `result_team`: relationship → Team.
  - `result_practice_url`: page link → Practice Area.
- **Content:** the summary is the excerpt. The story is the post content (The challenge / Our approach / The outcome / quote). There are 10 results; the $18.4M verdict is featured.

**Templates**
- **Case Results Archive** (753):
  - **Conditions:** post type archive → case-result, and archive → terms `result-area::all`. The term condition must be `archiveType: term` + `archiveTerms`, not `main: terms` (that one is for single posts). Otherwise the Blog Archive's "any archive" condition wins.
  - **Sections:**
    - hero with stats
    - featured loop (`result_featured = 1`)
    - practice-area chips (term loop + "All results")
    - grid (main archive query, 9 per page)
    - Bricks Pagination
    - disclaimer
    - CTA band
- **Case Result Single** (754):
  - dark hero with the big amount and a facts strip (each fact hidden when empty)
  - Post Content
  - disclaimer, and links back to all results and to the practice-area page
  - sidebar: Case at a glance, Trial team (relationship loop, `team-photo` images), form #3
  - More results (3)
- **Sandbox `hc-case-results.php`:** the main archive query excludes the featured result. The featured loop is pinned to page 1 and is empty on practice-area filter pages, where the featured result appears in the grid instead.
- **Menus:** Case Results in the header and footer now link to `/case-results/`.

### Areas We Serve: city accordions on mobile

Each city in the Areas We Serve mega menu is now a native `<details>` element:
- **Elements:** the loop element `marcty` uses a custom tag `details`. The new `marsum` has a custom tag `summary` and the class `areas-menu__summary`; it contains the city link and a Bricks **Icon** element `marchv` (Ionicons `ion-ios-arrow-down`, class `areas-menu__chevron`).
- **Desktop (>1279px):** the site script (§12 in `main.js` / Bricks body-footer script) keeps every city `open`, and blocks toggling on the summary. The chevron is hidden, so the mega menu is unchanged.
- **Mobile (≤1279px):**
  - every city starts closed
  - tapping the chevron or the empty part of the row opens that city's 10 service links (indented, with a gold guide line)
  - opening one city closes the others
  - tapping the city name still opens the city page
- **CSS** lives in the classes `areas-menu__grid`, `areas-menu__city`, `areas-menu__city-name`, `areas-menu__services`, `areas-menu__summary` and `areas-menu__chevron`. The mobile services indent uses `.main-nav .areas-menu__services`, because `.main-nav ul { padding: 0 }` otherwise wins.
- **Why not an SVG element for the chevron:** a Bricks SVG element with inline code does not output on the frontend, so the native Icon element is used instead.

### Practice Area Single: alignment fixes (template 463)

- **Layout:** the root `article-layout` container is now wrapped in a section (`pawrp1`, padding top/bottom 0), so tablet and phone get the side gutter.
- **`practice-block`:** row gap `var(--space-m)`. **`practice-block__title`:** margin-bottom 0. These remove the large gap under section headings.
- **`practice-block__head`:** direction row, so "All results" sits on the right of "Recent results".
- **`timeline`:** an old custom-CSS `padding: 0` was overriding the native padding-left, so it was removed. The dots and line now sit beside the text.
- **`callout`:** align stretch and text-align left (the "Texas law" label was centred).
- **`faq__list`:** align stretch. **`faq-item`:** width 100%. FAQ rows now span the column.
- **`damages__title`:** Public Sans (it had fallen back to the serif heading font).

### Blog Single: fixes (template 462)

- **Hero meta facts:** the labels and values of Published / Legally reviewed by / Reading time were plain divs, so the `.article-meta__facts dt/dd` styles did not apply. They now use custom tags `dt`/`dd`.
- **Key point box:** written in the post content as `<aside class="callout">`, but the `callout` class CSS only reaches Bricks elements. The `prose` class now styles `.prose .callout` and `.prose .callout__title`.
- **Tags row:** `{post_terms_post_tag}` outputs ", " between links. The `tags` class sets `font-size: 0` on the wrapper (the links keep their own size), and the element tag changed from `p` to `div`.
- **Author box:** the `author-box` class now uses direction row (photo left, text right), stacking at ≤480px.
- **Mobile cover:** Bricks' `flex-wrap: wrap` on containers below 767px squeezed `.article-cover` to 120px, so the image overlapped the first paragraph. The `article-cover` class sets flex-wrap nowrap, natively plus a `.article-cover.article-cover` rule to beat Bricks' default.

## 19. Areas We Serve single template (one template for every city page)

**Template "Areas We Serve Single"** (ID 761, stored in option `hc_city_tpl_id`). It is assigned to post types `cities` and every `city-<slug>` post type. The sandbox file `hc-city-template.php` re-syncs these conditions on `admin_init`, so a new city post type is picked up automatically.

**Same template, two kinds of page:**
- **City page** (`/dallas/`): "Dallas Trial Lawyers". The practice-area list shows the city's 10 service pages.
- **City service page** (`/dallas/truck-accidents/`): "Truck Accidents Lawyer in Dallas". The list shows the city's other 9 services, and the breadcrumb includes the city.

**Custom dynamic tags** (from `hc-city-template.php`, group "Hartwell & Crane" in the Bricks dynamic data picker):
- `{hc_city_name}`, `{hc_city_url}`
- `{hc_heading}`, `{hc_lede}`, `{hc_breadcrumb}`
- `{hc_services_heading}`, `{hc_why_heading}`
- `{hc_intro}`: the page's own post content when it has any, otherwise a generated intro for that city/service. Writing content in the editor replaces the generated text.

**Sections:**
- hero with breadcrumb, eyebrow, heading and buttons (the lede and stats box were removed on request; `{hc_lede}` is still available)
- intro
- practice areas in the city (`city-services`: a 2-column practice-list grid)
- why clients choose us (checklist)
- recent results (4 case results)
- sidebar: free case review form (#3) and "Other areas we serve" (other cities)
- CTA band

**Query loops:** the services and other-cities loops are set to `cities` in the builder. The sandbox filter re-points them at runtime: services → `city-<slug>` for the current city, excluding the current page; cities → all cities except the current one. Their element IDs are stored in the option `hc_city_tpl_loops`.

**`breadcrumb` class:** now includes `.breadcrumb ol { margin: 0; padding: 0; }`.

### Practice Area Single hero (update)
The hero lede (`{acf_hero_lede}`) and the hero stats box (`acf_hero_stats` loop) were removed from template 463 on request. The hero now shows the breadcrumb, eyebrow, title and buttons. The ACF fields still hold their data, so they can be re-added later.

### The Firm mega menu (header template 346)

`mdfirm` is now a mega menu (`megaMenu`, selector `#brx-header .header__inner`; its toggle links to `/about/`). The content `mdficn` uses the class `firm-menu`:
- **Left (`firm-menu__intro`):** eyebrow, heading, and 4 links (`firm-menu__link` with title and description): About Us, Our Team, Case Results, Testimonials.
- **Right (`firm-menu__team`):**
  - header row: "Meet our attorneys" and "View the whole team →"
  - **query loop `fmcard`:** Team, `tax_query: ["team-category::33"]`, 4 posts by menu order. Each card is an Image `{featured_image}` with the `team-photo` class (4:5 cover), plus `{post_title}` and `{acf_team_position}`, linking to the profile.
  - **term loop `fmchip`:** team-category, linking to `/team/#{term_slug}` with "{term_name} ({term_count})".
- **Desktop:** 30rem links column plus a 4-column team grid. The panel padding uses `.main-nav ul.firm-menu`, because `.main-nav ul { padding: 0 }` otherwise wins.
- **≤1279px (mobile overlay):**
  - single column; eyebrow, heading and link descriptions hidden
  - team cards become compact rows (56px portrait + name/role), 2 columns on tablets and 1 column under 600px
  - chips wrap

### Mobile menu: dropdown panel padding
`main-nav` class custom CSS (≤1279px): `.main-nav .brx-dropdown-content { padding: var(--space-xs) var(--space-m) var(--space-s); margin-bottom: var(--space-s); background: var(--white); border: 1px solid var(--base-trans-10); border-radius: var(--radius); }`. The selector is generic, so it covers The Firm, Practice Areas, Areas We Serve, Resources and any future dropdown. Desktop is unaffected.

### Footer: Areas We Serve column (footer template 347)
- **Placement:** a new `footer__col` nav (`ftarea`), after Practice Areas, with the heading "Areas We Serve".
- **Links:** an `li` query loop over the **Cities** post type (menu order, all) with a Text Link `{post_title}` → `{post_url}`. City pages only, no service pages; new cities appear automatically.
- **`footer__inner` grid:**
  - desktop: `minmax(0, 1.3fr) repeat(4, minmax(0, 1fr))`, gap `--space-l`
  - ≤1100px: 3 columns, with the brand block spanning the full row
  - ≤767px: 2 columns
  - ≤480px: 1 column

### Social icons (footer and Contact page)

These use the native Bricks **Social Icons** element with Font Awesome 6 Brands icons: `fab fa-facebook-f`, `fab fa-x-twitter`, `fab fa-linkedin-in`, `fab fa-youtube`. Each link opens in a new tab, with `aria-label` "Hartwell & Crane on {network}".

- **Footer** (template 347): element `ftsoc1`, under the firm description in the first column. Classes `social-links social-links--light` (white icons, gold on hover).
- **Contact page** (610): a "Follow us" widget `ctfol1` after Office hours in the sidebar, with element `ctfols`. Classes `social-links social-links--dark` (green icons).
- **Class `social-links`:**
  - native settings: row, left-aligned, icon size 2rem, margin-top `--space-s`
  - custom CSS: gap `--space-l`, no item stretching, a 4.4rem (48px) tap target per icon, and a small lift on hover
- **Links are `#` placeholders.** Set the real profile URLs in each Social Icons element (Content → Icons → Link) in both places.

### Homepage contact details: label and text gap
The text blocks in the homepage "Talk to a Partner" list (`u05e34`, `1x6ay4`, `6plpy5`: label + phone, email or address) now use the class **`contact__text`**, with native flex column and row gap **0.3rem**. Before, they had no class and took the default flex gap of about 24px.

## 20. Team templates: gutter fix and BEM class audit

### Gutter
- **Team Archive (654):** the card section `naezv4` (class `team-groups-section`) had `padding: 0` in custom CSS. That removed the ACSS section side gutter, so the cards ran edge to edge on tablet and phone.
  - The class now sets only native padding top/bottom `0`. The vertical rhythm still comes from `team-groups` (`padding-block`).
  - Measured content edges: 100 / 36 / 17 px at 1440 / 900 / 390 widths, the same as every other section.
- **Team Single (653):** every root is a section with the gutter. The body section `tmswrp` had inline padding and no class. It now uses **`profile-body`** (native padding top/bottom 0).

### BEM global classes
Loose `_cssClasses` were converted to global classes, and every unclassed element in both templates got a block__element class. Existing descendant CSS (`.breadcrumb li`, `.profile-list strong`, `.hours dt`, ...) still applies; the new classes are hooks for future styling.

| Block | Elements / modifiers added |
|---|---|
| `page-hero` | `page-hero--team`, `page-hero--profile` (were loose) |
| `breadcrumb` | `__list`, `__item`, `__link`, `__current` |
| `hero-stats` | `__label`, `__value` |
| `team-group` (was loose) | `team-group__heading` |
| `attorney-card` | `attorney-card__body` (was loose; also on the Home and About cards) |
| `team-card` | `__more-text`, `__more-icon` |
| `team-careers` | `__content` |
| `cta-band` | `__phone-icon`, `__phone-text` |
| `profile-hero` | `__name` (was loose), `__contact-item`, `__contact-icon`, `__contact-link`, `__contact-text` |
| `profile-body` | new section block (Team Single body) |
| `profile-quote` | `__text` |
| `profile-tags` | `__item`, `__link` |
| `profile-list` | `__item`, `__title`, `__detail` |
| `profile-honors` (was loose) | `__title`, `__detail` (detail: `--text-s`, `--base-semi-dark`); `profile-honors__text` is now a flex column, so the title and detail stack on every width |
| `checklist` | `__item`, `__icon` |
| `hours` | `__label`, `__value` |
| `widget` | `__phone-icon`, `__phone-text` |
| `team-more` | `team-more` (section), `team-more__inner` (container) for "Meet more of the team" |
| `section__head` | `section__heading-group` (eyebrow + title wrapper) |

Elements inside ACSS buttons (`btn--*` text + icon) were left without classes. They are styled by the ACSS button.

**Site-wide:** any loose class that already existed as a global class was moved to the global class. That includes `btn--*` on the header, homepage and practice templates, and `form__note`. Loose classes that are left on other pages are section-level names (`about`, `faq`, `page-hero--city`, ...) and `js-*` hooks. The `js-*` hooks stay loose on purpose.

## 21. Site-wide BEM + ACSS refactor (all pages, templates, header, footer)

Scope: Home, About, Contact, Testimonials, Header, Footer and every template (Team, Practice Area, Blog, News, Case Results, Areas We Serve: archives and singles). That is 16 Bricks documents and 2,164 elements.

### Result
| Check | Before | After |
|---|---|---|
| Elements with no class | 553 | **0** |
| Element-level (inline) style settings | 16 | **0** |
| Loose (non-global) classes | 60+ | only JS/state hooks: `js-slider`, `js-slide-prev/next`, `js-copy-link`, `js-toc`, `js-prose`, `is-active` |
| Custom classes carrying custom CSS | 355 | 198 (contextual/pseudo/plugin rules only, see below) |
| Root CSS declarations moved into the native style panel | n/a | ~1,070 |
| Descendant rules moved onto the element's own class | n/a | 57 declarations (e.g. `.hero-stats dt` -> `hero-stats__label`) |

Verification: computed styles of every element on 14 page types at 1440 / 900 / 390 were captured before and after each phase and diffed. The only visual changes are listed under "Intentional changes".

### Shared classes (one class = one component everywhere)
- `section__inner`: the content container inside every `.section` (was unclassed in 15 sections).
- `section__heading-group`: the eyebrow + title wrapper inside every `section__head`.
- `article-section` (+ `article-section--cover` on Blog Single): the body section that wraps `article-layout` on all single templates (Team, Practice, Blog, News, Case Result, City). It replaces 6 inline paddings and the old `city-body` / `profile-body`.
- `page-hero`: now carries the section padding (top/bottom 0) for every page hero. **Intentional change:** the Blog archive and Practice Area heroes had an extra 108px of section padding. They now match the other 10 heroes.
- Buttons: see §22. All buttons are native Bricks Button elements; `btn__text` / `btn__icon` were removed.
- Repeated parts share one class: `breadcrumb__list/__item/__link/__current`, `checklist__item/__icon/__text`, `hours__label/__value`, `hero-stats__label/__value`, `cta-band__phone-icon/-text`, `widget__phone-icon/-text`, `faq-item__question/__answer/__icon`, `footer__list/__item/__link`, `office-card__address-line`, `news-card__link-text/-icon`, `result-card__link-text/-icon`, and so on.
- Section blocks that were loose are now global classes: `about`, `practice`, `process`, `results`, `testimonials`, `insights`, `offices`, `faq`, `story`, `values`, `milestones`, `community`, `reviews`, `review-feature`, `related`, `attorneys`, `stats__inner`, `toc`, `article`, `page-hero--{about,city,news,practice,result,results,reviews}`.
- New modifiers for the old inline styles: `section--tight-top` (Contact offices), `form__note--compact`, `widget__intro`.

### ACSS variables
- Spacing in padding / margin / gap uses `--space-*` (and `calc(var(--space-xs) * 0.5 | 0.75)` for small gaps) when the token stays within ~2.5px of the original at 390, 900 and 1440. That gives 1–2px drift on some small gaps.
- Font sizes use `--text-*` / `--h*` when within 1px. Sizes below `--text-s` are exact ratios of the fixed ACSS tokens, e.g. `calc(var(--text-xs) * 0.885)`, so they follow ACSS if you change the text scale. Sizes with no matching token keep their rem value (e.g. the brand name 2.3rem).
- Radius uses `--radius-*` (pill = `--radius-circle`). Border widths use `var(--border-size)` (accent bars = `calc(var(--border-size) * 3)`). Colours are ACSS tokens. Transparent colours are `color-mix(in srgb, var(--token) N%, transparent)`.
- Fonts in remaining CSS use `var(--heading-font-family)` / `var(--text-font-family)`.
- Theme Style: `--pc-shadow-*` now mix ACSS `--base-ultra-dark` / `--primary-ultra-dark`. `--pc-page-bg` = `color-mix(in srgb, var(--base-light) 75%, var(--base-ultra-light))`.

### What stays as custom CSS (and why)
- Contextual rules for third-party or generated markup: Fluent Forms internals, post-content (`.prose …`), Bricks nav internals (`.brx-submenu-toggle`, `.brx-nav-nested-items`), WordPress pagination.
- Pseudo-elements and states (`::before`, `::after`, `:hover` on children, `[open]`, `:has()`), gradients, `box-shadow` vars, `list-style`, `font-variant-numeric`, `backdrop-filter`, scroll-snap.
- Media queries at non-Bricks widths (1366 / 1280 / 1100 / 1520). The rule for the same property at a Bricks breakpoint is kept next to them in CSS so the cascade stays correct.
- Classes on special Bricks elements (Social Icons, Pagination, Nav Nested, Dropdown, Toggle, Icon, Search, Image). On these elements native `padding` / `margin` target inner parts (e.g. `li a`), so their root styles stay in CSS.
- Geometry with no ACSS token: icon width/height, decorative "&" sizes, focus `outline-offset`, small position offsets.

### Reference copy
- `build/bricks/migrations/global-classes-after-bem-refactor.json` is the custom class set right after the refactor. The temporary database backup was deleted in the §25 cleanup at the owner's request.

## 22. Native Bricks Button elements (all buttons)

Every button on the site is now the Bricks **Button** element styled only with ACSS classes (`btn--primary | btn--accent | btn--white`, `btn--outline`, `btn--s | btn--m`, `width--full`), plus a component class where one existed (`post-card__cta`, `post-featured__cta`, `header__cta`, `footer__cta`).
- **Before:** 19 were a Div (tag `a`) holding a Basic Text and an SVG element. 29 were Text Link elements with `btn--*` classes. The 34 child text/SVG elements were removed.
- **Icons:** set natively in the Button element (Content > Icon > SVG) from three Media Library files: `icon-arrow-right.svg` (ID 765), `icon-phone.svg` (766) and `icon-document.svg` (767), all in `uploads/2026/11/`. They draw with `currentColor`, so they take the button's text colour. Icon position: right for arrows, left for phone numbers.
- **Theme Style CSS ("Native Bricks buttons" block):**
  - `.bricks-button:where([class*="btn--"]) { gap: var(--space-m) }` replaces the Bricks default `gap: 10px` (component classes such as `post-card__cta` can still override it).
  - `[class*="btn--"] svg { width/height: 1.2em }` with a 3px nudge on hover. The old `[class*="btn--"] .icon` rule was removed from the `icon` class.
- **Verified:** 138 button instances on 8 page types at 1440 / 390 have the same box, colours, padding, font, icon size and icon position as before.
- **To add a button:** insert a Button element, add the ACSS classes, set the link, and (optional) pick an icon from the Media Library and set its position. No custom CSS is needed.

## 23. Recognition strip ("Recognized by peers and the bench")

- **Post type:** **Recognitions** (`recognition`, ACF post type ID 769, admin menu icon: awards). It is not public: no single pages or archive. It supports Title, **Featured image (labelled "Logo")** and **Order**.
  - Six placeholder entries (IDs 771–781), with fictional logos, WebP 2.6–5.8KB each, 480×160 transparent, primary green: Bench & Bar, Peer Merit, Lone Star Legal Review, Verdict Circle, Client Choice, Gulf Coast Litigators Society. Logo sources: `assets/img/recognition/`.
  - **To use real logos:** edit each Recognition, set its Logo (featured image) and title (used as the alt text), and use Order to sort. Best results come from a transparent PNG/WebP/SVG about 3:1, single colour.
- **One shared section:** Bricks template **Recognition Strip** (ID 782, type Section). Home and About insert it with a Template element, so edit it once.
- **Continuous carousel (native Bricks Slider (Nested), Splide):**
  - Structure: `section.recognition` > `container.recognition__inner` > `h2.recognition__label` (Heading element; keeps the small uppercase body-font eyebrow look; centred at every width, with no breakpoint overrides) + `slider-nested.recognition__carousel` > `div.recognition__item` (query loop: `recognition`, all, Order ascending, so each logo is a slide) > `img.recognition__logo` (`{featured_image}`, alt `{post_title}`).
  - Options type **Custom**: `type: loop, autoWidth, gap 4.8rem, autoplay, interval: 1, speed: 4000, easing: linear, waitForTransition: true, perMove 1, pauseOnHover/Focus, no arrows/pagination/drag`. At ≤767px: gap 3.2rem, speed 3200. That gives a steady ~48px/s glide with no pauses. **Speed:** raise `speed` to slow it down, lower it to speed up. Splide stops autoplay for visitors who set "reduce motion".
  - `recognition__inner`: flex column, centred, gap `--space-m` (the same layout at every width).
  - `recognition__carousel`: width 100%, transparent background, edge fade via `mask-image` (custom CSS).
  - `recognition__logo`: height 4.8rem (4rem mobile), width auto, contain, opacity 0.75 → 1 on hover.
- **Perfmatters:**
  - `recognition__logo` was added to the Lazy Load exclusions, so cloned slides always have their image.
  - `splide.min.js` was removed from the Delay JavaScript list (it was listed from before any slider existed). Otherwise Splide waited for the first user interaction and the strip stayed hidden.

## 24. Stats band dividers (Home + About)

- Before, each `.stat` drew `border-left` via `+ .stat`, plus `nth-child` border fixes at ≤768px. The grid had a 24px gap, so lines broke at the gaps on mobile and sat off-centre on desktop.
- Now, with one rule set for every width:
  - `stats__grid` has gap `0` and overflow `hidden`.
  - `stat` has a native Box Shadow `calc(var(--border-size) * -1) calc(var(--border-size) * -1) 0 0 var(--accent-light)`. That draws a hairline on each card's top and left edge. The grid clips the ones on its outer edge, so only the inner dividers show, at any column count (4 on desktop, 2 at ≤767px).
- The old `+ .stat` selector and the nth-child media rules were removed.

## 25. Database cleanup (2026-11-05)

**Removed**
- **Backups and temporary options:** `hc_backup_pre_bem_20261105_095849` (1.3MB pre-refactor backup), plus helper options that nothing reads any more (`hc_btn_icons`, `hc_paper_texture_id`, `hc_featured_loop_ids`, `hc_tmp_*`). The temporary snapshot helper file in `novamira-sandbox/` was already removed.
- **Revisions:** all 134 post revisions. 114 of them held old Bricks layouts, about 4.5MB of postmeta. Postmeta is now about 0.7MB in total.
- **Trash and auto-drafts:** 5 trashed posts (4 testimonials: Bastin, Joy, Antho, Ronald; 1 team member: Lorem Ipsum) and 3 empty auto-drafts.
- **Transients:** expired transients. Orphaned postmeta: none found.
- **Unused global classes (5):** `post-card__byline`, `post-card__author`, `post-card__read`, `avatar--s`, `pagination__dots`.
  - How "unused" was decided: not rendered on any of the 172 public URLs (every post, page, CPT single, archive + page 2, term archive, search and 404), not assigned to any element in any Bricks layout, and not referenced in JS, PHP, Fluent Forms or post content.
  - All other 685 custom classes are in use.
- **Dead CSS rules (2):** `.post-content.prose > * + *` (the Post Content element never outputs `post-content`) and `.nav-dropdown .nav-dropdown__all` (no such element).

**Kept on purpose**
- **`has-paper`:** documented opt-in hook for the paper texture.
- **CSS for runtime states:** `.is-scrolled` and `.is-current` (inline site JS), `.brx-open` (Bricks nav), `.dots` (pagination with many pages), Fluent Forms error/success messages.
- **Plugin and framework data:** ACSS imported classes; `hc_city_*` options (used by `hc-city-*.php`); Bricks internals (`bricks_global_classes_locked/_changes`, colour palette); WPvivid settings; Novamira data.
- **Media:** not deleted. A quick reference scan isn't reliable enough for media (featured images and ACF fields).

## 26. Testimonial author block (Home slider)

- `testimonial__author` now has a native row gap of `0.2rem`. The name and case type were 18–24px apart from an inherited default.
  - On the Testimonials page the same class is a row (avatar + text), so that layout is unchanged.
- `testimonial__name` now carries its colour natively (`var(--primary-dark)`). On Home it rendered light grey because the colour only lived in a `.testimonial__who .testimonial__name` rule that Home doesn't match. That descendant rule was removed.

## 27. Real photography (Unsplash, WebP)

All placeholder imagery was replaced with Unsplash photos (Unsplash License: free for commercial use, no attribution required). Each attachment's description records the source URL. Files were downloaded as WebP (q 70; anything over 150KB re-saved at q 62). WordPress generates the smaller sizes the cards use.

| Slot | Attachment IDs | Size | Unsplash photo IDs |
|---|---|---|---|
| Team portraits (featured image; used on Team archive/single, attorney cards, Firm menu, news/result sidebars) | 783–794 | 800×1000, face-cropped, 31–130KB | Eleanor Hartwell `1508214751196-bcfd4ca60f91`, Marcus Crane `1560250097-0b93528c311a`, Ben Foster `1500648767791-00dcc994a43e`, Grace O'Neill `1438761681033-6461ffad8d80`, Carlos Mendez `1559548331-f9cb98001426`, Linda Park `1614644147724-2d4785d69962`, Aisha Bennett `1573497161161-c3e73707e25c`, James Whitaker `1519085360753-af0119f7cbe7`, Rosa Delgado `1567532939604-b6b5b0db2604`, Samuel Ortiz `1629425733761-caae3b5f2e50`, Daniel Reyes `1557862921-37829c790f19`, Priya Okafor `1611432579699-484f7990b127` |
| Blog featured images (all 10 posts) | 795–804 | 1600×1000, 51–135KB | truck `1519003722824-194d4455a60c`, non-compete `1517245386807-bb43f82c33c4`, probate `1450101499163-c8848c66ca85`, family business `1554224155-6726b3ff858f`, police `1453873531674-2151bcd01707`, retaliation `1568992687947-868a62a9f521`, contract `1521791055366-0d553872125f`, dog bite `1543466835-00a7907e9de1`, child support `1609220136736-443140cffec6`, expunction `1575505586569-646b2ca898fc` |
| Home "About" frame | 805 | 800×1000, 70KB | courthouse `1436450412740-6b988f486c6b` |

The old generated portrait JPGs (662–673) were deleted.

**Template changes (native Image elements, BEM classes)**
- Post cards (Home Insights, Blog archive, related posts on Blog Single and Practice Single):
  - `post-card__media` now holds an Image with class `post-card__image` (100% × 100%, cover).
  - Loops use `{featured_image}` (medium_large). The 3 static Home cards use their post's image.
  - The icon and gradient placeholders were removed, along with the classes `post-card__media--injury/--employment/--estate`. Card hover now zooms the photo (`post-card` selector `&:hover .post-card__image`, scale 1.04).
- Blog archive featured post: `post-featured__media` > `post-featured__image` (absolute, cover, `{featured_image}`, large). The "Featured" badge sits above it (`z-index 1`).
- Blog Single cover: `article-cover__image` (21:9, overflow hidden, shadow) > `article-cover__photo` (`{featured_image}`, full).
- Home About frame:
  - `about__frame` > `about__photo` (absolute, cover).
  - The quote area `about__figure` carries a dark gradient so the white quote stays readable. The inset gold border (`about__frame::after`) is kept.
- **To change any of these photos:** set the post's or team member's Featured image (or replace attachment 805 for the About frame).

### 27a. Follow-up: law-firm-appropriate portraits, all looped images from the post

- **Six casual headshots replaced with business portraits** (blazers or suits; WebP, 62–98KB). New attachments 806–811; the previous files were deleted.
  - Eleanor Hartwell `1573497019940-1c28c88b4f3e`
  - Linda Park `1573497019236-17f8177b81e8`
  - Priya Okafor `1563132337-f159f484226c`
  - Daniel Reyes `1600878459138-e1123b37cb30`
  - Samuel Ortiz `1556474835-b0f3ac40d4d1`
  - Rosa Delgado `1598257006458-087169a1f08d`
- **Home "Insights" is now a query loop** (latest 3 posts, sticky ignored) cloned from the Blog archive card, so its image is `{featured_image}`. The hand-built static cards with fixed images were removed.
- **Rule:** every image inside a query loop comes from the post itself:
  - featured image: blog cards, featured post, article cover, team photos, recognition logos
  - ACF field: wherever a template needs a second image
  - Static images are only used outside loops (the Home "About" frame).

### 27b. Blog images: law-firm themed

Four off-topic blog photos (laptop meeting, café office, beagle, family) were swapped for legal imagery. New attachments 812–815, WebP 61–126KB; the previous files were deleted.
- Non-compete: law library `1521587760476-6c12a4b040da`
- Retaliation: judge's gavel `1593115057322-e94b77572f20`
- Dog bites / premises liability: Lady Justice scales `1589994965851-a8f479c573a9`
- Child support: Lady Justice with law books `1505664194779-8beaceb93744`

The other six already read as legal in context (truck on highway, signing documents ×2, legal paperwork, police car, gavel).

Note: unsplash.com search pages are bot-protected from this environment. Photos are chosen by CDN ID (`images.unsplash.com/photo-…`) and checked visually on contact sheets. To pick specific photos yourself, open them on unsplash.com and set them as the post's Featured image.
