# PNW Trenchless homepage: Bricks + ACSS handoff

Design file: `index.html` (with `assets/trailer.jpg`). Open it in a browser to see the approved design.
Every value in the CSS is an ACSS-named variable, so the build is mostly entering values in ACSS and then building the HTML structure as Bricks elements.

**Design direction ("Surface / Underground"):** deep-ink sections stand for the ground the pipe runs through, and stone-white sections stand for the yard we leave intact. Headlines are set in wide Archivo, with the emotional words ("Keep the yard.") picked out in colour only (the Instrument Serif italic was dropped on the live site, 2026-11-09). The sewer-camera feed, with its amber footage readout, is the signature detail.

## 1. ACSS settings

| ACSS setting | Value | Used for |
|---|---|---|
| Primary | `#2F7A4B` (dark `#215936`, light `#6CC08A`, ultra-light `#E7F1EA`) | CTAs, accents. Use the light shade for green text on ink |
| Secondary | `#2B5BB5` (dark `#1F468F`, light `#9AB8F2`) | Water-line art, review avatars, the I-90 marker |
| Accent | `#F0B03A` (dark `#9A6200`) | Stars, camera readouts, focus ring |
| Base | `#0E1621` (dark `#090F17`, medium `#1A2533`, light `#2B3747`) | Ink sections, header, footer |
| Neutral | `#616B66` (medium `#A3ABA6`, light `#DCE1DB`, ultra-light `#F1F3EF`) | Stone sections, borders, muted text |
| Heading font | **Archivo** variable (`wdth` 62–125, weights 400–900). H1 `font-stretch:118%`, H2 112% | Headings |
| Body font | **Public Sans** 400–700, line height 1.65, base size 17px | Body text |
| H1 / H2 / H3 | `clamp(2.75rem…6rem)` / `clamp(2.1rem…3.75rem)` / `clamp(1.35rem…1.75rem)` | Fluid type scale |
| Content width | 80rem | `.container` |
| Section padding | `--section-space-m` = `clamp(4.5rem, 3rem + 6vw, 9rem)` | Every section |
| Radius | s 6px · default 12px · l 22px · buttons are pill-shaped | |

Paste these into **ACSS > Custom CSS (`:root`)**. ACSS has no equivalent for them. Every project variable uses the `--pnw-` prefix. This is what is on the staging site (2026-11-08):

```css
:root {
  --pnw-font-serif: "Instrument Serif", Georgia, "Times New Roman", serif; /* italic accent words */
  --pnw-font-mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace; /* eyebrows, labels, readouts */
  --pnw-header-h: 80px;
  --pnw-ease: cubic-bezier(.2, .7, .2, 1);
  --pnw-border: 1px solid var(--neutral-light);
  --pnw-border-dark: 1px solid color-mix(in srgb, var(--white) 10%, transparent);
  --pnw-shadow-primary: 0 10px 30px -12px color-mix(in srgb, var(--primary) 80%, transparent);
}
h1 { font-stretch: 118%; }
h2 { font-stretch: 112%; }
h3 { font-stretch: 108%; }
html { scroll-padding-top: calc(var(--pnw-header-h) + 16px); }
```

`index.html` still uses the old names. Rename them when copying rules out of it:

| Old name in `index.html` | Use in Bricks |
|---|---|
| `--serif-font-family` | `--pnw-font-serif` |
| `--mono-font-family` | `--pnw-font-mono` |
| `--header-h` | `--pnw-header-h` |
| `--ease` | `--pnw-ease` |

Fonts to load in Bricks > Custom Fonts (or self-host them):
- Archivo (variable, **including the width axis** `wdth` 62–125. The file currently on the staging site is weight-axis only, so `font-stretch` has no effect until it is replaced)
- Instrument Serif (italic)
- Public Sans
- JetBrains Mono

## 2. Global classes

Copy each rule set from the `<style>` block in `index.html` into a Bricks global class with the same name:

- **Layout:** `section`, `container`, `bg--ink`, `bg--ink-dark`, `bg--stone`, `bg--white`, `grain` (film-grain overlay on ink sections), `head`, `head--row`, `head__main`, `head__lede`
- **Type:** `eyebrow`, `serif` (wrap accent words in a span with this class), `tbc` (highlights content still to confirm; remove before launch)
- **Buttons:** `btn`, `btn--primary`, `btn--ghost`, `btn--ghost-light`, `btn--block`, `link-arrow`
- **Camera-feed motif:** `feed`, `feed--roots`, `feed--clean`, `feed--blue`, `feed__hud`, `feed__hud--top`, `feed__ft`, `feed__rec`, `feed__cross`, `feed__label`
- **Motion:** `rise`, `rise-2` … `rise-5` (hero load sequence, disabled automatically for reduced-motion users)

## 3. Section map

| Section (class) | Bricks build | Interaction / notes |
|---|---|---|
| Top bar + header `topbar`, `header` | **Header template**. Sticky with a glass blur. Nav Menu element, phone link, CTA button | Below 1200px the nav collapses to a toggle. Replace the logo stand-in with the final SVG |
| Hero `hero` | Section with a background image (trailer) and a gradient overlay. Content grid on the left, camera-feed card on the right, 3-item proof strip below | The footage counter ticks up (a small JS snippet in a Code element). Final photo: Mike and the rig on a job |
| Service ticker `ticker` | Section with 2 rows, each a Div track holding the same group twice (CSS `ticker` animation). Row 1: large service links (icon + name + spec chip such as CIPP / HDPE / CTS POLY / CCTV), every other name outlined. Row 2: moves the opposite way with tagline words and city names | Pauses on hover/focus, edges fade out. In the duplicate group, set `aria-hidden` and `tabindex="-1"` on its links |
| Stats `stats` | Block of 4 items with large numerals | |
| Warning signs `signs` | Two columns: sticky intro on the left, list of 6 rows on the right | Rows slide in on hover |
| Explainer `explain` + `xsec` | Text + photo card (client job photo; there is no video), then the **interactive cross-section** (inline SVG in a Code element) | The Traditional / Trenchless toggle switches the SVG and the 4 fact cells via a `data-mode` attribute (a few lines of JS) |
| Services `services` | Light **stone** section (`bg--stone`). `svc-grid` is a 2-column grid of 4 white `svc-card`s, each a dark inset art panel (inline SVG / camera feed) + spec label with colored dot, arrow button, H3 with a green serif accent word, description, "Best for" tag row. Below the grid sits a dark `svc-strip` CTA bar. Build with Div/Block cards, or a Query Loop over a Services CPT | The whole card is clickable (H3 link stretched), and each card sets its own `--card-accent`. 1 column below 860px. No JS. The comparison section that follows switched to `bg--white` so light sections alternate |
| Who we serve `audience` | White section, 3 `aud-card`s: Homeowners, Commercial properties, Industrial & municipal (icon, text, check list) | Copy based on the live site's "residential, commercial and industrial" positioning |
| Comparison `compare` | Table (Code element) with the trenchless column raised as a dark card | Scrolls horizontally on mobile |
| Decision flow `decide` / `flow` | Circular camera feed → dotted connector SVG → 3 outcome cards | Connector lines hidden on mobile |
| Process `steps` | `ol` with 5 steps. Outlined numerals come from a CSS counter | Becomes a vertical list below 1000px |
| Meet Mike `mike` | Portrait (placeholder) with a name plate, trailer inset photo, serif pull quote, credentials grid, signature line | |
| Projects `projects` | Featured **before/after slider** + 2 mini cards. Use a Query Loop of a Projects CPT (ACF fields: before still, after still, location, problem, method, duration) | The slider is a range input that clips the "after" image. Use a Code element or a before/after plugin |
| Reviews `reviews` | Rating card + horizontal scroll-snap row of reviews, then the warranty / financing pair | Feed it real Google reviews only |
| Service areas `areas` | Large city link list + dark map (inline SVG, roughly to scale with a 10-mile bar) | The Clayton pin pulses |
| FAQ `faq` | Sticky aside + **Bricks Accordion (nested)** using `faq__item` | Enable FAQPage schema |
| Estimate `estimate` | Big phone number, 3 next steps, **Fluent Form / GHL form** styled with the `form`, `field`, `chips` and `upload` classes | Issue-type chips replace the dropdown. The GA4/Ads conversion fires on submit |
| Footer `footer` | **Footer template** with a large outlined "TRENCHLESS" wordmark | |
| Mobile call bar `callbar` | Footer template, fixed, visible only below 700px | Adds bottom padding to `body` on mobile |

## 4. Content still needed before launch

Everything wrapped in `.tbc` is highlighted in amber in the design:

- Google rating and review count; 3 real reviews
- Warranty length and what it covers; financing partner (if offered)
- Typical job timeline; liner design life; founding year
- Quote from Mike; manufacturer certifications
- Real projects (before and after camera stills, location, method, duration)
- FAQ answers: drafts are written, and Mike needs to confirm or edit each one
- Price range wording; permit handling; whether camera inspections are offered as a standalone service
- Address or service-area setting; hours
- Photography: Mike and the rig on a live job (hero), Mike's portrait. No video: the client has none, so the explainer uses a job photo
- Final SVG logo

## 5. Pre-launch checks

- No hex codes or px values typed into Bricks style panels. Use the ACSS variables or classes above.
- Delete the `.tbc` class from every element once its content is final.
- Test on a real phone:
  - header menu
  - cross-section toggle
  - services tabs
  - before/after slider
  - FAQ accordion
  - form (the conversion fires)
  - mobile call bar

## 6. Content and assets taken from the live site (pnwtrenchless.com)

| Item | Where it's used |
|---|---|
| Logo (`assets/logo.png`, made from the site's `logo 1.png` with the black background removed) | Header and footer |
| Facebook: https://www.facebook.com/profile.php?id=61589495076554 | Top bar, quote section, footer |
| Email: info@pnwtrenchless.com · Call/Text 509-953-2036 · WA Reg. PNWTRT*744KQ | Top bar, quote section, footer |
| Services: Pipe bursting (HDPE, 50+ yr lifespan, can upsize), CIPP lining, Water line pulling (CTS poly, pressure/leak tested), Point repairs / localized relining | Service cards, ticker, decision flow, footer |
| Customer types: residential, commercial, industrial; "keep your property running"; evaluation through final testing and documentation | "Who we serve" section, hero, FAQ |
| Mission: "honest work, fair pricing, and results built to last", family-owned, 14+ years | Hero, About quote and bio |
| "Request a true and honest quote" | Quote section heading |
| Areas: Spokane, Spokane Valley, Deer Park, Clayton, Stevens County, Spokane County | Top bar, area list, footer |
| Real job photos (`assets/job-during.jpg`, `job-after.jpg`, `job-waterline.jpg`, from the contact page) | Projects section |

Images on the live site that were **not** used: the AI-generated trailer render, the YouTube-style bursting thumbnail and the stock "Pipe-lining.jpg". Their usage rights are unclear.

## 7. Quote form (directly above the footer)

Fields: service needed (chips), property type (Residential / Commercial / Industrial), name, phone, email, address, details, photo/video upload. There are also one-tap Call, Text, Email and Facebook buttons. Build it in Fluent Forms or GHL with the same fields and style it with the `form`, `field`, `chips` and `upload` classes.

## 8. What is built on staging (2026-11-08)

The build is generated from code in `wp-build/`: `classes.py` → `classes.json` (259 global classes), `elements.py` → `elements.json` (header, footer, 16 Home sections). `import.php` syncs both to the site through the Novamira Bricks abilities. Section-level names differ from section 2 above where the house conventions apply: `section--dark` / `--deep` / `--tint` / `--white` instead of `bg--ink` / `bg--stone`, `section__head`, `section__intro`, ACSS `btn--primary`, `btn--white btn--outline` and `btn--base btn--outline` instead of the custom `.btn` rules. Icons render through the Bricks SVG element from the media library. The cross-section toggle uses Bricks `setAttribute` interactions. Screenshots: `screenshots/bricks-staging/`.

## Service pages (built)

- **Services CPT:** ACF Pro post type `service`, URL base `/services/`, Bricks enabled for it.
- **Sewer Pipe Lining:** service post 464, `/services/sewer-pipe-lining/`, built natively from `service-sewer-pipe-lining.html` (13 sections, BEM classes in the PNW category). It uses the site-wide header and footer templates. Generated by `wp-build/elements_lining.py`, synced by `wp-build/import.php`.
- **Testimonials:** ACF post type `testimonial` with fields review_text, rating, city, source, source_url, review_date, services (relationship), featured and is_placeholder. 10 dummy posts ("Dummy Reviewer A–J", flagged `is_placeholder`) are for layout testing only; delete them before launch.
- **Review loops:** Home Reviews shows the 3 newest featured testimonials; each service page shows the 2 newest testimonials linked to it (Service mentioned field). The Reviews page (`/reviews/`, page 1165) lists every testimonial, newest first (up to 30). To change which reviews appear, edit the testimonial posts, not the page.
- **About (built 2026-11-09):** page 706, `/about/`, from the approved `about.html` (builder `wp-build/elements_about.py`). Menu and footer "About" links point to it.
- **Contact (built 2026-11-09):** page 785, `/contact/`, from the approved `contact.html` (builder `wp-build/elements_contact.py`). Menu and footer "Contact" links point to it.
- **Pipe Bursting (built 2026-11-09):** service post 842, `/services/pipe-bursting/`, from the approved `service-pipe-bursting.html` (builder `wp-build/elements_bursting.py`). Footer service links now go to the two service pages.
- **Projects (built 2026-11-09):** ACF post type `project` + field group "Project details"; `/projects/` page (1088) and the "Single: Project" template (1040) use Bricks query loops and dynamic data (builder `wp-build/elements_projects.py`). To add a project: Projects › Add New, fill the Card and Photos tabs (the rest is optional; empty fields stay hidden).

## Site-wide quote section (2026-11-09)

The "Request a quote" section with the Fluent form lives in the **footer template**, above the footer, and shows on every page except Contact (element condition: Post ID is not 785). Pages no longer have their own quote section. To change the quote section, edit the footer template; to hide it on another page, add that page ID to the condition.
