# Blocker checklist — what could stop this build or this business

Run this in Phase 6, for the **wedge**, before scoring feasibility. Blockers are the
things that are cheap to check now and expensive to discover after a month of
building. In the running-apps test, one Reddit thread ("developer now needs a paid
subscription") quietly threatened the whole Strava-sync idea. A checklist makes
that deliberate.

Go through every row. For each, write `clear`, or a blocker with a severity and a
source. A row you could not check is `unchecked`, and that goes in the report.

| # | Area | Questions |
|---|---|---|
| 1 | **Platform and store policy** | Will it pass App Store and Play review? Any rule on subscriptions, health or fitness claims, minors, location, or background activity that this idea touches? |
| 2 | **API and data dependencies** | Does it depend on another company's API or data (sync, import, maps, health data)? Is access free, paid or being restricted? Can they switch it off or charge you? Check the terms and recent changes (the events scan). |
| 3 | **Hardware and OS access** | Does it need background GPS, sensors, a watch app, HealthKit or Health Connect, Bluetooth or notifications that the OS limits? How reliable is it in the background? |
| 4 | **Content and ongoing cost** | Does it need content (audio, plans, coaching, data feeds) that someone must produce or license? Does it have a per-user running cost (maps, servers, AI calls)? |
| 5 | **Legal, privacy and safety** | Health, medical or training advice and injury risk. Personal location data. Children. GDPR and similar rules. Anything that invites harassment. |
| 6 | **Cold start and network effects** | Is the product only useful once others join (social feed, leaderboards, matching)? If so, how does it get its first users? |
| 7 | **Distribution dependency** | Does growth rely on one platform's goodwill (store featuring, a single social channel) or on an incumbent's audience? |
| 8 | **Regional availability** | Which countries can it launch in? Any payment, language or regulatory limits? |
| 9 | **Incumbent response** | Could an incumbent copy the wedge cheaply (see the wedge's "why they won't fix it")? How would they respond? |
| 10 | **Builder fit** | Does the builder have the skills, time and audience this needs? A solo build that needs a data scientist or a content studio is blocked. |

## Severity

- **minor** — annoying, understood, workable (a known review quirk, a small cost).
- **major** — could cost weeks or change the product (a paid API you would depend
  on, a content requirement, a cold-start problem). A major blocker caps the
  feasibility score at 6 and must be named in the dossier with its source.
- **fatal** — the idea cannot be built or run as scoped (the platform forbids it,
  the only data source is closed, a legal bar). A fatal blocker is a kill gate. If a
  narrower wedge avoids it, say so and rescore the narrower wedge instead.

## Recording it

In `scores.json`, give every candidate a `blockers` list, even if it is empty,
which proves the checklist was done:

```json
"blockers": [
  {"area": "API and data dependencies", "severity": "major",
   "note": "Strava developer API now needs a paid subscription", "source": "https://..."},
  {"area": "Legal, privacy and safety", "severity": "minor",
   "note": "training plans: avoid injury or medical claims", "source": ""}
]
```

Areas you checked and found clear need no row. List any you could not check under
`"unchecked_areas"`; they will be reported as a gap.
