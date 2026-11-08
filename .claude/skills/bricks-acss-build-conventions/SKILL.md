---
name: bricks-acss-build-conventions
description: House conventions for building WordPress sites in Bricks Builder with Automatic.css (ACSS), Fluent Forms, ACF and HappyFiles through the Novamira MCP connector. Use when designing a page that will be rebuilt in Bricks, when building or editing pages/templates/classes in Bricks, or when preparing a Bricks + ACSS handoff.
---

# Bricks + ACSS build conventions

Learned from the agency's reference build (the "Hartwell & Crane" template on whitecrowtemplate.kinsta.cloud). Follow these on every new build so all sites share the same structure.

## Before touching any site

1. Confirm **which WordPress site** the work is for. Never write to a site the user hasn't named for this project.
2. Start **read-only**. Use the `novamira/bricks-get-design-system`, `novamira/bricks-check-setup`, `novamira/bricks-list-templates`, `novamira/bricks-list-global-classes`, `bricks/get-page-structure`, `novamira/bricks-read-css` and `novamira/memory-list` abilities to learn the site first. Reuse existing classes, templates and forms before creating new ones.
3. Read the site's Novamira memories (`novamira/memory-get`) and follow them.

## Stack

- Bricks (theme), Automatic.css, ACF Pro, Fluent Forms + Pro, HappyFiles Pro, Perfmatters.
- **ACSS owns the variables.** Don't create Bricks global variables for design tokens. Put project-specific variables in the **Global theme style > Custom CSS** `:root` block with a project prefix (e.g. `--pc-…`, `--pnw-…`), and build them from ACSS colours with `color-mix()`.
- **Google Fonts are disabled in Bricks.** Self-host woff2 files as Bricks Custom Fonts.
- Breakpoints are desktop-first: base 1279, tablet portrait 991, mobile landscape 767, mobile portrait 478.

## Structure and naming

- Every section: **Section › Container › Div/Block**.
- One **BEM global class** per element (`hero`, `hero__inner`, `hero__content`, `service-card__title`). Style the class, not the element.
- Shared section classes:
  - `section` (padding `var(--section-space-m)`)
  - modifiers `section--tint`, `section--dark`, `section--tight-top`
  - `section__inner`, `section__head` (`--split`, `--center`), `section__title`, `section__intro`
- **Buttons:** the native Button element with **ACSS button classes** (`btn--primary`, `btn--outline`, `btn--white`, sizes `btn--s/m/l`). Set the icon in the Button element.
- Icons are inline SVG with a shared `icon` class (1.2em, currentColor).
- **Clickable cards:** stretched link (`.card__link::after { content:""; position:absolute; inset:0 }`), never an `<a>` around the whole card.
- Card lists are `ul`/`li` with `list-style: none`.
- Repeating content (team, services, projects, reviews, locations, posts) uses **custom post types (ACF) + Bricks single/archive templates + Query Loops**. Reusable strips (CTA band, testimonials slider, logos strip) are **Section templates** inserted with a Template element.

## Styling rules

**Hard rule (user, 2026-11-08):**
- **Use Automatic.css framework variables and classes only** for colour, margin, padding, spacing, gaps, grids and buttons:
  - **Colour:** only ACSS colour variables (`var(--primary)`, `--primary-dark`, `--base`, `--base-medium`, `--neutral-ultra-light`, `--accent`, `--text-dark`, `--text-light-muted`, the `-trans-*` variants…). No hex, rgb or hsl in Bricks.
  - **Margin, padding, spacing:** only `var(--space-xs…xxl)`, `var(--section-space-*)`, `var(--gutter)` / `--section-padding-x`, `var(--content-gap)` / `--container-gap`. No px or rem values.
  - **Gaps:** `var(--grid-gap)`, `var(--content-gap)`, `var(--container-gap)`, `var(--space-*)`.
  - **Grids:** ACSS grid classes and variables first (`grid--2`, `grid--3`, `grid--auto-*`, breakpoint variants like `grid--m-1`, the `--grid-*` variables), custom grid CSS only if those can't do it.
  - **Buttons:** only the native Bricks Button element with ACSS `btn--` classes (`btn--primary`, `btn--outline`, `btn--white`, `btn--white-outline` / `btn--primary-outline`, sizes `btn--s/m/l`). No custom `.btn` rules.
  - Custom values only where ACSS has nothing for the job: the `--pnw-` variables in ACSS custom CSS (fonts, ease, header height, borders, primary shadow), pseudo-elements and the camera-feed motif. Even there, build them from ACSS variables (e.g. `color-mix()`).

- Only ACSS variables:
  - spacing: `--space-xs…xxl`, `--section-space-m`, `--grid-gap`
  - type: `--h1…h4`, `--text-xs…xl`
  - colour: `--primary` / `-dark` / `-ultra-dark` / `-light` / `-ultra-light`, `--accent…`, `--base`, `--base-semi-dark`, `--white-trans-10/20/60`, `--base-trans-10`
  - shape: `--radius`, `--radius-s`, `--radius-circle`, `--border-size`

  No hardcoded hex/px in the builder.
- Use native Bricks controls first. A class's custom CSS is only for pseudo-elements, child `:hover`, Fluent Forms selectors and things the controls can't express.
- Put responsive changes in the class's breakpoint settings (e.g. grid 3 → 2 at 767 → 1 at 478).
- Motion is CSS only and always disabled under `prefers-reduced-motion`:
  - scroll-driven card reveal (`.brx-animated` + keyframes)
  - `::details-content` FAQ animation
  - scroll-drawn process connector

## Section patterns to reuse

| Need | Pattern |
|---|---|
| Hero over a photo | `hero` with `::before` gradient overlay (`--primary-ultra-dark` → `-trans-60`), `hero__inner` grid 1.25fr/1fr, 1 column below 991 |
| Stats band | `stats` > `stats__grid` (4 → 2 cols) > `stat` (`stat__value`, `stat__label`) |
| Service/practice cards | `practice-card`: icon, title, text, stretched `__link`, hover fills `--primary` |
| Process | `process__steps` (ol) + `process-step` with a `__num` circle and dashed connector (vertical below 991) |
| FAQ | `faq__inner` (sticky `faq__intro`) + `faq-item` using `details`/`summary`, icon rotates 45° |
| Quote/contact before the footer | `contact` on `--primary-dark`: `contact__inner` grid, `contact__details` with round icons, white `contact__form` card with large shadow |
| Footer | `footer`, `footer__inner`, `footer__col`, `footer__legal`, `social-links--light` |

## Forms (Fluent Forms)

- Wrap the form in the global class `form` (add `form--dark` on dark backgrounds). That class styles labels, inputs (`--base-ultra-light`, `--primary` focus ring) and a full-width submit button.
- Side-by-side fields use the Fluent Forms container class `ff-half` inside a 2-column grid `fieldset`, 1 column below 480px.
- Set a same-page confirmation message. Wire the form to the client's CRM (e.g. GoHighLevel) and the GA4/Ads conversion.

## Media

- Every upload goes into a **HappyFiles folder** (taxonomy `happyfiles_category`): Brand > Logos, Brand > Fonts, Images > Hero / About / Team / Services / Projects / Testimonials, Images > Placeholders, Icons, Documents.

## Design-to-Bricks handoff checklist

- An HTML design uses ACSS-named tokens in `:root` (so values copy straight into ACSS) and BEM classes that match the names above.
- The handoff document lists: ACSS colour/type/spacing values, custom variables, global classes, a section-by-section Bricks element tree, form fields, CPTs/templates, content still to confirm.
- Pre-launch:
  - no hardcoded values
  - remove placeholder classes
  - test the mobile menu, interactive parts, form submit/conversion and the mobile call bar on a real phone

## Gotchas learned on the PNW staging build (Bricks 2.4.5 + ACSS 3.3.8, via Novamira)

- **ACSS CSS regenerated from execute-php/REST skips the Bricks platform** (its `option-bricks` filter is only registered in admin). Result: near-empty `automatic-bricks.css` and no `btn--` classes. Regenerate with `add_filter('automaticcss_framework_variables', fn($v)=>$v+['option-bricks'=>'on'])` before `save_settings()`, or save from the ACSS admin screen.
- **ACSS contextual buttons can't be switched off** (`bg-*-button` empty falls back to `primary`). Inside `bg--ultra-dark` / `bg--ultra-light` every `btn--*` is repainted primary. Use your own section modifiers (`section--dark`, `section--tint`) built from ACSS variables when you need white or ink outline buttons.
- **Bricks blocks default to `width: 100%`, `max-width: 100%` and `flex-direction: column`.** Write `flex-direction: row` explicitly, set `width: auto` on inline-style blocks (logos, chips, link groups, absolute HUD rows) and `max-width: none` on `max-content` tracks (tickers).
- **Never send an empty settings object (`{}` / stdClass)** through set/insert-content: Bricks fatals ("Cannot use object of type stdClass as array"). Send `[]`.
- **`backdrop-filter` on a header makes it the containing block for the fixed mobile menu.** Put the blur on a `::before` layer.
- **ACSS only pads `<section>`.** A Bricks section with tag `footer` needs its own padding.
- **Global class CSS is only output for classes on elements.** Inline helper spans in text (`serif`, `tbc`) need their CSS in the theme style.
- **Avoid class names Bricks already uses** (`icon`, `toggle`, `tag`, `field`).
- **Accordion content:** never set `display` on the content wrapper class. It overrides Bricks' `display: none` for closed items.
- **Headless screenshots of stackstaging sites:** the page cache and bot challenge block Playwright. Fetch HTML with curl plus a cache-busting query, add `<base href>`, and route asset requests through `route.fetch` with a curl user-agent. Full-page captures stop at 16,384px.
