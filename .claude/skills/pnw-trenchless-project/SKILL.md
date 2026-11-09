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

- **The only WordPress site for PNW is the one the user named: Novamira connector `novamira-shibunew-com-us` (https://shibunew-com.us.stackstaging.com, staging).** Don't write to any other site.
- **Never use the whitecrowtemplate WordPress site/connector for PNW work.** It was studied read-only as a style reference only.
- Never invent reviews, ratings, warranty terms, prices, timelines or project details. Unknown facts stay as visible placeholders (class `tbc`, amber highlight), and FAQ drafts are marked "Draft · confirm with Mike".
- Do not use these images from the old site: the AI-generated trailer render, the YouTube-style pipe-bursting thumbnail, or the stock "Pipe-lining.jpg" (rights unclear).
- Commit and push work to the session's designated git branch. Do not open a pull request unless asked.
- Build target is **WordPress + Bricks Builder + Automatic.css (ACSS)**. Follow the `bricks-acss-build-conventions` skill when building.
- **Use Automatic.css framework variables and classes only** for colour, margin, padding, spacing, gaps, grids and buttons:
  - **Colour:** only ACSS colour variables (`var(--primary)`, `--primary-dark`, `--base`, `--base-medium`, `--neutral-ultra-light`, `--accent`, `--text-dark`, `--text-light-muted`, the `-trans-*` variants…). No hex, rgb or hsl in Bricks.
  - **Margin, padding, spacing:** only `var(--space-xs…xxl)`, `var(--section-space-*)`, `var(--gutter)` / `--section-padding-x`, `var(--content-gap)` / `--container-gap`. No px or rem values.
  - **Gaps:** `var(--grid-gap)`, `var(--content-gap)`, `var(--container-gap)`, `var(--space-*)`.
  - **Grids:** ACSS grid classes and variables first (`grid--2`, `grid--3`, `grid--auto-*`, breakpoint variants like `grid--m-1`, the `--grid-*` variables), custom grid CSS only if those can't do it.
  - **Buttons:** only the native Bricks Button element with ACSS `btn--` classes (`btn--primary`, `btn--outline`, `btn--white`, `btn--white-outline` / `btn--primary-outline`, sizes `btn--s/m/l`). No custom `.btn` rules.
  - Custom values only where ACSS has nothing for the job: the `--pnw-` variables in ACSS custom CSS (fonts, ease, header height, borders, primary shadow), pseudo-elements and the camera-feed motif. Even there, build them from ACSS variables (e.g. `color-mix()`).

## Build site and progress

- **Site:** Novamira connector `novamira-shibunew-com-us`, https://shibunew-com.us.stackstaging.com (staging). Named by the user on 2026-11-08. whitecrowtemplate stays off-limits.
- **Starting state (previous session):** Bricks 2.4.2 child theme (licence valid), Automatic.css 3.3.6, Novamira + Novamira Pro. No pages, templates, theme styles or Novamira memories. ACF Pro, Fluent Forms, HappyFiles and Perfmatters were not installed.
- **Verified 2026-11-08 (read-only):** WordPress 7.1.4, PHP 8.4. Active plugins are now **ACF Pro 6.8.11, Automatic.css 3.3.8, HappyFiles Pro 1.9.1**, Novamira 1.12.15 and Novamira Pro 1.13.3. Still no Bricks templates or theme styles, no Novamira memories. The only page is the default draft "Privacy Policy".
- **Plugins still missing:** **Fluent Forms (+ Pro)** and **Perfmatters**. The quote form can't be built the conventional way until Fluent Forms is installed. Ask the user before working around it.
- **ACSS configured (2026-11-08):** settings saved through `Automatic_CSS\Model\Database_Settings::get_instance()->save_settings()` so the CSS regenerated. **Previous settings are backed up in the WP option `pnw_acss_settings_backup_20261108`.**
  - Colours: primary #2F7A4B, secondary #2B5BB5, accent #F0B03A, base #0E1621, neutral #616B66, every shade from the handoff, medium shade on.
  - Text colours: text-dark #111A16, text-dark-muted #4B5550, text-light #F3F5F2, text-light-muted #A8B3BF.
  - Type: Archivo headings, Public Sans body. H1 2.75→6rem, H2 2.1→3.75rem, H3 1.35→1.75rem, H4 1.15rem, body 17px / 1.65.
  - Spacing: space-m 1→1.5rem, section-space-m 4.5→9rem, gutter 1→3rem, content width 80rem. Radius 12px.
  - Shadows m and l from the design. Buttons pill-shaped, weight 700. Focus ring amber.
  - Backgrounds: `bg-ultra-dark` = `var(--base)` (ink), `bg-ultra-light` = `var(--neutral-ultra-light)` (stone).
- **Project variables (`--pnw-` prefix), in ACSS > Custom CSS (`custom-global-css`):** `--pnw-font-serif`, `--pnw-font-mono`, `--pnw-header-h`, `--pnw-ease`, `--pnw-border`, `--pnw-border-dark`, `--pnw-shadow-primary`, plus `font-stretch` on h1 (118%), h2 (112%), h3 (108%), `scroll-padding-top` and font smoothing. They live in ACSS custom CSS rather than the theme style because no theme style exists yet. These replace the handoff's old `--serif-font-family`, `--mono-font-family`, `--header-h`, `--ease`. Use only the `--pnw-` names.
- **Fonts:** Archivo, Public Sans, Instrument Serif, JetBrains Mono uploaded by the user through the Bricks font manager (`bricks_fonts` posts 19, 26, 33, 38; all published, woff2). **Archivo is a variable font on the weight axis only (`wght` 100–900, checked with fontTools). It has no `wdth` axis, so the `font-stretch` rules on h1/h2/h3 currently do nothing.** The wide headings need the Archivo file with the width axis (`wdth` 62–125) uploaded in its place. Google Fonts are not yet disabled in Bricks settings.
- **User decisions (2026-11-08):** "all google fonts are already uploaded to wordpress, fluent form - skip for now.. use dummy style form".
  - Fonts: use the self-hosted Bricks fonts. Don't block on Archivo's missing width axis. Build the headings as they are, and the wide stretch arrives when a variable Archivo file with the `wdth` axis is uploaded.
  - Quote form: no Fluent Forms for now. Build a styled dummy form (native Bricks elements or the Bricks Form element) with the design's fields: service chips, property type, name, phone, email, address, details, upload. Style it with `form` / `field` / `chips` / `upload` using ACSS variables only, and make it easy to swap for Fluent Forms later.
- **Build status (2026-11-08, user said "start now", build without stopping):** stages 1–4 done on staging.
  - Theme style `PNW Trenchless` (id `ts-8paif5`, condition: entire site). Google Fonts disabled in Bricks.
  - ACSS had been regenerated without the Bricks platform flag (empty `automatic-bricks.css`, no `btn--` classes). Rebuilt with it; base (ink) buttons enabled. Second backup: `pnw_acss_settings_backup_20261108b`.
  - Media: logos, trailer, 3 job photos, 37 SVG icons/illustrations (`pnw-trenchless/wp-assets/svg/`), in HappyFiles folders. IDs stored in WP option `pnw_media_ids`.
  - 259 BEM global classes, category `PNW`, ACSS variables only. Source: `pnw-trenchless/wp-build/classes.py`.
  - Header template 101, footer template 102 (entire site). The nav is the native **Nav (Nestable)** element (`nav-nested`, mobile below 1200px). Its links live in `NAV_LINKS` in `elements.py` (the WP menu `PNW Main`, id 10, is no longer used). The mobile menu is a full-width drop-down under the sticky header, as in the design (user correction 2026-11-08: not a side panel). The header toggle morphs to the X in place, the area below the panel dims and closes the menu on tap, and the links rise in with a stagger, with an arrow on hover/active. Below the links: phone, Get a Quote, email/Facebook and the service-area line. It starts below the WP admin bar. The toggles match the 44px phone button. Bricks handles the scroll lock, focus trap, Esc, outside tap and anchor-link close. The call bar hides while the menu is open. Home = page 94 (front page), 16 sections. Source: `pnw-trenchless/wp-build/elements.py`.
  - Re-sync everything with `pnw-trenchless/wp-build/import.php` (run through execute-php with `$sha` = a pushed commit). It rebuilds the Home page, so manual Bricks edits to page 94 / templates 101–102 are overwritten: change the generators instead, or stop using the script.
  - Final screenshots: `pnw-trenchless/screenshots/bricks-staging/`.
  - Full design-vs-build audit (2026-11-08): `pnw-trenchless/AUDIT.md`, side-by-sides in `pnw-trenchless/screenshots/audit/`. Container width comes from the theme style `container` group (the root-container setting doesn't reach containers inside sections).
- **Known differences from the design / open items:**
  - Archivo has no width axis yet, so headings are not stretched wide.
  - Quote form is a styled dummy (no inputs submit). Swap for Fluent Forms later, keep the `form` wrapper class.
  - Not built (would need a code element, needs explicit user OK): hero footage counter animation.
  - FAQ schema is off until Mike confirms the draft answers. Service and city links point to `#estimate` / anchors until those pages exist.
  - Repeating content (services, projects, reviews, areas) is static, not CPT + Query Loop yet. ACF Pro is now available for that.

## Service pages

- **Sewer Pipe Lining (CIPP)** — design `pnw-trenchless/service-sewer-pipe-lining.html` (2026-11-09), redesigned from the user's wireframe "Service page · Sewer Pipe Lining" (13 sections: hero + byline, quick answer + facts, is lining right, process diagram + 6 steps, before/after camera stills (no video), specs, cost, Mike, lining projects, reviews, FAQ, related + near you, quote form). Built in the homepage system (same tokens, header, footer). Source pieces: `pnw-trenchless/src/lining-main.html` + `src/lining.css`. All bracketed wireframe values are `tbc`; FAQ answers taken from the homepage drafts are marked "Draft · Mike to confirm". **Status: approved and built (2026-11-09)** as a native Bricks page in the `service` post type: post 464, https://shibunew-com.us.stackstaging.com/services/sewer-pipe-lining/. Uses the site-wide header (101) and footer (102) templates; no page-level header/footer.
- **Services CPT:** ACF Pro post type `service` (ACF post 443), archive and rewrite slug `services`, REST on, supports title/editor/thumbnail/excerpt/revisions/custom-fields. Bricks is enabled for `page` + `service` (Bricks › Settings › Post types).
- **Build:** `wp-build/elements_lining.py` returns the page (13 sections) into `elements.json` → `pages`; `import.php` finds the post by slug + post type (creates it if missing), clears it, inserts each section and runs a render test. Next service pages: add an `elements_<slug>.py` and append it in `elements.py` `build()`.

- **About / Meet Mike** — design `pnw-trenchless/about.html` (2026-11-09), redesigned from the user's wireframe "About page · Meet Mike" (9 sections: hero + portrait, numbers, story + career timeline, how we work (6 promises), equipment, credentials (block `verify`; `.creds` is taken by the homepage), local & family, reviews that mention Mike, conversion form with `source = About`). Built with `python3 src/build_about.py` from the service page shell + `src/about-main.html` + `src/about.css` (it reuses the service-page blocks). AboutPage + Person JSON-LD. Unknowns are `tbc` (career years, past employer name, job/footage counts, review count, equipment brands, bond/insurance, certifications, memberships, family detail, photos). Address shown as North Spokane County (wireframe said Clayton). **Status: approved and built (2026-11-09)** as WordPress page 706, https://shibunew-com.us.stackstaging.com/about/ (builder `wp-build/elements_about.py`, 9 sections, element IDs `a0…a8`). Uses the site-wide header/footer, Website Settings fields (address, phone, rating, review count, with conditions), the Testimonials loop (3 newest; there is no "mentions Mike" filter yet) and the Fluent quote form. Mountain art `art-local-mountains.svg` = media 689. The menu "About", footer "About", Home "Read Mike's full story" and the lining page "About Mike" links now go to `/about/`.

- **Contact** — design `pnw-trenchless/contact.html` (2026-11-09, no wireframe; designed in the site system). 5 sections: hero with ways to reach Mike (call, text a photo, email, Facebook; hours `tbc`), quote form (same fields as Fluent #3) + "what happens next" + info card (based in North Spokane County, hours/reply time `tbc`, WA Reg.), urgent "Sewer backing up right now?" strip (after-hours availability `tbc`), service area (city list + map, no "home base" label), contact FAQ (free estimate / reply time drafts). ContactPage JSON-LD. Built with `python3 src/build_contact.py`. **Status: waiting for the user's approval. Do not build it in Bricks until they say so.**

## Testimonials CPT

- ACF Pro post type `testimonial` (ACF post 545): not public (no single pages or archive), shown in admin and REST, menu icon star. Title = reviewer name.
- Field group `group_pnw_testimonial` (ACF post 546): `review_text` (textarea, required), `rating` (1–5, default 5), `city`, `source` (google / facebook / direct, returns label e.g. "Google review"), `source_url`, `review_date` (Ymd), `services` (relationship to `service`, returns IDs; service pages filter by it), `featured` (show on home), `is_placeholder` (dummy flag).
- **10 dummy reviews** (posts 556–565, "Dummy Reviewer A–J", text starts "Dummy review text.", `is_placeholder` on), added at the user's request (2026-11-09) to test layouts. A, B and C are featured; A, C, E, G and J are linked to Sewer Pipe Lining. **They are not real reviews: delete all `is_placeholder` testimonials before launch** and replace them with real Google reviews.
- **Review cards are Bricks query loops** (`review_loop()` in `wp-build/elements.py`): one `review` figure with `hasLoop` over `testimonial`, filled by `{acf_review_text}`, `{post_title}`, `{acf_city} · {acf_source}`; stars carry `data-rating="{acf_rating}"` (the `stars` class dims 1–4 star ratings); the avatar letter is the first letter of the name via `review__initial::first-letter`. Home: 3 newest with `featured` = 1. Service pages: 2 newest whose `services` field contains the page (`LIKE '"__POST_ID__"'`, which `import.php` replaces with the post ID). The Google average/count block stays `tbc`.

## Website Settings (ACF options page)

- Options page `website-settings` ("Website Settings" in the WP admin menu, ACF post 615), values stored in the default `options` store. Field group `group_pnw_site_settings` (ACF post 616).
- Fields (Bricks dynamic data `{acf_<name>}`): `site_phone` (= 509-953-2036), `site_email` (= info@pnwtrenchless.com), `site_address` (= "North Spokane County", set by the user 2026-11-09), `site_hours`, `site_google_url`, `site_google_rating` (0–5, step 0.1; = 4.9, set by the user 2026-11-09 as a temporary value: confirm against Google before launch), `site_google_review_count`, `site_google_map_iframe` (raw embed code).
- Hours, Google URL, review count and map embed are empty until the client confirms them. Never fill the rating or count with made-up numbers.
- **Wired into the build (2026-11-09)** through Bricks dynamic data (constants at the top of `wp-build/elements.py`: `PHONE`, `TEL`, `SMS`, `MAIL`, `EMAIL`, `ADDRESS`, `RATING`, `REVIEWS`, `GOOGLE_URL`, `HOURS`, `MAP_IFRAME`). Phone and email everywhere (top bar, header, mobile menu, hero, estimate, footer, call bar, lining page), call/text/mail links (`tel:{acf_site_phone}` etc.), address in the footer, Mike's plate and creds, and the lining page's "Family-owned" badge; hours in the footer; rating in the hero chip and the reviews box; review count line; "Read them on Google" link; the Google map embed replaces the illustrated service-area map when filled in.
- Empty values are hidden with Bricks element conditions (`when()` helper in `elements.py`). Rating empty → reviews box falls back to the `tbc` "X.X"; review count empty → "Average Google rating".
- Service-area city lists (Clayton etc.), the map illustration's labels and the "Est. 2025" year stay static.
- **Page cache:** StackCache (host) only purges a post's own URL. The mu-plugin `wp-content/mu-plugins/pnw-cache-purge.php` (source `wp-build/mu-plugins/pnw-cache-purge.php`) purges everything when Website Settings, a testimonial or a service is saved, trashed or deleted.

## Quote form (Fluent Forms)

- Fluent Forms (free, 6.2.17) installed from wordpress.org on 2026-11-09. Form **#3 "Request a quote"**: service (radio chips: Sewer line repair, Pipe lining, Pipe bursting, Water line, Camera inspection, Not sure yet; required), property type (radio chips), name + phone (required, `ff-half`), email + address (`ff-half`), details textarea, a photo tip (custom HTML), submit "Request My Quote" with the ACSS `btn--primary` class. Same-page confirmation, form hidden after submit. Fluent stores the page URL with each entry, so there is no hidden source field.
- In Bricks the `estimate()` section embeds it with a **Shortcode** element (`[fluentform id="3"]`, constant `QUOTE_FORM_ID` in `elements.py`) carrying the class `form__fluent`, inside the white `form` card (title, "Takes about a minute", fine print stay as Bricks elements).
- `form__fluent` restyles Fluent's markup with ACSS variables (labels, inputs, radio chips with `:has(input:checked)`, error text, tip box, submit using ACSS `--btn-*` variables plus an arrow, success message) and maps Fluent's `--fluentform-primary/-danger/-border-color` to ACSS colours. The dummy-form classes (chips, chip-option, form__row, form__field*, form__sep, upload) were deleted.
- Not done yet: **file upload** needs Fluent Forms Pro; email notification recipients and the GoHighLevel / GA4 hookup still to set up.

## Still unknown (ask Mike / the user)

- Google rating, review count and real reviews
- Warranty length and coverage; financing
- Typical timeline; liner design life; price range; permits
- Hours and address
- Project locations and methods
- Manufacturer certifications
- Founding year (2025?)
- Mike's portrait and more job photos; final SVG logo
- **No video exists for this client** (user, 2026-11-08). Don't design video placeholders; use photos (the client's own first). Stock, if ever needed, must be free-licence, captioned neutrally, marked "replace with PNW job photo", and logged in `pnw-trenchless/IMAGE-CREDITS.md`.

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
