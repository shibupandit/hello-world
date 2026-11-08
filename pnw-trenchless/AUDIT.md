# PNW Trenchless: design vs Bricks staging audit (2026-11-08)

Scope: `index.html` (approved design) vs the staging build on shibunew-com.us.stackstaging.com: header template 101, Home page 94, footer template 102. Compared section by section at 1440 and 390 (screenshots), and checked layout/overflow at 991 and 768.

Side-by-side screenshots (design left, staging right): `screenshots/audit/{1440,390}-NN-<section>.jpg`.

## 1. Visual differences found and fixed

| # | Where | Issue | Fix |
|---|---|---|---|
| 1 | Every section | Content width was ~1100px (Bricks' default container width) instead of the design's 80rem / 1280px. The theme-style "root container width" only applies to root-level containers, not containers inside sections | Theme style `container.width = var(--content-width)`, `widthMax = 100%` |
| 2 | Section heads (audience, process, projects, areas, services) | Headings wrapped earlier than the design because the head blocks were capped in `ch` | `section__head` max-width `var(--width-l)`, `section__head-main` `calc(var(--width-l) - var(--space-xl))` |
| 3 | Type sizes | Several titles used `--text-xl` (32px at desktop) where the design uses 1.35–1.6rem: audience cards, reviews, assurance, form title, footer phone, ticker words. Stats, rating, process and signature numerals were too small on mobile | Mapped to the design's sizes with ACSS tokens, e.g. `calc(var(--h4) * 1.3)` = 24px, `calc(var(--h2) * 1.4)` for stats (3rem→5.25rem), `calc(var(--h3) * 1.37)` for service titles |
| 4 | Decision flow | Camera circle smaller than the design (its `em` resolved against the feed's small mono font size) | `width: min(100%, calc(var(--text-m) * 22))`, mobile `calc(var(--text-m) * 7.5)` |
| 5 | Projects | During/after photos did not fill the feature card height | `job-pair` rows stretch, figure is a flex column, image `aspect-ratio: auto` above 991px |
| 6 | Mobile rows (flow start, upload, icon + text rows) | Bricks blocks allow wrapping by default, so the second item dropped onto a new line | Every flex row is now generated with `flex-wrap: nowrap` unless the rule asks for wrapping |
| 7 | Quote form | "Tell us what's going on" was a single-line field; the design has a textarea | New modifier `form__field--area` (min-height 6.5em) |
| 8 | Footer | Logo smaller than the design (72px) | `logo--footer` image height `calc(var(--text-m) * 4.25)` |
| 9 | Footer wordmark | "TRENCHLESS" smaller than the design on phones | `clamp(var(--h2), calc(var(--space-xs) + 8.4vw), calc(var(--h1) * 1.55))` |
| 10 | Explainer video card | The client has no video (user, 2026-11-08) | Replaced with a photo card using the client's own job photo (`job-during.jpg`), with a caption; the play button, duration and video wording are gone |
| 11 | Mobile menu | Side panel didn't match the design | Rebuilt as a full-width drop-down under the header with Nav (Nestable); see `screenshots/bricks-staging/mobile-menu-dropdown-*.jpg` |

Checked and matching: top bar, header, hero, ticker (two rows, outline names, joints), stats, warning signs, explainer and cross-section (toggle works through Bricks interactions), services cards, comparison table, process, about/Mike, reviews, service areas and map, FAQ accordion, quote section, footer, mobile call bar. No horizontal scroll at 1440, 991, 768 or 390 (the ticker, review row, comparison table and cross-section scroll inside themselves, as in the design).

## 2. Code audit

Checked automatically from the generators (`wp-build/classes.py`, `wp-build/elements.py`) and on the rendered page.

- **BEM:** all 266 PNW classes match `block`, `block__element` or `block--modifier`. Fixed: the state class `is-selected` became `chip-option--selected`.
- **Mixes kept on purpose (BEM mix, one block class plus a shared motif or utility):** `feed …` (camera-feed motif on hero, flow and mini cards), `rise rise--N` (hero load animation), `grain` (film grain on ink sections), `section section--dark …`, `split split--…`, `logo logo--footer`, ACSS `btn--*`.
- **Unused classes:** none left. Deleted: `feed--clean`, `feed--blue`, `feed__hud--center`, and the earlier `nav__close`, `nav__brand`, `icon`, `toggle`, `tag`, `field*`.
- **Element-level styles:** none left. The two intro `max-width`s moved to `section__intro--narrow`, and the hero container gap moved into the `hero` class. Elements carry classes, content, links, attributes and interactions only.
- **IDs:** element IDs are used only as anchors (`#services`, `#how`…) and interaction targets (`#xsec`, `#xsec-dig`, `#xsec-trenchless`), never for styling. The one ID selector in CSS is Bricks' own `#brx-header` wrapper (sticky header), in the theme style.
- **Buttons:** all buttons are native Button elements with ACSS classes (`btn--primary`, `btn--white btn--outline`, `btn--base btn--outline`, `btn--s`). There are no custom `.btn` rules.
- **ACSS variables:** colour, spacing, gaps, radius, shadow and type sizes come only from ACSS variables or `--pnw-*` tokens built from them. Raw values still present, and why:
  - Camera-feed scanlines `1px`/`3px` in `feed`: hairline pattern inside the signature motif, which ACSS has no token for (allowed exception).
  - `0px` fallbacks in `var(--pnw-topbar-h, 0px)`, `var(--wp-admin--admin-bar--height, 0px)` and `env(safe-area-inset-bottom, 0px)`: a unitless `0` is invalid inside `calc()` subtraction.
  - Media query widths (`991/767/478/1200px`): breakpoints, not styling values.
  - The SVG illustrations (cross-section, map, service art) keep their own colours inside the files.
- **Grids:** component grids (cards, stats, steps, splits) are BEM classes with ACSS gap/spacing variables. ACSS `grid--*` utility classes weren't used, because they can't express the design's uneven tracks (`.9fr/1.1fr`, `1.25fr/.75fr`) or the per-component breakpoints.
- **Semantics and accessibility:**
  - One `h1` (hero), one `h2` per section, `h3` for cards and items. Fixed: footer column titles were `h4` with no `h3` before them; they're now `h2` (same look).
  - Card lists are `ul`/`li` (services, audience, signs, creds, checklist, cities, proof); steps and next steps are `ol`.
  - Every image has alt text (the hero background is decorative, `alt=""`).
  - The duplicate ticker group and the second ticker row carry `aria-hidden`, and the duplicate links have `tabindex="-1"`.
  - The cross-section toggle uses `aria-pressed`; the mobile menu toggle uses `aria-expanded`, with a focus trap and Esc to close.
  - The amber focus ring comes from ACSS (`focus-color: var(--accent)`).
  - Text on ink sections uses `--text-light` / `--text-light-muted` (#A8B3BF on #0E1621, about 9:1).

## 3. Left as is, needs a decision

| Item | Notes |
|---|---|
| Archivo width axis | The uploaded Archivo has no `wdth` axis, so headings and the ticker aren't stretched wide like the design (most visible in the hero). Upload the variable Archivo file with `wdth` 62–125 to the Bricks font manager; the `font-stretch` rules are already in place |
| Breakpoint 961–991px | The design switches some grids at 960, 900 or 860px. The build uses Bricks' 991px tablet breakpoint, so between 961 and 991px a few sections already stack |
| `tbc` content | Google rating, review count and reviews; warranty and financing; timelines; founding year; certifications; project details; FAQ answers ("Draft · Mike to confirm"); hours and address; Mike's portrait; video |
| Quote form | Styled dummy. Swap for Fluent Forms (or GHL) and keep the `form` wrapper classes |
| Hero footage counter | Static. Animating it needs a code element, which needs the user's explicit OK |
| FAQ schema | Off until Mike confirms the draft answers |
| Repeating content | Services, projects, reviews and areas are static. ACF Pro is now installed, so they can move to CPTs and Query Loops |
| ACSS contextual buttons | `bg--ultra-dark` / `bg--ultra-light` repaint every `btn--*` primary, and ACSS 3.3.8 can't switch this off. The build avoids those classes on sections (it uses `section--dark` / `section--tint`) |
