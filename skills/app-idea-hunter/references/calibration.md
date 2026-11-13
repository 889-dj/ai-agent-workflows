# Calibration — are the weights right?

The 100-point rubric is judgement. It has not been tested against real outcomes, and
this skill should not pretend otherwise. This file explains how to find out, slowly
and honestly.

## Why not backtest on famous apps today

It is tempting to run the pipeline on known winners and flops. It does not work:
the data (Reddit, Trends, reviews, store rankings) is scraped as of *now*, so a
known winner already looks like a winner. That tests hindsight, not the method.

## What works: a prediction log

1. At the end of every hunt, record the scored candidates with a date:
   `python3 scripts/backtest.py add hunt/scores.json log/predictions.json`
   Each is stored as `pending` with its axis scores, tier, wedge and predicted band.
   (`assets/prediction-log.json` already holds the two hunts run while building the
   skill, both pending.)
2. Three to twelve months later, resolve each case in the file: set `outcome.result`
   to `success`, `partial` or `failure`, with a link or note in `outcome.evidence`.
   Use one yardstick every time and write it down:
   - **success** — paying users, and growing or sustaining (or a comparable product did)
   - **partial** — some traction, not enough to justify the build
   - **failure** — no traction, or abandoned
3. Run `python3 scripts/backtest.py report log/predictions.json`. It shows whether
   high totals went with good outcomes, how often predicted builds worked and
   predicted kills failed, and which axis correlates best with the outcome.

## How to read it

- Under **eight resolved cases** every number is an anecdote; the report says so.
- A total that does not correlate with outcomes means the rubric is not measuring
  what matters. Look at which axes do, and change weights only when several more
  cases agree.
- Selection bias is real: you only learn the outcome of ideas you built or could
  observe. Resolve some cases from outside observation (a similar app launched and
  succeeded or not) and say so in the evidence.
- The log stores the raw axis sum. The scorer's total can be lower when a
  one-giant-category penalty applies.

## Cheap sanity checks that need no outcomes

- Monotonicity: improving one axis by itself should never lower the total or move a
  candidate down a band. (`scripts/test_score.py` covers the gates and ranking.)
- Kill gates should fire on obvious cases: a T0 pain grade, a flat trend, a fatal
  blocker, an over-budget build.
- Two analysts scoring the same evidence should land within a few points. If not, an
  axis description is too loose; tighten it in `scoring.md`.

## Provisional status

Until the log has enough resolved cases, treat the weights as provisional and say so
when presenting a score. The confidence ranges in `scoring.md` exist for this
reason: they show how much a verdict can move before anyone has proven the weights.
