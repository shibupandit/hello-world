# Bricks build inputs

Generated from `index.html` and `assets/css/style.css` for the native Bricks import on the WordPress site.

- `all.html`: header, homepage sections and footer markup, with the SVG icon sprite inlined (Bricks can't use `<use href="#…">`).
- `components.css`: component CSS (from "Sections" onward in `style.css`). The font tokens are written as literal family names, because Bricks writes `font-family` literally.
- `theme.css`: the global base CSS, stored in the Bricks theme style (Global → Custom CSS).

ACSS supplies all `--primary`, `--space-*`, `--text-*` and similar variables. The `--pc-shadow-*`, `--pc-ease` and `--pc-page-bg` tokens are Bricks global variables in the "Hartwell & Crane" category.
