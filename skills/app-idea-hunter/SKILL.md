---
name: app-idea-hunter
description: Research, validate, and score app, micro-SaaS, side-project, and hackathon ideas using market, demand, distribution, and product-market-fit evidence. Use when someone asks what to build, requests app ideas or niche research, or wants to know whether an existing idea is worth building.
---

# App Idea Hunter

Most app ideas die because nobody checked whether the pain was real and already
being paid for. This skill replaces guessing with a repeatable funnel: harvest
candidates from places where money is already visible, prove demand is rising,
prove the idea is marketable, then — last — go read what actual humans on Reddit
say about the problem. Ideas that survive all of it get a build brief. Everything
else gets killed on the record, with a reason.

The funnel is deliberately ordered so the expensive judgement happens on a
shrinking list: ~30 candidates in, 3 dossiers out.

## Three rules that are not optional

**1. Parallelize research when the environment supports it.** Assign each
research worker one focused source or candidate and give it the matching prompt
from `references/scouts/`. Prefer a fast, economical model that can browse and
extract evidence reliably. The coordinating agent defines the briefs, reviews
structured returns, makes judgments, scores candidates, and records kills. If
subagents are unavailable, run the phases inline at reduced breadth and state
that limitation instead of implying parallel research occurred.

**2. The Reddit gate runs last and it can kill anything.** A candidate with
$40k/mo competitors, a rising trend line, and viral TikToks still dies if real
people aren't describing the pain in their own words. Revenue data proves a
market existed; Reddit proves it still hurts. Phase 5 is a gate, not a tiebreak.

**3. Cover every source.** The funnel is designed so that different source types
catch different failure modes — marketplaces catch "does this make money", trends
catch "is it dying", virality catches "can I get distribution", Reddit catches
"is the pain real". Skipping a category doesn't just lose data, it removes a
whole class of kill. Tick off the coverage checklist in `references/sources.md`
before writing the report, and state any source you couldn't reach and why.

## Before research

Confirm source access before burning time. Several sources in `references/sources.md`
are login-walled or paid — Sensor Tower, Astro, Viral Ad Library, Acquire's
filtered search. Ask the user which they have, and use the free proxies listed in
`references/sources.md` for the rest. Never fabricate a revenue figure or a
keyword difficulty score to fill a gap: write `unavailable` and let the scorer
handle the missing axis.

Ask the user before doing any of these, every time: creating accounts, signing up
for a marketplace, publishing a landing page, posting to social, or DMing anyone.
Drafting those artifacts is fine; shipping them is the user's call.

## Phase 0 — Scope

Get four things from the user. If they only gave you "find me app ideas", ask —
one round, then proceed with defaults.

- **Domain or "open"** — a niche they know, or unconstrained hunting
- **Build budget** — days of solo work they'll accept (default: 14)
- **Platform** — iOS / Android / web / cross-platform (default: whatever their
  stack suggests)
- **Monetization** — subscription, one-time, ads, freemium (default: subscription)

Write these to `hunt/00-scope.md`. Every later phase filters against them.

## Phase 1 — Harvest (target ~30 candidates)

Fan out research workers across the harvest sources — one scout per source when
parallelism is available. Give each worker
`references/scouts/idea-scout.md`; it defines the return schema.

The harvest grounds, and what each is actually for:

- **Acquire.com / MicroAcquire** — filter to mobile/app, then look at listings
  *under* $10k MRR. These are founder-built products that got traction and
  stalled: each listing is a free case study of what users paid for and what
  didn't scale. You're not buying the company, you're taking the pattern.
- **Flippa** — sort apps by most profitable. Live proof of what boring ideas earn.
- **Acquire, annual revenue high→low** — the ceiling. QR readers and homework
  scanners at eight figures are the argument for simplicity.
- **TrustMRR** — verified indie SaaS revenue, so you're not pattern-matching on
  screenshot flexes.
- **Product Hunt top launches, this week and last month** — read for *repeating
  categories*, not individual products. The category that keeps reappearing is
  the demand signal; the winners are usually boring.
- **App Store / Play Store top-grossing by category** — the incumbents.
- **1-star and 3-star reviews of those incumbents** — phrase-mine for
  "I wish it did", "why can't it just", "annoying that it doesn't". Each is an
  unbuilt feature someone already wants.
- **Support handles on X** (@NotionHQ, @SlackHQ, @ClickUp, @canva and equivalents
  in the user's domain) — public support threads are next month's feature
  requests, written by users, for free. A complaint that repeats is a market gap.
- **Reddit / YouTube / X comment sections** in the domain — harvest-grade only
  here; the rigorous Reddit work is Phase 5.
- **LLM-led ideation** for the domain: have a scout generate adjacent niches and
  underserved segments, then treat every one of them as an unvalidated guess that
  still has to survive Phases 2–5. Ideation seeds the funnel; it never exits it.

De-duplicate, merge near-identical candidates into one line, and write
`hunt/01-candidates.md`.

## Phase 2 — Money check (does this niche already pay?)

Use `references/scouts/revenue-scout.md`, one assignment per candidate, batched
around eight at a time when parallel workers are available.

For each candidate the scout establishes: who the incumbents are, what they appear
to earn (Sensor Tower estimates, Flippa and Acquire asking prices and stated
monthly revenue, TrustMRR entries), and how they monetize.

Competition is the signal you want. Silence is a graveyard — an empty niche
usually means nobody could get paid there. **Kill any candidate with no evidence
of anyone earning money in the space.**

Write `hunt/02-money.md`.

## Phase 3 — Demand check (is it growing, and can you rank?)

Use `references/scouts/demand-scout.md` for each survivor.

- **Google Trends** on the core keyword, 5-year, the user's target geo plus
  worldwide. Flat or declining → kill. Up and to the right → proceed. Record the
  shape of the curve, not just a number.
- **App Store keyword research** (Astro, or the free proxies in
  `references/sources.md`). The target zone is **popularity above 20 with
  difficulty below 50** — real search volume that isn't yet contested. Report
  three to five keywords with both numbers.

A candidate with rising trends but every keyword above difficulty 70 isn't dead,
it's a distribution problem — flag it rather than killing it, because Phase 4 may
find a social channel that routes around ASO entirely.

Write `hunt/03-demand.md`.

## Phase 4 — Marketability

Use `references/scouts/virality-scout.md` for each survivor. Marketing decides
most of whether an app wins;
an average app with distribution beats a great app nobody sees. So check
distribution *before* committing to build, not after.

- **Viral Ad Library** — search the niche, sort by most views, compare organic vs
  paid. High organic view counts mean the niche spreads without ad spend.
- **TikTok** — search the core keywords, sort by most-liked of all time. Viral
  videos in the niche prove the content angle exists, and they double as a
  content template to copy.
- **Controversy read** — is there an argument inside this topic? Contested topics
  (quitting a habit, money, dating, health) get comment sections, and comment
  sections are free reach. Note the angle and note the risk; controversy that
  would get an app pulled from the store is a kill, not a feature.

Then answer honestly: *what is the first video about this app?* If nobody can
write that one sentence, marketability is low regardless of view counts.

Write `hunt/04-marketability.md`.

## Phase 5 — The Reddit PMF gate (mandatory, last, and it kills)

Everything so far was inference from markets. This phase is the direct check:
**do real people say they have this problem, in their own words, recently?**

Use `references/scouts/reddit-pmf-scout.md` for each survivor. The full protocol —
pain-language query patterns, the four evidence tiers, and the evidence bar — is
in `references/reddit-pmf.md`. Read it before dispatching.

The short version: search the *pain*, never the product name. Require at least
five distinct threads across at least two subreddits, at least one from the past
six months, and at least one person explicitly asking what tool to use. Then
grade T0–T3:

- **T0** — nobody is talking about it → **kill**
- **T1** — complaints exist but people are content with their workaround → **kill**
- **T2** — repeated complaints, people asking for a tool, real upvotes → **pass**
- **T3** — people already paying for something bad, or hand-rolling spreadsheets
  and shortcuts to cope → **pass, and prioritize**

Paraphrase what people said. Quote sparingly — under fifteen words, one quote per
thread — and always link the thread so the user can read it themselves.

Write `hunt/05-reddit-pmf.md`. Record kills together with the searches that were
run: a null result is a finding, and the user should be able to audit it.

## Phase 6 — Feasibility, score, report

For each survivor, the main model (not a scout) judges feasibility:

- Can the MVP be **one problem, one feature**? A puff counter that counted puffs
  reached $44k/mo. A QR reader reached eight figures. Simplicity is the strategy,
  not a compromise.
- Does it fit the Phase 0 build budget? Over by more than ~50% → kill, or cut
  scope until it fits.
- What are the real blockers — platform review policy, an API that doesn't exist,
  data access, a cold-start problem?

Then score. Fill `hunt/scores.json` and run:

```bash
python3 scripts/score.py hunt/scores.json
```

The rubric, weights, and hard kill gates are in `references/scoring.md`. Read it
before assigning numbers so scores mean the same thing across runs.

Produce `hunt/REPORT.md` using `assets/dossier-template.md`:

1. **Scorecard** — every candidate, one row, scores per axis, verdict
2. **Top 3 dossiers** — full evidence per axis, with links
3. **Kill list** — every rejected idea with the specific gate it failed
4. **Next 48 hours** — for the #1 pick only, the validation steps below

Lead with the kill list summary, not the winners. The user needs to trust the
filter before they'll trust what came through it.

## Phase 7 — Cheap validation (draft only, ship on approval)

For the top pick, prepare — do not publish:

- A **one-pager landing page**: one headline, one image, one button, one email
  field. Draft the copy; generate a live artifact with the user's preferred
  builder (Google AI Studio, v0.dev, or plain HTML) only if they ask.
- **Distribution drops**: short posts for X, LinkedIn and Instagram, plus a list
  of the exact Reddit threads and X support complaints found in Phases 1 and 5
  where this landing page would be a genuine, on-topic answer.
- **The bar**: ten signups in a week is the green light. Fewer, and the pain
  wasn't sharp enough — move to candidate #2 rather than rescuing this one.

Hand the drafts over with the target list. Posting, DMing, and account creation
are the user's to do or explicitly authorize.

## Working notes

- Keep everything in `hunt/`. Each phase writes its own file so a run can be
  resumed and audited.
- Report `unavailable` sources loudly. A hunt that skipped Sensor Tower and
  Reddit is a weaker artifact and the user should know which one they got.
- When a scout returns something surprising — a niche earning far more than
  expected, a trend spiking last month — send a second scout at it before you
  build a recommendation on it.
- Sensor Tower numbers are estimates. Say "estimated" in the report, and prefer
  marketplace listings and TrustMRR entries, where a number was at least attested.

## Reference files

- `references/sources.md` — every source, its URL, cost, exactly what to pull
  from it, and a free fallback. Also the coverage checklist for Rule 3.
- `references/scoring.md` — the 100-point rubric, weights, and kill gates.
- `references/reddit-pmf.md` — the Phase 5 protocol in full.
- `references/scouts/` — portable task briefs for delegated research workers.
- `assets/dossier-template.md` — the report format.
- `scripts/score.py` — scorer; enforces gates and ranks candidates.
