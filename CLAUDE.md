# Working memory: Bricks Builder + Automatic.css builds

Rules learned building the White Crow Law site (Bricks 2.4, ACSS 3.3, Fluent Forms, ACF Pro, Perfmatters, Kinsta).
Apply them by default on every Bricks/ACSS build. Do not wait to be asked.

## Mega menus and dropdowns (Nav Nested + Dropdown)

Every time a mega menu or any dropdown is built, ship this touch fix with it. Without it, phones show a blue
tap-highlight flash on each dropdown and hover/tap race each other.

- Set each Dropdown element `toggleOn` to `both` (hover on desktop, tap on touch). Never `hover` only.
- On the nav's class:
  ```css
  .mega-nav, .mega-nav * { -webkit-tap-highlight-color: transparent; }
  .mega-nav .brx-submenu-toggle, .mega-nav .brx-submenu-toggle *, .mega-nav__toggle, .mega-nav__close {
    touch-action: manipulation; -webkit-user-select: none; user-select: none; }
  @media (hover: none) {
    .mega-nav .brxe-dropdown:hover > .brx-submenu-toggle > * { color: inherit; }
    .mega-nav .brxe-dropdown.open > .brx-submenu-toggle > * { color: var(--primary); } }
  ```
- Site-wide (ACSS custom CSS): `html { -webkit-tap-highlight-color: transparent; }` and
  `a, button, summary, [role="button"] { touch-action: manipulation; }`. Keep `:focus-visible` rings.
- Verify with Playwright touch devices (Pixel 7, iPhone 13, iPad Mini): tap each dropdown and log class changes with
  a MutationObserver. One tap must give exactly one open, with no open→closed→open sequence.
- Mobile menu: the close toggle uses a real close icon (`ti-close`), and the logo sits above the open panel
  (`position: relative; z-index: 10001`).
- The Toggle element is often disabled in Bricks → Settings → Elements. Nav Nested needs it, so enable it.

## Frosted glass and abstract backgrounds

- Abstract background: one fixed `body::before` layer of large `radial-gradient` blobs in brand colours (no image, no
  `filter: blur`), drifting slowly with a transform animation. Add a faint SVG-noise `body::after` (about 4% opacity)
  for grain. Turn the animation off under `prefers-reduced-motion`.
- Glass panels: translucent backgrounds from shared variables (`--glass-bg`, `--glass-sand`, `--glass-border`,
  `--glass-shadow`, `--glass-blur`). Use real `backdrop-filter` only on surfaces that pass over detailed content
  (the sticky header). Blurring every card makes phones stutter.
- Never put `backdrop-filter` (or transform or filter) on an element that contains the mobile nav. It becomes the
  containing block for `position: fixed` and collapses the full-screen menu. Put the blur on the header's `::before`
  (`position: absolute; inset: 0; z-index: -1`, with `isolation: isolate` on the header).
- A blurred child inside a blurred parent cannot blur the page, so text shows through it. Mega menu panels and the
  mobile menu panel stay solid (`var(--white)` / `var(--neutral-ultra-light)`) for readability.
- Provide an `@supports not (backdrop-filter…)` fallback with a solid background.
- Architectural grid layer (the user's preferred look): `html::after`, fixed, `z-index: -1`, width
  `min(var(--content-width), calc(100% - 2 * var(--gutter)))`, centred. It has 1px brand-tinted `border-inline` (about 8%
  alpha) and a faint dashed centre line (`repeating-linear-gradient`). Add 1px lines between sections
  (`#brx-content > .brxe-section + .brxe-section`, `#brx-footer`). Raise the grain to about 7%.
- Warm glow: one injected `.bg-glow` div (fixed, about 64vmax radial in a brand copper tone). Move it with the
  `translate` property only, so it runs on the compositor. It follows the pointer on fine pointers (rAF plus a 1.6s
  ease) and drifts with a CSS keyframe on touch. Static under `prefers-reduced-motion`. Paint order of the negative
  layers: `body::before` (aurora), then `.bg-glow`, then `body::after` (grain), then `html::after` (grid).
- Keep the CSS in ACSS custom CSS between `/* bg2:start */` and `/* bg2:end */`, and the script in Bricks custom code
  with id `wc-bg-glow`.

## Bricks

- BEM global classes only. Identical elements share one class across all pages. No styling on elements; move one-offs
  into modifier classes (`--flush`, `--narrow`, `--portrait`, …).
- Global class custom CSS does NOT replace `%root%`. Write the real selector (`.card { … }`).
- Query loops only repeat on container elements (div/block/section). Put `hasLoop` on a div and nest the text inside.
- Grids inside a container need `width: 100%` or they shrink to their content.
- Flex rows that wrap need `row-gap` as well as `column-gap`.
- Section side padding lives on the class (`var(--section-padding-x)`), never as element padding.
- `<figure>` and `<blockquote>` carry browser margins (40px). Reset them on the class.
- Use native `<details>/<summary>` for accordions and office rows (no JS). Animate with `::details-content`.
- Template conditions:
  - Search templates use `main: search`. 404 templates use `main: error`. Never `any`, which hijacks every page.
  - A content template for "postType page" overrides pages that have their own layout. Scope it with `main: ids`.
- After changing template conditions, re-check the H1 of every page.
- Do not use the Breadcrumbs element (it loads Font Awesome). Build breadcrumbs from text links.
- Testimonial carousels use Nested Slider with `quote-slider` classes. Arrows go below the cards, dots hidden, and
  cards get equal heights.

## Arch images and image motion

- Never draw arch shapes with a large `border-radius` (for example 260px). On phones the browser scales the radii down
  and the top curve flattens. Use an SVG mask on the frame class instead (`.media-arch`), with a fixed
  `aspect-ratio: 4 / 5` and a viewBox 0 0 400 500 path drawing a semicircle top and 16-unit bottom corners
  (`mask-size: 100% 100%`). Reveal clip-path keyframes must not carry `round` values.
- Image motion (mouse depth plus scroll parallax): one small inline script in Bricks → Custom code (body footer, id
  `wc-arch-motion`) that only writes CSS variables. Use rAF with lerp, IntersectionObserver so only visible images
  update, the mouse effect only under `(hover: hover) and (pointer: fine)`, and nothing at all under
  `prefers-reduced-motion`.
- Move images with the individual `translate` / `scale` properties, not `transform`. Entrance animations with
  `fill-mode: both` keep their final `transform` and would override it. Scale the image (1.14) so parallax never
  shows the frame edge.
- The arch reveal (`wc-arch` + `wc-settle`) lives on the shared `media-arch` class, not on one hero. Inside
  `.home-hero`/`.page-hero` it plays on load. Elsewhere it uses `animation-timeline: view()` (inside `@supports`), so it
  plays as the image scrolls in. A non-scaling SVG stroke on `::before` draws a thin edge, so white-background
  portraits still read as an arch.
- Two-column hero grids (`home-hero__grid`, `page-hero__grid`, `profile`) are vertically centred (`align-items:
  center`), never top or end aligned.

## Automatic.css

- Save settings with `\Automatic_CSS\Model\Database_Settings::get_instance()->save_settings($vars, true)`.
- Never put a custom `clamp()` in `section-padding-block`. It empties automatic.css. Tune `space-adjust-section`
  instead.
- After every save, check that `uploads/automatic-css/automatic.css` is not 0 bytes.
- The `btn--white` button is not generated in this setup. Use shared `btn-on-dark` / `btn-on-dark--ghost` classes.

## Performance and caching

- After CSS changes, clear the Perfmatters used-CSS cache and the Kinsta cache (`kinsta_cache_purge_all` and a GET to
  `/kinsta-clear-cache-all/`).
- Animations are CSS only. Fade the hero from opacity 0 only if LCP stays fast. Respect `prefers-reduced-motion`.
- Perfmatters lazy-loads images until the first interaction. Headless checks must move the mouse or scroll first.
- Perfmatters "critical images" preloads the first `<img>` in the HTML, which is often a header or mega menu image.
  Add the attribute `data-perfmatters-skip-preload` and `loading: lazy` to every header and mega image so the hero
  image gets the preload.
- The hero (LCP) image is WebP at quality 70–75 with an accurate `sizes` attribute, for example
  `(max-width: 479px) 92vw, (max-width: 991px) 45vw, 500px`. Aim for under 60 KB.
- Imported photos are often badly compressed (about 0.6 bytes per pixel). Recompress any size above about 0.35 bytes
  per pixel with GD (`imagewebp` 72 / `imagejpeg` 78). WordPress `set_quality` + `save` to the same path did not
  shrink them.
- Check that WordPress thumbnail (150) and medium (300) sizes are not 0. Without them, small cards load 600px files.
- Self-host latin font subsets only. Drop latin-ext faces unless the content needs them.
- Measure with throttled Playwright (Moto G4, 4× CPU) and Lighthouse 12. Target mobile 90+, CLS 0, TBT under 100 ms.

## Verification

- QA every page at 1440, 991, 767 and 390. Check for horizontal overflow, console errors, failed requests, broken
  images, raw `{dynamic_tags}`, and exactly one H1 per page.
- Back up options and post meta to a `wc_backup_*` option before destructive changes.
