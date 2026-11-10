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

## Shared component classes (2026-11-10)

Common layouts use **one shared class** site-wide, so a change to it applies everywhere. Before adding a
page class, check this list: if the layout already exists, use the shared class, and add a page class only
for what is truly specific (it then sits next to the shared class on the element, e.g. `text-block cost__text`).

- Source: the "Shared components" section at the top of `wp-build/classes.py`.
- How the merge was done and checked: `wp-build/tools/merge_classes.py` (families in `SPEC`, mapping in
  `tools/merge_map.json`, offline check with `--verify`). 588 classes became 510; the old classes were deleted.
- Checked on the live site with a before/after snapshot of 12 pages at desktop and phone width (8,914 element states: computed styles and positions). One cascade-order regression was found and fixed: a modifier that overrides its own block (`who__kicker--dark`) must stay a page class defined after the block, not a shared class.
- "Merged away" classes no longer exist. "Kept" classes still exist but only hold their own extras.

| Shared class | What it sets | Merged away | Kept (extras only) |
|---|---|---|---|
| `caption` | color: var(--text-dark-muted); font-size: var(--text-s); | `sign__text`, `signature__role`, `steps-mini__text`, `pcard__text`, `docs__text`, `ws-svc__text`, `job__spec`, `mini__text`, `verify-card__fine`, `pj-inline__cap`, `who__cap`, `widget__muted` | — |
| `caption-light` | font-size: var(--text-s); color: var(--text-light-muted); | `mike__role`, `jump__note`, `svc-hero__cap`, `bigphone__note`, `milestone__text` | — |
| `caption-neutral` | font-size: var(--text-s); color: var(--neutral); | `mike__sig-role`, `form__hint` | — |
| `fine-light` | color: var(--text-light-muted); font-size: var(--text-xs); | `review__meta`, `portrait__role` | — |
| `text-muted` | color: var(--text-dark-muted); | `compare__cell--them`, `promise__text` | — |
| `text-light-muted` | color: var(--text-light-muted); | `footer__hours`, `score__count`, `rv-steps__text` | — |
| `text-accent-light` | color: var(--primary-light); | `project__link`, `who__kicker--dark`, `crumbs__current` | — |
| `strong-dark` | font-weight: 700; color: var(--text-dark); | `signature__name`, `rv-card__name`, `widget__name` | — |
| `value-light` | margin: 0; font-weight: 600; color: var(--white); | `info-card__value`, `pj-meta__value`, `pj-card__value` | — |
| `title-light` | font-family: var(--heading-font-family); font-weight: 800; font-size: var(--text-l); color: var(--white); | `portrait__name`, `ind__fact-value` | `jump__title` |
| `title-l` | font-size: var(--text-l); | `sign__title`, `verify-card__title`, `docs__title`, `who__h3` | — |
| `title-card` | font-size: calc(var(--h4) * 1.3); | `aud-card__title`, `fit-card__title` | — |
| `title-block` | font-size: calc(var(--h3) * 1.05); | `urgent__title`, `pj-block__title` | — |
| `accent-light` | color: var(--primary-light); | `svc-hero__title`, `owner__title` | — |
| `label` | font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase | `story__meta`, `pj-glance__label`, `spec-table__term` | `outcome__if` |
| `label-light` | font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase | `reach__label`, `pj-meta__term`, `ind__fact-label`, `fact__label` | — |
| `label-accent` | font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase | `score__label` | `jump__label`, `info-card__term`, `pj-card__term` |
| `label-wide` | font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase | `hero__seo`, `ticker__city` | — |
| `stack-l` | display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-l); min-width: 0; | `hero__content`, `mike__content`, `svc-hero__content`, `owner__content` | — |
| `stack-m` | display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); min-width: 0; | `pj-hero__title`, `near` | `who__text` |
| `stack-s` | display: flex; flex-direction: column; gap: var(--space-s); min-width: 0; | `hero__aside`, `who__col` | — |
| `stack-xl` | display: flex; flex-direction: column; gap: var(--space-xl); min-width: 0; | `pj-story__body`, `city-main` | — |
| `figure-stack` | margin: 0; display: flex; flex-direction: column; gap: var(--space-s); min-width: 0; | `who__media`, `svc-hero__media` | — |
| `text-block` | display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); min-width: 0; | `areas__text`, `local__text` | `explain__text`, `cost__text` |
| `text-block-light` | display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-l); min-width: 0; | `rig__text` | `estimate__text`, `rv-leave__text` |
| `id-stack` | display: flex; flex-direction: column; gap: 0; width: auto; | `portrait__id`, `signature__id`, `rv-card__id`, `review__name` | — |
| `mini-stack` | width: auto; display: flex; flex-direction: column; gap: .35em; | `mike__sig`, `score__side` | — |
| `chip-row` | display: flex; flex-direction: row; flex-wrap: wrap; gap: var(--space-xs); | `materials`, `near__cities` | `who__links` |
| `grow` | flex: 1 1 auto; min-width: 0; | `byline__text`, `related__label` | — |
| `btn-block` | width: 100%; justify-content: center; | `nav__quote`, `form__submit` | — |
| `section--tight` | padding-block: var(--space-xxl); | `urgent` | — |
| `split` | display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: var(--space-xxl); align-items: st | `specs__grid`, `ind` | — |
| `split-even` | display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: var(--space-xxl); align-items: cente | `local__grid`, `rv-leave__grid` | — |
| `split-wide` | display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr); gap: var(--space-xxl); align-items: ce | `rig__grid`, `cost__grid` | — |
| `grid-2` | display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-l); width: 100%; | `fit__grid`, `inside__grid` | — |
| `grid-3` | list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: | `aud-grid`, `jobs__grid` | — |
| `grid-3-2` | list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: | `promises__grid`, `pcards` | — |
| `grid-4` | list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: | `docs__grid`, `ws-svc`, `verify__grid` | `timeline__list` |
| `list-plain` | list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0; width: 100%; | `widget__list`, `widget__svc` | — |
| `list-ruled` | list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0; border-top: var(--pnw- | `who__list`, `fit-card__list` | — |
| `list-ruled-dark` | list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0; border-top: var(--pnw- | `next`, `rv-steps`, `cost-card__list` | — |
| `list-ruled-strong` | list-style: none; margin: 0; padding: 0; border-top: var(--border-size) solid var(--text-dark); display: flex; | `city-list`, `sign-list` | — |
| `num-row` | display: grid; grid-template-columns: 2.5em minmax(0, 1fr); gap: var(--space-s); padding: var(--space-s) 0; bo | `next__item`, `cost-card__item` | — |
| `num-row__num` | font-family: var(--pnw-font-mono); color: var(--accent); font-size: var(--text-s); padding-top: .2em; | `next__num`, `cost-card__num`, `rv-steps__num` | — |
| `ico-tile` | width: 52px; height: 52px; flex: none; border-radius: var(--radius); display: grid; place-items: center; backg | `jump__ico`, `who__ico` | `ws-svc__ico` |
| `ico-round` | width: 3em; height: 3em; aspect-ratio: 1; flex: none; border-radius: var(--radius-circle); display: grid; plac | `promise__ico`, `docs__ico` | — |
| `card-num` | position: absolute; top: var(--space-l); right: var(--space-l); font-family: var(--pnw-font-mono); font-size:  | `promise__num`, `docs__num` | — |
| `tag--after` | background: var(--primary); | `job-pair__tag--after`, `mosaic__tag--after`, `still__tag--after` | — |
| `card-soft` | position: relative; display: flex; flex-direction: column; gap: var(--space-s); padding: var(--space-l); borde | `docs__item` | `promise` |
| `card-dark` | display: flex; flex-direction: column; gap: var(--space-m); padding: var(--space-l); border-radius: var(--radi | `pj-card` | `cost-card` |
| `rows-dark` | margin: 0; width: 100%; border-top: var(--pnw-border-dark); display: flex; flex-direction: column; gap: 0; | `kit`, `pj-card__list` | — |
