---
name: "mobile-ui-pipeline-v2"
description: "Design and build a working mobile app or set of screens (Expo / React Native) in one strong pass. Asks only the few questions that change the result, runs a wide parallel research fan-out on Haiku 5.5 subagents, distils it into a design direction, builds real functional screens with animation, and self-reviews before showing anything. Use for 'make me a X-like app', 'build these screens', 'design and build a mobile UI'."
---

# Mobile UI Pipeline v2

Goal: the user's first result should be close enough to final that they need few iterations. That means
(1) the right few questions, (2) wide research that becomes a concrete design direction, (3) screens that
actually work, (4) a self-review before the user sees anything. There are no stage gates after intake.

```
1. Intake        <=4 questions, one call, only ones that change the output
2. Spec          silent: screens, core loop, real capabilities, states
2b. Feasibility  toolchain check BEFORE promising anything native
3. Research      parallel Haiku 5.5 fan-out -> Design Direction one-pager
4. Build         functional, animated, every state handled
5. Self-review   run it, walk every control, critique, fix
6. Handoff       short: what's real, what's not, how to run, next options
```

---

## 1. Intake: ask little, ask well

Use ONE AskUserQuestion call with at most 4 questions. Each question must change what you build. Skip any
question the request, the repo, or a sensible default already answers. Mark a recommended default first.

Pick from these, in priority order:
1. **Core job**: what the one main action is, if the request is ambiguous (e.g. "Strava-like": record a run, or social feed, or training plan?).
2. **Visual direction**: offer 3 named directions that fit the category (e.g. "Dark + electric lime, athletic", "Light + warm, editorial", "Glass + gradient, premium"). Never ask "what colors do you like".
3. **Functional depth**: real device data / real backend / persistence, or realistic seeded data. Default: real device capabilities + local persistence, seeded history.
4. **Where**: new project or existing folder (only if not obvious).

Do not ask about: fonts, spacing, icon style, navigation library, animation libraries, platform (default iOS-first
visuals, cross-platform code), anything with a good default. If the user already answered something earlier in
the conversation, do not ask it again. If the user says "just do it", skip intake and state your assumptions.

## 2. Spec (do not gate on it)

In your head or in 6-10 lines in chat: screens in scope; the core loop; which capabilities must be REAL
(sensors, location, camera, storage, notifications, network); permissions and their denied-state behaviour;
the states each screen needs (empty, loading, error, permission denied, success). State assumptions, move on.

## 2b. Feasibility: check the toolchain before promising features

Run this before you commit to anything that needs native code (video export, background location, camera, custom modules):
- `node -v`, `xcodebuild -version`, `java -version`, and `ls ~/Library/Android/sdk/platforms` as needed.
- Fetch the Expo SDK requirements page for the installed major version (https://docs.expo.dev/versions/v<major>.0.0/) and compare: Xcode, Node, Android compileSdk.
- If a development build is required and this machine cannot make one, say so in the first message after intake, build the feature with a clearly-labelled fallback that works in Expo Go, and list "native path unverified" in the handoff. Never discover this at the end.

## 3. Research: wide, parallel, on Haiku 5.5

Research is the main lever on first-pass quality, so go wide. Spawn 6-10 research subagents IN PARALLEL in one
turn, each with `model: "haiku"` (Haiku 5.5). Each gets ONE source cluster and ONE lens so they don't overlap.

Source clusters (assign one per agent; adapt to the category):
- **Category leaders**: the top 4-6 real apps in the category (store pages, screenshots, teardown articles, release notes).
- **Design galleries**: Dribbble, Behance, Refero, Screenlane, UI Movement, Collect UI, Pttrns, Lapa Ninja, Land-book, Godly, Awwwards, Mobbin public pages, Appshots.
- **Flow teardowns**: Appllama, ScreensDesign, Pageflows, UX Archive, Appkittie (onboarding, paywall, core flow).
- **Motion**: 60fps.design, Codrops, Dribbble animation shots, Lottie/Rive showcases. Return concrete timings and easings.
- **Visual identity**: Pinterest/Designspiration moodboards, palette and type pairing ideas that fit the chosen direction.
- **Writing and critique**: Muzli, Smashing, UX Collective, Reddit (r/UI_Design, r/FigmaDesign), X. What do designers praise or criticise in this category?
- **User pain**: App Store / Play Store 1-3 star reviews of the leaders. What annoys users? Each complaint is a design requirement.
- **Feasibility**: docs for the APIs the build needs (Expo docs per AGENTS.md / https://docs.expo.dev/llms.txt), known pitfalls, permission flows.

Brief every research agent with: the product, the chosen direction, their cluster, the exact output format,
and these rules:
- WebSearch/WebFetch do NOT run JavaScript. An empty or placeholder result from Dribbble, Behance, Refero, Mobbin, Pinterest, Land-book or any gallery means "needs a rendered browser", NOT "blocked". Do not report it as blocked.
- Paid sources (Mobbin MCP / its `search_screens`, `search_flows`, `search_sections` tools, Appllama Pro, Refero, etc.) are a bonus, never a requirement: see "Paid sources" below.
- Loading vs blocked (see the protocol below): never give up on the first empty page.
- Every finding must carry a URL. No URL, no finding.
- Borrow patterns, never brand assets, logos, copy or illustrations.
- Max ~12 tool calls. Report under 350 words, as: `PATTERN | WHERE SEEN (url) | CONCRETE VALUES | USE OR AVOID`.
  Concrete values means hex colors, font names, sizes, radii, durations, easing, layout proportions. When a source is a screenshot or shot, zoom in and read the values off the image; say which are measured versus guessed.


### Paid sources: use if available, never block on them

Before spawning agents, spend one quick check (no more than 2-3 calls) on what premium access exists this session:
- Mobbin or similar connector tools: look for them via ToolSearch (e.g. "mobbin", "search_screens", "search_flows"). If they load and answer a test query, the MAIN thread runs them (agents may not have them) for the product category and each screen in scope, and passes the findings (screen names, flows, URLs, values read off the screenshots) into the synthesis. Mark them `paid: loaded` in the handoff.
- Logged-in sites (Appllama Pro, Mobbin web, Refero, etc.): if Claude in Chrome is connected (`list_connected_browsers`), a research agent or the main thread may read these pages in the user's own signed-in session. Read only; never sign in, create accounts, or enter credentials. If the page shows a login or upgrade wall, the user is not signed in: skip it.
- If a paid tool errors, needs auth, or returns nothing: say `paid: unavailable (reason)` once in the handoff, and continue the normal free-source research. Do not stop, ask the user to fix it, or slow the build.
Paid findings must still carry a URL or screen/flow name and measured values where possible. Borrow patterns, never assets.

### Loading vs blocked: the protocol

Pages that look empty are usually still loading, or lazy-loading as you scroll. Treat them as loading until proven otherwise:
1. **Signs of "still loading"**: blank page, grey skeleton boxes, blurred or placeholder cards, a spinner, missing images, a tiny fraction of the expected text.
2. **Do this first**: wait 3-5 s, scroll down a few ticks to trigger lazy content, then read the page TEXT (more reliable than screenshots), then screenshot. If still thin, wait 10-20 s and retry once more. Only then decide.
3. **Use a rendered browser for JS-heavy sites**: the built-in browser pane, or Claude in Chrome (the user's own Chrome, with their sessions) when connected. Check `list_connected_browsers` and prefer it when a site rejects the built-in browser.
4. **Truly blocked** means one of: HTTP 403/429 that repeats after a retry, a captcha, a login wall, or an "upgrade" gate where the content is still hidden after scrolling and waiting. Then skip and say why. Never try to bypass a block, never create accounts, never enter credentials.
5. **Free tiers show part of the content.** If a gate says "upgrade for full access" but some items are visible, read what is visible and note the limit. Do not conclude the whole section is locked.
6. **Parallel agents and one browser**: two agents must not drive the same tab. Give each browser-using agent its own tab, or run the JS-heavy sources from the main thread one after another.
7. **Report a status per source**: `loaded`, `loaded after retry`, `partial (free tier)`, `blocked (reason)`, or `needs login`. The handoff summarises these.

Then YOU synthesize (never paste raw agent output). Write `design/DIRECTION.md` in the project (one page):
1. **Direction name** and one-sentence idea.
2. **Tokens**: color (bg, surface, text, mute, accent, danger, semantic), type pair + scale, spacing, radii, elevation.
3. **Per screen**: the single focal element, layout sketch in words, patterns borrowed (each with source URL).
4. **Signature moments**: 2-3 memorable interactions (e.g. count-up ring, route draw-in, hold-to-finish).
5. **Motion spec**: durations (micro 120-200ms, transitions 250-350ms), springs vs timing, haptic moments, reduce-motion fallback.
6. **Anti-patterns**: what the research says to avoid, including the user-pain list.

If research is thin (many sources blocked), say so in the handoff; do not pretend.

## 4. Build: functional first

Follow the project's AGENTS.md. For Expo, read the installed `expo` major version and use the matching docs; use
`npx expo install` for every package.

Rules that make it "functional", not a mockup:
- **Every tappable element works or is removed.** No dead buttons, no fake toggles.
- **Real capabilities are real**: sensors, location, camera, storage as specified. Wire permissions, handle denial with a recovery path (open settings).
- **Persist what a user would expect to persist** (e.g. finished activities, settings) with local storage; Home reads from it.
- **Seed data is allowed only for history/demo content**, clearly isolated in one `seed` module and replaced by real data as it appears.
- **All states exist**: empty, loading, error, permission denied, success.
- Theme file generated from DIRECTION.md tokens; no hard-coded values in components.
- Fonts actually loaded (not system default) with numerals that don't jitter when they update (fixed-width cells or tabular figures).
- Motion pass implemented from the Direction's spec on the UI thread (Reanimated), with haptics at key moments and reduce-motion respected.
- Safe areas, 44pt touch targets, primary action in the thumb zone.

Default stack: Expo + React Native + TypeScript, Reanimated, expo-haptics, expo-linear-gradient, react-native-svg.
Prefer Expo modules over third-party libraries.

## 5. Self-review: before the user sees it

Do all of this and fix what you find. Do not hand over on "it compiles".
1. `npx tsc --noEmit`, `npx expo lint`, and a production bundle (`npx expo export`) must be clean.
2. **Run it** if a simulator or browser target exists. Known pitfall: Expo Go on the simulator may fail on the LAN URL; retry with `npx expo start --localhost --ios`. Give it one retry. If it still won't run, stop and say it is untested on-device; do not loop on it.
3. **Render check**: take a screenshot of every screen and state, or write "not seen on a screen" in the handoff. Look specifically for text truncated with "…", overlapping numbers, and clipped content on a small phone.
4. **Numerals rule**: numbers that sit side by side must be sized from their actual width (fit the font size to the available width and give wider numbers wider columns). Never put numerals in fixed-width, single-line cells that can truncate; use clip, not ellipsis.
5. **Interaction walk**: list every interactive element per screen and what it does. Anything with no effect: fix or delete.
6. **Critique against DIRECTION.md**: one clear focal element per screen? hierarchy readable at arm's length? contrast AA? any default-looking gray box, system font, or unstyled control? does each signature moment exist? are the user-pain items avoided?
7. Fix, then re-check the failing items.

## 6. Handoff

Short, in this shape:
- What was built (screens, one line each) and where it is.
- **Real vs seeded**: what is genuinely functional, what is demo data.
- How to run it, and how to test on a phone (device sensors need a real phone).
- What was NOT verified, and why.
- Research summary: per-source status (loaded / loaded after retry / partial / blocked / needs login), how many yielded findings, and the 3 biggest decisions they drove.
- 2-3 concrete next-iteration options, so the user can pick instead of describing.

## Figma and gates

Figma is optional: use it only if the user supplies a file or asks. Tokens live in `design/DIRECTION.md` and the
theme file otherwise. Ask the user again only when blocked by something only they can provide (credentials,
payment, legal choices, an irreversible action). Everything else: decide, state the assumption, continue.
