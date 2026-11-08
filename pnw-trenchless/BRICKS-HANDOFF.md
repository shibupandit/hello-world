# PNW Trenchless homepage: Bricks + ACSS handoff

Design file: `index.html` (with `assets/trailer.jpg`). Open it in a browser to see the approved design.
Every value in the CSS is an ACSS-named variable, so the build is mostly entering values in ACSS and then building the HTML structure as Bricks elements.

## 1. ACSS settings

Enter these in **ACSS Dashboard**. When ACSS generates shades automatically, check that they come out close to these values.

| ACSS setting | Value | Used for |
|---|---|---|
| Primary | `#2C6B3F` (dark `#1F4C2D`, light `#D7E8DB`, ultra-light `#EDF4EE`) | Main CTAs, checks, eyebrows (trailer green) |
| Secondary | `#2A4E9B` (dark `#1E3A78`, light `#DCE4F4`) | Links, process steps, warranty card (trailer blue) |
| Accent | `#E8A41C` (dark `#9A5F00`) | Stars, camera-feed readouts, focus ring |
| Base | `#22272C` (dark `#181B1F`, ultra-dark `#111316`, medium `#3A4148`) | Body text, dark bands, footer |
| Neutral | `#5B615C` (medium `#A9ADA4`, light `#D5D8D0`, ultra-light `#F3F4EF`) | Muted text, borders, page background |
| Heading font | **Archivo** (variable, `wdth` 62–125, weights 500–900). Headings use `font-stretch: 112%` | All headings |
| Body font | **Public Sans** 400/500/600/700 | Body text |
| Root font size | 16px. Body line height 1.6. Headings line height 1.08 | |
| Content width | 76rem (1216px) | `.container` |
| Section padding | `--section-space-m` ≈ 56 → 104px fluid | Every section |
| Radius | s 4px · default 8px · l 14px | Inputs · buttons/cards · large cards |

Paste these into **ACSS > Custom CSS (`:root`)**. ACSS has no equivalent for them:

```css
:root {
  --mono-font-family: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
  --feed-bg: radial-gradient(circle at 50% 50%, #0B0D0F 0 9%, #1A1F1B 10% 22%, #2A302A 23% 34%, #3D433A 35% 46%, #262B27 47% 64%, #15181A 65%);
  --header-h: 76px;
}
```

Load JetBrains Mono 500/700 (eyebrows, labels and footage readouts), Archivo and Public Sans through Bricks > Custom Fonts, or self-host them.

## 2. Global classes to create in Bricks

Copy each rule set from the `<style>` block in `index.html` into a Bricks global class with the same name:

- **Layout:** `section`, `container`, `bg--white`, `bg--yard`, `bg--base`, `bg--base-dark`, `border-block`, `section-head`, `section-head--split`, `section-head__lede`
- **Type:** `eyebrow`, `tbc` (highlights content still to confirm; remove before launch)
- **Buttons:** `btn`, `btn--primary`, `btn--outline`, `btn--light`, `btn--block`, `link-arrow`. If the ACSS button classes already match, use those instead.
- **Camera-feed motif:** `feed`, `feed__hud`, `feed__hud--top`, `feed__ft`, `feed__rec`, `feed__label`, `feed--after`, `feed--water`

Every other class is component-scoped (BEM). Create it on the component it belongs to.

## 3. Section map (Bricks element tree)

| # | Section (class) | Bricks structure | Notes |
|---|---|---|---|
| – | Top bar `topbar` | Header template › Div › 2× Text | Goes in the Bricks **Header template** |
| – | Header `header` | Header template › Container › Logo (Image/SVG), Nav Menu, phone link, Button | Sticky. Below 1200px the nav collapses to the Bricks mobile-menu toggle. Replace the logo stand-in with the final SVG |
| 01 | Hero `hero` | Section › Container › Block `hero__grid` (2 columns) › content Block + Image. Below it, Block `trustbar` › 4 icon items | The badge over the photo is a `feed` Div positioned absolutely |
| 02 | Signs `signs` | Section › Container › `section-head` + Block `signs__grid` (3 columns, 2 below 860px, 1 below 540px) › 6× `sign-card` + CTA strip | Icons are inline SVG. Use the Bricks Icon element |
| 03 | Trenchless explainer `explain` | Section › Block `explain__grid` › Video (YouTube/self-host) + text + `diagram` (Code or SVG element) | The diagram SVG sits inside a horizontal-scroll wrapper on mobile |
| 04 | Services `services` | Section › `services__grid` (4 columns, 2, then 1) › 4× `service-card` | Each card links to its own service page. Swap the SVG art for real photos when they exist |
| 05 | Comparison `compare` | Section `bg--base` › table (Code element, or the Bricks Table element) + `compare__note` | Keep the `overflow-x:auto` wrapper |
| 06 | Decision guide `decide` | Section › `decide__grid` › 3× `decide-card` | |
| 07 | Process `process` | Section › `ol.process__list` › 5× `li.process-step` | Step numbers come from a CSS counter. Becomes a vertical timeline below 980px |
| 08 | Meet Mike `mike` | Section › `mike__grid` › photo grid + content (quote, `creds` list) | |
| 09 | Projects `projects` | Section › `projects__grid` › **Query Loop** of a Projects CPT (ACF: before/after still, location, problem, method, duration) | Each card is a `project-card`. Before/after images replace the `feed` placeholders |
| 10–11 | Reviews + warranty/financing `reviews` | Section › head with rating summary › `reviews__grid` (Query Loop or GBP feed) › `assure__grid` 2 cards | Use real Google reviews only |
| 12 | Service areas `areas` | Section › `areas__grid` › text + city link grid + map | The map is a static SVG (in the file) or a Leaflet map |
| 13 | FAQ `faq` | Section › `faq__grid` › sticky aside + **Bricks Accordion (nested)** using `faq__item` | Turn on FAQPage schema in the accordion settings or with Rank Math |
| 14 | Estimate `estimate` | Section `bg--base` › `estimate__grid` › text + **Fluent Form / GHL form** styled with `form` classes | Form goes to GHL. The GA4/Ads conversion fires on submit |
| – | Footer `footer` | Footer template | |
| – | Mobile call bar `callbar` | Footer template › Div (fixed, visible only below 700px) | Adds 4.5rem of bottom padding to `body` on mobile |

## 4. Content still needed before launch

Everything wrapped in `.tbc` is highlighted in the design so it can't be missed:

- Google rating and review count; 3 real reviews
- Warranty length and what it covers; financing partner (if offered)
- Typical job timeline; liner design life
- Founding year; quote from Mike; manufacturer certifications
- 3 real projects (before and after camera stills, location, method, duration)
- FAQ answers: drafts are written, and Mike needs to confirm or edit each one
- Price range wording; permit handling; whether camera inspections are offered as a standalone service
- Business address or service-area setting; hours
- Photography: Mike and the rig on a live job (hero), Mike's portrait, wrapped truck, service photos, a 60–90s explainer video
- Final SVG logo

## 5. Pre-launch checks

- No hex codes or px values typed into Bricks style panels. Use the ACSS variables or classes above.
- Delete the `.tbc` class from every element once its content is final.
- Test the header's mobile menu, the FAQ accordion, the form (the conversion fires) and the mobile call bar on a real phone.
