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
3. **Page build** (`smoke-test/index.html`): a single static file, no build step,
   mobile-first, fast, accessible (labels, contrast, focus states), with the form
   `action` as a clearly marked placeholder for the user's form endpoint
   (e.g. a form-backend URL or mailing-list embed). Include a plain,
   privacy-respecting analytics note, but no trackers by default. Use
   `assets/page-template.html` as the starting point.
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
6. **Readout template** (`smoke-test/RESULTS.md`): a blank table for visits,
   signups, conversion by source and headline, plus the decision rule copied
   from step 1, ready to fill in.

## Rules

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
