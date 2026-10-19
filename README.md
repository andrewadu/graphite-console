# Graphite Console

A design system for backoffice consoles and system-admin tools: 38 components, light and dark themes, built on shadcn/ui token names so it drops straight into a Next.js console.

Live site: https://andrewadu.github.io/graphite-console/

## Use it

- `tokens.css`: every colour (light and dark), spacing, radius, shadow and type style as CSS custom properties. Paste into `globals.css`, or `<link>` it. Switch themes with `<html data-theme="dark">`.
- `tokens.json`: the source of truth, in the shape the Claude Design System artifact and `build.py` read.
- `components/<Name>/preview.html`: reference markup for each component, styled only with the tokens; `components/<Name>/README.md` holds the usage guidelines.
- `DESIGN.md`: the brand book (principles, colour rules, type, spacing, iconography, content).

## Develop

```sh
python3 build.py          # regenerates tokens.css, index.html and components/*/index.html
python3 -m http.server    # then open http://localhost:8000
```

Edit `tokens.json` or a component's `preview.html`/`README.md`, rebuild, commit. GitHub Pages deploys from `main` on every push.
