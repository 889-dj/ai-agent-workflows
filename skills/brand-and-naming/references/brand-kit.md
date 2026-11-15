# Brand kit for the chosen name

Keep it to what a solo builder will actually use. One page: `brand/BRAND.md`.

## 1. Positioning and tagline

- **One-line positioning**: "For <specific person>, <name> is the <category> that
  <one differentiator>, unlike <incumbent>." Every claim must be true of the v1.
- **Tagline**: 3 options, under 8 words, each in a different register (plain, punchy,
  warm). Say which one you would use. Taglines must not promise what v1 will not do or
  make medical or financial claims.

## 2. Voice

Three traits (for example: calm, direct, a little dry), then two example lines per
channel (button, error message, store description) showing the voice, and a short
do/don't list ("do say 'Saved', don't say 'Awesome! Your run was saved! 🎉'"). The voice
should match the user's answer to the copy-voice question in the landing-page skill.

## 3. Visual direction mapped to a theme

Pick the landing-page theme from the feel, then suggest an accent. The accent must keep
readable button text (the landing-page fill script enforces contrast).

| Feel | Theme | Accent starting points |
|---|---|---|
| sleek, technical, fast | `midnight` | lime `#c6ff3d`, cyan `#35e0ff`, amber `#ffb020` |
| calm, trustworthy, grown-up | `paper` | ultramarine `#1c3dff`, ink red `#c9341d`, forest `#14633a` |
| bold, playful, loud | `pop` | tomato `#ff4b2b`, pink `#ff4fa3`, electric blue `#2b59ff` |
| gentle, caring, organic | `calm` | forest `#2c6a4c`, dusty blue `#3a6ea5`, plum `#7a4a6d` |

Name the type feel in words (geometric sans, editorial serif, rounded sans, mono
numerals) and the shape language (sharp, soft, pill). If no built-in theme fits, say what
a custom theme needs.

## 4. Icon concepts (three, as briefs)

Describe each as a shape idea in words and a colour pair, with the reasoning. Do not
generate or copy existing marks. Constraints: simple enough to read at about 29 px,
one focal shape, no text, no photo, no gradient noise, no look-alike to an incumbent's
icon, and a square master (the App Store requires a 1024 px square without transparency;
verify the current spec). Suggest how to try them: a quick vector draft, then a
screenshot at 60, 40 and 29 px beside the competitors' icons.

## 5. Store name and subtitle

- **Name**: the chosen name, optionally with a short keyword after a separator if there
  is room. Keep within the store's limit (30 characters at the time of writing; verify).
- **Subtitle**: 3 options within the limit (30 characters at the time of writing;
  verify), plain language, the main benefit, no pricing claims or competitor names.
- Keep keywords for the launch step; do not stuff them here.

## 6. Handoff block

```
APP_NAME: <name>      THEME: <midnight|paper|pop|calm|path>     ACCENT: <hex or default>
VOICE: <3 traits>     HEADLINE VOICE: <calm and confident | bold and punchy | warm and friendly>
DIRECTION FAMILY for the UI build: <e.g. dark + single lime accent, athletic>
STORE NAME / SUBTITLE: <...>
```
