# Access layer — how research workers actually reach each source

Scouts that "browse" are the weakest link in the funnel: login walls, bot
blocking and flaky search turn into silent gaps. This file fixes the order in
which every worker reaches a source, so evidence comes back as real rows with
dates and links instead of a model's summary.

## Priority order

For every source, try in this order and record which one produced the data:

1. **Apify connector (primary).** Structured rows from a named actor. Runs on
   Apify's servers, so it is not affected by blocking of cloud IP ranges.
2. **Agent Reach (secondary, free).** An open-source CLI/skill that lets an agent
   read Reddit, YouTube, X, GitHub and other platforms without paid APIs. Use it
   when Apify is not connected, the actor failed or returned nothing, or the user
   wants a zero-cost run. Install only from the upstream repo
   (`github.com/Panniantong/Agent-Reach`); many third-party pages republish it
   under other names and some charge per call.
3. **Manual web search / fetch (last resort).** `site:` queries and page fetches.
   Slowest and least verifiable; state clearly when this was the only layer.

The report's source line must name the layer used per phase, for example
"Reddit: Apify (harshmaur/reddit-scraper); Trends: Apify; X: unavailable".

## Credentials

- **Apify** — the connector is per user. Inside an agent that already has the
  Apify connector authenticated, nothing more is needed. Elsewhere the token comes
  from the `APIFY_TOKEN` environment variable. Never write a token into the repo,
  `hunt/` files, scout briefs or chat, and never ask the user to paste one into
  chat. If it is missing, fall through to layer 2 and say so.
- **Agent Reach** — no key. The exception is X/Twitter, which needs a logged-in
  browser cookie from the user's own account. **Leave X off unless the user
  explicitly opts in**, because it acts through their account.
- No spending cap is enforced by this skill — each user's connector and plan set
  their own limits. Before a large fan-out, give a rough estimate (results × the
  actor's per-result price) and ask for a go-ahead; after the run, report what was
  fetched. Prefer the cheap early screens (see Phase 1.5) so most spending lands on
  survivors.

## Failure semantics (non-negotiable)

- **A failed, blocked, empty-because-erroring, or rate-limited run is
  `unavailable`. It is never a null result.** Do not grade T0, mark `money:
  none`, or call a trend flat because a tool returned nothing. Check the run
  status and row count before interpreting an empty dataset; an actor that
  returns zero rows with a failed status is a failure, not evidence.
- A genuinely empty result from a run that succeeded, with queries you can list,
  is a valid null finding.
- Community actors break when sites change. Each source below lists a preferred
  actor and a backup; if both fail, drop to the next layer.
- Pin the actor you used (`username/name`) in the phase file so a run can be
  reproduced and audited.

## Source → tool map

Check each actor's input schema with `fetch-actor-details` before calling it;
the field names below are a starting point, not a contract. Actor popularity and
ratings were observed at time of writing and will drift.

| Need | Preferred (Apify) | Backup | Agent Reach / manual |
|---|---|---|---|
| Reddit pain threads (Phase 1.5, 5) | `harshmaur/reddit-scraper` — has pain, willingness-to-pay, feature-request and asks-for-help flags plus a posted-after filter | `automation-lab/reddit-scraper`, `fatihtahta/reddit-scraper-search-fast` | Agent Reach Reddit; `site:reddit.com` search. Reddit may 403 cloud IPs on this path |
| TikTok viral content (Phase 4) | `clockworks/tiktok-scraper` — keyword search, search sorting, minimum-likes filter | `apidojo/tiktok-scraper` | manual TikTok search |
| Google Trends (Phase 3) | `apify/google-trends-scraper` — geo and time range | `scrapesage/google-trends-scraper` | trends.google.com by hand |
| App reviews, charts (harvest) | `automation-lab/apple-app-store-scraper` (apps, charts, star-filtered reviews: `mode: reviews`, `reviewMaxRating: 3`); `thewolves/appstore-reviews-scraper` | `neatrat/google-play-store-reviews-scraper` for Android (`ratingFilter`, `maxReviews`) | store pages. Feed rows to `scripts/review_themes.py` |
| Product Hunt (harvest) | `maximedupre/product-hunt-scraper` | `memo23/producthunt-scraper` | producthunt.com leaderboards |
| Flippa (harvest, money) | `fatihtahta/flippa-search-scraper` | `parseforge/flippa-scraper` | flippa.com listings. Small actors, treat as unproven |
| Market events (Phase 3) | `apify--web-search`-style search if connected, otherwise the agent's web search; `apify/web-fetch` to read a source page | — | manual search of company blogs, changelogs and news |
| X support complaints (harvest) | not verified — search the Store before relying on one | — | Agent Reach X, **opt-in only** |
| Acquire, TrustMRR, Sensor Tower, Astro, Viral Ad Library | not checked — search the Store; login-walled or paid sources often have no actor | — | user-supplied access, else the free proxies in `sources.md` |

## Observed in a live test (`harshmaur/reddit-scraper`)

- Two runs of 52 and 38 posts finished in about 50–60 seconds each and cost a
  few cents. Rows carried title, subreddit, date, score, comment count and link.
- The AI flag fields (`hasPain`, `wantsHelp`, `willingToPay`, `painPoint`) were
  requested with `aiAnalysis` on but did **not** appear in the returned dataset.
  Do not depend on them; read titles and bodies and grade yourself. Re-check if the
  actor updates.
- Query shape matters more than the tool; see "Shaping the query" in
  `reddit-pmf.md`.
- Dataset rows include large media fields. Request only the fields you need
  (`title,communityName,createdAt,score,commentsCount,postUrl,body`) to keep
  output small.

### Other actors, observed

- **`apify/google-trends-scraper`** — worked, 25–55s per run. The weekly timeline
  for one term is about 60 KB of JSON, so reading it costs real context: fetch a
  single term at a time and read only the shape. Related-queries are cheap and
  useful but expose ambiguous terms: "subscription tracker" was dominated by
  fitness and AirTag queries, so check the related list before trusting a shape.
- **`clockworks/tiktok-scraper`** — worked in about 15s. Most-liked sorting returns
  popular but loosely matched videos (unrelated viral posts appeared for
  "cancel subscriptions"); filter by topic before counting videos above 100k likes.
- **`automation-lab/apple-app-store-scraper`** — worked in about 7s. `maxItems`
  caps the whole run, not each keyword, so a second keyword can get nothing; raise
  it or run one keyword per call. It returns price, rating and rating count, not
  revenue, so it supports "incumbents exist", never a revenue claim.
- **Google Trends can show a shared artifact** (`scripts/trend_check.py` now
  detects it). Two unrelated terms ("subscription
  tracker", "running app") returned near-identical curves: flat to mid-2025, a
  step in Aug 2025, a peak around May 2026, a fall since Oct 2026. When two
  different terms share a shape, treat it as unreliable (`spiky`) and lean on the
  steadier years and on related-query signals instead.
- **Reading comments is cheap.** Passing thread URLs through `startUrls` with
  `crawlCommentsPerPost` took about 6 seconds for two threads and surfaced the
  decisive evidence (what people switch to, whether they would pay). Do this for
  the two or three strongest threads per candidate.
- **One run per subreddit** with 3–4 short keyword queries gives clean, on-topic
  rows; running-niche subreddits (`running`, `Strava`, `AdvancedRunning`) each
  returned 37–62 usable rows in about a minute.
- A thread that looks like a signal can be a scam or noise. Read the post and a
  few comments before counting it (a "paid for a bad app" thread turned out to be
  a cancellation-page scam).

## Verification (orchestrator, not scout)

Scouts return rows; the orchestrator checks them. Before accepting a
candidate's evidence, open at least two returned links at random per candidate
and confirm they exist and say what the row claims. A return with no URLs for a
claim that needs them is rejected and re-run. Fabricated or unreachable links
mean the whole scout return is discarded, not patched.
