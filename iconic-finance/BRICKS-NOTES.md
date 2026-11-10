# Iconic Finance homepage redesign — Bricks + ACSS build notes

`index.html` is a static prototype of the new homepage. `hero-a.html` keeps the earlier navy hero for comparison; it did not receive the latest polish pass. Open it in a browser; it needs no build step.
Images are hot-linked from the current site, so download them into the new Media Library during the build.

## 1. ACSS settings (Automatic.css dashboard)

| ACSS setting | Value |
|---|---|
| Primary | `#a71e5b` (brand magenta) |
| Secondary | `#a8863f` (logo gold). Use the dark shade `#7a5f24` for small gold text on light backgrounds (AA contrast) |
| Base | `#1e1a45` (deep navy) |
| Neutral / body background | `#faf8f5`, alt section `#f1ede7` |
| Heading font | Jost 500 (tracking -0.03em display, -0.02em h2, -0.01em h3) |
| Text font | IBM Plex Sans 400/500/600, tabular numerals for figures |
| Content width | 1240px |
| Section padding (M) | `clamp(4.5rem, 9vw, 7.5rem)` |
| Radius | 14px (cards), 24px (large cards) |

All custom properties in the prototype's `:root` use ACSS names (`--primary`, `--space-m`, `--section-space-m`, etc.), so the CSS ports over largely unchanged.

## 2. Section → Bricks structure (top to bottom)

| # | Section | Bricks build |
|---|---|---|
| 1 | Header | Header template: Logo, Nav Menu (nested, with dropdowns), phone link (44px target), Button. Sticky. |
| 2 | Hero | Light section → 2-col: headline, lead and a 2×2 "What brings you here?" link list; Nicolette portrait with name, role and a call link |
| 3 | Proof bar | Navy strip: one line of figures and credentials (no big-number tiles) |
| 4 | Who we help | Heading row → 5 editorial rows (title / description / link) separated by rules. Query Loop over a Services CPT |
| 5 | How it works | Bg Base → 2-col: sticky intro + CTA left, numbered step list right |
| 5b | Lenders | White section → 2-col: intro + link left, 2×2 lender types right, panel note below |
| 6 | Tools | Bg Light → centred intro, calculator (Code element for JS) with dark result panel, then 3 text links in columns |
| 7 | Broker | Quote-led: large quote with attribution left, credentials list right (no second portrait) |
| 8 | Case studies | Bg Light → table-style rows. Query Loop over a Case Studies CPT |
| 8b | Reviews | White section → three client quotes in columns divided by rules |
| 9 | Property report | Full-width magenta → copy left, Bricks Form right with visible labels |
| 10 | FAQ | Heading left, Accordion (nestable) right |
| 11 | CTA band | Bg Base, centred |
| 12 | Footer | Footer template: 5-col grid + compliance block; column titles are h2 for correct outline |

## Accessibility requirements carried into the build

- **Form labels:** every field has a visible label. No field relies on placeholder text alone.
- **Tap targets:** at least 44px for the phone link, social icons, sliders and buttons.
- **Keyboard:** the Esc key closes the mobile menu and dropdowns. Focus rings are gold.
- **Sticky header:** anchor targets use `scroll-margin-top` so the header doesn't cover them.
- **Form submit:** the button changes to "Sending…" and is disabled while sending, then a success message is announced to screen readers.
- **Capitalisation:** sentence case for all navigation and labels.

Class names follow BEM (`.block__element`) to suit Bricks' global class manager.

## 3. Content to confirm before publishing

- **FAQ answers.** All six answers are placeholders. They need to be written by the broker and compliance-reviewed.
- **Property report disclaimer.** It is still marked `[VERIFY]` (data source wording to be confirmed with the provider).
- **"5★ Google reviews".** The current site shows "5" next to stars. Confirm this is the star rating, not the review count.
- **New copy not on the current site:** the closing CTA heading "Find out what you can borrow, and how to structure it", and the "60+ Lender panel to compare" badge. Everything else is the existing wording.
- **Repayment estimator.** This is new. It uses the standard principal & interest formula and sits under the existing calculator disclaimer.
- **Links still set to `#`:** social profiles, LinkedIn and compliance pages. Point them at the real URLs.
- **Report form.** It only shows a thank-you message for now. Connect it to the Bricks form action or CRM.

See `SITE-REVIEW.md` for the full-site findings and the list of sign-offs still needed.
