---
name: brand-and-naming
description: Name an app and give it a basic brand - generate dozens of name candidates across proven strategies, screen them for domain, App Store and look-alike conflicts with a script that never reports a failed lookup as "available", rank a shortlist for the user to pick, then produce a brand kit (tagline, voice, visual direction mapped to a landing-page theme, icon concepts, store name and subtitle). Use when someone needs a name for an app or product, wants to check if a name is taken, or asks for branding, a tagline, voice, or icon direction.
---

# Brand and Naming

A name is hard to change once people have found it. This skill makes the choice
deliberately: wide candidates, honest conflict checks, a ranked shortlist the user
decides on, and then a brand kit that the rest of the pipeline can use.

Output (in the project, not the skill folder): `brand/NAMES.md` (candidates, screen
results, shortlist), `brand/BRAND.md` (the kit for the chosen name).

## Rules that are not optional

1. **Never say a name is available unless a check said so, and say which check.**
   `unknown` stays `unknown`. A domain "not found" is `likely-available`; premium or
   reserved names look the same, so confirm at a registrar.
2. **The user picks the name.** Present a ranked shortlist with reasons and ask;
   do not choose silently and build the brand around your favourite.
3. **Not legal advice.** The script does not check trademarks. State that, give the
   search links in the checklist, and recommend a trademark attorney before the
   user invests in a name.
4. **Never imitate.** No names that resemble an incumbent, a famous brand, or a real
   person. If the user asks for one, explain the risk and offer alternatives.
5. **Do not register, buy, or claim anything** (domains, handles, store names). The
   user does that.
6. **Cultural and language checks are flagged, not claimed.** You can spot obvious
   problems; you cannot certify a name is safe in every language. Say which
   languages and markets you considered.

## Inputs

Take them in this order and do not re-ask what they answer: a `design/MVP.md` or an
`app-idea-hunter` dossier (what it does, who it is for, platform); a
`competitor-teardown` (incumbent names to avoid resembling); the user's words.

## Steps

1. **Ask what taste they want** (never default silently). One `AskUserQuestion`,
   at most 3 questions, skipping any the inputs already answer:
   - **Name style**: *Short and invented* (e.g. Strava, Figma: ownable, needs
     explaining), *Plain and descriptive* (says what it does, easy to search, harder to
     own), *Evocative* (a metaphor or feeling, e.g. Stride), or Other.
   - **Feel**: calm and trustworthy / bold and playful / sleek and technical / warm
     and friendly (this also picks the landing-page theme later).
   - **Constraints**: must or must not contain a word, target markets and languages,
     maximum length, a domain TLD they need. Free text.
   Skip the questions only if the user says to just do it; then state the style you
   chose and why.
2. **Write the naming brief** (5 lines in `NAMES.md`): what the name must do, who
   hears it first, the feel, the constraints, the names to avoid resembling.
3. **Generate 30 to 40 candidates** across the strategies in
   `references/naming-strategies.md`, each with a one-line rationale. Aim for variety,
   not 40 versions of one idea. Drop anything that fails the quick tests in that file.
4. **Screen the survivors** (about 15 to 20) with the script:
   `python3 scripts/check_names.py --names "A,B,C" --tlds com,app,io --competitors "<incumbents>"`
   It checks domains (RDAP), App Store collisions (iTunes Search) and look-alikes, and
   labels each name conservatively. Read the verdicts: `incomplete-check` means a
   lookup failed and you must retry or flag it; `clear-so-far` only means the
   automated checks found nothing. If the network is blocked, say so and treat every
   name as unchecked.
5. **Manual checks for the final 5 to 8** (the script cannot do these; give the user
   the checklist in `references/naming-strategies.md`): trademark search (USPTO,
   EUIPO, WIPO), Google Play, social handles, a web search for "<name> app", and
   meaning in the main languages of the target markets.
6. **Rank and ask.** Score the shortlist on the criteria in the reference, show the
   top 5 with the reasoning, evidence of each check and any open risk, say which you
   would pick and why, then ask the user to choose with `AskUserQuestion` (or accept a
   different name, which you then screen the same way).
7. **Brand kit** (`brand/BRAND.md`) for the chosen name, using
   `references/brand-kit.md`: tagline options, one-line positioning, voice (traits and
   do/don't examples), visual direction mapped to a landing-page theme and accent
   (Midnight, Paper, Pop, Calm or custom), three icon concepts, and App Store name and
   subtitle candidates within the store's length limits.
8. **Handoffs.** Give the exact values for `landing-page-smoke-test` (`APP_NAME`,
   `THEME`, `ACCENT`, headline voice), for `mobile-ui-pipeline-v2` (direction family,
   accent, type feel), and the store name and subtitle for the future launch step.

## Handoff note

State the files written, the chosen name, every check that ran and its result, every
check that did NOT run and who must do it, and that nothing was registered or bought.
