"""PNW Trenchless: Bricks global classes, generated from pnw-trenchless/index.html.

Rules (see .claude/skills/pnw-trenchless-project/SKILL.md, hard rules):
- Colour, spacing, gaps, radii, shadows: ACSS variables only (or --pnw-* built from them).
- No hex / rgb / px / rem values. Component sizes use em or ch.
- %root% resolves to the class selector.
Breakpoints (Bricks, desktop-first): 991 / 767 / 478.

Run: python3 classes.py  -> writes classes.json
"""
import json, pathlib

T = "@media (max-width: 991px)"   # tablet portrait
L = "@media (max-width: 767px)"   # mobile landscape
P = "@media (max-width: 478px)"   # mobile portrait
NAV = "@media (max-width: 1200px)"  # header nav collapse

C = {}  # name -> css


def c(name, css, cat="PNW"):
    C[name] = (css.strip(), cat)


# --------------------------------------------------------------------------
# Shared: sections and heads
# --------------------------------------------------------------------------
c("section", """
%root% { position: relative; }
%root% > .brxe-container { position: relative; z-index: 1; gap: var(--space-xl); }
""")
c("section--dark", """
%root% { background-color: var(--base); color: var(--text-light); }
%root% :is(h1, h2, h3, h4, h5, h6) { color: var(--text-light); }
""")
c("section--deep", """
%root% { background-color: var(--base-dark); color: var(--text-light); }
%root% :is(h1, h2, h3, h4, h5, h6) { color: var(--text-light); }
""")
c("section--tint", "%root% { background-color: var(--neutral-ultra-light); }")
c("section--white", "%root% { background-color: var(--white); }")
c("section--flush-top", "%root% { padding-top: 0; }")
c("section--tight", "%root% { padding-block: var(--space-xxl); }")
c("grain", """
%root%::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 0; opacity: .5; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .09 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E");
}
""")
c("section__head", """
%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); max-width: 52ch; }
""")
c("section__head--split", """
%root% { max-width: none; width: 100%; flex-direction: row; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: var(--space-m) var(--space-xl); }
""")
c("section__head-main", """
%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); max-width: 46ch; min-width: 0; }
""")
c("section__intro", """
%root% { font-size: var(--text-l); color: var(--text-dark-muted); max-width: 56ch; }
:is(.section--dark, .section--deep) %root% { color: var(--text-light-muted); }
""")
c("eyebrow", """
%root% {
  font-family: var(--pnw-font-mono); font-size: var(--text-xs); font-weight: 700; line-height: 1.4;
  letter-spacing: .16em; text-transform: uppercase; color: var(--primary);
  display: inline-flex; align-items: center; gap: .75em;
}
%root%::before { content: ""; flex: none; width: .65em; height: .65em; border-radius: var(--radius-circle); background: currentColor; box-shadow: 0 0 0 .35em color-mix(in srgb, currentColor 22%, transparent); }
:is(.section--dark, .section--deep) %root% { color: var(--primary-light); }
""")
c("link-arrow", """
%root% { display: inline-flex; align-items: center; gap: .5em; width: fit-content; font-weight: 700; text-decoration: none; color: var(--primary); border-bottom: .1em solid currentColor; padding-bottom: .15em; }
%root%::after { content: "\\2192"; transition: transform .25s var(--pnw-ease); }
%root%:hover::after { transform: translateX(.25em); }
:is(.section--dark, .section--deep, .rating, .projects__info) %root% { color: var(--primary-light); }
""")
c("ico", """
%root% { width: 1.2em; height: 1.2em; flex: none; color: currentColor; }
""")
c("rise", """
%root% { animation: pnw-rise .9s var(--pnw-ease) both; }
@keyframes pnw-rise { from { transform: translateY(1em); opacity: .001; } to { transform: none; opacity: 1; } }
@media (prefers-reduced-motion: reduce) { %root% { animation: none; } }
""")
for i, d in [(2, ".08s"), (3, ".16s"), (4, ".24s"), (5, ".32s")]:
    c(f"rise--{i}", f"%root% {{ animation-delay: {d}; }}")

# --------------------------------------------------------------------------
# Camera-feed motif (signature). Colours built from ACSS tokens.
# --------------------------------------------------------------------------
c("feed", """
%root% {
  position: relative; overflow: hidden; isolation: isolate; display: block; max-width: 100%;
  background: radial-gradient(circle at 50% 52%,
    var(--black) 0 8%,
    color-mix(in srgb, var(--neutral) 18%, var(--base-dark)) 9% 20%,
    color-mix(in srgb, var(--neutral) 32%, var(--base-dark)) 21% 31%,
    color-mix(in srgb, var(--neutral) 52%, var(--base-dark)) 32% 42%,
    color-mix(in srgb, var(--neutral) 36%, var(--base-dark)) 43% 60%,
    color-mix(in srgb, var(--neutral) 12%, var(--base-dark)) 61%);
  color: var(--white); font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .08em;
}
%root%::after { content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 2;
  background: repeating-linear-gradient(0deg, var(--white-trans-10) 0 1px, transparent 1px 3px), radial-gradient(ellipse at center, transparent 55%, var(--black-trans-50)); opacity: .9; }
""")
c("feed--clean", """
%root% { background: radial-gradient(circle at 50% 52%, var(--black) 0 9%, color-mix(in srgb, var(--primary) 30%, var(--base-dark)) 10% 24%, var(--primary-dark) 25% 37%, color-mix(in srgb, var(--primary) 60%, var(--base-dark)) 38% 56%, color-mix(in srgb, var(--primary) 18%, var(--base-dark)) 57%); }
""")
c("feed--blue", """
%root% { background: radial-gradient(circle at 50% 52%, var(--black) 0 10%, color-mix(in srgb, var(--secondary) 30%, var(--base-dark)) 11% 26%, var(--secondary) 27% 39%, var(--secondary-dark) 40% 58%, color-mix(in srgb, var(--secondary) 15%, var(--base-dark)) 59%); }
""")
c("feed--roots", """
%root%::before { content: ""; position: absolute; inset: 0; z-index: 1;
  background:
    radial-gradient(ellipse 6% 22% at 62% 34%, color-mix(in srgb, var(--accent-dark) 55%, var(--base-dark)) 0 60%, transparent 62%),
    radial-gradient(ellipse 4% 16% at 40% 66%, color-mix(in srgb, var(--accent-dark) 45%, var(--base-dark)) 0 60%, transparent 62%),
    radial-gradient(ellipse 18% 4% at 50% 30%, color-mix(in srgb, var(--accent-dark) 35%, var(--base-dark)) 0 60%, transparent 62%); }
""")
c("feed__hud", """
%root% { position: absolute; left: .9em; right: .9em; bottom: .8em; z-index: 3; display: flex; justify-content: space-between; gap: .6em; text-transform: uppercase; }
""")
c("feed__hud--top", "%root% { top: .8em; bottom: auto; }")
c("feed__hud--center", "%root% { justify-content: center; }")
c("feed__ft", "%root% { color: var(--accent); font-weight: 700; font-variant-numeric: tabular-nums; }")
c("feed__rec", """
%root% { display: inline-flex; align-items: center; gap: .5em; }
%root%::before { content: ""; width: .6em; height: .6em; border-radius: var(--radius-circle); background: color-mix(in oklab, var(--accent) 45%, var(--accent-dark)); box-shadow: 0 0 .5em var(--accent-trans-60); animation: pnw-blink 1.4s steps(2, start) infinite; }
@keyframes pnw-blink { to { visibility: hidden; } }
@media (prefers-reduced-motion: reduce) { %root%::before { animation: none; } }
""")
c("feed__cross", """
%root% { position: absolute; inset: 0; z-index: 3; pointer-events: none; }
%root%::before, %root%::after { content: ""; position: absolute; left: 50%; top: 50%; background: var(--white-trans-40); transform: translate(-50%, -50%); }
%root%::before { width: 2em; height: .1em; }
%root%::after { width: .1em; height: 2em; }
""")
c("feed__label", """
%root% { position: absolute; inset: 0; z-index: 3; display: grid; place-items: end start; padding: var(--space-m); text-align: left; color: var(--white); letter-spacing: 0; }
""")

# --------------------------------------------------------------------------
# Header / top bar
# --------------------------------------------------------------------------
c("topbar", f"""
%root% {{ background: var(--base-dark); color: var(--text-light-muted); font-size: var(--text-xs); letter-spacing: .02em; padding-block: var(--space-xs); padding-inline: var(--gutter); border-bottom: var(--pnw-border-dark); line-height: 1.6; }}
%root% .topbar__area {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }}
{L} {{ %root% .topbar__links {{ display: none; }} }}
%root% a {{ color: inherit; text-decoration: none; }}
%root% a:hover {{ color: var(--white); }}
""")
c("topbar__inner", f"""
%root% {{ width: 100%; max-width: var(--content-width); margin-inline: auto; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: calc(var(--space-xs) / 2) var(--space-m); }}
""")
c("topbar__area", """
%root% { display: inline-flex; align-items: center; gap: .5em; }
%root%::before { content: ""; width: .5em; height: .5em; border-radius: var(--radius-circle); background: var(--primary-light); }
""")
c("topbar__links", """
%root% { display: inline-flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: calc(var(--space-xs) / 2) var(--space-s); }
""")
c("topbar__link", """
%root% { display: inline-flex; align-items: center; gap: .4em; }
%root% svg { width: 1.1em; height: 1.1em; }
""")
c("header", f"""
%root% {{ position: relative; z-index: 2; isolation: isolate; border-bottom: var(--pnw-border-dark); color: var(--text-light); padding-inline: var(--gutter); }}
%root%::before {{ content: ""; position: absolute; inset: 0; z-index: -1; background: var(--base-trans-90); -webkit-backdrop-filter: saturate(1.5) blur(.9em); backdrop-filter: saturate(1.5) blur(.9em); }}
""")
c("header__inner", f"""
%root% {{ width: 100%; max-width: var(--content-width); margin-inline: auto; min-height: var(--pnw-header-h); display: flex; flex-direction: row; align-items: center; gap: var(--space-l); }}
""")
c("logo", """
%root% { display: inline-flex; align-items: center; flex: none; }
%root% img { height: 3.4em; width: auto; display: block; }
""")
c("logo--footer", "%root% img { height: 4.25em; }")
c("nav", f"""
%root% {{ margin-inline: auto; }}
{NAV} {{
  %root% {{ margin-inline: auto 0; order: 3; }}
  /* backdrop */
  %root%::before {{ content: ""; position: fixed; inset: 0; z-index: 98; background: var(--base-trans-60); opacity: 0; visibility: hidden; pointer-events: none; transition: opacity .4s var(--pnw-ease), visibility 0s linear .4s; }}
  %root%.brx-open::before {{ opacity: 1; visibility: visible; transition: opacity .4s var(--pnw-ease), visibility 0s; }}
  %root%.brx-open.brx-closing::before {{ opacity: 0; transition: opacity .2s ease-in; }}
}}
""")
c("nav__items", f"""
%root% {{ display: flex; flex-direction: row; align-items: center; gap: calc(var(--space-xs) / 2) clamp(var(--space-s), 2vw, var(--space-l)); list-style: none; margin: 0; padding: 0; }}
{NAV} {{
  .nav %root% {{
    display: flex !important; flex-direction: column; align-items: stretch; justify-content: flex-start; gap: 0;
    position: fixed !important; top: 0; right: 0; bottom: 0; left: auto; z-index: 99; width: min(100%, 26em); height: 100dvh; max-height: none;
    padding: calc(var(--pnw-header-h) + var(--space-s)) var(--gutter) var(--space-l); overflow-y: auto; overscroll-behavior: contain;
    background: var(--base); border-left: var(--pnw-border-dark); box-shadow: var(--box-shadow-l);
    visibility: hidden; opacity: 0; transform: translateX(100%);
    transition: transform .4s var(--pnw-ease), opacity .4s var(--pnw-ease), visibility 0s linear .4s;
  }}
  .nav.brx-open %root% {{ visibility: visible; opacity: 1; transform: none; transition: transform .4s var(--pnw-ease), opacity .3s var(--pnw-ease), visibility 0s; }}
  .nav.brx-open.brx-closing %root% {{ opacity: 0; transform: translateX(30%); transition: transform .2s ease-in, opacity .2s ease-in; }}
  %root% > li {{ width: 100%; }}
  .nav.brx-open:not(.brx-closing) %root% > li {{ animation: pnw-nav-in .45s var(--pnw-ease) both; }}
  {"".join(f".nav.brx-open:not(.brx-closing) %root% > li:nth-child({n}) {{ animation-delay: {0.06 + n * 0.04:.2f}s; }} " for n in range(1, 10))}
}}
@keyframes pnw-nav-in {{ from {{ opacity: 0; transform: translateY(.75em); }} to {{ opacity: 1; transform: none; }} }}
@media (prefers-reduced-motion: reduce) {{ .nav %root%, .nav %root% > li, .nav::before {{ transition: none !important; animation: none !important; }} }}
""")
c("nav__link", f"""
%root% {{ position: relative; display: inline-block; color: var(--text-light-muted); font-weight: 600; font-size: var(--text-s); padding-block: var(--space-xs); white-space: nowrap; text-decoration: none; transition: color .2s; }}
%root%::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: .15em; background: var(--primary-light); transform: scaleX(0); transform-origin: left; transition: transform .3s var(--pnw-ease); }}
%root%:hover, %root%[aria-current] {{ color: var(--white); }}
%root%:hover::after, %root%[aria-current]::after {{ transform: scaleX(1); }}
{NAV} {{
  %root% {{ display: block; width: 100%; color: var(--text-light); font-family: var(--heading-font-family); font-size: var(--text-xl); font-weight: 800; letter-spacing: -.02em; padding: var(--space-s) 0; border-bottom: var(--pnw-border-dark); }}
  %root%::after {{ display: none; }}
  %root%:hover, %root%:focus-visible, %root%[aria-current] {{ color: var(--primary-light); }}
}}
""")
c("nav__extras", f"""
%root% {{ display: none; }}
{NAV} {{ %root% {{ display: flex; flex-direction: column; align-items: stretch; gap: var(--space-m); margin-top: auto; padding-top: var(--space-l); }} }}
""")
c("nav__phone", "%root% { display: flex; flex-direction: row; align-items: center; gap: .6em; width: auto; color: var(--white); text-decoration: none; }\n%root%:hover .header__phone-num { color: var(--primary-light); }")
c("nav__quote", "%root% { width: 100%; justify-content: center; }")
c("nav__open", f"""
%root% {{ display: none; }}
{NAV} {{ %root% {{ display: grid; place-items: center; width: 2.9em; height: 2.9em; padding: 0; border: var(--pnw-border-dark); border-radius: var(--radius-circle); color: var(--white); --brxe-toggle-scale: .62; }} }}
%root% .brxa-wrap, %root% .brxa-inner {{ color: inherit; }}
""")
c("nav__close", f"""
%root% {{ display: none; }}
{NAV} {{ %root% {{ display: grid; place-items: center; position: absolute; top: calc((var(--pnw-header-h) - 2.9em) / 2); right: var(--gutter); width: 2.9em; height: 2.9em; padding: 0; border: var(--pnw-border-dark); border-radius: var(--radius-circle); color: var(--white); --brxe-toggle-scale: .62; }}
  %root%:hover {{ border-color: var(--primary-light); color: var(--primary-light); }} }}
""")
c("header__cta", f"""
%root% {{ display: flex; flex-direction: row; align-items: center; gap: var(--space-m); flex: none; }}
{NAV} {{ %root% {{ margin-left: auto; gap: var(--space-s); }} }}
{L} {{ %root% .brxe-button {{ display: none; }} }}
""")
c("header__phone", f"""
%root% {{ display: flex; flex-direction: row; align-items: center; gap: .6em; text-decoration: none; color: var(--white); }}
{NAV} {{ %root% .header__phone-text {{ display: none; }} }}
""")
c("header__phone-ico", """
%root% { width: 2.6em; height: 2.6em; flex: none; border-radius: var(--radius-circle); display: grid; place-items: center; border: var(--border-size) solid var(--white-trans-20); }
%root% svg { width: 1.05em; height: 1.05em; }
""")
c("header__phone-text", "%root% { display: flex; flex-direction: column; line-height: 1.15; }")
c("header__phone-label", "%root% { font-size: var(--text-xs); letter-spacing: .12em; text-transform: uppercase; color: var(--text-light-muted); font-weight: 600; }")
c("header__phone-num", "%root% { font-family: var(--heading-font-family); font-size: var(--text-m); font-weight: 800; letter-spacing: -.01em; }")

# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------
c("hero", f"""
%root% {{ padding-block: 0; overflow: hidden; }}
""")
c("hero__bg", f"""
%root% {{ position: absolute; inset: 0; z-index: 0; margin: 0; }}
%root% img {{ width: 100%; height: 100%; object-fit: cover; object-position: 70% 55%; }}
%root%::after {{ content: ""; position: absolute; inset: 0; background:
  linear-gradient(90deg, var(--base) 0%, var(--base-trans-90) 34%, var(--base-trans-50) 62%, var(--base-trans-20) 100%),
  linear-gradient(0deg, var(--base) 0%, transparent 35%); }}
{T} {{ %root% {{ bottom: auto; height: clamp(18em, 75vw, 28em); }} %root% img {{ object-position: 35% 50%; }}
  %root%::after {{ background: linear-gradient(180deg, var(--base-trans-10) 0%, var(--base-trans-50) 45%, var(--base) 100%); }} }}
""")
c("hero__inner", f"""
%root% {{ position: relative; z-index: 1; width: 100%; padding-block: clamp(var(--space-xxl), 8vw, var(--section-space-m)) var(--space-xl); display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, .75fr); gap: var(--space-xl); align-items: end; }}
{T} {{ %root% {{ grid-template-columns: 1fr; padding-top: clamp(12em, 52vw, 20em); }} }}
""")
c("hero__content", "%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-l); min-width: 0; }")
c("hero__kicker", """
%root% { display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: var(--space-xs) var(--space-s); font-size: var(--text-s); color: var(--text-light-muted); }
""")
c("chip", """
%root% { display: inline-flex; align-items: center; gap: .5em; padding: .4em .9em .4em .5em; border-radius: var(--radius-circle); background: var(--white-trans-10); border: var(--border-size) solid var(--white-trans-20); color: var(--white); font-weight: 600; }
%root% .tbc { background: var(--accent); color: var(--base); border: 0; border-radius: var(--radius-circle); padding: .1em .55em; font-size: .8em; }
""")
c("hero__seo", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--text-light-muted); }")
c("hero__title", "%root% .serif { color: var(--primary-light); display: block; }")
c("hero__lede", "%root% { font-size: var(--text-l); color: var(--white-trans-80); max-width: 52ch; }")
c("hero__actions", f"""
%root% {{ display: flex; flex-direction: row; flex-wrap: wrap; gap: var(--space-s); }}
{P} {{ %root% .brxe-button {{ width: 100%; }} }}
""")
c("hero__aside", "%root% { display: flex; flex-direction: column; gap: var(--space-s); min-width: 0; }")
c("hero-feed", "%root% { border-radius: var(--radius-l); aspect-ratio: 4 / 3; border: var(--border-size) solid var(--white-trans-20); box-shadow: var(--box-shadow-l); }")
c("hero-feed__cap", "%root% { font-size: var(--text-s); color: var(--text-light-muted); }\n%root% strong { color: var(--white); }")
c("hero__proof", f"""
%root% {{ position: relative; z-index: 1; list-style: none; margin: 0; padding: 0; border-top: var(--pnw-border-dark); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("hero__proof-item", f"""
%root% {{ display: flex; flex-direction: row; gap: var(--space-s); align-items: flex-start; padding: var(--space-m) var(--space-m) var(--space-m) 0; color: var(--white-trans-80); font-size: var(--text-s); line-height: 1.45; }}
%root% + %root% {{ padding-left: var(--space-m); border-left: var(--pnw-border-dark); }}
%root% svg {{ width: 1.4em; height: 1.4em; flex: none; color: var(--primary-light); }}
{T} {{ %root% + %root% {{ padding-left: 0; border-left: 0; border-top: var(--pnw-border-dark); }} }}
""")

# --------------------------------------------------------------------------
# Ticker
# --------------------------------------------------------------------------
c("ticker", """
%root% { position: relative; overflow: hidden; background: var(--base-dark); color: var(--text-light); border-block: var(--pnw-border-dark); padding: var(--space-l) 0 var(--space-m); display: flex; flex-direction: column; gap: var(--space-s); }
%root%:hover .ticker__track, %root%:focus-within .ticker__track { animation-play-state: paused; }
""")
c("ticker__row", """
%root% { overflow: hidden; width: 100%; -webkit-mask-image: linear-gradient(90deg, transparent, var(--black) 7%, var(--black) 93%, transparent); mask-image: linear-gradient(90deg, transparent, var(--black) 7%, var(--black) 93%, transparent); }
""")
c("ticker__track", """
%root% { display: flex; flex-direction: row; flex-wrap: nowrap; width: max-content; max-width: none; animation: pnw-ticker 55s linear infinite; }
@keyframes pnw-ticker { to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { %root% { animation: none; } }
""")
c("ticker__track--reverse", "%root% { animation-duration: 70s; animation-direction: reverse; }")
c("ticker__group", """
%root% { width: max-content; max-width: none; flex: none; display: flex; flex-direction: row; flex-wrap: nowrap; align-items: center; gap: clamp(var(--space-l), 2.5vw, var(--space-xxl)); padding-right: clamp(var(--space-l), 2.5vw, var(--space-xxl)); white-space: nowrap; }
""")
c("ticker__group--sub", "%root% { gap: var(--space-l); padding-right: var(--space-l); }")
c("ticker__item", """
%root% { display: inline-flex; align-items: center; gap: .25em; text-decoration: none; color: var(--white); font-family: var(--heading-font-family); font-weight: 900; text-transform: uppercase; font-size: calc(var(--h1) * .8); line-height: 1; letter-spacing: -.045em; transition: color .3s var(--pnw-ease); }
%root%:hover { color: var(--primary-light); }
%root%:hover .ticker__ico { background: var(--primary); border-color: var(--primary); color: var(--white); }
""")
c("ticker__item--outline", """
%root% .ticker__name { color: transparent; -webkit-text-stroke: .02em var(--white-trans-60); transition: color .3s, -webkit-text-stroke-color .3s; }
%root%:hover .ticker__name { color: var(--primary-light); -webkit-text-stroke-color: transparent; }
""")
c("ticker__ico", """
%root% { width: .85em; height: .85em; flex: none; border-radius: var(--radius-circle); display: grid; place-items: center; border: .03em solid var(--white-trans-20); color: var(--primary-light); transition: background-color .3s, border-color .3s, color .3s; margin-right: .2em; }
%root% svg { width: 46%; height: 46%; }
""")
c("ticker__name", "%root% { display: inline-block; }")
c("ticker__spec", """
%root% { align-self: flex-start; margin-top: .35em; margin-left: .2em; font-family: var(--pnw-font-mono); font-size: var(--text-xs); font-weight: 700; letter-spacing: .14em; line-height: 1.2; color: var(--accent); padding: .3em .55em; border: var(--border-size) solid var(--accent-trans-40); border-radius: var(--radius-circle); }
""")
c("ticker__joint", """
%root% { width: clamp(.9em, 1vw + .6em, 1.4em); height: clamp(.9em, 1vw + .6em, 1.4em); flex: none; border-radius: var(--radius-circle); border: .2em solid var(--base-light); box-shadow: inset 0 0 0 .2em var(--base-dark), inset 0 0 0 1em var(--accent); }
""")
c("ticker__word", "%root% { font-family: var(--pnw-font-serif); font-style: italic; font-size: var(--text-xl); color: var(--primary-light); }")
c("ticker__city", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--text-light-muted); }")
c("ticker__dot", "%root% { width: .3em; height: .3em; flex: none; border-radius: var(--radius-circle); background: var(--base-light); }")

# --------------------------------------------------------------------------
# Stats
# --------------------------------------------------------------------------
c("stats__grid", f"""
%root% {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr 1fr; row-gap: var(--space-l); }} %root% > :nth-child(3) {{ border-left: 0; padding-left: 0; }} }}
{P} {{ %root% {{ grid-template-columns: 1fr; row-gap: 0; }} %root% > * {{ padding-left: 0 !important; padding-block: var(--space-m); border-left: 0 !important; }} %root% > * + * {{ border-top: var(--pnw-border); }} }}
""")
c("stat", """
%root% { padding: var(--space-s) var(--space-l); display: flex; flex-direction: column; gap: var(--space-xs); }
%root%:first-child { padding-left: 0; }
%root% + %root% { border-left: var(--pnw-border); }
""")
c("stat__num", """
%root% { font-family: var(--heading-font-family); font-weight: 900; font-size: calc(var(--h1) * .875); line-height: .9; letter-spacing: -.05em; color: var(--text-dark); font-variant-numeric: tabular-nums; white-space: nowrap; }
%root% small { font-size: .42em; letter-spacing: -.02em; color: var(--primary); }
""")
c("stat__label", "%root% { font-weight: 600; color: var(--text-dark-muted); max-width: 20ch; line-height: 1.4; }")

# --------------------------------------------------------------------------
# Signs
# --------------------------------------------------------------------------
c("split", f"""
%root% {{ display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: var(--space-xxl); align-items: start; width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; gap: var(--space-xl); }} }}
""")
c("split--faq", f"%root% {{ grid-template-columns: minmax(0, .85fr) minmax(0, 1.4fr); }}\n{T} {{ %root% {{ grid-template-columns: 1fr; gap: var(--space-l); }} }}")
c("split--center", f"%root% {{ align-items: center; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }}\n{T} {{ %root% {{ grid-template-columns: 1fr; }} }}")
c("split--areas", f"%root% {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr); }}\n{T} {{ %root% {{ grid-template-columns: 1fr; }} }}")
c("split--mike", f"%root% {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); }}\n{T} {{ %root% {{ grid-template-columns: 1fr; }} }}")
c("sticky-aside", f"""
%root% {{ position: sticky; top: calc(var(--pnw-header-h) + var(--space-l)); display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); }}
%root% > p {{ color: var(--text-dark-muted); font-size: var(--text-l); }}
{T} {{ %root% {{ position: static; }} }}
""")
c("sign-list", "%root% { list-style: none; margin: 0; padding: 0; border-top: var(--border-size) solid var(--text-dark); display: flex; flex-direction: column; }")
c("sign", f"""
%root% {{ display: grid; grid-template-columns: 3.5em minmax(0, 1fr) auto; gap: var(--space-m); align-items: center; padding: var(--space-m) 0; border-bottom: var(--pnw-border); border-radius: var(--radius); transition: padding .35s var(--pnw-ease), background-color .35s; }}
%root%:hover {{ padding-inline: var(--space-s); background: var(--white); }}
%root%:hover .sign__ico {{ background: var(--primary); color: var(--white); border-color: var(--primary); }}
{L} {{ %root% {{ grid-template-columns: 3em minmax(0, 1fr); }} %root% .sign__tag {{ grid-column: 2; justify-self: start; }} }}
""")
c("sign__ico", """
%root% { width: 3.5em; height: 3.5em; border-radius: var(--radius-circle); display: grid; place-items: center; background: var(--white); border: var(--pnw-border); color: var(--primary); transition: background-color .3s, color .3s, border-color .3s; }
%root% svg { width: 1.5em; height: 1.5em; }
""")
c("sign__body", "%root% { display: flex; flex-direction: column; gap: calc(var(--space-xs) / 2); }")
c("sign__title", "%root% { font-size: var(--h4); }")
c("sign__text", "%root% { color: var(--text-dark-muted); font-size: var(--text-s); }")
c("sign__tag", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .1em; text-transform: uppercase; color: var(--neutral); padding: .3em .65em; border: var(--pnw-border); border-radius: var(--radius-circle); white-space: nowrap; }")

# --------------------------------------------------------------------------
# Explainer + cross-section
# --------------------------------------------------------------------------
c("explain__text", "%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); min-width: 0; }\n%root% > p { color: var(--text-dark-muted); font-size: var(--text-l); }\n%root% strong { color: var(--text-dark); }")
c("video", "%root% { border-radius: var(--radius-l); aspect-ratio: 16 / 11; box-shadow: var(--box-shadow-l); width: 100%; }")
c("video__play", """
%root% { position: absolute; inset: 0; margin: auto; z-index: 4; width: 5.5em; height: 5.5em; border-radius: var(--radius-circle); background: var(--white); color: var(--base); display: grid; place-items: center; transition: transform .3s var(--pnw-ease); font-size: var(--text-m); }
%root%::before { content: ""; position: absolute; inset: -.75em; border-radius: var(--radius-circle); border: var(--border-size) solid var(--white-trans-40); animation: pnw-pulse 2.4s var(--pnw-ease) infinite; }
%root%:hover { transform: scale(1.06); }
%root% svg { width: 1.6em; height: 1.6em; margin-left: .25em; }
@keyframes pnw-pulse { 0% { transform: scale(.9); opacity: 1; } 100% { transform: scale(1.35); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { %root%::before { animation: none; } }
""")
c("video__meta", "%root% { color: var(--text-light-muted); font-size: var(--text-xs); text-transform: uppercase; }")
c("video__title", "%root% { display: block; font-family: var(--heading-font-family); font-size: var(--h4); font-weight: 700; color: var(--white); letter-spacing: -.01em; }")
c("video__caption", "%root% { display: flex; flex-direction: column; gap: .2em; }")
c("xsec", """
%root% { background: var(--base); color: var(--text-light); border-radius: var(--radius-l); overflow: hidden; display: flex; flex-direction: column; min-width: 0; width: 100%; }
%root% :is(h3) { color: var(--text-light); }
""")
c("xsec__bar", "%root% { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--space-s) var(--space-m); padding: var(--space-m) var(--space-l); border-bottom: var(--pnw-border-dark); }")
c("xsec__title", "%root% { font-size: var(--h4); }")
c("xsec__toggle", """
%root% { display: inline-flex; flex-direction: row; padding: .25em; border-radius: var(--radius-circle); background: var(--base-medium); border: var(--pnw-border-dark); }
""")
c("xsec__toggle-btn", """
%root% { appearance: none; border: 0; background: transparent; color: var(--text-light-muted); font: inherit; font-weight: 700; font-size: var(--text-s); padding: .65em 1.2em; border-radius: var(--radius-circle); cursor: pointer; transition: background-color .3s var(--pnw-ease), color .3s; }
%root%[aria-pressed="true"] { background: var(--white); color: var(--base); }
.xsec[data-mode="trenchless"] %root%[aria-pressed="true"] { background: var(--primary); color: var(--white); }
""")
c("xsec__art", """
%root% { overflow-x: auto; }
%root% svg { width: 100%; min-width: 42em; height: auto; display: block; }
%root% .xsec__trench { transform-origin: 50% 0; transform-box: fill-box; transition: transform .7s var(--pnw-ease), opacity .5s; }
%root% .xsec__pit { transform-origin: 50% 0; transform-box: fill-box; transition: transform .6s var(--pnw-ease) .2s, opacity .4s; }
%root% .xsec__newpipe { stroke-dasharray: 760; stroke-dashoffset: 760; transition: stroke-dashoffset 1.1s var(--pnw-ease) .35s; }
%root% .xsec__oldpipe { transition: opacity .5s .3s; }
%root% .xsec__pitlabel { transition: opacity .4s .4s; }
.xsec[data-mode="trenchless"] %root% .xsec__trench { transform: scaleY(0); opacity: 0; }
.xsec[data-mode="trenchless"] %root% .xsec__newpipe { stroke-dashoffset: 0; }
.xsec[data-mode="trenchless"] %root% .xsec__oldpipe { opacity: .2; }
.xsec:not([data-mode="trenchless"]) %root% .xsec__pit { transform: scaleY(0); opacity: 0; }
.xsec:not([data-mode="trenchless"]) %root% .xsec__pitlabel { opacity: 0; }
""")
c("xsec__facts", f"""
%root% {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-top: var(--pnw-border-dark); }}
{T} {{ %root% {{ grid-template-columns: 1fr 1fr; }} %root% > :nth-child(3) {{ border-left: 0; }} %root% > :nth-child(n+3) {{ border-top: var(--pnw-border-dark); }} }}
{P} {{ %root% {{ grid-template-columns: 1fr; }} %root% > * + * {{ border-left: 0 !important; border-top: var(--pnw-border-dark); }} }}
""")
c("xsec__fact", """
%root% { padding: var(--space-m) var(--space-l); display: flex; flex-direction: column; gap: .25em; }
%root% + %root% { border-left: var(--pnw-border-dark); }
%root% [data-show="trenchless"] { display: none; }
.xsec[data-mode="trenchless"] %root% [data-show="dig"] { display: none; }
.xsec[data-mode="trenchless"] %root% [data-show="trenchless"] { display: inline; color: var(--primary-light); }
""")
c("xsec__fact-label", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .12em; text-transform: uppercase; color: var(--text-light-muted); }")
c("xsec__fact-value", "%root% { font-family: var(--heading-font-family); font-size: var(--h4); font-weight: 700; line-height: 1.25; }")

# --------------------------------------------------------------------------
# Services
# --------------------------------------------------------------------------
c("svc-grid", f"""
%root% {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-l); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("svc-card", """
%root% { --card-accent: var(--primary); height: 100%; position: relative; display: flex; flex-direction: column; min-width: 0; background: var(--white); border: var(--pnw-border); border-radius: calc(var(--radius-l) + var(--space-xs)); padding: var(--space-xs); box-shadow: var(--box-shadow-m); transition: transform .45s var(--pnw-ease), box-shadow .45s var(--pnw-ease), border-color .45s; }
%root%:hover { transform: translateY(-.35em); box-shadow: var(--box-shadow-l); border-color: color-mix(in srgb, var(--card-accent) 35%, var(--neutral-light)); }
%root%:hover .svc-card__art svg { transform: scale(1.05); }
%root%:hover .svc-card__go { background: var(--primary); border-color: var(--primary); color: var(--white); }
%root%:hover .svc-card__go svg { transform: rotate(0); }
%root%:has(.svc-card__link:focus-visible) { outline: .2em solid var(--accent); outline-offset: .25em; }
""")
c("svc-card--accent", "%root% { --card-accent: var(--accent-dark); }")
c("svc-card--water", "%root% { --card-accent: var(--secondary); }")
c("svc-card__art", """
%root% { position: relative; aspect-ratio: 16 / 9; border-radius: var(--radius-l); overflow: hidden; background: radial-gradient(70% 90% at 30% 50%, color-mix(in srgb, var(--card-accent) 22%, transparent), transparent 70%), var(--base); }
%root% svg { position: absolute; inset: 0; width: 100%; height: 100%; transition: transform .8s var(--pnw-ease); }
""")
c("svc-card__body", f"""
%root% {{ padding: var(--space-l) var(--space-l) var(--space-m); display: flex; flex-direction: column; gap: var(--space-s); flex: 1; }}
%root% > p {{ color: var(--text-dark-muted); max-width: 54ch; }}
{P} {{ %root% {{ padding-inline: var(--space-m); }} }}
""")
c("svc-card__top", "%root% { display: flex; flex-direction: row; justify-content: space-between; align-items: center; gap: var(--space-s); }")
c("svc-card__spec", """
%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--card-accent); display: inline-flex; align-items: center; gap: .55em; }
%root%::before { content: ""; width: .7em; height: .7em; border-radius: var(--radius-circle); background: var(--card-accent); }
""")
c("svc-card__go", """
%root% { width: 3em; height: 3em; flex: none; border-radius: var(--radius-circle); display: grid; place-items: center; background: var(--neutral-ultra-light); border: var(--pnw-border); color: var(--text-dark); transition: background-color .35s, color .35s, border-color .35s; }
%root% svg { width: 1.15em; height: 1.15em; transform: rotate(-45deg); transition: transform .45s var(--pnw-ease); }
""")
c("svc-card__title", """
%root% { font-size: calc(var(--h3) * 1.3); font-weight: 800; letter-spacing: -.035em; line-height: 1; }
%root% .serif { color: var(--primary); }
""")
c("svc-card__link", """
%root% { color: inherit; text-decoration: none; }
%root%::after { content: ""; position: absolute; inset: 0; z-index: 5; border-radius: inherit; }
%root%:focus-visible { outline: none; }
""")
c("svc-card__foot", """
%root% { margin-top: auto; padding-top: var(--space-s); border-top: var(--pnw-border); display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: var(--space-xs); }
""")
c("svc-card__foot-label", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase; color: var(--neutral); font-weight: 700; margin-right: .3em; }")
c("pill-tag", "%root% { font-size: var(--text-s); font-weight: 600; line-height: 1.3; padding: .32em .75em; border-radius: var(--radius-circle); background: var(--neutral-ultra-light); border: var(--pnw-border); color: var(--text-dark); }")
c("svc-strip", f"""
%root% {{ display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--space-m); padding: var(--space-m) var(--space-l); border-radius: var(--radius-l); background: var(--base); color: var(--text-light); width: 100%; }}
{P} {{ %root% .brxe-button {{ width: 100%; }} }}
""")
c("svc-strip__text", """
%root% { display: inline-flex; flex-direction: row; align-items: center; gap: .7em; font-weight: 600; }
%root% svg { width: 1.3em; height: 1.3em; color: var(--accent); flex: none; }
""")

# --------------------------------------------------------------------------
# Audience
# --------------------------------------------------------------------------
c("aud-grid", f"""
%root% {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-m); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("aud-card", """
%root% { height: 100%; position: relative; display: flex; flex-direction: column; gap: var(--space-s); padding: var(--space-l); border-radius: var(--radius-l); background: var(--neutral-ultra-light); border: var(--pnw-border); transition: transform .4s var(--pnw-ease), box-shadow .4s, background-color .4s; }
%root%:hover { transform: translateY(-.25em); box-shadow: var(--box-shadow-m); background: var(--white); }
%root% > p { color: var(--text-dark-muted); }
""")
c("aud-card__ico", """
%root% { width: 3.5em; height: 3.5em; border-radius: var(--radius); display: grid; place-items: center; background: var(--base); color: var(--primary-light); margin-bottom: var(--space-xs); }
%root% svg { width: 1.6em; height: 1.6em; }
""")
c("aud-card__title", "%root% { font-size: var(--text-xl); }")
c("checklist", """
%root% { list-style: none; margin: 0; padding: var(--space-s) 0 0; display: flex; flex-direction: column; gap: var(--space-xs); border-top: var(--pnw-border); margin-top: auto; }
""")
c("checklist__item", """
%root% { display: flex; flex-direction: row; gap: .55em; align-items: flex-start; font-size: var(--text-s); font-weight: 600; }
%root% svg { width: 1.1em; height: 1.1em; color: var(--primary); flex: none; margin-top: .2em; }
""")

# --------------------------------------------------------------------------
# Comparison (div-based table so it stays native)
# --------------------------------------------------------------------------
c("compare", "%root% { width: 100%; overflow-x: auto; }")
c("compare__table", """
%root% { min-width: 42em; display: grid; grid-template-columns: 24% minmax(0, 1fr) minmax(0, 1fr); gap: 0; color: var(--text-dark); }
""")
c("compare__cell", """
%root% { padding: var(--space-s) var(--space-m); border-bottom: var(--pnw-border); display: block; font-size: var(--text-m); align-self: stretch; }
""")
c("compare__cell--head", """
%root% { display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-end; gap: .35em; padding-block: var(--space-m); border-bottom: var(--border-size) solid var(--text-dark); font-family: var(--heading-font-family); font-weight: 800; font-size: var(--h4); letter-spacing: -.01em; }
""")
c("compare__cell--label", "%root% { font-weight: 600; color: var(--text-dark-muted); font-size: var(--text-s); }")
c("compare__cell--them", "%root% { color: var(--text-dark-muted); }")
c("compare__cell--us", """
%root% { background: var(--base); color: var(--white); border-bottom-color: var(--white-trans-10); font-weight: 600; }
%root%:not(.compare__cell--head)::before { content: ""; display: inline-block; vertical-align: -.25em; margin-right: .65em; width: 1.25em; height: 1.25em; border-radius: var(--radius-circle); background: var(--primary) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 12.5l4 4 8-9'/%3E%3C/svg%3E") center / 65% no-repeat; }
%root%.compare__cell--head { background: var(--primary); border-bottom-color: var(--primary); border-radius: var(--radius-l) var(--radius-l) 0 0; }
%root%.compare__cell--last { border-radius: 0 0 var(--radius-l) var(--radius-l); border-bottom: 0; }
%root% .tbc { background: var(--accent-trans-30); border-bottom-color: var(--accent); }
""")
c("compare__cell--last", "%root%.compare__cell--us { border-radius: 0 0 var(--radius-l) var(--radius-l); border-bottom: 0; }")
c("is-selected", "%root%.chip-option { background: var(--base); color: var(--white); border-color: var(--base); }")
c("mike__id", "%root% { display: flex; flex-direction: column; }")
c("compare__kicker", "%root% { display: block; font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase; font-weight: 700; opacity: .7; }")
c("note", """
%root% { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: var(--space-m); align-items: start; max-width: 54em; padding: var(--space-m) var(--space-l); border-radius: var(--radius); background: var(--white); border: var(--pnw-border); }
%root% svg { width: 1.6em; height: 1.6em; color: var(--accent-dark); }
%root% p { color: var(--text-dark-muted); }
%root% strong { color: var(--text-dark); }
""")

# --------------------------------------------------------------------------
# Decision flow
# --------------------------------------------------------------------------
c("flow", f"""
%root% {{ display: grid; grid-template-columns: minmax(0, .9fr) 5em minmax(0, 1.4fr); align-items: stretch; width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; gap: var(--space-l); }} }}
""")
c("flow__start", f"""
%root% {{ display: flex; flex-direction: column; gap: var(--space-m); justify-content: center; align-items: flex-start; }}
%root% > p {{ font-weight: 600; color: var(--text-dark-muted); max-width: 26ch; }}
{T} {{ %root% {{ flex-direction: row; align-items: center; }} }}
""")
c("flow__feed", f"""
%root% {{ border-radius: var(--radius-circle); aspect-ratio: 1; width: min(100%, 22em); border: .4em solid var(--white); box-shadow: var(--box-shadow-l); }}
%root% .feed__hud {{ justify-content: center; bottom: 18%; }}
%root% .feed__hud--top {{ top: 18%; bottom: auto; }}
{T} {{ %root% {{ width: 8em; flex: none; border-width: .25em; }} }}
""")
c("flow__lines", f"""
%root% {{ position: relative; }}
%root% svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; color: var(--neutral-medium); }}
{T} {{ %root% {{ display: none; }} }}
""")
c("flow__outcomes", "%root% { display: flex; flex-direction: column; gap: var(--space-s); }")
c("outcome", f"""
%root% {{ --pill: var(--primary); display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: var(--space-xs) var(--space-m); align-items: center; padding: var(--space-m) var(--space-l); background: var(--neutral-ultra-light); border: var(--pnw-border); border-radius: var(--radius-l); transition: transform .35s var(--pnw-ease), box-shadow .35s, background-color .35s; }}
%root%:hover {{ transform: translateX(.35em); box-shadow: var(--box-shadow-m); background: var(--white); }}
%root% > p {{ grid-column: 1; color: var(--text-dark-muted); font-size: var(--text-s); }}
{L} {{ %root% {{ grid-template-columns: 1fr; }} %root% .outcome__pill {{ grid-row: auto; grid-column: 1; justify-self: start; }} }}
""")
c("outcome--burst", "%root% { --pill: var(--base); }")
c("outcome--spot", "%root% { --pill: var(--accent-dark); }")
c("outcome--water", "%root% { --pill: var(--secondary); }")
c("outcome__if", "%root% { grid-column: 1 / -1; font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase; color: var(--neutral); }")
c("outcome__title", "%root% { font-size: var(--h4); }")
c("outcome__pill", "%root% { grid-row: 2 / span 2; grid-column: 2; align-self: center; padding: .55em 1.1em; border-radius: var(--radius-circle); background: var(--pill); color: var(--white); font-weight: 700; font-size: var(--text-s); white-space: nowrap; }")

# --------------------------------------------------------------------------
# Process
# --------------------------------------------------------------------------
c("steps", f"""
%root% {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); counter-reset: step; border-top: var(--pnw-border-dark); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; border-top: 0; }} }}
""")
c("step", f"""
%root% {{ counter-increment: step; position: relative; padding: var(--space-l) var(--space-m) var(--space-m) 0; display: flex; flex-direction: column; gap: var(--space-s); }}
%root% + %root% {{ padding-left: var(--space-m); border-left: var(--pnw-border-dark); }}
%root%::before {{ content: counter(step, decimal-leading-zero); font-family: var(--heading-font-family); font-weight: 900; font-size: calc(var(--h2) * 1.2); line-height: 1; letter-spacing: -.04em; color: transparent; -webkit-text-stroke: .025em var(--white-trans-40); }}
%root%:last-child::before {{ -webkit-text-stroke-color: var(--primary-light); }}
%root%::after {{ content: ""; position: absolute; top: -.1em; left: 0; width: 2.5em; height: .2em; background: var(--primary-light); }}
%root% + %root%::after {{ left: var(--space-m); }}
%root% > p {{ color: var(--text-light-muted); font-size: var(--text-s); }}
{T} {{ %root%, %root% + %root% {{ padding: var(--space-m) 0; border-left: 0; border-top: var(--pnw-border-dark); display: grid; grid-template-columns: 5.5em minmax(0, 1fr); column-gap: var(--space-m); align-content: start; }}
  %root%::before {{ grid-row: span 2; font-size: var(--h2); }} %root%::after, %root% + %root%::after {{ left: 0; }} }}
""")
c("step__title", "%root% { font-size: var(--h4); }")

# --------------------------------------------------------------------------
# Mike
# --------------------------------------------------------------------------
c("mike__media", "%root% { position: relative; }")
c("mike__photo", f"""
%root% {{ position: relative; border-radius: var(--radius-l); overflow: hidden; aspect-ratio: 4 / 5; background: linear-gradient(160deg, var(--base-light), var(--base)); color: var(--text-light-muted); }}
{T} {{ %root% {{ aspect-ratio: 1; }} }}
""")
c("mike__silhouette", "%root% { position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 72%; height: auto; color: var(--white-trans-10); }")
c("mike__photo-ph", """
%root% { position: absolute; inset: 0 0 30% 0; z-index: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: var(--space-l); font-size: var(--text-s); gap: var(--space-s); }
%root% svg { width: 3em; height: 3em; opacity: .5; }
""")
c("mike__plate", """
%root% { position: absolute; left: var(--space-m); right: var(--space-m); bottom: var(--space-m); z-index: 2; display: flex; flex-direction: row; justify-content: space-between; align-items: flex-end; gap: var(--space-s); padding: var(--space-m); border-radius: var(--radius); background: var(--base-trans-70); -webkit-backdrop-filter: blur(.6em); backdrop-filter: blur(.6em); color: var(--white); border: var(--pnw-border-dark); }
""")
c("mike__name", "%root% { display: block; font-family: var(--heading-font-family); font-size: var(--h4); font-weight: 800; }")
c("mike__role", "%root% { font-size: var(--text-s); color: var(--text-light-muted); }")
c("mike__est", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .1em; color: var(--accent); text-align: right; text-transform: uppercase; }")
c("mike__inset", f"""
%root% {{ position: absolute; right: calc(-1 * var(--space-l)); top: var(--space-xl); width: 44%; height: auto; border-radius: var(--radius); border: .3em solid var(--neutral-ultra-light); box-shadow: var(--box-shadow-l); aspect-ratio: 4 / 3; object-fit: cover; object-position: 25% 50%; z-index: 3; }}
{T} {{ %root% {{ right: var(--space-s); top: var(--space-s); width: 40%; }} }}
""")
c("mike__content", "%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-l); min-width: 0; }")
c("mike__quote", """
%root% { margin: 0; padding: 0; border: 0; font-family: var(--pnw-font-serif); font-size: calc(var(--h3) * 1.45); line-height: 1.15; letter-spacing: -.01em; color: var(--text-dark); }
%root%::before { content: "\\201C"; display: block; font-size: 2.5em; line-height: .6; color: var(--primary); margin-bottom: .1em; }
""")
c("mike__bio", "%root% { color: var(--text-dark-muted); font-size: var(--text-l); max-width: 58ch; }")
c("creds", f"""
%root% {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border-top: var(--pnw-border); width: 100%; }}
{P} {{ %root% {{ grid-template-columns: 1fr; }} %root% > :nth-child(even) {{ padding-left: 0 !important; border-left: 0 !important; }} }}
""")
c("creds__item", """
%root% { display: flex; flex-direction: row; gap: .7em; align-items: flex-start; padding: var(--space-s) var(--space-s) var(--space-s) 0; border-bottom: var(--pnw-border); font-weight: 600; font-size: var(--text-s); line-height: 1.4; }
%root%:nth-child(even) { padding-left: var(--space-s); border-left: var(--pnw-border); }
%root% svg { width: 1.25em; height: 1.25em; flex: none; color: var(--primary); }
""")
c("mike__sign", "%root% { display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-m); width: 100%; }")
c("mike__sig", "%root% { display: flex; flex-direction: column; gap: .35em; }")
c("mike__sig-name", "%root% { font-family: var(--pnw-font-serif); font-style: italic; font-size: var(--h3); line-height: 1; color: var(--text-dark); }")
c("mike__sig-role", "%root% { font-size: var(--text-s); color: var(--neutral); }")

# --------------------------------------------------------------------------
# Projects
# --------------------------------------------------------------------------
c("project", f"""
%root% {{ display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); border-radius: var(--radius-l); overflow: hidden; background: var(--base); color: var(--text-light); box-shadow: var(--box-shadow-l); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("job-pair", """
%root% { position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: .2em; background: var(--base); min-width: 0; }
""")
c("job-pair__fig", """
%root% { position: relative; margin: 0; min-width: 0; }
%root% img { width: 100%; height: 100%; aspect-ratio: 4 / 5; object-fit: cover; display: block; }
%root% figcaption, %root% .job-pair__tag { position: absolute; left: var(--space-s); top: var(--space-s); }
""")
c("job-pair__tag", """
%root% { position: absolute; left: var(--space-s); top: var(--space-s); z-index: 2; padding: .35em .75em; border-radius: var(--radius-circle); background: var(--black-trans-60); -webkit-backdrop-filter: blur(.4em); backdrop-filter: blur(.4em); color: var(--white); font-family: var(--pnw-font-mono); font-size: var(--text-xs); font-weight: 700; letter-spacing: .12em; }
""")
c("job-pair__tag--after", "%root% { background: var(--primary); }")
c("project__info", """
%root% { padding: var(--space-l); display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); min-width: 0; }
%root% .link-arrow { color: var(--primary-light); }
%root% .eyebrow { color: var(--primary-light); }
""")
c("project__title", "%root% { font-family: var(--heading-font-family); font-size: var(--h3); font-weight: 800; letter-spacing: -.02em; line-height: 1.1; color: var(--text-light); }\n%root% .serif { color: var(--primary-light); }")
c("spec", "%root% { margin: 0; display: grid; grid-template-columns: auto minmax(0, 1fr); border-top: var(--pnw-border-dark); width: 100%; }")
c("spec__term", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .12em; text-transform: uppercase; color: var(--text-light-muted); padding: var(--space-s) var(--space-m) var(--space-s) 0; border-bottom: var(--pnw-border-dark); }")
c("spec__value", "%root% { margin: 0; font-weight: 600; padding: var(--space-s) 0; border-bottom: var(--pnw-border-dark); }")
c("projects__more", f"""
%root% {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-m); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("mini", f"""
%root% {{ display: grid; grid-template-columns: 9em minmax(0, 1fr); gap: var(--space-m); align-items: center; padding: var(--space-s); background: var(--neutral-ultra-light); border: var(--pnw-border); border-radius: var(--radius-l); text-decoration: none; color: inherit; transition: box-shadow .3s, transform .3s var(--pnw-ease), background-color .3s; }}
%root%:hover {{ box-shadow: var(--box-shadow-m); transform: translateY(-.2em); background: var(--white); }}
%root% .feed, %root% img {{ aspect-ratio: 1; border-radius: var(--radius); width: 100%; height: auto; object-fit: cover; display: block; }}
{P} {{ %root% {{ grid-template-columns: 6em minmax(0, 1fr); }} }}
""")
c("mini__body", "%root% { display: flex; flex-direction: column; gap: .25em; }")
c("mini__title", "%root% { font-family: var(--heading-font-family); font-size: var(--text-l); font-weight: 800; }")
c("mini__text", "%root% { font-size: var(--text-s); color: var(--text-dark-muted); }")

# --------------------------------------------------------------------------
# Reviews + assurance
# --------------------------------------------------------------------------
c("reviews__grid", f"""
%root% {{ display: grid; grid-template-columns: minmax(0, .7fr) minmax(0, 1.6fr); gap: var(--space-xl); align-items: stretch; width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("rating", """
%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-s); padding: var(--space-l); border-radius: var(--radius-l); background: var(--base-medium); border: var(--pnw-border-dark); }
%root% > p { color: var(--text-light-muted); }
%root% .link-arrow { margin-top: auto; }
""")
c("rating__num", "%root% { font-family: var(--heading-font-family); font-weight: 900; font-size: calc(var(--h1) * 1.08); line-height: .9; letter-spacing: -.05em; }")
c("stars", "%root% { color: var(--accent); letter-spacing: .12em; font-size: var(--text-l); line-height: 1; }")
c("review-row", f"""
%root% {{ display: grid; grid-auto-flow: column; grid-auto-columns: minmax(18em, 1fr); gap: var(--space-m); overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: var(--space-xs); scrollbar-width: thin; scrollbar-color: var(--base-light) transparent; }}
{P} {{ %root% {{ grid-auto-columns: 85%; }} }}
""")
c("review", """
%root% { margin: 0; height: 100%; scroll-snap-align: start; display: flex; flex-direction: column; gap: var(--space-m); padding: var(--space-l); border-radius: var(--radius-l); background: var(--white-trans-10); border: var(--pnw-border-dark); }
""")
c("review__quote", "%root% { margin: 0; padding: 0; border: 0; font-family: var(--pnw-font-serif); font-size: var(--text-xl); line-height: 1.3; color: var(--text-light); }")
c("review__by", "%root% { margin-top: auto; display: flex; flex-direction: row; align-items: center; gap: .75em; font-size: var(--text-s); }")
c("review__av", "%root% { width: 2.6em; height: 2.6em; border-radius: var(--radius-circle); display: grid; place-items: center; background: var(--secondary); color: var(--white); font-weight: 800; flex: none; }")
c("review__name", "%root% { display: flex; flex-direction: column; }")
c("review__meta", "%root% { color: var(--text-light-muted); font-size: var(--text-xs); }")
c("assure", f"""
%root% {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border-top: var(--pnw-border-dark); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr; }} %root% > * + * {{ padding-left: 0 !important; border-left: 0 !important; border-top: var(--pnw-border-dark); margin-top: var(--space-l); }} }}
""")
c("assure__item", """
%root% { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: var(--space-xs) var(--space-m); padding: var(--space-l) var(--space-l) 0 0; }
%root% + %root% { padding-left: var(--space-l); border-left: var(--pnw-border-dark); }
%root% svg { width: 2.75em; height: 2.75em; grid-row: span 2; color: var(--primary-light); }
%root% > p { color: var(--text-light-muted); }
""")
c("assure__title", "%root% { font-size: var(--text-xl); }")

# --------------------------------------------------------------------------
# Areas
# --------------------------------------------------------------------------
c("areas__text", "%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-m); min-width: 0; }\n%root% > p { color: var(--text-dark-muted); font-size: var(--text-l); }")
c("materials", "%root% { display: flex; flex-direction: row; flex-wrap: wrap; gap: var(--space-xs); }")
c("material", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .1em; text-transform: uppercase; padding: .4em .75em; border-radius: var(--radius-circle); border: var(--pnw-border); background: var(--white); color: var(--text-dark-muted); }")
c("city-list", "%root% { list-style: none; margin: 0; padding: 0; border-top: var(--border-size) solid var(--text-dark); width: 100%; display: flex; flex-direction: column; }")
c("city", """
%root% { display: flex; flex-direction: row; align-items: baseline; justify-content: space-between; gap: var(--space-m); padding: var(--space-s) 0; border-bottom: var(--pnw-border); text-decoration: none; color: var(--text-dark); font-family: var(--heading-font-family); font-weight: 800; font-size: var(--h3); letter-spacing: -.02em; transition: color .25s, padding .35s var(--pnw-ease); }
%root%:hover { color: var(--primary); padding-left: var(--space-s); }
""")
c("city__note", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .1em; font-weight: 500; color: var(--neutral); text-transform: uppercase; }")
c("map", """
%root% { margin: 0; border-radius: var(--radius-l); overflow: hidden; background: var(--base); box-shadow: var(--box-shadow-l); width: 100%; }
%root% svg { width: 100%; height: auto; display: block; }
%root% .map__pulse { animation: pnw-map-pulse 2.6s var(--pnw-ease) infinite; transform-box: fill-box; transform-origin: center; }
@keyframes pnw-map-pulse { 0% { transform: scale(.6); opacity: .9; } 100% { transform: scale(2.6); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { %root% .map__pulse { animation: none; } }
""")
c("map__caption", "%root% { padding: var(--space-s) var(--space-m); font-size: var(--text-xs); color: var(--text-light-muted); border-top: var(--pnw-border-dark); font-family: var(--pnw-font-mono); letter-spacing: .06em; }")

# --------------------------------------------------------------------------
# FAQ (Bricks nested accordion)
# --------------------------------------------------------------------------
c("faq__list", "%root% { border-top: var(--border-size) solid var(--text-dark); width: 100%; }")
c("faq__item", """
%root% { border-bottom: var(--pnw-border); }
%root% .accordion-title-wrapper, %root% > .brxe-block:first-child { cursor: pointer; display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-between; align-items: center; gap: var(--space-m); padding: var(--space-m) 0; }
%root% .accordion-title-wrapper::after, %root% > .brxe-block:first-child::after { content: ""; flex: none; width: 2.5em; height: 2.5em; border-radius: var(--radius-circle); border: var(--pnw-border); background: var(--white) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23111A16' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M12 6v12M6 12h12'/%3E%3C/svg%3E") center / 45% no-repeat; transition: transform .35s var(--pnw-ease), background-color .3s; }
%root%.brx-open .accordion-title-wrapper::after, %root%.brx-open > .brxe-block:first-child::after { transform: rotate(135deg); background-color: var(--primary); background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M12 6v12M6 12h12'/%3E%3C/svg%3E"); border-color: var(--primary); }
%root%:hover .faq__q { color: var(--primary); }
""")
c("faq__q", "%root% { flex: 1 1 auto; min-width: 0; font-family: var(--heading-font-family); font-weight: 700; font-size: var(--text-l); line-height: 1.3; letter-spacing: -.01em; transition: color .2s; margin: 0; }")
c("faq__answer", f"""
%root% {{ padding: 0 var(--space-xxl) var(--space-m) 0; color: var(--text-dark-muted); }}
%root% > * + * {{ margin-top: var(--space-xs); }}
{T} {{ %root% {{ padding-right: 0; }} }}
""")
c("draft", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .1em; text-transform: uppercase; color: var(--accent-dark); }")

# --------------------------------------------------------------------------
# Estimate + form (dummy form, swap for Fluent Forms later)
# --------------------------------------------------------------------------
c("estimate", "%root% { overflow: hidden; }")
c("estimate__glow", """
%root% { position: absolute; inset: 0; pointer-events: none; z-index: 0; background: radial-gradient(60em 30em at 85% 20%, var(--primary-trans-30), transparent 60%), radial-gradient(40em 30em at 0% 100%, var(--secondary-trans-20), transparent 60%); }
%root%::after { content: ""; position: absolute; left: -18em; bottom: -18em; width: 44em; height: 44em; border-radius: var(--radius-circle); background: repeating-radial-gradient(circle, transparent 0 2.4em, var(--white-trans-10) 2.4em 2.5em); opacity: .5; }
""")
c("estimate__text", "%root% { display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-l); min-width: 0; }\n%root% > p { color: var(--text-light-muted); font-size: var(--text-l); max-width: 46ch; }\n%root% .serif { color: var(--primary-light); }")
c("bigphone", """
%root% { display: flex; flex-direction: column; gap: .35em; text-decoration: none; color: var(--white); width: fit-content; }
%root%:hover .bigphone__num { color: var(--primary-light); }
""")
c("bigphone__label", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--accent); }")
c("bigphone__num", "%root% { font-family: var(--heading-font-family); font-weight: 900; font-size: calc(var(--h2) * 1.07); line-height: 1; letter-spacing: -.04em; font-variant-numeric: tabular-nums; transition: color .25s; }")
c("bigphone__note", "%root% { color: var(--text-light-muted); font-size: var(--text-s); }")
c("contact-ways", f"""
%root% {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-xs); width: 100%; }}
{L} {{ %root% {{ grid-template-columns: 1fr 1fr; }} }}
""")
c("contact-way", """
%root% { display: flex; flex-direction: column; align-items: flex-start; gap: .35em; padding: var(--space-s); border-radius: var(--radius); border: var(--pnw-border-dark); background: var(--white-trans-10); color: var(--white); text-decoration: none; font-weight: 700; font-size: var(--text-s); transition: background-color .25s, border-color .25s; min-width: 0; }
%root%:hover { background: var(--white-trans-20); border-color: var(--white-trans-30); }
%root% svg { width: 1.25em; height: 1.25em; color: var(--primary-light); }
""")
c("contact-way__note", "%root% { font-weight: 500; font-size: var(--text-xs); color: var(--text-light-muted); overflow-wrap: anywhere; }")
c("next", "%root% { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; border-top: var(--pnw-border-dark); width: 100%; }")
c("next__item", """
%root% { display: grid; grid-template-columns: 2.5em minmax(0, 1fr); gap: var(--space-s); padding: var(--space-s) 0; border-bottom: var(--pnw-border-dark); color: var(--white-trans-80); }
""")
c("next__num", "%root% { font-family: var(--pnw-font-mono); color: var(--accent); font-size: var(--text-s); padding-top: .2em; }")
c("form", f"""
%root% {{ background: var(--white); color: var(--text-dark); border-radius: var(--radius-l); padding: var(--space-l); display: flex; flex-direction: column; gap: var(--space-s); box-shadow: 0 2.5em 6em -2em var(--black-trans-70); min-width: 0; }}
%root% :is(h3) {{ color: var(--text-dark); }}
""")
c("form__head", "%root% { display: flex; flex-direction: row; justify-content: space-between; align-items: baseline; gap: var(--space-s); flex-wrap: wrap; padding-bottom: var(--space-xs); }")
c("form__title", "%root% { font-size: var(--text-xl); }")
c("form__hint", "%root% { font-size: var(--text-s); color: var(--neutral); }")
c("form__sep", "%root% { height: var(--border-size); background: var(--neutral-light); margin-block: calc(var(--space-xs) / 2); width: 100%; }")
c("form__row", f"""
%root% {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-s); width: 100%; }}
{P} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("form__field", """
%root% { display: flex; flex-direction: column; gap: .4em; font-size: var(--text-s); font-weight: 600; width: 100%; }
%root% :is(input, textarea, select) { font: inherit; font-weight: 400; font-size: var(--text-m); color: var(--text-dark); width: 100%; min-height: 3.1em; padding: var(--space-s) var(--space-m); border: var(--border-size) solid var(--neutral-light); border-radius: var(--radius); background: var(--neutral-ultra-light); transition: border-color .2s, box-shadow .2s, background-color .2s; }
%root% textarea { min-height: 6.5em; resize: vertical; }
%root% :is(input, textarea, select):focus { outline: none; border-color: var(--primary); background: var(--white); box-shadow: 0 0 0 .25em var(--primary-ultra-light); }
""")
c("form__field-label", "%root% { font-size: var(--text-s); font-weight: 600; }")
c("form__field-input", """
%root% { display: block; width: 100%; min-height: 3.1em; padding: var(--space-s) var(--space-m); border: var(--border-size) solid var(--neutral-light); border-radius: var(--radius); background: var(--neutral-ultra-light); font-weight: 400; color: var(--neutral); }
%root%:empty::before { content: attr(data-placeholder); }
.form__field:last-of-type > %root% { min-height: 3.1em; }
""")
c("chips", """
%root% { display: flex; flex-direction: column; gap: var(--space-xs); border: 0; padding: 0; margin: 0; min-width: 0; }
""")
c("chips__legend", "%root% { font-size: var(--text-s); font-weight: 600; }")
c("chips__list", "%root% { display: flex; flex-direction: row; flex-wrap: wrap; gap: var(--space-xs); }")
c("chip-option", """
%root% { display: inline-block; padding: .55em .95em; border-radius: var(--radius-circle); border: var(--border-size) solid var(--neutral-light); font-size: var(--text-s); font-weight: 600; line-height: 1.2; cursor: pointer; background: var(--white); color: var(--text-dark); transition: background-color .2s, color .2s, border-color .2s; }
%root%:hover { border-color: var(--base); }
%root%.is-selected, %root%[aria-pressed="true"] { background: var(--base); color: var(--white); border-color: var(--base); }
""")
c("upload", """
%root% { display: flex; flex-direction: row; align-items: center; gap: var(--space-s); padding: var(--space-s) var(--space-m); border: .1em dashed var(--neutral-medium); border-radius: var(--radius); font-size: var(--text-s); color: var(--text-dark-muted); cursor: pointer; transition: border-color .2s, background-color .2s; position: relative; width: 100%; }
%root%:hover { border-color: var(--primary); background: var(--primary-ultra-light); }
%root% svg { width: 1.5em; height: 1.5em; color: var(--primary); flex: none; }
""")
c("form__submit", "%root% { width: 100%; justify-content: center; }")
c("form__fine", "%root% { font-size: var(--text-xs); color: var(--neutral); text-align: center; width: 100%; }")

# --------------------------------------------------------------------------
# Footer + call bar
# --------------------------------------------------------------------------
c("footer", f"""
%root% {{ padding: var(--section-space-m) var(--gutter) var(--space-l); color: var(--text-light-muted); font-size: var(--text-s); }}
%root% a {{ color: inherit; text-decoration: none; transition: color .2s; }}
%root% a:hover {{ color: var(--white); }}
%root% > .brxe-container {{ gap: 0; }}
""")
c("footer__grid", f"""
%root% {{ display: grid; grid-template-columns: minmax(0, 1.5fr) repeat(3, minmax(0, 1fr)); gap: var(--space-l); padding-bottom: var(--space-xl); border-bottom: var(--pnw-border-dark); width: 100%; }}
{T} {{ %root% {{ grid-template-columns: 1fr 1fr; }} }}
{P} {{ %root% {{ grid-template-columns: 1fr; }} }}
""")
c("footer__col", "%root% { display: flex; flex-direction: column; gap: var(--space-xs); align-items: flex-start; }")
c("footer__heading", "%root% { font-family: var(--pnw-font-mono); font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--white); margin-bottom: calc(var(--space-xs) / 2); font-weight: 700; }")
c("footer__phone", "%root% { font-family: var(--heading-font-family); font-weight: 900; font-size: var(--text-xl); letter-spacing: -.02em; }\n.footer %root% { color: var(--white); }")
c("footer__word", """
%root% { font-family: var(--heading-font-family); font-weight: 900; font-size: clamp(var(--h2), 8.4vw, calc(var(--h1) * 1.55)); line-height: .85; letter-spacing: -.06em; color: transparent; -webkit-text-stroke: .008em var(--white-trans-20); text-align: center; padding-block: var(--space-xl) var(--space-m); white-space: nowrap; overflow: hidden; user-select: none; width: 100%; }
""")
c("footer__bottom", "%root% { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; gap: var(--space-xs) var(--space-l); font-size: var(--text-xs); width: 100%; }")
c("footer__legal", "%root% { display: flex; flex-direction: row; gap: var(--space-xs); }")
c("social", "%root% { display: flex; flex-direction: row; gap: var(--space-xs); margin-top: var(--space-xs); }")
c("social__link", """
%root% { width: 2.5em; height: 2.5em; border-radius: var(--radius-circle); display: grid; place-items: center; border: var(--border-size) solid var(--white-trans-20); color: var(--white); transition: background-color .25s, border-color .25s; }
%root%:hover { background: var(--secondary); border-color: var(--secondary); }
%root% svg { width: 1.05em; height: 1.05em; }
""")
c("callbar", f"""
%root% {{ display: none; }}
{L} {{
  %root% {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-xs); position: fixed; left: 0; right: 0; bottom: 0; z-index: 65; background: var(--base-trans-90); -webkit-backdrop-filter: blur(.75em); backdrop-filter: blur(.75em); border-top: var(--pnw-border-dark); padding: var(--space-xs) var(--gutter) calc(var(--space-xs) + env(safe-area-inset-bottom, 0px)); }}
  %root% .brxe-button {{ justify-content: center; }}
  body {{ padding-bottom: 4.75em; }}
}}
""")


AUTO_WIDTH = ["logo", "topbar__links", "topbar__link", "header__cta", "header__phone", "header__phone-text",
              "ticker__item", "feed__hud", "mike__plate", "xsec__toggle", "mike__id", "mike__sig", "footer__legal",
              "svc-strip__text", "review__name", "social", "chips__list", "upload"]


def _row_default(css):
    """Bricks blocks default to flex-direction: column; make flex rules explicit rows."""
    import re

    def fix(rule):
        body = rule.group(2)
        if re.search(r"display:\s*(inline-)?flex", body) and "flex-direction" not in body:
            body = re.sub(r"(display:\s*(?:inline-)?flex;)", r"\1 flex-direction: row;", body, count=1)
        return rule.group(1) + "{" + body + "}"

    return re.sub(r"([^{}]*)\{([^{}]*)\}", fix, css)


# Icon + text rows: keep the icon beside the text at every width.
for _n in ["creds__item", "hero__proof-item", "checklist__item", "svc-strip__text", "topbar__link"]:
    _css, _cat = C[_n]
    C[_n] = (_css + "\n%root% { flex-wrap: nowrap; }\n%root% > :not(svg) { flex: 1 1 auto; min-width: 0; width: auto; }", _cat)


def build():
    for n in AUTO_WIDTH:
        css, cat = C[n]
        C[n] = (css.replace("%root% {", "%root% { width: auto;", 1), cat)
    out = [{"name": n, "css": _row_default(css), "category": cat} for n, (css, cat) in C.items() if css]
    p = pathlib.Path(__file__).with_name("classes.json")
    p.write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    out = build()
    print(len(out), "classes")
