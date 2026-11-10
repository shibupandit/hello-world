"""One-off refactor tool (2026-11-10): merge BEM classes that share the same layout into common classes.

For each family in SPEC it derives the shared CSS (the declarations and rules every member has),
creates/updates the common class with it, strips that CSS from the members (a member with nothing
left is deleted) and rewrites the element builders so elements carry the common class.

  python3 tools/merge_classes.py            dry run: report per family
  python3 tools/merge_classes.py --apply    rewrite classes.py and elements*.py
  python3 tools/merge_classes.py --verify OLD_ELEMENTS.json OLD_CLASSES.json
        after --apply and a rebuild: prove every element still gets the same set of declarations

All comparisons use the final CSS (after classes.build() post-processing), so the regenerated
definitions are written as final CSS and removed from the post-processing lists.
"""
import ast, glob, json, pathlib, re, sys, collections

HERE = pathlib.Path(__file__).resolve().parent.parent
MEDIA = {"@media (max-width: 991px)": "T", "@media (max-width: 767px)": "L", "@media (max-width: 478px)": "P", "@media (max-width: 1200px)": "NAV"}

# (common class, members, declarations to force into the common class even if a member lacks them)
SPEC = []


def fam(common, members, add=()):
    SPEC.append((common, members.split(), list(add)))


T991, L767 = "@media (max-width: 991px)", "@media (max-width: 767px)"
ONE = "grid-template-columns: minmax(0, 1fr)"   # same as `1fr` here, and never overflows

# ---- text styles --------------------------------------------------------------------------
fam("caption", "sign__text signature__role steps-mini__text pcard__text docs__text ws-svc__text job__spec mini__text verify-card__fine pj-inline__cap who__cap widget__muted")
fam("caption-light", "mike__role jump__note svc-hero__cap bigphone__note milestone__text")
fam("caption-neutral", "mike__sig-role form__hint")
fam("fine-light", "review__meta portrait__role")
fam("text-muted", "compare__cell--them promise__text")
fam("text-light-muted", "footer__hours score__count rv-steps__text")
fam("text-accent-light", "project__link who__kicker--dark crumbs__current")
fam("strong-dark", "signature__name rv-card__name widget__name")
fam("value-light", "info-card__value pj-meta__value pj-card__value")
fam("title-light", "portrait__name ind__fact-value jump__title")
fam("title-l", "sign__title verify-card__title docs__title who__h3")
fam("title-card", "aud-card__title fit-card__title")
fam("title-block", "urgent__title pj-block__title")
fam("accent-light", "svc-hero__title owner__title")
# ---- mono labels --------------------------------------------------------------------------
fam("label", "story__meta pj-glance__label spec-table__term outcome__if")
fam("label-light", "reach__label pj-meta__term ind__fact-label fact__label")
fam("label-accent", "score__label jump__label info-card__term pj-card__term")
fam("label-wide", "hero__seo ticker__city")
# ---- stacks and rows ----------------------------------------------------------------------
fam("stack-l", "hero__content mike__content svc-hero__content owner__content")
fam("stack-m", "pj-hero__title near who__text", add=["min-width: 0"])
fam("stack-s", "hero__aside who__col")
fam("stack-xl", "pj-story__body city-main")
fam("figure-stack", "who__media svc-hero__media")
fam("text-block", "areas__text local__text explain__text cost__text", add=["min-width: 0"])
fam("text-block-light", "rig__text estimate__text rv-leave__text", add=["min-width: 0"])
fam("id-stack", "portrait__id signature__id rv-card__id review__name")
fam("mini-stack", "mike__sig score__side")
fam("chip-row", "materials near__cities who__links")
fam("grow", "byline__text related__label")
fam("btn-block", "nav__quote form__submit")
fam("section--tight", "section--tight urgent")
# ---- grids --------------------------------------------------------------------------------
fam("split", "split specs__grid ind", add=[(T991, ONE)])
fam("split-even", "local__grid rv-leave__grid")
fam("split-wide", "rig__grid cost__grid", add=[(T991, ONE)])
fam("grid-2", "fit__grid inside__grid")
fam("grid-3", "aud-grid jobs__grid")
fam("grid-3-2", "promises__grid pcards", add=[(L767, ONE)])
fam("grid-4", "docs__grid ws-svc verify__grid timeline__list", add=[(L767, ONE)])
# ---- lists --------------------------------------------------------------------------------
fam("list-plain", "widget__list widget__svc")
fam("list-ruled", "who__list fit-card__list", add=["width: 100%"])
fam("list-ruled-dark", "next rv-steps cost-card__list", add=["width: 100%"])
fam("list-ruled-strong", "city-list sign-list", add=["width: 100%"])
fam("num-row", "next__item cost-card__item")
fam("num-row__num", "next__num cost-card__num rv-steps__num")
# ---- icons, tags, cards -------------------------------------------------------------------
fam("ico-tile", "jump__ico who__ico ws-svc__ico")
fam("ico-round", "promise__ico docs__ico")
fam("card-num", "promise__num docs__num")
fam("tag--after", "job-pair__tag--after mosaic__tag--after still__tag--after")
fam("card-soft", "promise docs__item")
fam("card-dark", "pj-card cost-card")
fam("rows-dark", "kit pj-card__list")


# ---- css model ----------------------------------------------------------------------------
def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def parse(css):
    """-> list of (context, selector, [declarations]); context is '' or the @media query."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        head = norm(css[i:j])
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith("@media"):
            out += [(head, s, d) for _, s, d in parse(body)]
        elif head.startswith("@"):
            out.append(("", head, [norm(body)]))  # keyframes etc.: opaque
        else:
            out.append(("", head, decls(body)))
        i = k
    return out


def decls(body):
    parts, cur, depth, q = [], "", 0, None
    for ch in body:
        if q:
            q = None if ch == q else q
        elif ch in "\"'":
            q = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == ";" and not depth and not q:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [norm(x) for x in parts if norm(x)]


def emit(rules):
    by = collections.OrderedDict()
    for ctx, sel, ds in rules:
        by.setdefault(ctx, []).append((sel, ds))
    lines = []
    for ctx, items in by.items():
        txt = [(f"{sel} {{ {ds[0]} }}" if sel.startswith("@") else f"{sel} {{ {'; '.join(ds)}; }}") for sel, ds in items]
        lines += txt if not ctx else [f"{ctx} {{ {' '.join(txt)} }}"]
    return "\n".join(lines)


def prop(d):
    return d.split(":", 1)[0].strip()


def overlap(a, b):
    """True when declaration lists a and b touch the same property (or a shorthand of it)."""
    pa, pb = {prop(x) for x in a}, {prop(x) for x in b}
    for x in pa:
        for y in pb:
            if x == y or x.startswith(y + "-") or y.startswith(x + "-"):
                return (x, y)
    return None


def load_final():
    sys.path.insert(0, str(HERE))
    import importlib, classes
    importlib.reload(classes)
    return {c["name"]: c["css"] for c in classes.build()}


def plan(F):
    """-> {common: (common_rules, {member: remaining_rules}), ...} plus warnings."""
    res, warn = collections.OrderedDict(), []
    for common, members, add in SPEC:
        missing = [m for m in members if m not in F]
        if missing:
            warn.append(f"{common}: unknown {missing}")
            continue
        P = {m: parse(F[m]) for m in members}
        first = P[members[0]]
        keys = [(ctx, sel) for ctx, sel, _ in first]
        keys += [(a[0], "%root%") for a in add if not isinstance(a, str) and (a[0], "%root%") not in keys]
        common_rules = []
        for ctx, sel in keys:
            per = []
            for m in members:
                hit = [ds for c2, s2, ds in P[m] if (c2, s2) == (ctx, sel)]
                per.append(hit[0] if hit else None)
            base = [d for d in per[0] if all(p is not None and d in p for p in per)] if all(p is not None for p in per) else []
            if sel == "%root%":
                for a in add:
                    actx, d = ("", a) if isinstance(a, str) else a
                    if actx != ctx or d in base:
                        continue
                    for m, p in zip(members, per):
                        clash = [x for x in (p or []) if prop(x) == prop(d) and x != d]
                        if clash:
                            warn.append(f"{common}: {m} {clash[0]!r} becomes {d!r}" + (f" in {ctx}" if ctx else ""))
                    base.append(d)
            if base:
                common_rules.append((ctx, sel, base))
        if not any(sel == "%root%" and ctx == "" for ctx, sel, _ in common_rules) and common not in ("accent-light",):
            warn.append(f"{common}: no shared base rule")
        rest = {}
        for m in members:
            r = []
            for ctx, sel, ds in P[m]:
                cm = [cd for c2, s2, cd in common_rules if (c2, s2) == (ctx, sel)]
                left = [d for d in ds if not cm or (d not in cm[0] and prop(d) not in {prop(x) for x in cm[0]})]
                if left:
                    r.append((ctx, sel, left))
                    if cm and overlap(left, cm[0]):
                        warn.append(f"{common}: {m} keeps {left} overlapping the common rule {overlap(left, cm[0])}")
            rest[m] = r
        res[common] = (common_rules, rest)
    return res, warn


def report(res, warn, F):
    saved = 0
    for common, (rules, rest) in res.items():
        before = sum(len(F[m]) for m in rest)
        after = len(emit(rules)) + sum(len(emit(r)) for r in rest.values())
        saved += before - after
        gone = [m for m, r in rest.items() if not r and m != common]
        kept = {m: emit(r) for m, r in rest.items() if r}
        print(f"\n== {common}  ({before} -> {after} bytes)\n   {emit(rules)[:300]}")
        print(f"   merged away: {gone}")
        for m, t in kept.items():
            print(f"   keeps {m}: {t[:200]}")
    print("\nWARNINGS:" if warn else "\nno warnings")
    for w in warn:
        print("  !", w)
    print("bytes saved:", saved, "of", sum(len(v) for v in F.values()))


def py_def(name, rules):
    css = emit(rules)
    for q, k in MEDIA.items():
        css = css.replace(q, "\x00" + k + "\x01")
    css = css.replace("{", "{{").replace("}", "}}").replace("\x00", "{").replace("\x01", "}")
    quote = '"""' if '"' in css or "\n" in css else '"'
    body = f"\n{css}\n" if quote == '"""' else css
    return f'c("{name}", rf{quote}{body}{quote})'


def apply(res):
    src_path = HERE / "classes.py"
    src = src_path.read_text()
    tree = ast.parse(src)
    spans = {}
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and getattr(node.value.func, "id", "") == "c":
            a0 = node.value.args[0]
            if isinstance(a0, ast.Constant):
                spans[a0.value] = (node.lineno, node.end_lineno)
    lines = src.split("\n")
    edits, renames, also, shared = {}, {}, {}, []  # line span -> new text
    for common, (rules, rest) in res.items():
        if common in spans:  # the common class is an existing class: rewrite in place
            edits[spans[common]] = py_def(common, rules)
        else:
            shared.append(py_def(common, rules))
        for m, r in rest.items():
            if m == common:
                continue
            if r:
                edits[spans[m]] = py_def(m, r)
                also[m] = common
            else:
                edits[spans[m]] = None
                renames[m] = common
    for (a, b), text in sorted(edits.items(), reverse=True):
        lines[a - 1:b] = [text] if text is not None else []
    src = "\n".join(lines)
    # shared section goes before the first section header
    marker = "# --------------------------------------------------------------------------\n# Shared: sections and heads"
    assert marker in src
    block = ("# --------------------------------------------------------------------------\n"
             "# Shared components (2026-11-10): one class per common layout, used on every page.\n"
             "# Page classes below only add what is specific to them. Written as final CSS.\n"
             "# --------------------------------------------------------------------------\n" + "\n".join(shared) + "\n\n")
    src = src.replace(marker, block + marker, 1)
    # selectors that point at a merged-away class now point at the common class
    for old, new in renames.items():
        src = re.sub(r"\." + re.escape(old) + r"(?![\w-])", "." + new, src)
    # post-processing lists: merged or regenerated classes already carry their final CSS
    touched = set(renames) | set(also) | set(res)

    def clean_list(m):
        items = re.findall(r'"([^"]+)"', m.group(2))
        keep = [x for x in items if x not in touched]
        return m.group(1) + ", ".join(f'"{x}"' for x in keep) + m.group(3)
    src = re.sub(r"(AUTO_WIDTH = \[)(.*?)(\])", clean_list, src, count=1, flags=re.S)
    src = re.sub(r"(for _n in \[)(.*?)(\]:)", clean_list, src, count=1, flags=re.S)
    src_path.write_text(src)

    plain = []
    for path in sorted(glob.glob(str(HERE / "elements*.py"))):
        s = pathlib.Path(path).read_text()
        for old, new in list(renames.items()) + [(o, f"{n} {o}") for o, n in also.items()]:
            rx = re.compile(r"(?<![\w-])" + re.escape(old) + r"(?![\w-])")
            if re.fullmatch(r"[a-z]+", old):  # a plain word: only as a whole class string or a token next to another class
                rx = re.compile(r'(?<=")' + re.escape(old) + r'(?=["])|(?<=")' + re.escape(old) + r'(?= [a-z-]+(?:__|--))|(?<=[a-z] )' + re.escape(old) + r'(?=")')
                plain += [(pathlib.Path(path).name, old, s[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")) for m in rx.finditer(s)]
            s = rx.sub(new, s)
        pathlib.Path(path).write_text(s)
    json.dump({"renames": renames, "also": also}, open(HERE / "tools" / "merge_map.json", "w"), indent=1)
    print("renamed", len(renames), "extended", len(also), "new shared", len(shared))
    for p in plain:
        print("  plain-word match:", p)


def verify(old_elements, old_classes):
    mp = json.load(open(HERE / "tools" / "merge_map.json"))
    ren = mp["renames"]
    oldF = {c["name"]: c["css"] for c in json.load(open(old_classes))}
    newF = {c["name"]: c["css"] for c in json.load(open(HERE / "classes.json"))}

    def canon(sel):
        return re.sub(r"\.([\w-]+)", lambda m: "." + ren.get(m.group(1), m.group(1)), sel)

    def decl_set(names, F):
        out = set()
        for nm in names:
            for ctx, sel, ds in parse(F.get(nm, "")):
                for d in ds:
                    out.add((ctx, canon(sel), d))
        return out

    def flat(d):
        els = d["header"] + d["footer"] + [e for s in d["sections"] for e in s["elements"]]
        for p in d["pages"]:
            els += [dict(e, id=p["key"] + "/" + e["id"]) for s in p["sections"] for e in s["elements"]]
        for t in d["templates"]:
            els += [dict(e, id=t["key"] + "/" + e["id"]) for e in t["elements"]]
        return {e["id"]: e for e in els}

    old, new = flat(json.load(open(old_elements))), flat(json.load(open(HERE / "elements.json")))
    assert old.keys() == new.keys(), "element ids changed"
    bad = collections.Counter()
    examples = {}
    for i in old:
        a = decl_set(old[i]["settings"].get("_cls", []), oldF)
        b = decl_set(new[i]["settings"].get("_cls", []), newF)
        if a != b:
            key = (tuple(sorted(a - b)), tuple(sorted(b - a)))
            bad[key] += 1
            examples.setdefault(key, (i, old[i]["settings"].get("_cls"), new[i]["settings"].get("_cls")))
    print("elements:", len(old), "| with a different declaration set:", sum(bad.values()))
    for (lost, gained), n in bad.most_common():
        print(f"\n x{n} e.g. {examples[(lost, gained)]}\n    lost:   {lost}\n    gained: {gained}")
    unused = [n for n in newF if not any(n in e["settings"].get("_cls", []) for e in new.values())]
    print("\nclasses:", len(oldF), "->", len(newF), "| css bytes:", sum(map(len, oldF.values())), "->", sum(map(len, newF.values())), "| unused:", unused)


if __name__ == "__main__":
    if "--verify" in sys.argv:
        i = sys.argv.index("--verify")
        verify(sys.argv[i + 1], sys.argv[i + 2])
    else:
        F = load_final()
        res, warn = plan(F)
        report(res, warn, F)
        if "--apply" in sys.argv:
            apply(res)
