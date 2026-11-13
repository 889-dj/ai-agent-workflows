# Scoring

100 points across five axes, with hard gates that override the total. Assign the
numbers from evidence already collected in `hunt/01`–`hunt/05` — if an axis has no
evidence, score it `null` rather than guessing, and let the scorer flag it.

## Kill gates (checked first, override everything)

A candidate failing any of these is dead regardless of its score. Report it in
the kill list with the gate named.

1. **Reddit PMF is T0 or T1.** No real, current, unprompted pain → dead.
2. **No money in the niche.** You looked properly and no incumbent shows revenue
   → dead. Silence is a graveyard, not an opening. Two exceptions, both in the
   script: data you *could not reach* is `unknown`, never `none`, and does not
   kill (it lowers confidence instead); and a **T3** candidate is not killed by
   this gate, because T3 means people are already paying or hacking around the
   problem — flag it and verify the payers before building.
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
- up to 14 — strong proxy signals but no revenue data (three or more independents
  at mid size with a visible paywall); 10 for moderate, 6 for weak. Proxies can
  never reach the 18 or 25 bands. See `revenue.md` and
  `scripts/incumbent_signals.py`.
- 0 — nothing found after a proper search (kill gate)

If the category is one giant and nothing else, set `"giant_category": true`. The
script subtracts 5 from this axis for you — do not subtract it by hand. A single
giant is a harder market for a solo builder than a spread of mid-size
independents.

### Demand — 20 points
Trend direction and keyword opportunity, per Phase 3.

- 12 for trend: rising in both geo and worldwide = 12, rising in one = 8,
  spiky or seasonal = 5, flat = 0. A curve flagged by `trend_check.py` as a shared
  artifact is `spiky`; if a second independent signal agrees it is rising, you may
  argue for `rising_one` and must say what the second signal was.
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

## Confidence per axis

Every score gets a confidence: `high`, `medium` or `low`. It answers "how sure am I
of this number", not "how good is it".

- **high** — verified figures, or evidence read first-hand and cross-checked.
- **medium** — good evidence with a known gap (for example a thin sample).
- **low** — proxies, estimates, an unreliable trend, or data you could not reach.

The scorer turns this into a **range**: low-confidence axes can move by a quarter of
their maximum, medium by a tenth. If the range crosses a verdict band, the scorer
warns that the verdict is sensitive. That is the cue to go and raise confidence on
the weakest axis (usually by finding revenue numbers or a second trend signal)
before deciding.

Limits the script enforces: money confidence cannot be `high` unless the evidence is
`verified`; demand confidence cannot be `high` when the trend is `spiky` or
`unknown`; pain confidence cannot be `high` before Phase 5 has graded the candidate.

## Score the wedge, not the category

Axes are scored for the **wedge** defined in Phase 5.5. Money and demand should be
judged against the incumbents and keywords that wedge would actually compete with,
and feasibility against the wedge's real build, not a full-featured category leader.
Record it as `"wedge"` in `scores.json` (a short sentence).

## Status of the weights

The weights are provisional judgement. Log predictions with `scripts/backtest.py`
and resolve outcomes over time (`calibration.md`) before relying on them.

## Reading the total

- **80+** — build it. Go to Phase 7 and validate this week.
- **65–79** — strong; usually one axis is thin. Name the thin axis and what would
  fix it before committing.
- **50–64** — parking lot. Real, but you would be choosing it over better options.
- **under 50** — kill, with the reason.

Rank T3-pain candidates above T2 candidates when totals are within about five
points. Observed demand beats inferred demand, and the total is not precise enough
to justify overriding that.

## Consistency checks the script enforces

The structured fields and the hand-entered axis scores must agree, so a score
cannot quietly contradict its own evidence.

- **Pain ceiling by tier:** T2 ≤ 18, T3 ≤ 25, T0/T1 = 0.
- **Demand ceiling by trend:** rising_both 20 · rising_one 16 · spiky/seasonal 13 ·
  flat/declining 8 · unknown 20.
- **Marketability** ≤ 10 when `first_video` is false.
- Axis values must be numbers or `null`, within each axis maximum.
- Duplicate candidate names, unknown enum values and non-boolean `hazard` are errors.

## Input file

`hunt/scores.json`. Allowed values:

- `pmf_tier` — `T0` `T1` `T2` `T3` (leave out until Phase 5 has graded it)
- `money_evidence` — `verified` · `estimated` · `listed` · `unknown` · `none`
  (`unknown` = data unreachable, `none` = looked properly and found nothing)
- `trend` — `rising_both` · `rising_one` · `spiky` · `seasonal` · `flat` ·
  `declining` · `unknown`
- `hazard`, `giant_category`, `first_video` — true/false
- `confidence` per axis — `high` · `medium` · `low`

```json
{
  "candidates": [
    {
      "name": "short idea name",
      "wedge": "one sentence: who it is for and the one complaint it fixes",
      "pmf_tier": "T3",
      "money_evidence": "verified",
      "trend": "rising_both",
      "build_days": 10,
      "budget_days": 14,
      "hazard": false,
      "giant_category": false,
      "first_video": true,
      "scores": {
        "pain": 25,
        "money": 25,
        "demand": 18,
        "marketability": 14,
        "feasibility": 10
      },
      "confidence": {
        "pain": "high",
        "money": "high",
        "demand": "medium",
        "marketability": "medium",
        "feasibility": "medium"
      },
      "notes": "one line"
    }
  ]
}
```

Run the tests with `python3 scripts/test_score.py`.
