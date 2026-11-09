# Build conventions learned from whitecrowtemplate (read-only study)

Source: a read-only review of the whitecrowtemplate.kinsta.cloud build (the "Hartwell & Crane" law-firm template) on 2026-11-08. I didn't change anything on that site. These are the patterns to repeat when the PNW Trenchless design goes into Bricks. The build site is the staging site `shibunew-com.us.stackstaging.com` (Novamira connector `novamira-shibunew-com-us`).

## Stack on that build

- Bricks 2.4.5, Automatic.css 3.3.8, ACF Pro, Fluent Forms + Pro, HappyFiles Pro, Perfmatters
- **Bricks Variables Manager not used.** ACSS owns the variables. Project-specific variables live in the **Global theme style > Custom CSS** `:root` block with a project prefix (`--pc-shadow-s/m/l`, `--pc-ease`, `--pc-page-bg`, …), written with ACSS colours through `color-mix()`.
- **Google Fonts disabled in Bricks.** Fonts are self-hosted (woff2) and registered as Bricks Custom Fonts.
- Breakpoints: Desktop base 1279, tablet portrait 991, mobile landscape 767, mobile portrait 478 (desktop-first).
- One global theme style: body font, size `var(--text-m)`, line height 1.65, colour `var(--base)`, site background `var(--white)`, container width `var(--content-width)`.

## Structure and naming

- Every section is **Section › Container › Div/Block**. Each element carries **one BEM global class** (`hero`, `hero__inner`, `hero__content`, `practice-card__title` …), and almost nothing is styled on the element itself.
- Shared section classes: `section` (padding `var(--section-space-m)`), modifiers `section--tint` (primary-ultra-light), `section--dark` (primary), `section--tight-top`, plus `section__inner`, `section__head` (`--split`, `--center`), `section__title`, `section__intro`.
- **Buttons use the ACSS button classes** (`btn--primary`, `btn--outline`, `btn--white`, size `btn--s/m/l`) on the native Button element, with the icon set in the Button element. A small theme-style rule handles icon gap and hover nudge.
- Icons are inline SVG with a shared `icon` class (1.2em, `currentColor`).
- Cards are clickable through a **stretched link** (`…__link::after { content:""; position:absolute; inset:0 }`) instead of wrapping the card in an `<a>`.
- Lists of cards are `ul`/`li` with `list-style:none` (e.g. `practice__grid`, `attorneys__grid`, `insights__grid`).
- Repeating content (team, posts, case results, news, cities) uses **CPTs plus Bricks templates** (single and archive), filled by Query Loops. Reusable strips are **Section templates** (e.g. "Recognition Strip", "Testimonials Slider") inserted with a Template element.

## Styling rules

- All spacing, type and colour come from ACSS variables: `--space-xs…xxl`, `--section-space-m`, `--h1…h4`, `--text-xs…xl`, `--primary/-dark/-ultra-dark/-light/-ultra-light`, `--accent…`, `--base`, `--base-semi-dark`, `--white-trans-10/20/60`, `--base-trans-10`, `--radius`, `--radius-s`, `--radius-circle`, `--border-size`, `--grid-gap`.
- Native Bricks controls are used wherever possible. Global-class custom CSS covers only pseudo-elements, `:hover` on children, `@media` overrides and Fluent Forms selectors.
- Responsive changes go in Bricks breakpoint settings on the class (for example, a grid goes from 3 columns to 2 at mobile landscape and to 1 at mobile portrait).
- Motion is CSS only:
  - a scroll-driven card reveal (`hc-reveal` keyframes on `.brx-animated`)
  - a `::details-content` FAQ open/close animation
  - a scroll-drawn process connector
  - everything disabled under `prefers-reduced-motion`

## Patterns that map directly to the PNW design

| PNW section | Pattern from that build |
|---|---|
| Hero with photo + overlay | `hero` with a `::before` gradient overlay using `--primary-ultra-dark` / `-trans-60`, `hero__inner` grid 1.25fr / 1fr |
| Stats band | `stats` > `stats__grid` (4 → 2 columns) > `stat` with `stat__value` / `stat__label` |
| Services cards | `practice-card` pattern: icon, title, text, stretched `__link` |
| Process | `process__steps` (ol) + `process-step` with `__num` circle and a dashed connector that turns vertical below 991px |
| FAQ | `faq__inner` (sticky `faq__intro`) + `faq-item` built on `details`/`summary` with an icon that rotates 45° |
| Quote form before the footer | `contact` section (primary-dark): `contact__inner` grid, `contact__details` list with round icons, `contact__form` white card with shadow `--pc-shadow-l` |
| Footer | `footer` with `footer__inner`, `footer__col`, `footer__legal`, `social-links--light` |

## Forms (Fluent Forms)

- The form sits in a wrapper with the global class `form` (plus `form--dark` on dark backgrounds). That class restyles Fluent Forms: labels, inputs on `--base-ultra-light`, a focus ring in `--primary`, and a full-width submit button.
- Two-column fields use the Fluent Forms container class `ff-half` inside a grid `fieldset`, collapsing to 1 column below 480px.
- Example: "Case Review (short)" has Full name (`ff-half`), Phone (`ff-half`), a Type of matter select and a "Briefly, what happened?" textarea, with a same-page confirmation message.
- PNW (built 2026-11-09): Fluent Forms #3 "Request a quote", embedded with a Bricks Shortcode element that has the class `form__fluent` inside the `form` card; see the project skill for fields and styling. Originally planned: create the "Request a quote" form the same way. Name and Phone use `ff-half`, Email and Address use `ff-half`, the service type and property type are radio/select fields, then details and a file upload. Style it with the `form` class.

## Media

- Every upload is filed in a **HappyFiles folder** (taxonomy `happyfiles_category`): Brand > Logos, Brand > Fonts, Images > Hero / About / Team / Services / Blog / Testimonials, Images > Placeholders, Icons, Documents.

## What this changes in the PNW handoff

1. Rename the design's ad-hoc classes to this vocabulary:
   - `bg--ink` → `section--dark` (or a `--primary-dark` modifier); `bg--stone` → `section--tint`
   - `head` → `section__head`; `head__lede` → `section__intro`
   - `btn--ghost` → `btn--outline`
2. Use ACSS button classes instead of the custom `.btn` rules.
3. Put PNW-only variables in custom CSS with a `--pnw-` prefix rather than in Bricks variables. Done: `--pnw-font-serif`, `--pnw-font-mono`, `--pnw-header-h`, `--pnw-ease`, `--pnw-border`, `--pnw-border-dark`, `--pnw-shadow-primary` (currently in ACSS custom CSS).
4. Self-host Archivo, Public Sans and JetBrains Mono, because Google Fonts are disabled on that build pattern.
5. Build services, projects, reviews and service areas as CPTs + Query Loops, and the ticker, reviews and quote CTA as Section templates.
6. File every PNW asset in HappyFiles folders.
