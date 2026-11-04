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

## 2. ACSS dashboard settings

### Colors (ACSS → Colors)

| ACSS color | Hex | Use |
|---|---|---|
| Primary | `#123a31` (chancery green) | Hero, dark bands, primary buttons, headings |
| Accent | `#b08a4f` (aged brass) | Main CTAs, icons, the hero ampersand |
| Base | `#1a2421` (green-tinted ink) | Body text |
| White / Black | `#ffffff` / `#0a0f0d` | |

Let ACSS generate the shades. The prototype values used for each are listed in `acss-shim.css`. If the generated shade is far off, override it: `primary-ultra-light #eef4f1` (tinted sections), `primary-light #c9dbd4` (text on dark), `primary-ultra-dark #061512` (topbar, footer), `accent-light #e6d6bb`, `accent-dark #6f5430` (eyebrows, links on white).

Contrast to keep in mind: `accent` on white is only about 3:1, so use it for large text, icons and buttons with white text in bold. For small text on white use `accent-dark`.

### Typography (ACSS → Typography)

- Root font size: **62.5%** (ACSS default; 1rem = 10px)
- Heading font: **Libre Caslon Display**, weight 400. Use Libre Caslon Text for italic quotes and testimonials.
- Text font: **Public Sans**, weights 400/500/600/700
- Load both from Google Fonts (Bricks → Settings → Custom fonts, or self-host for GDPR)
- Body text: min 16px, max 18px. H1: 40 → 72px. H2: 32 → 52px. H3: 24 → 32px. H4: 20 → 24px.
- Headings line-height ~1.05–1.1, letter-spacing −0.01em. Text line-height 1.65.

### Spacing, layout, radius

- Content width: **1240px** (`--content-width`)
- Gutter: 16px → 48px
- Section padding: use ACSS default section spacing; the prototype uses `--section-space-m` on most sections and `--section-space-l` on the hero
- Radius: 6px base (`--radius`), 4px small (`--radius-s`). Keep corners tight; this is a law firm, not an app.

### Project custom tokens

Add these under ACSS → Custom CSS (or Bricks → Settings → Custom code → CSS). They are prefixed `--pc-` so they never collide with ACSS:

```css
:root {
  --pc-font-display: "Libre Caslon Display", Georgia, serif;
  --pc-font-serif: "Libre Caslon Text", Georgia, serif;
  --pc-font-body: "Public Sans", Arial, sans-serif;
  --pc-boxed-width: 144rem;
  --pc-page-bg: #dfe4e1;
  --pc-line: color-mix(in srgb, var(--base) 12%, transparent);
  --pc-line-inverse: color-mix(in srgb, var(--white) 16%, transparent);
  --pc-shadow-s: 0 1px 2px rgb(10 15 13 / .06), 0 2px 8px rgb(10 15 13 / .05);
  --pc-shadow-m: 0 2px 4px rgb(10 15 13 / .05), 0 12px 32px rgb(10 15 13 / .08);
  --pc-shadow-l: 0 30px 80px rgb(6 21 18 / .18);
  --pc-ease: cubic-bezier(.2, .7, .2, 1);
}
```

> Check variable names against your installed ACSS 3.x version. All the color, `--space-*`, `--section-space-*`, `--text-*`, `--h1…h6`, `--radius*` and `--content-width` names follow the v3 docs. If one is renamed in your version, search-and-replace it in `style.css`.

---

## 3. Bricks global settings

1. **Bricks → Settings → General**: enable *Disable default Bricks styles* is optional; ACSS v3 handles base styles.
2. **Theme Styles**: set *Site layout* to **Boxed**, max-width `1440px`, box shadow `var(--pc-shadow-l)`, outer background `var(--pc-page-bg)`. This replaces `body.is-boxed .site` in the CSS. To switch to full-width later, change only this setting.
3. **Theme Styles → Typography**: point heading font to `var(--pc-font-display)` and body to `var(--pc-font-body)` if ACSS is not already setting them.
4. **Theme Styles → Links**: color `inherit`, no underline in nav. Keep underlines in body copy for accessibility.
5. **Breakpoints** (Bricks → Settings → Breakpoints) to match the CSS: desktop, 1180 (nav collapses), 900, 640.

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
| `.btn--primary`, `.btn--accent`, `.btn--outline` | ACSS button classes `btn--primary`, `btn--accent`, `btn--primary btn--outline` on a Bricks **Button** |
| `.btn--lg` | ACSS `btn--l` |
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
Section  .topbar  (hide on mobile: display none at 640)
└ Container .topbar__inner  (flex row, space-between, wrap)
  ├ Icon list / Text: address, hours
  └ Text-link: email, "Se habla español"
Section  .header  (Sticky: Bricks header "Sticky on scroll", add class .is-scrolled via Bricks interaction or main.js)
└ Container .header__inner  (flex row, align center, space-between)
  ├ Logo element (or Div .brand with .brand__mark + .brand__text)
  ├ Nav Menu element  .nav   (Bricks native: mobile menu toggle at 1180px)
  └ Div .header__actions
    ├ Icon + text link .header__phone
    └ Button .btn--primary "Free Case Review"
```

The Bricks Nav Menu (or Nav Nestable) element provides the mobile menu, so `main.js` sections 1–2 are not needed. Style its mobile panel to match `.nav` at the 1180 breakpoint.

### Hero (component: `Hero – Consultation`)

```
Section .hero   (bg: gradient from CSS; ::before ampersand stays in custom CSS)
└ Container .hero__inner   (grid 1.25fr / 1fr; stack at 1180)
  ├ Block .hero__content
  │ ├ Text  .eyebrow .eyebrow--light
  │ ├ Heading h1 .hero__title   (wrap "goes to trial" in <em>)
  │ ├ Text  .hero__lede
  │ ├ Block .hero__actions → 2 Buttons (btn--accent btn--l, outline light)
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
Use Bricks **Slider (Nestable)** with 3 per page / 2 at 1180 / 1 at 640, gap `var(--grid-gap)`, custom arrows placed in `.slider-controls`. Each slide = `.testimonial` card. Or keep the CSS scroll-snap track and `main.js` section 4; both work.

### FAQ
Use Bricks **Accordion (Nestable)** with *Independent toggle* off (one open at a time), title class `.faq-item__q`, content `.faq-item__a`. Add the **FAQPage schema** via your SEO plugin.

### Insights
Query loop on Posts, 3 items, `.post-card` with featured image in `.post-card__media` (aspect 16/10). Category and date via dynamic data `{post_terms_category}`, `{post_date}`.

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
Section `.footer .bg--primary-ultra-dark` → Container `.footer__inner` (grid 1.4fr repeat(3,1fr)) → brand, two Nav Menus (vertical), office address. Second Container `.footer__legal` with copyright `{current_date:Y}`, the attorney-advertising disclaimer, and legal links.

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
