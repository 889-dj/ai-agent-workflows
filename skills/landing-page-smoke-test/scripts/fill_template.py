#!/usr/bin/env python3
"""Fill assets/page-template.html from a JSON file of {TOKEN: value}.

Usage: fill_template.py TEMPLATE.html VALUES.json OUT.html

HEADLINE may mark accent words with asterisks: "A run tracker that *never sells you* anything."
The script derives HEADLINE_HTML (animated word spans), HEADLINE_PLAIN and strips
the asterisks from HEADLINE. FORM_ENDPOINT may be left unset: the page then shows an
honest "not connected" message instead of a fake success. Exits 1 if any other token is unfilled.
"""
import html, json, re, sys

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

def main(tpl_path, values_path, out_path):
    s = open(tpl_path, encoding="utf-8").read()
    v = json.load(open(values_path, encoding="utf-8"))
    raw = v["HEADLINE"]
    v["HEADLINE_HTML"] = headline_html(raw)
    v["HEADLINE_PLAIN"] = html.escape(raw.replace("*", ""), quote=True)
    v["HEADLINE"] = raw.replace("*", "")
    v.setdefault("NAV_CTA", v.get("CTA_LABEL", "Join the waitlist"))
    v.setdefault("ACCENT", "#C6FF3D")
    v.setdefault("YEAR", "2026")
    for k, val in v.items():
        s = s.replace("{{%s}}" % k, str(val) if k in ("HEADLINE_HTML",) else html.escape(str(val), quote=False))
    left = sorted(set(re.findall(r"\{\{(\w+)\}\}", s)) - {"FORM_ENDPOINT"})
    open(out_path, "w", encoding="utf-8").write(s)
    if left:
        print("UNFILLED TOKENS:", ", ".join(left)); sys.exit(1)
    if "{{FORM_ENDPOINT}}" in s:
        print("note: FORM_ENDPOINT not set; the form will say 'not connected yet'. Set an https endpoint to go live.")
    print("wrote", out_path)

if __name__ == "__main__":
    if len(sys.argv) != 4: sys.exit(__doc__)
    main(*sys.argv[1:])
