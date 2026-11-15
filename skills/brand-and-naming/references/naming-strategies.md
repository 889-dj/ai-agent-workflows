# Naming: strategies, tests, scoring, and the manual checklist

## Strategies (generate across all of them)

| Strategy | Idea | Example shape | Trade-off |
|---|---|---|---|
| Descriptive | says what it is | Plain Run, QuickNotes | easy to understand and search; hard to own, often taken |
| Compound | two real words fused | Pocketsmith, Dropbox | memorable; check spelling and spacing |
| Evocative | a word that carries a feeling | Stride, Ember | brand-able; needs a hook to explain |
| Metaphor / animal / object | something with the right traits | Fox, Anchor | ownable if unusual; crowded if common |
| Invented | made-up but pronounceable | Strava, Figma | most ownable; needs marketing to mean something |
| Altered spelling | a real word, trimmed or twisted | Lyft, Flickr | searchable; hard to say out loud, typo-prone |
| Verb / action | what the user does | Strive, Track | energetic; usually taken |
| Foreign / borrowed | a word from another language | Kilo (Greek), Lumen | elegant; check meaning both ways |

Generate roughly 4 to 6 per strategy. Ask for rationale, not just a list.

## Quick tests (cut a candidate that fails any)

- **Say it once, spell it back**: heard on a podcast, can someone type it? Two
  common spellings is a fail.
- **Length**: 4 to 10 letters is easiest; the App Store name field is limited (30
  characters at the time of writing; verify), and the visible home-screen label is much
  shorter, so the name must still read when truncated.
- **Distinctive in search**: a search for the name should not drown in generic results.
  One common dictionary word with a huge existing meaning is a search problem.
- **No hyphens, numbers, or doubled letters** unless it is deliberate.
- **Not too close to an incumbent** (`--competitors` flags this) or to another candidate.
- **Sound and rhythm**: two syllables is the sweet spot; avoid tongue-twisters.
- **Meaning**: nothing offensive, medical, or financial that would invite claims you do
  not support (a name like "CureRun" promises something).

## Scoring (1 to 5 each; weight as you like, default equal)

Memorable and pronounceable · Fits the product and feel · Distinctive and searchable ·
Room to grow (not boxed in by the first feature) · Availability (domain and store).
Keep the scores next to the evidence; a 5 on availability needs a check that actually ran.

## What the script covers, and what it does not

Covers: domain registration status via RDAP for each TLD; existing App Store apps with
the same or a very similar name (iTunes Search API); similarity to incumbents and to
other candidates.
Does not cover: trademarks, Google Play, social handles, premium domain pricing,
other-language meanings. Those are manual.

## Manual checklist for the final shortlist

- [ ] **Trademark**: search your name in the national and regional registers where you
      will sell (USPTO trademark search, EUIPO eSearch plus, WIPO Global Brand Database).
      Software classes are 9 and 42 (verify the classes for your product). Look for
      identical and similar marks, not only identical. A pro check before investing is wise.
- [ ] **Google Play**: search the Play Store for the name and close variants.
- [ ] **Social handles**: check the handles you need on the networks you will use. Sites
      block automated checks, so do this by hand.
- [ ] **Web search**: "<name>", "<name> app", "<name> reviews". Who owns the first page?
- [ ] **Language and culture**: ask someone fluent, or at least search the name plus
      "meaning" in the main languages of your markets.
- [ ] **Domain**: if the .com is taken but parked or for sale, note the asking price; if
      available, the user registers it.
