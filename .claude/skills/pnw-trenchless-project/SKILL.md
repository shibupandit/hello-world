---
name: pnw-trenchless-project
description: Project brief and working rules for the PNW Trenchless website (pnwtrenchless.com, Spokane WA trenchless sewer and water line contractor). Use whenever the task mentions PNW Trenchless, Mike Jeisma, pnwtrenchless.com, the trenchless homepage design, or continuing the Bricks + ACSS build of that site.
---

# PNW Trenchless — project brief

You are continuing an existing project. Read this whole file before doing anything, then read the files listed under "Source files".

## The client

- **Business:** PNW Trenchless, a family-owned trenchless sewer and water line contractor. Owner and lead technician: **Mike Jeisma**, with 14+ years in the trenchless industry. Based in Clayton, WA.
- **Services (exactly four):**
  1. **Pipe bursting:** a new HDPE pipe pulled in while the old one is burst outward. A completely new pipe with a 50+ year lifespan, and it can be upsized.
  2. **CIPP pipe lining:** a resin liner cured inside the old pipe. A seamless, jointless pipe within a pipe.
  3. **Water line pulling:** a new CTS poly line pulled underground, reconnected, and tested for pressure and leaks.
  4. **Point repairs / localized relining:** used when damage is isolated to one section.

  A CCTV camera inspection is the first step of every job. Their old site doesn't list it as a standalone service, so mark that as unconfirmed.
- **Customers:** residential, commercial and industrial (homes, businesses, industrial/municipal sites).
- **Service areas:** Spokane, Spokane Valley, Deer Park, Clayton, Stevens County, Spokane County.
- **Contact:**
  - Call/Text 509-953-2036
  - info@pnwtrenchless.com
  - Facebook https://www.facebook.com/profile.php?id=61589495076554
  - WA Contractor Reg. PNWTRT*744KQ
- **Their wording to reuse:**
  - "Less digging. Less disruption. Built to last."
  - "Request a true and honest quote"
  - "We treat every project like it's for our own family"
  - "honest work, fair pricing, and results built to last"
- **Brand colours** (from the logo and trailer wrap): pine green, royal/trailer blue, navy/charcoal ink, white.

## Design decisions (current state)

The approved direction is the **light and dark mix** design in `pnw-trenchless/index.html`:
- **Ink (navy) sections:** hero, service ticker, process, reviews, quote form, footer.
- **Stone/white sections:** stats, warning signs, explainer, services, who we serve, comparison, decision flow, about/Mike, projects, service areas, FAQ.
- **Type:** wide Archivo display headings, Instrument Serif italic accent words, Public Sans body, JetBrains Mono labels.
- **Signature motif:** sewer-camera "feed" frames with an amber footage readout.

Section order:
1. Top bar
2. Sticky header (real logo)
3. Hero: "Fix the pipe. *Keep the yard.*", with the trailer photo across the full width
4. Two-row service ticker
5. Stats
6. Warning signs
7. What-is-trenchless explainer with the interactive dig/trenchless cross-section
8. Services: **2-column light cards** on a stone background
9. Who we serve (Homeowners / Commercial / Industrial & municipal)
10. Comparison table
11. Decision flow ("the camera decides")
12. Process (5 steps)
13. About / Mike
14. Projects (real during/after photos)
15. Reviews and warranty/financing
16. Service areas with map
17. FAQ
18. **Quote form directly above the footer**
19. Footer

Mobile call bar.

## Feedback history (the user's taste)

- The first wireframe-faithful version was rejected as "robotic, boring". They wanted **premium**.
- **Services section:**
  1. The tabs version was rejected.
  2. The bento grid was rejected ("change again").
  3. The hover-reveal list was rejected.
  4. The user asked for **2-column grid cards on a light background**, and that is the current design.
- "Service scrolling section" = the ticker band under the hero. The user asked for it to be redesigned, and it's now a two-row ticker.
- A fully light "clean modern" version was built (git commit `6002f0f`). The user then asked to **reverse to the light and dark mix design**. Don't switch back to all-light unless asked.
- The user wants real client content pulled from the live site, a quote form before the footer, and full-page desktop screenshots when a design is finished.

## Hard rules

- **Do not push or publish to any WordPress site until the user names which site to use for PNW.**
- **Never use the whitecrowtemplate WordPress site/connector for PNW work.** It was studied read-only as a style reference only.
- Never invent reviews, ratings, warranty terms, prices, timelines or project details. Unknown facts stay as visible placeholders (class `tbc`, amber highlight), and FAQ drafts are marked "Draft · confirm with Mike".
- Do not use these images from the old site: the AI-generated trailer render, the YouTube-style pipe-bursting thumbnail, or the stock "Pipe-lining.jpg" (rights unclear).
- Commit and push work to the session's designated git branch. Do not open a pull request unless asked.
- Build target is **WordPress + Bricks Builder + Automatic.css (ACSS)**. Follow the `bricks-acss-build-conventions` skill when building.

## Still unknown (ask Mike / the user)

- Google rating, review count and real reviews
- Warranty length and coverage; financing
- Typical timeline; liner design life; price range; permits
- Hours and address
- Project locations and methods
- Manufacturer certifications
- Founding year (2025?)
- Mike's portrait and more job photos; final SVG logo

## Source files (in the git repo)

- `pnw-trenchless/index.html`: the approved design (open it in a browser). Assets are in `pnw-trenchless/assets/`:
  - `logo.png`: for dark backgrounds
  - `logo-dark.png`: for light backgrounds
  - `trailer.jpg`
  - `job-during.jpg`, `job-after.jpg`, `job-waterline.jpg`
- `pnw-trenchless/BRICKS-HANDOFF.md`: ACSS values, class list, section-by-section Bricks build, form fields, content sources.
- `pnw-trenchless/BUILD-CONVENTIONS.md`: conventions learned from the reference build.
- `pnw-trenchless/screenshots/`: desktop screenshots of the approved design.
- The original wireframe was a bundled HTML file ("PNW Trenchless Homepage Wireframe"), with 14 sections numbered 01–14.
