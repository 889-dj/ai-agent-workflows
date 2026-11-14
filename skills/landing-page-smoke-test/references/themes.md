# Themes: one look per idea

A theme is a CSS file in `assets/themes/` that sets design tokens (colour, type,
shape, atmosphere, phone interior) and may add a few structural rules. The page
template reads only those tokens, so a theme changes everything, not just colour.
List them with `python3 scripts/fill_template.py --themes`.

## Built-in themes

| Theme | Look | Hero | Suits |
|---|---|---|---|
| `midnight` | dark, sleek, glowing lime accent, mono numerals | split | fitness, dev tools, AI tools, productivity, crypto, anything fast and technical |
| `paper` | light, editorial serif, hairlines, flat, ultramarine accent | split | finance, writing, education, B2B, anything that should feel trustworthy and considered |
| `pop` | flat yellow, chunky outlines, hard shadows, giant centred headline | stacked | consumer apps, games, social, food, creators, students, anything fun and loud |
| `calm` | soft sage, rounded, serif headlines, gentle shadows | split | wellness, health, meditation, sleep, habits, family, anything gentle |

Pick the default for the product category, but the user's choice always wins. Do not
reuse the same theme and accent for two different ideas in one project unless asked.

## Asking the user

Use one `AskUserQuestion` call: (1) the look, recommended theme first, with "Other"
for "describe the taste / name a reference site / give an accent colour"; (2) the
copy voice (calm and confident, bold and punchy, warm and friendly). Never choose
silently unless the user said to just do it, and then state the choice.

## Tweaking a theme

- Accent only: set `"ACCENT": "#hex"` in the values JSON. The script picks a readable
  button text colour automatically.
- Anything else, or a new look: copy `assets/themes/_custom-template.css` to the
  project (e.g. `smoke-test/theme.css`), edit the tokens, and set
  `"THEME": "smoke-test/theme.css"`. Choose fonts that fit the product: one display
  face and one mono, from Google Fonts, set in the `@meta fonts:` line. Avoid
  defaulting to Inter, Roboto or Arial.
- Structural changes (a centred hero, a different card style) go at the bottom of the
  theme file as ordinary CSS; the theme loads before the template's mobile rules, so
  the mobile layout still works.

## Quality gates (the fill script enforces the first)

- Contrast of text on background, muted text on background and surface, and button
  text on accent must be at least 4.5:1, or the script exits with an error.
- A theme must keep the phone interior readable on its own (`--p-*` tokens).
- After building, open it: confirm `--bg` actually changed (a theme that fails to load
  silently falls back to Midnight), screenshot desktop and mobile, and use the
  interactions. See "Verify in a browser" in `SKILL.md`.
