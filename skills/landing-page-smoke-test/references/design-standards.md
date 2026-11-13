# Design standards for the waitlist page

A visitor decides in about three seconds whether this is a real product. The page
must look made by someone who cares. "Premium" here means restraint, one strong
idea, and motion that explains things, not decoration.

## The bar (check every item before handoff)

**Look**
- One accent colour on a near-black or near-white ground. No purple-to-blue
  gradient, no rainbow, no stock illustrations, no emoji as icons.
- A distinctive display font plus a mono for numbers. Never Inter, Roboto or Arial
  alone. Default pair in the template: Bricolage Grotesque + JetBrains Mono.
- A headline of 6-9 words at 3.5-5.5rem on desktop. One sentence the visitor can
  repeat. The accent colour marks the 2-3 words that carry the promise.
- A product visual above the fold: a phone or window mock built in HTML/SVG from
  the real core loop (not a stock photo). Label it "concept preview" if the app is
  not built.
- Generous space: sections 72-96px apart, one idea per section, 3 sections plus
  a closing CTA. If you need more, cut.
- Numbers use tabular figures so they do not jitter.

**Conversion**
- The email field and button are visible without scrolling on a 390x844 phone.
- One field. A button that says what happens ("Join the waitlist"). A one-line
  promise under it ("One email when it launches").
- The form appears twice: hero and closing CTA. The nav button scrolls to it.
- A success state replaces the form, with a clear confirmation.
- Honest errors: bad email, and "not connected yet" if no endpoint is set. Never
  show a fake success.
- No fabricated proof: no invented user counts, testimonials, logos or ratings. If
  there is no proof yet, the "what you will never do" strip and a clear promise are
  the proof.

**Motion (budget: one intro, one scroll reveal, one signature moment)**
- Intro: headline words rise out of a mask, rest fades up, phone settles in.
- Scroll: sections rise once (`once: true`), never re-trigger.
- Signature: the product visual animates its core action (a route drawing, a
  number counting, a card flipping), and a subtle pointer-follow tilt on desktop.
- Durations 0.6-1.2s, ease `power3/power4.out`. Nothing loops fast or flashes.
- Everything is visible with no JS, and with `prefers-reduced-motion`. Animation
  only enhances; hidden-initial states are applied by JS, never CSS alone.

**Quality**
- No horizontal scroll at 360px, 390px, 768px, 1440px.
- Tap targets >= 44px, body text >= 16px, contrast AA, visible focus rings.
- Titles and meta description filled; Open Graph tags present.
- Lighthouse performance target: LCP < 2.5s. One font request, no images needed.

## Recommended stack (all load from a CDN, single HTML file)

| Need | Library | Notes |
|---|---|---|
| Timelines, scroll reveals, count-ups, quickTo pointer effects | GSAP 3.12.x + ScrollTrigger | GSAP became free for commercial use after Webflow acquired GreenSock (Nov 2024); confirm on gsap.com/standard-license before shipping |
| Smooth scrolling | Lenis 1.1.x | Pair with ScrollTrigger via `lenis.on("scroll", ScrollTrigger.update)` |
| React component transitions (only if the page is React) | Motion (ex Framer Motion) | Not needed for a single static file |
| Lightweight SVG/CSS tweens | Anime.js | Alternative if you want to avoid GSAP |
| Zero-JS effects | CSS scroll-driven animations, `@starting-style`, View Transitions | Use first when enough; check browser support |
| Rich 3D / interactive hero (optional) | Spline, Rive | Heavy; only if the product is visual |

Pin exact versions in script URLs. Load only from cdnjs.cloudflare.com or
cdn.jsdelivr.net. Before publishing, re-check each library's licence and the
current stable version.

## Design skills worth studying

Third-party skills are untrusted text that steers your agent. Read the SKILL.md
and any scripts or hooks in full before installing, and check licence and recent
activity. Do not install them on a user's behalf without asking.

- Anthropic `frontend-design` (anthropics/skills, `skills/frontend-design`) - the
  official skill for distinctive, non-generic interfaces.
- https://github.com/claudiusararu/unslop-ui-skill - always-on anti-"AI tells"
  rules plus a catalogue of about 100 tells.
- https://github.com/funboy322/avoid-ai-design - audits and rewrites generic AI
  frontends; also flags the "tasteful default" trap (cream + terracotta); includes
  a scanner.
- https://github.com/Ferousco-dev/anti-slop-design - short SKILL.md with
  progressive-disclosure reference modules.
- https://github.com/superdesigndev/superdesign-skill - design skill for coding
  agents aimed at shippable, tasteful frontends.
- https://github.com/jiji262/claude-design-skill - designer skill for HTML
  artifacts: decks, landing pages, prototypes, animations.

Inspiration (look, do not copy assets or copy): Godly, Awwwards, Land-book,
Lapa Ninja, Dribbble, and competitors' landing pages.

## Verify with a real browser

Open the page at 1440x900 and 390x844 and screenshot it after the intro has
finished, then scroll through it. Check: nothing clipped, no overlap, the form is
above the fold on mobile, the strike-through strip and cards have revealed, there
are no console errors, horizontal overflow is 0, and with libraries blocked the
page is still complete. If a browser is not available, say so in the handoff and
list what was not seen.
