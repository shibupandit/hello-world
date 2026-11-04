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
