#!/usr/bin/env python3
"""Fill assets/page-template.html from a JSON file of {TOKEN: value} and apply a theme.

Usage:
  fill_template.py TEMPLATE.html VALUES.json OUT.html
  fill_template.py --themes                      # list built-in themes and what they suit

VALUES.json keys:
  THEME     built-in name (midnight | paper | pop | calm) or a path to a custom .css theme
            (copy assets/themes/_custom-template.css). Default: midnight.
  ACCENT    optional hex that overrides the theme's accent; the button text colour is
            chosen automatically for contrast.
  HEADLINE  may mark accent words with asterisks: "A run tracker that *never sells you* anything."
            The script derives HEADLINE_HTML (animated word spans) and HEADLINE_PLAIN.
  FORM_ENDPOINT may be left unset: the page then says "not connected yet" instead of faking success.

Exits 1 if any other token is unfilled or if a contrast pair is below WCAG AA (4.5:1).
"""
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEMES = HERE.parent / "assets" / "themes"
# Tokens the template places inside JavaScript string literals (may also contain simple HTML, e.g. <strong>).
JS_TOKENS = {"CURRENCY", "SPEND_ZERO_MSG", "SPEND_MSG", "PICKS_LIMIT", "PICKS_DONE"}

def headline_html(text):
    out, accent = [], False
    for part in re.split(r"(\*)", text):
        if part == "*":
            accent = not accent
            continue
        for w in part.split():
            w = html.escape(w)
            out.append(f'<span class="w"><span>{"<em>%s</em>" % w if accent else w}</span></span>')
    return " ".join(out)

def theme_meta(css):
    return dict(re.findall(r"@meta ([\w-]+):\s*(.+)", css))

def find_theme(name):
    p = Path(name)
    if "/" in name or name.endswith(".css"):
        return p
    return THEMES / f"{name}.css"

def list_themes():
    for f in sorted(THEMES.glob("*.css")):
        if f.name.startswith("_"): continue
        m = theme_meta(f.read_text(encoding="utf-8"))
        print(f"{f.stem:9} {m.get('color-scheme','?'):5} {m.get('vibe','')}\n{'':15}best for: {m.get('best-for','')}")

# ---- contrast ----
def _lin(c):
    c /= 255
    return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
def lum(hexc):
    h = hexc.lstrip("#"); h = "".join(c*2 for c in h) if len(h) == 3 else h
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return .2126*_lin(r) + .7152*_lin(g) + .0722*_lin(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)
def pick_ink(accent):
    return "#0a0a0b" if ratio(accent, "#0a0a0b") >= ratio(accent, "#ffffff") else "#ffffff"
def var(css, name, default=None):
    m = re.findall(r"--%s:\s*(#[0-9a-fA-F]{3,6})\b" % re.escape(name), css)
    return m[-1] if m else default

def main(tpl_path, values_path, out_path):
    s = open(tpl_path, encoding="utf-8").read()
    v = json.load(open(values_path, encoding="utf-8"))

    # --- theme ---
    theme_file = find_theme(v.get("THEME", "midnight"))
    if not theme_file.is_absolute() and not theme_file.exists():
        theme_file = Path(values_path).resolve().parent / theme_file
    if not theme_file.exists():
        sys.exit(f"theme not found: {v.get('THEME')}")
    css = theme_file.read_text(encoding="utf-8")
    meta = theme_meta(css)
    base_css = (THEMES / "midnight.css").read_text(encoding="utf-8")
    if v.get("ACCENT"):
        acc = v["ACCENT"]
        css += f"\n:root{{--accent:{acc};--accent-ink:{pick_ink(acc)};}}\n"
    css = re.sub(r"/\*.*?\*/", "", css, count=1, flags=re.S) if css.lstrip().startswith("/*") else css
    fonts = meta.get("fonts", "").replace("&", "&amp;")
    s = s.replace("/*{{THEME_CSS}}*/", css).replace("{{FONTS_URL}}", fonts)   # the slot is a CSS comment in the raw template
    s = s.replace("{{COLOR_SCHEME}}", meta.get("color-scheme", "dark")).replace("{{THEME_BG}}", meta.get("bg", "#0a0a0b"))
    if "{{THEME_CSS}}" in s: sys.exit("template has no theme slot")

    # --- contrast gate (reads the theme, falling back to template defaults) ---
    d = {"bg": "#0a0a0b", "text": "#f4f4f2", "mute": "#9a9aa3", "accent": "#c6ff3d", "accent-ink": "#0a0a0b", "surface": "#131316"}
    for k in d:
        d[k] = var(css, k, d[k])
    bad = []
    for label, a, b in (("text on bg", d["text"], d["bg"]), ("muted text on bg", d["mute"], d["bg"]),
                        ("muted text on surface", d["mute"], d["surface"]), ("button text on accent", d["accent-ink"], d["accent"])):
        r = ratio(a, b)
        if r < 4.5: bad.append(f"{label}: {a} on {b} = {r:.1f}:1")

    # --- copy ---
    raw = v["HEADLINE"]
    v["HEADLINE_HTML"] = headline_html(raw)
    v["HEADLINE_PLAIN"] = html.escape(raw.replace("*", ""), quote=True)
    v["HEADLINE"] = raw.replace("*", "")
    v.setdefault("NAV_CTA", v.get("CTA_LABEL", "Join the waitlist"))
    v.setdefault("YEAR", "2026")
    for k, val in v.items():
        if k in ("THEME", "ACCENT"):
            continue
        if k == "HEADLINE_HTML":
            rep = str(val)
        elif k in JS_TOKENS:
            rep = json.dumps(str(val), ensure_ascii=False)[1:-1].replace("</", "<\\/")
        else:
            rep = html.escape(str(val), quote=True)
        s = s.replace("{{%s}}" % k, rep)
    left = sorted(set(re.findall(r"\{\{(\w+)\}\}", s)) - {"FORM_ENDPOINT"})
    open(out_path, "w", encoding="utf-8").write(s)
    print(f"theme: {meta.get('name', theme_file.stem)} ({meta.get('color-scheme','dark')})")
    if bad:
        print("LOW CONTRAST (fix the theme or ACCENT):\n  " + "\n  ".join(bad)); sys.exit(1)
    if left:
        print("UNFILLED TOKENS:", ", ".join(left)); sys.exit(1)
    if "{{FORM_ENDPOINT}}" in s:
        print("note: FORM_ENDPOINT not set; the form will say 'not connected yet'. Set an https endpoint to go live.")
    print("wrote", out_path)

if __name__ == "__main__":
    if sys.argv[1:] == ["--themes"]: list_themes()
    elif len(sys.argv) != 4: sys.exit(__doc__)
    else: main(*sys.argv[1:])
