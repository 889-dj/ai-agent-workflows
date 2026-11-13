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

The funnel is ordered so the expensive work happens on a shrinking list: ~30
candidates in, a cheap screen that kills the obvious losers early, then the
deeper checks, 3 dossiers out. Cheap and decisive checks run first; the full
Reddit gate still runs last because it is the one that can overrule everything.

## Three rules that are not optional

**1. Parallelize research when the environment supports it.** Assign each
research worker one focused source or candidate and give it the matching prompt
from `references/scouts/` — paste the brief and any reference text it needs into
the dispatch, since a worker may not be able to read files from the skill
directory. Prefer a fast, economical model that can use tools and extract
evidence reliably. Workers reach sources through the layers in
`references/access.md` (Apify first, Agent Reach second, manual last). The coordinating agent defines the briefs, reviews
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
before writing the report, and state any source you couldn't reach and why. A
source that does not fit the idea type (TikTok for a B2B tool, ASO for a web app)
is marked `not applicable` with the reason, not forced and not silently dropped.

## Before research

Confirm source access before burning time. Read `references/access.md`: check
whether the Apify connector is available, whether Agent Reach is installed, and
which paid sources the user has — Sensor Tower, Astro, Viral Ad Library,
Acquire's filtered search. Use the free proxies in `references/sources.md` for the
rest. Never fabricate a revenue figure or a keyword difficulty score to fill a
gap: write `unavailable` and let the scorer handle the missing axis.

There is no spending cap in this skill; each user's connector sets its own limits.
Before a large fan-out, give a rough cost estimate and ask for a go-ahead. A tool
failure is `unavailable`, never evidence of absence (see `references/access.md`).
Never put an API token in any file or in chat.

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

Also note whether the target users plausibly gather on Reddit; if not, the Phase 5
fallback sources apply.

Write these to `hunt/00-scope.md`. Every later phase filters against them.

**Run folder.** `hunt/` below means this run's folder, `hunt/<YYYY-MM-DD>-<domain>/`,
so a second run never overwrites the first. Keep a `manifest.md` listing each
phase file, the tool layer and actors used, and sources marked unavailable, so a
run can be resumed and audited.

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
  unbuilt feature someone already wants. Run `references/scouts/review-scout.md`
  (App Store and Google Play review actors, then `scripts/review_themes.py`) for
  every candidate niche that has real incumbents; this is not optional, because it
  is the best source of specific, countable gaps.
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

## Phase 1.5 — Cheap screen (minutes per candidate, kills early)

Before spending on money, trend and virality research, run the two checks that are
cheapest and most decisive. Write `hunt/01b-screen.md`.

1. **Feasibility and hazard sketch.** Can it be one problem, one feature, inside
   the budget? Any hazard (health claims, minors, harassment risk, a store policy
   it will not clear)? A clear hazard or a build far beyond budget is killed here;
   a scope that can be cut is cut here.
2. **Reddit smoke test.** One batch of pain-language queries per candidate (see
   `references/reddit-pmf.md`), a few dozen posts, no grading. If no one is
   describing the problem anywhere, drop it now. If the audience clearly does not
   gather on Reddit, use the fallback sources instead. This is a pre-filter, not
   the gate: Phase 5 still does the full, graded work on survivors.

Keep roughly 10–15 candidates for Phase 2.

## Phase 2 — Money check (does this niche already pay?)

Use `references/scouts/revenue-scout.md`, one assignment per candidate, batched
around eight at a time when parallel workers are available.

For each candidate the scout establishes: who the incumbents are, what they appear
to earn, and how they monetize. Follow the evidence ladder in
`references/revenue.md`: listings with stated revenue and TrustMRR first, dated
public statements and paid estimates next, and only then proxy signals
(`scripts/incumbent_signals.py`). Proxies cap the money axis, so a hunt with no
revenue numbers should say that plainly and name the lookup that would settle it.

Competition is the signal you want. Silence is a graveyard — an empty niche
usually means nobody could get paid there. **Kill any candidate where a proper
search found no evidence of anyone earning money in the space.** Distinguish that
from `unknown` (the data could not be reached): unknown does not kill, it lowers
confidence. And a candidate showing people already paying for, or hand-rolling
around, the problem (T3 in Phase 5) is not killed by this gate — flag it and
verify who is paying.

Write `hunt/02-money.md`.

## Phase 3 — Demand check (is it growing, and can you rank?)

Use `references/scouts/demand-scout.md` for each survivor.

- **Google Trends** on the core keyword, 5-year, the user's target geo plus
  worldwide, **plus a control term**. Run `scripts/trend_check.py`: it classifies
  the shape and flags curves shared by unrelated terms as artifacts. Flat or
  declining → kill. Up and to the right → proceed. A shared or artifact curve is
  scored `spiky`, and a second independent signal is required (rising related
  queries, recent-activity share, Reddit volume over time, or recent TikTok).
  Record the shape of the curve, not just a number.
- **Keyword research, by platform.** For mobile apps: App Store keywords (Astro,
  or the free proxies in `references/sources.md`); the target zone is **popularity
  above 20 with difficulty below 50** — real search volume that isn't yet
  contested. Report three to five keywords with both numbers. For web or
  micro-SaaS: search-engine keyword volume and difficulty instead (Keyword
  Planner, or an SEO tool the user has); ASO does not apply.

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
write that one sentence, marketability is low regardless of view counts. For
B2B or non-visual products, replace TikTok with the channel where that buyer
actually learns about tools (LinkedIn, communities, search) and apply the same
test.

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

If the audience is unlikely to be on Reddit, use the fallback sources in
`references/reddit-pmf.md` and treat a T2 as weaker than it looks.

Label every thread you read and run `scripts/pain_table.py`; it checks the bar
and suggests the grade, so a grade can be reproduced and audited.

Do the deep read in `references/reddit-pmf.md`: fetch the three strongest threads
with their comments and record what people switch to, who would pay, and who
defends the incumbent. A grade given from titles alone is not valid.

Paraphrase what people said. Quote sparingly — under fifteen words, one quote per
thread — and always link the thread so the user can read it themselves.

Write `hunt/05-reddit-pmf.md`. Record kills together with the searches that were
run: a null result is a finding, and the user should be able to audit it.

## Phase 5.5 — Define the wedge (score a product, not a category)

A category is not something you can build. "Running apps" scored 63 and only reached
66 when it was cut to one concrete product. Before scoring, turn the evidence into
**one wedge**: a specific product for a specific person that fixes the most
repeated complaint.

Write `hunt/05b-wedge.md` with:

- **The person:** who exactly (for example "recreational runner who pays for Strava
  and resents the upsells").
- **The complaint it fixes:** the single most repeated pain from the Reddit table
  and the review themes, with their counts.
- **What it is, in one sentence:** one problem, one feature, with a price idea.
- **What it deliberately is not:** the features you will not build at first.
- **Why an incumbent will not just fix it:** a structural reason (their business
  model depends on the upsell, the feature conflicts with their product, they are
  too large to care about the niche), or an honest "they could".
- **Fallback wedge:** a second, narrower or different cut if the first fails.

Then run the money, demand and feasibility checks on the **wedge**, not the whole
category: which incumbents actually compete with it, what keywords it would target,
what the real build is. Score the wedge. Put its one-line description in
`scores.json` (`"wedge"`), so the scorecard shows what was scored.

If the evidence supports no wedge, say so; that is a finding, not a failure.

## Phase 6 — Feasibility, score, report

For each survivor, the main model (not a scout) judges feasibility:

- Can the MVP be **one problem, one feature**? A puff counter that counted puffs
  reached $44k/mo. A QR reader reached eight figures. Simplicity is the strategy,
  not a compromise.
- Does it fit the Phase 0 build budget? Over by more than ~50% → kill, or cut
  scope until it fits.
- What are the real blockers — platform review policy, an API that doesn't exist,
  data access, a cold-start problem?
- **Devil's advocate.** Write the strongest case against this idea in a few
  lines: will users keep paying after month two (retention), do price × realistic
  conversion beat the cost of acquiring a user, could a platform or a general AI
  assistant absorb the feature, and does the builder have any edge in this domain?
  Put the answer in the dossier under "What would change this verdict".

Then score. Fill `hunt/scores.json`, including a **confidence** (high, medium, low)
for each axis, and run:

```bash
python3 scripts/score.py hunt/scores.json
```

The rubric, weights, and hard kill gates are in `references/scoring.md`. Read it
before assigning numbers so scores mean the same thing across runs.

Score the wedge from Phase 5.5, not the category. Produce `hunt/REPORT.md` using
`assets/dossier-template.md`:

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
- **The bar**: signups only mean something against traffic. Define the test before
  running it — for example, 200+ relevant visitors in a week and at least 5%
  leaving an email, or better, a price-click or pre-order test, since an email is
  not payment. Clearing that is the green light. Well under it with enough
  traffic means the pain wasn't sharp enough — move to candidate #2 rather than
  rescuing this one. Too little traffic is inconclusive, not a fail.

Hand the drafts over with the target list. Posting, DMing, and account creation
are the user's to do or explicitly authorize.

## Working notes

- Keep everything in the run folder. Each phase writes its own file so a run can be
  resumed and audited, and `manifest.md` records tools, actors and gaps.
- Check scout returns before using them: open a couple of links per candidate,
  reject returns that lack URLs, and re-run a malformed or failed scout once
  before marking the source unavailable.
- Report `unavailable` sources loudly. A hunt that skipped Sensor Tower and
  Reddit is a weaker artifact and the user should know which one they got.
- When a scout returns something surprising — a niche earning far more than
  expected, a trend spiking last month — send a second scout at it before you
  build a recommendation on it.
- Sensor Tower numbers are estimates. Say "estimated" in the report, and prefer
  marketplace listings and TrustMRR entries, where a number was at least attested.

## Reference files

- `references/access.md` — how workers reach each source: Apify first, Agent
  Reach second, manual last; credentials, failure rules, actor map.
- `references/sources.md` — every source, its URL, cost, exactly what to pull
  from it, and a free fallback. Also the coverage checklist for Rule 3.
- `references/revenue.md` — the revenue evidence ladder and proxy signals.
- `references/scoring.md` — the 100-point rubric, weights, and kill gates.
- `references/reddit-pmf.md` — the Phase 5 protocol in full.
- `references/scouts/` — portable task briefs for delegated research workers.
- `assets/dossier-template.md` — the report format.
- `scripts/trend_check.py` — classifies Trends curves and flags shared artifacts.
- `scripts/review_themes.py` — counts recurring complaints in low-star reviews.
- `scripts/pain_table.py` — evidence table and suggested T0–T3 grade.
- `scripts/score.py` — scorer; enforces gates, checks scores against evidence,
  ranks candidates. `scripts/test_score.py` tests it.
