---
name: monetization-designer
description: Choose a pricing model, set price points, draw the free/paid line, and design the paywall (placement, copy, trial, restore/cancel handling) for an app, grounded in competitor pricing and revenue evidence instead of guesses. Use when someone asks how to monetize an app, what to charge, subscription vs one-time, freemium vs trial, or how to design a paywall; also after app-idea-hunter or mvp-scoper.
---

# Monetization Designer

Pricing is a hypothesis. This skill turns the evidence already gathered
(incumbent prices, revenue signals, complaints about paywalls) into a concrete,
testable monetization plan and a paywall spec the build can implement.

Output: `design/MONETIZATION.md`. Short, decision-first.

## Inputs

1. `app-idea-hunter` dossier: use the Money section (incumbents, price, model,
   revenue with source type) and the review complaints about price or paywalls.
2. `design/MVP.md` from `mvp-scoper`: the core loop and screens.
3. Otherwise ask, in one call, at most 3 questions: who pays (consumer, prosumer,
   business), how often the core loop is used, and any hard constraint (no
   accounts, no backend, platform stores only).
Never fabricate a competitor price or revenue figure. If a number is unknown,
mark it `unknown` and name the lookup (store page, pricing page, listing) that
would settle it. Distinguish `verified`, `reported`, and `estimated`.

## Method

1. **Value metric.** What does the user feel they are paying for? Pick one: time
   saved, a result unlocked, ongoing access, or capacity/usage. The model must
   follow it:
   - Repeated, ongoing value (daily/weekly loop, data that accumulates) ->
     subscription.
   - One-off, bounded outcome (a single scan, convert, export) -> one-time
     purchase or consumable credits.
   - Cheap to serve, huge audience, weak willingness to pay -> ads or
     sponsorship, flagged as a weaker option.
   Subscriptions need a recurring cost to serve or recurring value; "we want
   recurring revenue" is not a reason users accept.
2. **Competitor price map.** A table of incumbents: price, model, trial, what is
   free, source type, link. Position yours deliberately (undercut, match, or
   premium) and say why. Note price complaints in reviews: they are the opening.
3. **Free/paid line.** The free tier must deliver the core loop's first win, so
   users feel the value; the paywall sits at the point of proven value or at a
   limit, not in front of the first use. Define exactly what is gated: usage
   caps, exports, advanced modes, removal of limits. Never gate something the
   store or law requires to be free (account deletion, restoring purchases,
   privacy controls).
4. **Price points.** Propose a primary price and two test alternatives, with the
   reasoning (anchoring to the competitor map, billing period mix). Prefer
   showing annual with the monthly equivalent; offer a free trial only if the
   loop needs more than one session to prove value. Treat these as the first
   experiment, with a stated test plan (what to vary, how long, minimum sample)
   rather than a final answer.
5. **Paywall design.** Specify, for the build:
   - Trigger(s): where it appears (after first win, at a limit, on a gated
     action) and where it never appears.
   - Content: headline tied to the outcome, 3 benefits max, plans with the
     recommended one marked, price and billing period shown plainly, trial terms
     stated clearly, a visible close control, "Restore purchases", and links to
     terms and privacy.
   - Honest patterns only: the real price and renewal terms visible before
     purchase, easy dismissal, no fake countdowns, no pre-selected hidden
     charges, no confusing cancel path.
   - States: loading prices, purchase pending, success, failed, cancelled,
     already subscribed, offline.
6. **Implementation notes.** Name the purchase stack suited to the project (for
   Expo: a purchases SDK such as RevenueCat, or the store APIs via a dev build -
   in-app purchases need a development build, not Expo Go) and flag that
   store-product setup, tax/banking, and sandbox testing are the user's tasks.
   Platform rules: digital goods on iOS/Android generally must use the store's
   billing; check current guidelines before promising any other route.
7. **Metrics and kill/keep thresholds.** Define: paywall view rate, trial start
   rate, trial-to-paid, first-month retention, refund rate. Give a rough starting
   expectation only if you can cite a source; otherwise say "set a baseline from
   the first 2 weeks of data".

## Output shape

```
# <App> - Monetization
**Recommendation:** <model> at <price>, free tier = <...>, paywall at <...>
## Why this model (value metric)
## Competitor price map
| Product | Price | Model | Trial | Free tier | Source | Link |
## Free vs paid
| Capability | Free | Paid |
## Price experiments
| Variant | Price | Hypothesis | Success metric |
## Paywall spec
## Implementation notes & owner tasks
## Metrics and thresholds
## Risks & unknowns
```

## Rules

- Evidence over instinct: every price claim cites a source type or says unknown.
- No dark patterns. If the user asks for one, explain the store/legal risk and
  offer an honest alternative.
- Revenue projections are scenarios with stated assumptions, not forecasts.
- Do not create store products, accounts, or charges; deliver the plan.
