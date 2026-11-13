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
2. **Page copy** (`smoke-test/COPY.md`), in this order:
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
3. **Page build** (`smoke-test/index.html`): a premium single-file page, not a
   bare form. Read `references/design-standards.md` first; it is the quality bar.
   Write the copy into a JSON file (see `assets/example-values.json`) and fill
   `assets/page-template.html` with `scripts/fill_template.py`. The template ships
   a dark editorial design, an animated headline, a product mock built from the
   core loop, a "what it will never do" strip, three benefit cards, a closing
   CTA, GSAP + ScrollTrigger + Lenis motion that degrades to a complete static
   page, and an honest form (it shows "not connected yet" until a real https
   endpoint is set, never a fake success). Adapt the accent colour, mock content
   and section copy to the product; if the default look does not suit the
   category, change the design, not just the words. Optionally study the design
   skills listed in the standards file, but never install third-party skills
   without telling the user.
4. **Price test (optional, only if the user wants it):** after the email field,
   show the intended plan and price and a "Notify me when it launches" confirm
   step, or a two-variant split of prices across two URLs. Be explicit on the page
   that nothing is charged. Do not collect payment details for a product that
   does not exist.
5. **Traffic plan** (`smoke-test/TRAFFIC.md`): specific places, not channels. For
   each: the exact thread/community, why the post is a genuine answer, and the
   draft post. Follow each community's self-promotion rules; check them and say
   when a rule would forbid the post. Disclose that you built the thing. Draft
   posts for X/LinkedIn/Instagram as well. Never astroturf: no fake accounts, no
   fake upvotes, no pretending to be a user.
6. **Verify in a browser** (do not skip): screenshot at 1440x900 and 390x844 after
   the intro, scroll the whole page, confirm no horizontal overflow, no console
   errors, the form visible above the fold on mobile, the success state
   (`?demo` preview), and that the page is complete with the CDN scripts
   blocked and with reduced motion on. Fix anything that looks generic or broken
   before handoff; if no browser is available, say what was not seen.
7. **Readout template** (`smoke-test/RESULTS.md`): a blank table for visits,
   signups, conversion by source and headline, plus the decision rule copied
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
