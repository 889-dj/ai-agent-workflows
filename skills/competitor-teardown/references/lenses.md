# Lenses: what to collect and how to return it

One worker (or one inline pass) per competitor per lens. Paste the relevant block
into a worker's brief; it cannot read this file. Every finding becomes a row for
`research/teardown.json`:

```
{"lens": "...", "claim": "what this is", "value": "the number or short fact",
 "evidence": "verified|reported|estimated|unknown", "url": "https://...",
 "date": "YYYY-MM-DD", "note": "how estimated / caveats", "lookup": "for unknown only"}
```

Return rows, a one-line status per lens (`complete | partial (reason) | blocked (reason)`),
and the sources you tried in order. Under 350 words of prose.

## Source ladder (all lenses)

1. First-party pages: the store listing (App Store, Google Play), the company's
   website, pricing page, help centre, changelog. Prefer these; mark `verified`.
2. Structured store data when a tool is connected (a scraper actor, or the public
   iTunes Search / Lookup API for App Store metadata, and the App Store customer
   review feed for recent reviews).
3. Secondary sources: reviews and articles, teardown sites, founder posts. Mark
   `reported`.
4. Reference libraries of flows and screens (Mobbin, Appllama, ScreensDesign,
   Pageflows, Refero) if the session has access; read only, never sign in or bypass.
5. User-provided screenshots or screen recordings: read values off the images, and say
   which values were measured and which guessed.

JavaScript-heavy sites return empty pages to simple fetchers: that is "needs a
rendered browser", not "blocked". Retry with a rendered browser if available; else
mark `unknown`.

## positioning

Collect: store title and subtitle, the one-line promise on the listing, category and
rank if shown, rating and rating count (with the date read), the target user as
implied by the copy, screenshot captions (the story the store tells), update
cadence (dates of the last 5 versions), languages, platforms.
Useful output: what they claim to be best at, who they are NOT for.

## onboarding

Collect (from recordings, flow libraries, or detailed write-ups; otherwise `unknown`):
number of screens before the first useful action, what is asked up front (account,
permissions, personal data, goals), whether value is shown before a signup, where
permissions are requested and what the copy says, time to first win.
Useful output: the shortest path to value in the category and the friction points.

## paywall

Collect: where the paywall appears (before first use, after a first win, at a limit,
on a feature), what is gated, whether a free tier exists and what it does, trial
terms, whether the close control is easy to find, whether the price and renewal terms
are visible before purchase, whether there are urgency tricks (countdowns, "limited
offer"), what happens on cancel. Observations only; do not call anything illegal.
Useful output: patterns to match and patterns users resent.

## pricing

Collect, each with a source and date: price per period for each plan and region read,
trial length, family/student plans, one-time options, bundles, price changes. Prices
from aggregator sites are `reported`, never `verified`; only the store listing or the
company's pricing page is `verified`. Conflicting sources: record both and flag.
If a price cannot be established, `unknown` with the lookup ("App Store listing,
in-app purchases section, US storefront").

## reviews

Collect low-star (1 to 3) and high-star (4 to 5) reviews, the most recent few hundred
each if a tool allows. Count recurring themes by distinct reviews, not mentions: if
`app-idea-hunter` is installed, its `scripts/review_themes.py` does this; otherwise
tally by hand and say so. Return: sample size, store, country, date range, then per
theme the number of reviews and the share of the sample, whether it is a product gap,
quality, pricing or platform complaint, and a paraphrased example. Separate the praise
themes: they are what you must not lose. Ignore a single bad release's spike unless
it persists. A failed pull is `unknown`, never "no complaints".

## traction

Climb the evidence ladder and record the highest rung reached per competitor:
(1) marketplace listing with stated revenue; (2) a verified revenue database entry;
(3) a dated public statement; (4) a paid-tool estimate, always `estimated` with the
tool named; (5) proxy signals such as rating count growth, chart rank, review velocity,
team size and hiring, funding news; (6) looked and found nothing; (7) could not look.
Rungs 6 and 7 are never blurred. Never state a revenue or download figure without a
source.

## changes

Collect the last 12 to 18 months of events that change the picture: acquisitions,
shutdowns, pricing or paywall changes, API or policy changes, redesigns, layoffs,
regulation. Each with a date and URL, tagged opening / threat / neutral.

## ui

Collect patterns, not pixels: navigation model, the focal element of the core screen,
information hierarchy, how the core action is triggered, empty/loading/error states,
motion and haptics worth noting, accessibility problems, and what reviewers praise or
dislike about the design. For measured values (colours, type sizes, radii, durations)
say whether measured from an image or guessed. Do not return brand assets.
