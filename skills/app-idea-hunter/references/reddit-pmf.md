# The Reddit PMF gate

This is Phase 5, it runs last, and it can kill anything.

Everything upstream is inference. Marketplace revenue proves a market *existed*
when someone bought or built something. Trends prove interest is moving. Virality
proves a topic spreads. None of them prove that a person, today, has this problem
and wants it solved. That is what this phase is for, and it is why it runs after
the expensive analysis rather than before: by the time you get here the list is
short enough to read threads properly.

## Search the pain, not the product

Someone with the problem does not know your category exists. They are not
searching "subscription management tool" — they are typing what hurts. Query the
language of the sufferer.

Combine domain vocabulary with these patterns, as `site:reddit.com` web searches
and inside Reddit's own search:

```
"I wish there was an app that <domain>"
"does anyone know an app for <domain>"
"is there a tool that <specific pain>"
"how do you guys deal with <specific pain>"
"why is there no <thing>"
"I hate that <incumbent> <complaint>"
"any alternative to <incumbent>"
"<incumbent> is too expensive"
"<incumbent> too complicated"
"<domain> spreadsheet"          <- people hand-rolling a solution
"<domain> shortcut" / "automation"
```

That last group matters more than it looks. Someone maintaining a spreadsheet to
cope with a problem has already decided the problem is worth their time. They are
the easiest person on the internet to sell to.

Then find the two to four subreddits where this population actually gathers and
search inside them directly. Sort by top of the past year for depth, and check
the past month separately for whether it is still live.

## What counts

A thread counts when a person describes the problem as **their own**.

It does not count when:
- someone is promoting a product
- it is a listicle, a roundup, or an SEO post
- it is your own category vocabulary echoed back by a marketer
- the only complaint is about pricing of a product they otherwise love

## The bar

All four, or the candidate does not pass:

- at least **5** qualifying threads
- across at least **2** distinct subreddits
- at least **1** from the past **6 months**
- at least **1** person **explicitly asking what tool to use**

Two subreddits matters because a single community can have a local obsession that
does not generalize. Recency matters because a problem solved in 2022 by a good
app is not your opportunity. And someone asking what to use is the closest thing
to a raised hand you will find for free.

## Grading

**T0 — silence.** You ran the queries properly and found nothing. Kill. Report the
exact queries so the kill can be audited; the usual cause is searching the product
category instead of the pain, and the orchestrator should be able to catch that.

**T1 — complaints, contented workaround.** People mention the annoyance and then
describe what they do instead, without frustration. Kill. Real pain that people
have made peace with does not convert to paid.

**T2 — active want.** The same complaint recurs across threads, people ask for a
tool, threads have real upvotes and replies. Pass.

**T3 — already paying or already hacking.** People pay for something they dislike,
or maintain spreadsheets, shortcuts and manual routines to cope. Pass, and rank it
above the T2s. This is the strongest signal available anywhere in the funnel,
stronger than any revenue estimate, because it is demand observed rather than
inferred.

Grade honestly in both directions. A generous grade costs the user weeks of
building; an ungenerous one costs one more round of searching.

## Handling what you find

- **Paraphrase.** Under fifteen words if you quote, one quote per thread maximum,
  and link every thread so the user can read the original themselves.
- **Do not profile individuals.** Summarize the pattern, never the person. No
  usernames, no assembling a picture of anyone from multiple posts.
- **Report the null result properly.** A documented T0 with its query list is a
  genuinely valuable output — it saves the build. Write it up with the same care
  as a pass.

## Why this gate and not a survey

Reddit is not representative of everyone, and it skews toward certain
demographics and certain kinds of complaint. It is used here because it is the
cheapest available source of *unprompted* problem statements — nobody posting in
r/productivity was asked a leading question by a founder who wanted a yes. That
unprompted quality is the whole value, and it is why this evidence outranks the
market inference collected earlier, despite the sampling bias. Note the bias in
the report when the target user is unlikely to be on Reddit at all, and treat a
T2 in that situation as weaker than it looks.
