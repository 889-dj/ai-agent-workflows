# Sources

Every source the funnel uses, what it is actually good for, what it costs, and
what to do when it's locked. Confirm access with the user before Phase 1 —
finding out mid-hunt that Sensor Tower is paywalled wastes a whole fan-out.

Rule for all of them: record what you saw. `unavailable` and `not stated` are
valid entries. A fabricated revenue figure or difficulty score corrupts the score
and the user cannot tell it apart from a real one.

---

## Harvest — where ideas come from

### Acquire.com (formerly MicroAcquire)
`https://acquire.com` · free account required to see filtered listings

The most information-dense source in the funnel, because every listing is a
founder writing down what their product did, what it earned, and often why they
are leaving.

Two passes, both worth doing:

- **High to low.** Filter to mobile app, sort annual revenue descending. This is
  the ceiling, and it is dominated by unglamorous utilities — QR readers, homework
  scanners, VPNs. The lesson is that simplicity is not a compromise.
- **Under $10k MRR.** Founder-built products that found traction and stopped.
  Individually they are unremarkable; collectively the repeating themes tell you
  which categories reliably reach paying users. You are taking the pattern, not
  the codebase.

*Locked?* Search listing pages via web search, and lean harder on Flippa.

### Flippa
`https://flippa.com` · browsing free

Filter to apps, sort by most profitable. Listings state monthly revenue and
asking price. Treat the revenue as seller-attested — better than a screenshot,
weaker than a verified database.

### TrustMRR
`https://trustmrr.com` · free

Verified indie SaaS revenue, built specifically because fake MRR screenshots are
endemic. When a TrustMRR entry and a Sensor Tower estimate disagree, prefer
TrustMRR and say why in the report.

### Product Hunt
`https://producthunt.com` · free

Read the top launches for the current week and the previous month. **Do not
harvest individual products.** Harvest categories that repeat. Three habit
trackers in one week is a demand signal; one clever product is noise. The
categories that keep winning are consistently boring, because boring problems are
universal.

### App Store / Play Store top-grossing charts
Free, in the store apps or via web

Top grossing by category tells you who the incumbents are and how they charge.
Ignore the platform giants at the top; the interesting band is ranks 20–200,
where independents live.

### Incumbent app reviews
Free

Take the top three to five apps in the domain and read their 1-star and 3-star
reviews — 5-star reviews teach nothing. Phrase-mine: "I wish it did",
"why can't it just", "annoying that it doesn't", "the only thing missing is".
Each recurring complaint is an unbuilt product someone has already asked for.
Count how many reviews say something similar; frequency is the signal.

### Support handles on X
Free

Search the support accounts of major tools in the domain — @NotionHQ, @SlackHQ,
@ClickUp, @canva, or whatever the domain's equivalents are — plus mentions of
those products alongside "broken", "why can't", "doesn't work". These are
real-time support tickets written by users, in public, for free. This source is
badly underused and it is the fastest way to find a gap that is currently
annoying someone.

### Reddit / YouTube / X comment sections
Free

Harvest-grade scanning only at this stage. The rigorous work is Phase 5.

### LLM ideation
Free

Generate adjacent niches and underserved segments for the domain. Everything from
here is marked `speculative` and must survive Phases 2–5 like any other candidate.
Ideation seeds the funnel; it never exits it.

---

## Money — does this niche already pay?

### Sensor Tower
`https://sensortower.com` · paid; a limited free tier exists

Revenue and download estimates by app and category, and top-grossing breakdowns
per niche. The reason to use it is that it answers "are people paying in this
category" directly rather than by inference.

Always label its numbers **estimated**.

*Locked?* Combine top-grossing rank, visible subscription price, and review
count as a rough proxy, and mark the money axis low-confidence. Do not convert a
rank into a revenue number.

### Flippa / Acquire listings, TrustMRR
See above. For the money phase these are your highest-trust figures, because a
human attested to them.

---

## Demand — is it growing, and can you rank?

### Google Trends
`https://trends.google.com` · free

Five-year view, user's geo plus worldwide. Search the words a *sufferer* types,
not the category name. What matters is the shape: rising, flat, declining, spiky,
seasonal. Flat or declining is a kill signal, and it is a cheap one to collect,
which is why it runs early in the phase.

### Astro (App Store keyword research)
Paid · ASO keyword popularity and difficulty scores

The target zone is **popularity above 20, difficulty below 50**: enough people
searching for the keyword to matter, not so much competition that a new app is
invisible. This one rule is most of the value of the tool.

*Locked?* Use free proxies, and return a qualitative read (crowded / moderate /
open) rather than an invented number:
- **App Store search autocomplete** — type the seed keyword and record what the
  store suggests; those suggestions are ranked by real search behaviour
- **Result depth** — how many credible apps already rank for the term
- **Google Keyword Planner** — free with a Google Ads account, web-side volumes

---

## Marketability — can you get distribution?

### Viral Ad Library
`https://viraladlibrary.com` · paid tiers; some browsing free

Viral short-form content indexed by the app being promoted, with view counts, and
filterable by paid versus organic and by platform. Sort by most views.

Organic performance is the number that matters for a solo builder — paid
virality tells you the niche converts *if* you can fund ads; organic tells you
the topic spreads on its own.

*Locked?* Search TikTok and Instagram directly for the niche keywords and read
the top-performing videos manually. Slower, same signal.

### TikTok
Free

Search the core keywords, sort by most-liked of all time, then check the past
month for whether it is still alive. Count videos above ~100k likes, note the
recurring hooks, and note whether the creators are individuals sharing an
experience or brands marketing. Individuals sharing an experience is the stronger
signal.

### Controversy read
No tool — judgement

Contested topics generate comment sections, and comment sections are free reach.
Habits people are trying to quit, money, dating, health and productivity guilt
all qualify. Report the angle, and separately report the hazard: health claims,
anything involving minors, and anything that invites harassment are risks to the
app's survival, not growth levers.

---

## Validation — the last mile

### Reddit
Free — the Phase 5 gate. Full protocol in `reddit-pmf.md`.

### Landing page builders
Google AI Studio, v0.dev, or hand-written HTML. One headline, one image, one
button, one email field. Draft always; publish only when the user says to.

### Distribution for the test
X, LinkedIn, Instagram, plus the specific Reddit and X threads already found in
Phases 1 and 5. Ten signups in a week is the green light.

**Posting, DMing and account creation are the user's to authorize. Draft, hand
over, wait.**

---

## Coverage checklist

Tick before writing the report. Mark each: covered / unavailable (reason).

**Harvest** — Acquire high-to-low · Acquire under-$10k · Flippa · TrustMRR ·
Product Hunt · top-grossing charts · incumbent 1-star reviews · X support
handles · niche comment sections · LLM ideation

**Money** — Sensor Tower · marketplace listings · TrustMRR · visible pricing

**Demand** — Google Trends (geo + worldwide) · Astro or proxies (popularity >20,
difficulty <50)

**Marketability** — Viral Ad Library (organic vs paid) · TikTok most-liked ·
controversy read · first-video sentence

**PMF** — Reddit gate, graded T0–T3, evidence bar checked

**Feasibility** — one-problem-one-feature test · build budget · blockers
