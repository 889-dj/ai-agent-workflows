---
name: competitor-teardown
description: Take one to three competitor apps apart - positioning, onboarding and core flow, paywall and pricing, review complaints, traction signals, recent changes and UI patterns - with every finding sourced and tagged by trust level, then turn it into table stakes, weak spots to exploit, and concrete handoffs for scoping, pricing, UI and naming. Use when someone asks to analyse, dissect or benchmark a competitor or incumbent app, asks what a rival does well or badly, or wants evidence before scoping, pricing or designing a product.
---

# Competitor Teardown

Guessing about competitors produces copycat products and invented prices. This
skill replaces guessing with a sourced teardown: what the incumbent really does,
where its users are unhappy, what it charges, and what that means for your v1.

Output: `research/teardown.json` (the findings), `research/TEARDOWN.md` (the
analysis) and `research/matrix.md` (a side-by-side table). Keep them out of the
skill directory.

## Rules that are not optional

1. **No source, no finding.** Every finding carries an https URL and a date. If
   you cannot source it, record it as `unknown` with the lookup that would settle it.
   `scripts/teardown_check.py` enforces this and fails on violations.
2. **Tag every finding**: `verified` (read directly from the first-party page or
   store listing), `reported` (a secondary source states it), `estimated` (a tool or
   an inference; say how in `note`), `unknown` (could not be established).
3. **A failed lookup is not a null result.** A blocked page, a timeout, or a login
   wall is `unknown`. "I looked properly and found nothing" is a finding; "I could
   not look" is not. A lens nobody covered is reported as NOT COVERED.
4. **Never invent a number**: prices, revenue, downloads, ratings counts, review
   counts. Read it, cite it, or mark it unknown.
5. **Paraphrase reviews**; quote under 15 words, never include reviewer names.
6. **Borrow patterns, never assets**: no logos, copy, screenshots or illustrations
   reused as your own. Describe what they do, not what they look like to copy.
7. **Stay within what is public.** Do not log in to accounts, bypass paywalls,
   scrape behind a login, or enter credentials. Pages that look empty are usually
   still loading: wait, scroll, read the text, retry once; only a repeated 403/429,
   a captcha or a login wall is blocked. Never bypass a block.
8. **Not legal advice.** Report observed pricing and practices as observations.

## Inputs

- The competitor(s): one primary, up to two secondary. If the user did not name
  them, take the top apps from the category's store search and confirm in one line.
- Context if it exists: an `app-idea-hunter` dossier, `design/MVP.md`,
  `design/MONETIZATION.md`. Ask at most one question, and only if the answer changes
  which apps you tear down.
- Optional access that improves quality: a connected scraper (store reviews), a
  design-reference connector (flows and screenshots), or screen recordings and
  screenshots the user can share from their own device.

## Steps

1. **Frame.** State the product, the competitors chosen and why, and the one
   decision this teardown must inform (scope, price, design, naming). Write it at the
   top of `TEARDOWN.md`.
2. **Collect by lens.** The lenses are in `references/lenses.md`, each with a brief,
   the sources to try and the exact row format. If subagents exist, give each lens
   to a cheap worker with the brief pasted in (workers cannot read the skill folder),
   one competitor per lens call, and review every return yourself. If not, run the
   lenses inline at reduced breadth and say so. Lenses: `positioning`, `onboarding`,
   `paywall`, `pricing`, `reviews`, `traction`, `changes`, `ui`.
3. **Record and check.** Put every finding in `research/teardown.json` (schema in the
   script's docstring), then run
   `python3 scripts/teardown_check.py research/teardown.json --check`. Fix every
   error. Then `python3 scripts/teardown_check.py research/teardown.json > research/matrix.md`.
4. **Synthesize** into `research/TEARDOWN.md` using `assets/teardown-template.md`.
   Do not paste raw worker output. The sections that matter:
   - **Table stakes**: what every competitor does that users now expect (match it).
   - **Weak spots**: recurring, sourced complaints and gaps, ranked by how many
     reviews or competitors show them, with the count and sample size.
   - **The wedge**: the specific person and the one complaint a smaller product can
     fix, and why an incumbent will not simply fix it.
   - **Pricing read**: what they charge, how they gate, how users react.
   - **Do not copy**: patterns that users resent.
   - **Confidence**: what is verified, what is reported, what is unknown.
5. **Handoffs.** Write the specific lines other skills can use, and say where to
   put them: features to cut or add for `mvp-scoper`; the price map rows and the
   paywall reactions for `monetization-designer` (replace any `unknown` prices);
   UI patterns, motion and anti-patterns for `mobile-ui-pipeline-v2`; incumbent names
   to avoid resembling for `brand-and-naming`; the only comparison claims that are
   safe to put on a landing page (each with its source) for `landing-page-smoke-test`.

## Quality bar

- Every row in the matrix is traceable to a URL and a date.
- At least the pricing, reviews and paywall lenses are covered for the primary
  competitor, or the report says plainly why not.
- Sample sizes are stated (reviews read, date range, store and country).
- The wedge is falsifiable: it names the evidence that would disprove it.

## Handoff note

State the files written, which lenses are complete or partial, the biggest unknowns
and how to settle each, and that nothing was purchased, installed, or logged into.
