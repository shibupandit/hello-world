# Hartwell & Crane — attorney website prototype

A boxed, single-page law-firm homepage (topbar, header, hero with consultation form, recognition strip, about, practice areas, process, stats, attorneys, case results, testimonials, FAQ, insights, contact, footer), built as static HTML/CSS/JS ready to move into **WordPress + Bricks Builder + Automatic.css v3**.

- Open `index.html`, `blog.html` (blog archive) or `blog-single.html` (single post) in a browser.
- `blog.html` and `blog-single.html` are generated: edit `partials/*.main.html`, then run `python3 tools/build_pages.py`. The header and footer come from `index.html`.
- `assets/css/acss-shim.css` stands in for ACSS v3 variables; delete it once ACSS is installed.
- `assets/css/style.css` is written only with ACSS variables and BEM classes.
- `docs/bricks-acss-handoff.md` is the step-by-step Bricks + ACSS build guide.

All names, people and figures are placeholder content.
