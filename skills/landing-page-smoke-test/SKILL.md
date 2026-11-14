---
name: landing-page-smoke-test
description: Build a fake-door landing page (headline, proof, email waitlist, optional price test) plus drop-target threads and launch posts to find out whether real people want an app before any app code is written, with a pre-registered pass/fail bar. Use when someone wants to validate demand, test an idea before building, make a waitlist or landing page, or after app-idea-hunter's "Next 48 hours" step.
---

# Landing Page Smoke Test

Cheapest honest answer to "will anyone want this": show the promise, ask for a
commitment, count. This skill produces the page, the traffic plan, and the bar
for deciding - before the test runs, so results cannot be rationalized.

**Nothing is published, posted, or sent by this skill.** It writes drafts to
files and stops. Deploying, posting, and DMing are the user's decisions.

## Inputs

An `app-idea-hunter` dossier (use "The wedge", the Pain quotes, "Next 48 hours"
and the drop targets) or `design/MVP.md` from `mvp-scoper`. Otherwise ask, in one
call, at most 3 questions: who exactly it is for, the one problem it fixes, and
where those people hang out. Use the user's own words from the evidence for the
headline whenever possible - paraphrase real complaints, never invent quotes.

## Steps

1. **Pre-register the test** (write this first, in `smoke-test/PLAN.md`):
   - Primary metric: signups, and the traffic source for each.
   - **The bar**: default 10 signups in 7 days from targeted traffic (matches the
     dossier). Higher, e.g. 30, if traffic is paid.
   - **Decision rule**: >= bar -> build; between 50% and 100% of bar -> one
     iteration of headline/audience, rerun once; under 50% -> move to the next
     candidate. Do not rescue a failing idea by moving the goalposts.
2. **Choose the look (ask; never default silently).** Two ideas must not get the
   same page. Run `python3 scripts/fill_template.py --themes` to see the built-in
   themes, then ask the user in ONE `AskUserQuestion` call (max 2 questions):
   - **Look**: offer the four themes by name with one-line vibes (Midnight: dark and
     technical; Paper: light and editorial; Pop: loud, flat colour, chunky
     outlines; Calm: soft sage and rounded), put the one that best fits the product
     category first and mark it "(Recommended)" using the table in
     `references/themes.md`. "Other" lets them describe a taste, name a reference
     site, or give an accent colour; build that as a custom theme (see
     `references/themes.md`).
   - **Voice** for the copy: calm and confident / bold and punchy / warm and
     friendly. It changes the headline, subhead and microcopy, not just the colours.
   Skip the question only if the user already said what they want or told you to
   just do it; then pick by category, state the choice in one line, and never reuse
   the theme and accent of another idea the user has already built this session.
   Record the choice in `smoke-test/PLAN.md`.
3. **Page copy** (`smoke-test/COPY.md`), in this order, in the voice the user chose:
   - Headline: the outcome for a specific person, no jargon, under ~12 words.
     Offer 3 variants for A/B.
   - Subhead: how, in one sentence.
   - Three proof points: concrete pains solved, each traceable to evidence.
   - Social proof: only real. If none exists, omit - never fabricate testimonials,
     user counts, ratings, or logos.
   - Primary CTA: one email field and one button, with honest wording ("Get early
     access", not "Download now"). Do not imply the product exists if it doesn't.
   - Optional price test (see below).
   - Footer: a line saying it is in development, a privacy note, and an unsubscribe
     promise.
4. **Page build** (`smoke-test/index.html`): an interactive, premium single-file
   page, not a brochure. Read `references/design-standards.md` first; it is the
   quality bar. Write the copy into a JSON file (see `assets/example-values.json`)
   and fill `assets/page-template.html` with `scripts/fill_template.py`, setting
   `"THEME"` to the chosen look. A visitor
   needs a reason to commit, so the template gives them three things to *do*:
   - **A working preview of the core loop** in a phone mock (tap Start and the run
     plays out live). When it finishes, the CTA appears at the moment of delight.
     Adapt the mock to the product's real core loop (see `design/MVP.md`).
   - **A personal-stakes calculator** (here: a "what do you spend a year" slider
     with a live 3-year total). Replace it with whatever makes the pain
     personal for this product, using only numbers the visitor supplies or you
     can source. Never invent a competitor price.
   - **A vote-for-what-we-build-first picker** (up to 3 chips) that builds a
     "Your <app>" card next to the email field. Take the chips from the MVP's
     Defer list. The votes and slider value are posted with the email, so the
     smoke test also yields demand data.
   Plus an animated headline, a "what it will never do" strip, benefit cards, a
   mobile dock CTA, GSAP + ScrollTrigger + Lenis motion that degrades to a
   complete static page, and an honest form (it shows "not connected yet" until a
   real https endpoint is set, never a fake success). Change the design, not just
   the words, if the default look does not suit the category. Optionally study
   the design skills listed in the standards file, but never install third-party
   skills without telling the user.
5. **Price test (optional, only if the user wants it):** after the email field,
   show the intended plan and price and a "Notify me when it launches" confirm
   step, or a two-variant split of prices across two URLs. Be explicit on the page
   that nothing is charged. Do not collect payment details for a product that
   does not exist.
6. **Traffic plan** (`smoke-test/TRAFFIC.md`): specific places, not channels. For
   each: the exact thread/community, why the post is a genuine answer, and the
   draft post. Follow each community's self-promotion rules; check them and say
   when a rule would forbid the post. Disclose that you built the thing. Draft
   posts for X/LinkedIn/Instagram as well. Never astroturf: no fake accounts, no
   fake upvotes, no pretending to be a user.
7. **Verify in a browser** (do not skip): screenshot at 1440x900 and 390x844 after
   the intro, scroll the whole page, and *use* it: play the preview to the end,
   drag the slider (including 0), pick 3 chips and a 4th, submit with a bad
   email and with `?demo`. Confirm no horizontal overflow, no console errors,
   the form visible above the fold on mobile, the dock showing mid-page and
   hiding at the form, and that the page still works with the CDN scripts
   blocked and with reduced motion on. Fix anything that looks generic or broken
   before handoff; if no browser is available, say what was not seen.
8. **Readout template** (`smoke-test/RESULTS.md`): a blank table for visits,
   signups, conversion by source and headline, which preview/slider/vote interactions
   visitors used, the vote tally per feature, plus the decision rule copied
   from step 1, ready to fill in.

## Rules

- Looks matter: a page that looks like a template will not earn an email. Meet
  every item in `references/design-standards.md`.
- Honesty beats conversion: no fabricated social proof, no fake scarcity, no
  claim the app does something it will not.
- Collect the minimum: email only. State what it is used for.
- Comply with applicable email/consent law for the user's audience; mention it
  once in the handoff if the audience is in the EU/UK.
- Report conversion honestly, including small-sample caveats (10 signups from 30
  visits is signal; 2 from 2000 is a verdict).

## Handoff

List the files written, what the user must do (deploy the page, connect the form,
post), the bar and the decision rule, and the date to review results. State that
nothing has been published or sent.
