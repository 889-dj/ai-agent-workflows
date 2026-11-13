# Revenue evidence — how to answer "does this niche really pay?"

The money axis was the weakest part of the first two hunts: with no revenue
numbers it could not score above 10 of 25. This file sets out how to get real
revenue evidence when it exists, and how to use honest proxies when it does not,
without ever inventing a dollar figure.

## The evidence ladder

Record the highest rung you can reach for each incumbent, and label it.

| Rung | Evidence | Trust | `money_evidence` it supports |
|---|---|---|---|
| 1 | Marketplace listing with stated revenue (Flippa, Acquire) | high — seller-attested | `verified` |
| 2 | TrustMRR entry | high — verified | `verified` |
| 3 | Dated public statement by a founder or company (post, interview, filing) | medium | `estimated` |
| 4 | Paid-tool estimate (Sensor Tower, Appfigures, data.ai) | medium — always say "estimated" | `estimated` |
| 5 | Proxy signals (below) | low | `listed` |
| 6 | Looked properly, found nothing | — | `none` |
| 7 | Could not reach the data | — | `unknown` |

Rung 6 and 7 are different and must never be blurred. Silence kills a candidate;
a failed lookup does not.

## Where to get it

- **Flippa / Acquire listings:** the Flippa actors in `access.md` return price,
  revenue and profit. Search the niche keyword and the names of incumbents.
- **TrustMRR:** fetch the site's search or category pages for the niche keyword.
- **Dated public statements:** web search `"<product> revenue" OR "ARR" OR "MRR"`
  and read the source. Founder posts and interviews often state numbers.
- **Paid estimators:** only if the user has access. Label every figure
  `estimated` and prefer rungs 1–3 when they disagree.
- **Pricing pages:** fetch each incumbent's pricing page for tiers, trial length
  and annual discount. It shows what the market bears even without revenue.
- **Acquisitions and funding:** a product bought by a larger company, or funded,
  is evidence of value. Cite the source and date.

## Proxy signals (rung 5)

When there is no revenue number, read these and report a *signal strength*, never
a dollar amount. `scripts/incumbent_signals.py` computes the table from the App
Store scraper output.

- **Usage depth:** rating count. About 100k+ is large, 10k–100k mid, 1k–10k small,
  under 1k tiny.
- **Recent activity:** ratings on the current version as a share of all ratings.
  A high share means the app is still gaining users.
- **A visible paywall:** a subscription, a paid tier or in-app purchases.
- **Independents at scale:** how many non-giant developers sit at mid size or
  larger. Several is the best sign for a solo builder.
- **Update cadence:** a recent last-updated date means someone still earns enough
  to maintain it.
- **Absorption:** a niche app bought by a bigger company shows the category is
  valuable but also that giants are paying attention.

Signal strength: **strong** = three or more independents at mid size with a visible
paywall; **moderate** = one or two; **weak** = none, or only giants.

Never convert a rank or a rating count into revenue. A proxy tells you *that*
money exists and roughly how crowded it is, not how much.

## How it feeds the score

Money axis (25 points), see also `scoring.md`:

- Rung 1–2 evidence, several independents earning: **up to 25**
- Rung 3–4 estimates with clear incumbents: **up to 18**
- Strong proxy signals, no numbers: **up to 14**
- Moderate proxy signals: **up to 10**
- Weak proxy signals: **up to 6**
- Nothing found after a proper search: **0** and the money gate applies
- Data unreachable: score on what you have and set the money confidence to `low`

A proxy-only candidate can never reach the verified bands. If revenue evidence is
the thing that would change the verdict, say so in the dossier under "What would
change this verdict" and name the specific lookup to do.
