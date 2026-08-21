# Scoring

100 points across five axes, with hard gates that override the total. Assign the
numbers from evidence already collected in `hunt/01`–`hunt/05` — if an axis has no
evidence, score it `null` rather than guessing, and let the scorer flag it.

## Kill gates (checked first, override everything)

A candidate failing any of these is dead regardless of its score. Report it in
the kill list with the gate named.

1. **Reddit PMF is T0 or T1.** No real, current, unprompted pain → dead.
2. **No money in the niche.** No incumbent with evidence of revenue → dead.
   Silence is a graveyard, not an opening.
3. **Trend flat or declining** across both target geo and worldwide → dead.
4. **Build exceeds the budget by more than ~50%** and cannot be cut down → dead.
5. **Store-policy or safety hazard** — health claims, anything involving minors,
   anything that invites harassment → dead, no matter how good the numbers.

A candidate that fails only gate 4 can be revived by cutting scope. Say so
explicitly rather than silently dropping it.

## The axes

### Pain — 25 points
How sharp is the problem, per Phase 5.

- 25 — T3: people already paying for something bad, or hand-rolling workarounds
- 18 — T2 with the full evidence bar met and multiple recent threads
- 12 — T2, bar just met
- 0 — T1 or T0 (also a kill gate)

Pain carries the most weight because it is the only axis measured from people
rather than inferred from markets.

### Proven money — 25 points
Is anyone already paid here, per Phase 2.

- 25 — several independents visibly earning; verified figures (TrustMRR, or a
  marketplace listing with stated revenue)
- 18 — clear incumbents with estimated revenue (Sensor Tower) and visible pricing
- 10 — incumbents exist, monetization visible, no revenue data
- 0 — nothing (kill gate)

Subtract 5 if the category is one giant and nothing else — that is a harder market
for a solo builder than a spread of mid-size independents.

### Demand — 20 points
Trend direction and keyword opportunity, per Phase 3.

- 12 for trend: rising in both geo and worldwide = 12, rising in one = 8,
  spiky or seasonal = 5, flat = 0
- 8 for keywords: a keyword in the target zone (popularity >20, difficulty <50)
  = 8, close to the zone = 5, everything contested = 2, unavailable = null

### Marketability — 20 points
Can you get distribution, per Phase 4.

- 8 — organic viral content exists in the niche (not just paid)
- 6 — the first-video sentence is writable and specific
- 4 — a usable controversy angle with no safety hazard
- 2 — creators are individuals sharing experience rather than brands

Score each component independently and sum. A candidate that cannot produce the
first-video sentence should not exceed 10 here whatever else is true.

### Feasibility — 10 points
Per Phase 6, judged by the main model.

- 10 — one problem, one feature, comfortably inside the build budget
- 6 — inside budget but needs a real integration or nontrivial data work
- 3 — at the edge of budget, or has a cold-start problem
- 0 — over budget by >50% (kill gate)

Simplicity earns points here rather than losing them. The most profitable apps in
the marketplaces are frequently the least sophisticated.

## Reading the total

- **80+** — build it. Go to Phase 7 and validate this week.
- **65–79** — strong; usually one axis is thin. Name the thin axis and what would
  fix it before committing.
- **50–64** — parking lot. Real, but you would be choosing it over better options.
- **under 50** — kill, with the reason.

Rank T3-pain candidates above T2 candidates when totals are within about five
points. Observed demand beats inferred demand, and the total is not precise enough
to justify overriding that.

## Input file

`hunt/scores.json`:

```json
{
  "candidates": [
    {
      "name": "short idea name",
      "pmf_tier": "T3",
      "money_evidence": "verified",
      "trend": "rising_both",
      "build_days": 10,
      "budget_days": 14,
      "hazard": false,
      "scores": {
        "pain": 25,
        "money": 25,
        "demand": 18,
        "marketability": 14,
        "feasibility": 10
      },
      "notes": "one line"
    }
  ]
}
```
