# PNW Trenchless homepage: Bricks + ACSS handoff

Design file: `index.html` and the `assets/` folder. Open `index.html` in a browser to see the design, and use `screenshots/` for a quick look.
Every value in the CSS is an ACSS-named variable. The build is mostly entering the values below in ACSS, then building each section from Bricks elements with the listed classes.

**Direction: clean / modern / premium.**
- White and soft-stone sections with generous spacing.
- One typeface (Geist).
- Rounded photography and soft cards.
- Brand green carries every action.
- Navy appears only in the quote section and footer.

## 1. ACSS settings

| ACSS setting | Value | Used for |
|---|---|---|
| Primary | `#2F7A4B` (dark `#215936`, light `#7CC796`, ultra-light `#EBF4EE`) | Buttons, links, icons, eyebrow pills |
| Secondary | `#1F4FB0` (ultra-light `#EAF0FA`) | Logo blue: water-line art, review avatars |
| Accent | `#E3A42B` (ultra-light `#FBF3E2`) | Stars, the "honest note" box, `.tbc` highlights |
| Base | `#0E1621` (dark `#0A111A`) | Quote section, footer |
| Neutral | `#5D6761` (light `#E5E8E3` borders, ultra-light `#F5F6F3` soft sections) | Muted text, borders, soft backgrounds |
| Text | `#0F1A14` dark, `#56605A` muted | |
| Heading + body font | **Geist** 400/500/600/700. Headings weight 600, letter-spacing −0.035 to −0.04em | Everything |
| Mono font (custom) | **Geist Mono** 500 | Small service tags only |
| H1 / H2 / H3 | `clamp(2.5rem…4.5rem)` / `clamp(2rem…3.25rem)` / `clamp(1.25rem…1.5rem)` | |
| Body | 17px, line height 1.65 | |
| Content width | 76rem | `.container` |
| Section padding | `clamp(4.5rem, 3.25rem + 5vw, 8rem)` | Every section |
| Radius | 8 / 14 / 24 / 32px, buttons are pill-shaped | Inputs / chips / cards / large cards and photos |
| Shadows | s: `0 1px 2px rgb(15 26 20/.05)`; m: `+ 0 12px 32px -12px rgb(15 26 20/.14)`; l: `+ 0 30px 60px -24px rgb(15 26 20/.22)` | Cards on hover, floating cards, form |

Custom variables for **ACSS > Custom CSS**: `--mono-font-family`, `--header-h: 76px`, `--ease: cubic-bezier(.2,.7,.2,1)`.

## 2. Global classes

- **Layout:** `section`, `container`, `bg--white`, `bg--soft`, `bg--navy`, `head`, `head--center`, `head--row`, `lede`
- **UI:** `eyebrow` (pill label with a dot), `btn`, `btn--primary`, `btn--outline`, `btn--block`, `link`, `checks`, `float-card`, `tbc` (content to confirm; remove before launch)
- **Motion:** `fade-up` (`--2`, `--3`, `--4`), for the hero only

## 3. Section map (top to bottom)

| Section | Background | Bricks build | Notes |
|---|---|---|---|
| Top bar | soft | Header template: service areas, email, Facebook | |
| Header | white, sticky with blur | Logo (`assets/logo-dark.png`), Nav Menu, phone link, "Get a Quote" button | Mobile menu below 1100px |
| Hero | white | 2 columns: eyebrow, H1 (green second line), lede, 2 buttons, trust row; rounded trailer photo with 2 `float-card`s. Below: 4 `stat` tiles | |
| Services `#services` | soft | 2×2 `svc-card` grid: tinted art panel (inline SVG), service tag, H3 link (stretched so the whole card is clickable), text, tag chips, arrow button. Then a `svc-note` bar | Query Loop over a Services CPT works well |
| Who we serve `#who` | white | Centered head + 3 `aud-card`s (Homeowners, Commercial, Industrial & municipal) | |
| Warning signs | white | Sticky intro + 2×3 grid of `sign` tiles | |
| Why trenchless `#why` | soft | Interactive cross-section (`xsec`, inline SVG + toggle) + comparison table + `note` | The toggle needs a few lines of JS (Code element) |
| How it works `#process` | white | 5 numbered `step`s connected by a line | Becomes a vertical list on mobile |
| Projects `#projects` | white | During/after photo pair + `proj__info` panel with `spec` list and a water-line `proj__mini` link | Real photos from the client |
| About `#about` | soft | Photo with a "Family-owned" `float-card` + H2, bio, `quote`, `checks` | Swap in Mike's portrait when available |
| Reviews `#reviews` | soft | Rating pill + 3 `review` cards + warranty/financing `assure` cards | Real Google reviews only |
| Service areas `#areas` | white | Text, area `pills`, light map (inline SVG) | |
| FAQ `#faq` | soft | Sticky aside + Bricks Accordion (nested) styled as `faq__item` cards | Enable FAQPage schema |
| **Quote form** `#quote` | **navy** | Text, big phone number, 4 contact `ways` (Text, Email, Facebook, Call) + white `form` card | Directly above the footer. Fluent Forms or GHL |
| Footer | navy dark | Logo (`assets/logo.png`), contact, socials, 3 link columns | |
| Mobile call bar | white | Fixed bar below 700px: Call/Text + Get a Quote | |

## 4. Quote form fields

- **What do you need?** (chips): Sewer line repair, Pipe bursting, CIPP lining, Water line, Point repair, Not sure yet
- **Property type** (chips): Residential, Commercial, Industrial
- **Fields:** Name, Phone, Email, Property address or city, Details (optional), Photo/video upload (optional)
- **Submit:** "Request my quote". The form goes to GHL, and the GA4/Ads conversion fires on submit.

## 5. Content taken from the live site (pnwtrenchless.com)

| Item | Where it's used |
|---|---|
| Logo. `assets/logo.png` is for dark backgrounds; `assets/logo-dark.png` recolors the white parts to navy for light backgrounds | Footer / header |
| Facebook: https://www.facebook.com/profile.php?id=61589495076554 · info@pnwtrenchless.com · 509-953-2036 · WA Reg. PNWTRT*744KQ | Top bar, quote section, footer |
| Services: pipe bursting (HDPE, 50+ yr lifespan, upsizing), CIPP lining, water line pulling (CTS poly, pressure/leak tested), point repairs / localized relining | Services, form, footer |
| Customer types: residential, commercial, industrial | Hero, Who we serve, FAQ, form |
| Mission: family-owned, 14+ years, "honest work, fair pricing, results built to last", "treat every project like it's for our own family" | About |
| Service areas: Spokane, Spokane Valley, Deer Park, Clayton, Stevens County, Spokane County | Top bar, areas, footer |
| Job photos `job-during.jpg`, `job-after.jpg`, `job-waterline.jpg` | Projects, hero card |

Not used: the AI-generated trailer render, the YouTube-style bursting thumbnail and the stock "Pipe-lining.jpg". Their usage rights are unclear.

## 6. Still needed before launch (highlighted with `.tbc`)

- Google rating, review count and 3 real reviews
- Warranty length and coverage; financing (if offered)
- Typical job timeline; liner design life; permit handling; typical price range
- Project details (location, problem, method)
- Manufacturer certifications
- Photos: Mike's portrait and more job photos

## 7. Pre-launch checks

- No hex or px values typed into Bricks style panels. Use the ACSS variables and classes.
- Remove the `.tbc` class once content is final.
- Test on a real phone:
  - menu
  - cross-section toggle
  - FAQ
  - form submit and conversion
  - mobile call bar
