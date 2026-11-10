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
| 2 | Hero | Section bg Base → 2-col grid: text + Image (arched top), with a plain text row under it (stars + lender panel) |
| 3 | Stats | 5 figures in one row, divided by rules |
| 4 | Who we help | Split heading row → `.paths` grid of plain filled cards (6-col; cards 1–3 span 2, 4–5 span 3). Use a Bricks Component or a Query Loop over a Services CPT |
| 5 | How it works | Bg Base → 2-col: sticky intro + CTA on the left, numbered step list with divider lines on the right |
| 6 | Tools | Bg Light → centred intro, then calculator (inputs left, dark result panel right; Code element for the JS), then 3 text links in columns |
| 7 | Broker | Portrait left; name, quote and a 2-col credentials list right |
| 8 | Case studies | Bg Light → table-style rows (title / situation / challenge / outcome). Use a Query Loop over a Case Studies CPT |
| 9 | Property report | Full-width magenta section → copy left, Bricks Form on a white panel right |
| 10 | FAQ | Heading left, Accordion (nestable) right |
| 11 | CTA band | Bg Base, centred |
| 12 | Footer | Footer template: 5-col grid + compliance block |

## Design rules (avoid list)

- No small uppercase labels above headings.
- Icons are SVG only, never emoji or text glyphs.
- Each section uses a different layout.
- Only one level of container: no cards inside cards.
- No bold phrases mid-sentence.
- Minimum text size is 15px, and secondary text uses `#46425f`.
- Paragraphs are capped at about 62 characters per line.
- Headings use a line height of at least 1.1.
- No decorative motion or floating shapes. The only movement is hover colour changes.
- Separate things with fills or divider lines, not a border plus a shadow on every box.
- No purple-to-blue gradients, no coloured strips on top of cards, no italic accent words, and step numbers only on real steps.

Class names follow BEM (`.block__element`) to suit Bricks' global class manager.

## 3. Content to confirm before publishing

- **FAQ answers.** All six answers are placeholders. They need to be written by the broker and compliance-reviewed.
- **Property report disclaimer.** It is still marked `[VERIFY]` (data source wording to be confirmed with the provider).
- **"5★ Google reviews".** The current site shows "5" next to stars. Confirm this is the star rating, not the review count.
- **New copy not on the current site:** the closing CTA heading "Find out what you can borrow, and how to structure it", and the "60+ Lender panel to compare" badge. Everything else is the existing wording.
- **Repayment estimator.** This is new. It uses the standard principal & interest formula and sits under the existing calculator disclaimer.
- **Links still set to `#`:** social profiles, LinkedIn and compliance pages. Point them at the real URLs.
- **Report form.** It only shows a thank-you message for now. Connect it to the Bricks form action or CRM.
