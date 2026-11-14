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

## Verification

- QA every page at 1440, 991, 767 and 390. Check for horizontal overflow, console errors, failed requests, broken
  images, raw `{dynamic_tags}`, and exactly one H1 per page.
- Back up options and post meta to a `wc_backup_*` option before destructive changes.
