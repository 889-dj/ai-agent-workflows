---
name: mvp-scoper
description: Cut a validated app idea down to the smallest buildable v1 - one core loop, a screen list, an explicit not-in-v1 list, and a 1-2 week build plan - and write a spec that mobile-ui-pipeline-v2 can build from without re-asking questions. Use after app-idea-hunter picks an idea, or whenever someone has an app idea and asks what to build first, how to scope an MVP, or what to cut.
---

# MVP Scoper

Validated ideas still die in the build: scope creeps, v1 becomes v3, and nothing
ships. This skill makes the cuts up front, on the record, so the builder starts
with a small, finished-shaped target.

Output: `design/MVP.md` in the project (or the path the user names). Keep it to
one page of decisions, not an essay.

## Inputs

Take them in this order, and do not re-ask what they already answer:
1. An `app-idea-hunter` dossier (look for "The wedge", "Pain", "Feasibility",
   "Blockers"). The wedge is the scope boundary. The Pain section's complaints
   are the feature list. The Blockers section sets hard constraints.
2. Otherwise, the user's description. Ask at most 3 questions, in one call, only
   if the answer would change the cut: who the one target user is, the build
   budget in days (default 10), and the platform (default iOS-first, Expo).

## Method

1. **One sentence.** "For <specific person>, <app> does <one thing> so they can
   <outcome>." If it needs "and", it is two apps; pick one and park the other.
2. **The core loop.** The single repeated action that delivers the outcome
   (e.g. scan -> see answer -> save). Write it as 3-5 steps. Everything in v1
   must serve this loop or be required by a store/legal rule.
3. **Feature triage.** List every candidate feature (from the dossier, the user,
   and your own instincts), then sort each into exactly one bucket:
   - **Loop** - the loop does not work without it.
   - **Required** - permissions, onboarding, settings essentials, account
     deletion if accounts exist, restore purchases if there is a paywall.
   - **Defer** - real value, but v1 delivers its outcome without it.
   - **Kill** - nice idea, no evidence anyone asked for it.
   Default every uncertain feature to Defer. A feature earns Loop only by
   completing the sentence "without X, the user cannot ..."
4. **Cut tests** - apply to everything left in Loop and Required:
   - Accounts/login: needed only if data must sync or be shared. Default: no
     account, local storage.
   - Backend: needed only if the loop needs data the device cannot hold or fetch
     from a public API. Default: none.
   - Notifications, widgets, social, settings screens beyond essentials: Defer.
   - Anything the dossier lists as a major or fatal blocker: redesign around it
     or cut it, and say so.
5. **Screen list.** Only screens the loop and required items need. Per screen:
   name, its single job, entry point, and the states it needs (empty, loading,
   error, permission denied, success). Aim for 3-6 screens.
6. **Capabilities.** Which must be real (camera, location, sensors, storage,
   network, purchases) and which may be seeded. Note the denied-permission path.
7. **Build plan.** Order the work so a usable loop exists by the halfway point:
   day-by-day or milestone-by-milestone against the budget. If the loop does not
   fit the budget, cut features, never extend the budget silently. Include a
   buffer of ~20%.
8. **Success bar.** One measurable v1 target taken from the dossier's bar
   (default: 10 waitlist signups in 7 days before building, then 7-day retention
   or first-paywall-view rate after launch). Say what result means "keep going"
   versus "stop".

## Output shape (`design/MVP.md`)

```
# <App> - MVP
**One sentence:** ...
**Target user:** ...  **Platform:** ...  **Budget:** <n> days
## Core loop
1. ... 2. ... 3. ...
## v1 scope
| Feature | Bucket | Why |
## Not in v1 (with the trigger that would bring each back)
| Feature | Bucket | Revisit when |
## Screens
| Screen | Job | States |
## Real vs seeded capabilities
## Constraints & blockers (from the dossier)
## Build plan
| Milestone | Days | Done when |
## Success bar
## Open assumptions
```

## Handoff to mobile-ui-pipeline-v2

End `MVP.md` with a block the build skill can consume directly, so it can skip
intake: core job, screens in scope, which capabilities are real, platform, and a
suggested visual direction family if the dossier's category implies one. Tell the
user they can now run the build skill and it should treat `design/MVP.md` as the
answered intake.

## Rules

- Cuts are the deliverable. If the Defer/Kill list is shorter than the v1 list,
  you have not cut enough.
- Never invent evidence. A feature with no source is a Defer, not a Loop.
- Estimates are ranges with stated assumptions, not promises.
- Do not start building. Scoping ends at the written spec.
