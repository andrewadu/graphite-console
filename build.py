#!/usr/bin/env python3
"""Build the Graphite Console docs site.

Reads tokens.json and components/<Name>/{README.md,preview.html}, writes:
  tokens.css        CSS custom properties + type classes (generated)
  index.html        the gallery (all components, both themes)
  components/<Name>/index.html   a standalone page per component
"""
import json, re, html, os, pathlib

ROOT = pathlib.Path(__file__).parent
t = json.load(open(ROOT / "tokens.json"))
themes = [th["id"] for th in t["color"]["themes"]]


def val(tok, th):
    v = tok["value"]
    s = v if isinstance(v, str) else v.get(th, v[themes[0]])
    m = re.fullmatch(r"\{([A-Za-z0-9_.-]+)\}", s)
    return f"var(--{m.group(1)})" if m else s


# ---------- tokens.css ----------
css = ["/* Graphite Console. Generated from tokens.json by build.py; edit tokens.json, not this file. */\n"]
css.append(f':root, [data-theme="{themes[0]}"] {{\n  color-scheme: light;\n'
           + "".join(f'  --{c["name"]}: {val(c, themes[0])};\n' for c in t["color"]["tokens"])
           + "".join(f'  --{s["name"]}: {s["value"]};\n' for s in t.get("shadow", {}).get("tokens", []))
           + "}\n")
for th in themes[1:]:
    css.append(f'[data-theme="{th}"] {{\n  color-scheme: dark;\n'
               + "".join(f'  --{c["name"]}: {val(c, th)};\n' for c in t["color"]["tokens"]) + "}\n")
css.append(":root {\n"
           + "".join(f'  --{s["name"]}: {s["value"]};\n' for fam in ("spacing", "radius") for s in t[fam]["tokens"])
           + "".join(f"  --font-{k}: {v};\n" for k, v in t["type"]["families"].items()) + "}\n")
for g in t["type"]["groups"]:
    for s in g["styles"]:
        ls = f' letter-spacing: {s["letterSpacing"]};' if "letterSpacing" in s else ""
        css.append(f'.{s["name"]} {{ font: {s["fontWeight"]} {s["fontSize"]}/{s["lineHeight"]} var(--font-{g["family"]});{ls} }}\n')
(ROOT / "tokens.css").write_text("".join(css))

# ---------- components ----------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fira+Code:wght@400&display=swap" rel="stylesheet">')
comps = []
for d in sorted((ROOT / "components").iterdir()):
    p = d / "preview.html"
    if not p.exists() or d.name == "Cover":
        continue
    src = p.read_text()
    first, body = src.split("\n", 1)
    meta = {k: (a or b) for k, a, b in re.findall(r'(\w+)=(?:"([^"]*)"|(\d+))', first)}
    readme = (d / "README.md").read_text() if (d / "README.md").exists() else ""
    desc = re.sub(r"^#.*\n+", "", readme).strip()
    comps.append(dict(name=d.name, group=meta.get("group", "Other"), height=int(meta.get("height", 120)),
                      subtitle=meta.get("subtitle", ""), body=body, desc=desc))

cover = (ROOT / "components/Cover/preview.html").read_text().split("\n", 1)[1]


def frame(c, theme_attr):
    doc = (f'<!doctype html><html data-theme="{theme_attr}"><head><meta charset="utf-8">{FONTS}'
           f'<link rel="stylesheet" href="tokens.css"><style>html,body{{margin:0;background:var(--background)}}body{{overflow:hidden}}</style></head>'
           f'<body>{c["body"]}</body></html>')
    return doc


def page(c):
    return f'''<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>{c["name"]} · Graphite Console</title>
<meta name="viewport" content="width=device-width,initial-scale=1">{FONTS}<link rel="stylesheet" href="../../tokens.css"><link rel="stylesheet" href="../../site.css"></head>
<body><header class="top"><a href="../../">Graphite Console</a><span class="crumb">/ {c["group"]} / {c["name"]}</span><button class="btn" onclick="toggle()">Toggle theme</button></header>
<main class="page"><h1 class="display">{c["name"]}</h1><p class="small muted">{html.escape(c["subtitle"])}</p>
<div class="frame" style="min-height:{c["height"]}px">{c["body"]}</div>
<h2 class="title">Guidelines</h2><p>{html.escape(c["desc"])}</p>
<h2 class="title">Markup</h2><pre class="code"><code>{html.escape(c["body"].strip())}</code></pre></main>
<script src="../../site.js"></script></body></html>'''


for c in comps:
    (ROOT / "components" / c["name"] / "index.html").write_text(page(c))

groups = {}
for c in comps:
    groups.setdefault(c["group"], []).append(c)
order = ["Actions", "Forms", "Data display", "Navigation", "Overlays", "Feedback", "Pages", "Other"]
nav = "".join(f'<a href="#{g.lower().replace(" ", "-")}">{g}</a>' for g in order if g in groups)
sections = ""
for g in order:
    if g not in groups:
        continue
    cards = ""
    for c in groups[g]:
        cards += (f'<article class="card" id="c-{c["name"]}"><div class="card-h"><a href="components/{c["name"]}/">{c["name"]}</a>'
                  f'<span class="small muted">{html.escape(c["subtitle"])}</span></div>'
                  f'<iframe class="pv" title="{c["name"]} preview" loading="lazy" height="{c["height"]+34}" srcdoc="{html.escape(frame(c, "light"), quote=True)}"></iframe></article>')
    sections += f'<section id="{g.lower().replace(" ", "-")}"><h2 class="title">{g}</h2>{cards}</section>'

colors = "".join(f'<div class="sw"><i style="background:var(--{c["name"]})"></i><b>{c["name"]}</b><span class="small muted">{html.escape(c["usage"][:70])}</span></div>'
                 for c in t["color"]["tokens"] if not isinstance(c["value"], dict) or not c["value"]["light"].startswith("{"))
types = "".join(f'<div class="ty"><span class="{s["name"]}">{html.escape(s.get("sample", s["name"]))}</span><span class="small muted">{s["name"]} · {s["fontSize"]}/{s["lineHeight"]} · {s["fontWeight"]}</span></div>'
                for g in t["type"]["groups"] for s in g["styles"])

index = f'''<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>Graphite Console</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A design system for backoffice consoles and system-admin tools.">{FONTS}
<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="site.css"></head>
<body><header class="top"><a href="./">Graphite Console</a><nav>{nav}<a href="#tokens">Tokens</a></nav><button class="btn" onclick="toggle()">Toggle theme</button></header>
<div class="cover">{cover}</div>
<main class="page">
<p class="lede">A design system for backoffice consoles and system-admin tools. {len(comps)} components, light and dark, built on shadcn/ui token names so <code>tokens.css</code> drops straight into a Next.js console. <a href="DESIGN.md">Read the brand book</a> · <a href="https://github.com/andrewadu/graphite-console">Source</a></p>
{sections}
<section id="tokens"><h2 class="title">Colour tokens</h2><div class="swatches">{colors}</div>
<h2 class="title">Type scale</h2><div class="types">{types}</div></section>
</main><script src="site.js"></script></body></html>'''
(ROOT / "index.html").write_text(index)
print(f"built {len(comps)} components")
