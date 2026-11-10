# Iconic Finance homepage redesign — Bricks + ACSS build notes

`index.html` is a static prototype of the new homepage. Open it in a browser; it needs no build step.
Images are hot-linked from the current site, so download them into the new Media Library during the build.

## 1. ACSS settings (Automatic.css dashboard)

| ACSS setting | Value |
|---|---|
| Primary | `#a71e5b` (brand magenta) |
| Secondary | `#a8863f` (logo gold). Use the dark shade `#7a5f24` for small gold text on light backgrounds (AA contrast) |
| Base | `#1e1a45` (deep navy) |
| Neutral / body background | `#faf8f5`, alt section `#f1ede7` |
| Heading font | Jost 500 |
| Text font | Inter 400/500/600 |
| Content width | 1240px |
| Section padding (M) | `clamp(4.5rem, 9vw, 7.5rem)` |
| Radius | 14px (cards), 24px (large cards) |

All custom properties in the prototype's `:root` use ACSS names (`--primary`, `--space-m`, `--section-space-m`, etc.), so the CSS ports over largely unchanged.

## 2. Section → Bricks structure (top to bottom)

| # | Section | Bricks build |
|---|---|---|
| 1 | Header | Header template: Logo, Nav Menu (nested, with dropdowns), phone link, Button. Sticky. |
| 2 | Hero | Section `.hero` (bg Base) → Container 2-col grid: text block + Image (arched top radius) with two absolutely-positioned badge Divs |
| 3 | Stats | Section `.stats` → 5-col grid of `.stat` blocks |
| 4 | Who we help | Section → heading block + `.paths` grid (6-col; cards 1–3 span 2, cards 4–5 span 3). Each card is a Link block. Good candidate for a **Bricks Component** or Query Loop over a "Services" CPT |
| 5 | How it works | Section bg Base → `<ol>` `.steps` 4-col grid with CSS counters + CTA |
| 6 | Tools | Section → 2-col: repayment estimator (Code element, the JS is in the prototype) + 3 `.tool` link cards |
| 7 | Broker | Section bg Light → 2-col: Image + text, credentials as a list of chips |
| 8 | Case studies | Section → 3-col `.case` cards (Query Loop over a "Case Studies" CPT recommended) |
| 9 | Property report | Magenta `.report` card → 2-col: copy + Bricks Form (or the existing provider embed) |
| 10 | FAQ | Section bg Light → 2-col: heading + Accordion (nestable) element |
| 11 | CTA band | Section bg Base, centred |
| 12 | Footer | Footer template: 5-col grid + compliance block |

Class names follow BEM (`.block__element`) to suit Bricks' global class manager.

## 3. Content to confirm before publishing

- **FAQ answers.** All six answers are placeholders. They need to be written by the broker and compliance-reviewed.
- **Property report disclaimer.** It is still marked `[VERIFY]` (data source wording to be confirmed with the provider).
- **"5★ Google reviews".** The current site shows "5" next to stars. Confirm this is the star rating, not the review count.
- **New copy not on the current site:** the hero eyebrow "Sydney mortgage broker", the closing CTA heading "Find out what you can borrow, and how to structure it", and the "60+ Lender panel to compare" badge. Everything else is the existing wording.
- **Repayment estimator.** This is new. It uses the standard principal & interest formula and sits under the existing calculator disclaimer.
- **Links still set to `#`:** social profiles, LinkedIn and compliance pages. Point them at the real URLs.
- **Report form.** It only shows a thank-you message for now. Connect it to the Bricks form action or CRM.
