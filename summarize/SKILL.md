---
name: summarize
description: "Turn any content into a decision — articles, URLs, YouTube and other videos, PDFs, docs, threads, pasted text, or a pile of several sources at once. Use whenever someone says 'summarize', 'tldr', 'break this down', 'what does this say', 'give me the gist', 'digest this', 'cliff notes', 'is this worth reading', 'what are the key points', or 'what should I take away from this' — and also when they simply paste a link or a wall of text and clearly want sense made of it, without naming a command. Prefer this over reading and paraphrasing by hand: it fetches content that is otherwise hard to reach (video transcripts, PDFs, blocked pages), delivers an opinion rather than a neutral book report, flags what the source gets wrong, and never invents a summary of something it could not actually read."
---

# Summarize

Turn content into a decision. The user isn't asking for a shorter version of what they sent — they're asking "should I care about this?" and "what do I do with it?" Answer both. Raw information is cheap; judgment is what's valuable.

## Get the actual content first

Never summarize from a URL slug, a title, a search snippet, or memory. It is the one failure that destroys trust in this skill, because a fabricated summary is indistinguishable from a real one until someone acts on it and gets burned.

There's a bundled fetcher that handles the awkward cases — video transcripts, PDFs, entity-mangled HTML — so you don't have to reinvent them each time:

```bash
python3 <skill-dir>/scripts/get_content.py "<url-or-path>"
```

It prints a header saying **how** the text was obtained, then the text. Read that header: a human-written caption track is near-exact, an auto-generated one garbles names and technical terms, and a local transcription may mishear proper nouns. Let that inform how firmly you quote.

Exit codes: `0` got text, `2` reached the source but couldn't extract (paywall, JS-only, no captions), `3` couldn't reach it at all.

Pick your route by input:

| Input | Do this |
|---|---|
| Video URL (YouTube, Vimeo, Loom, TikTok…) | The script — captions first, local transcription if needed |
| Article or blog URL | The script; if it exits 2 or 3, fall back to WebFetch |
| PDF, local file, or file path | The script, or just read it directly |
| Text pasted into the conversation | Work with it directly — no fetching |
| Nothing supplied yet | Only now ask what they want broken down |

**When fetching fails, say so and stop.** Report what you tried and offer a route through — "paste the text and I'll take it from there", or ask whether to try a browser for a page behind a login. Never paper over the gap with what you'd guess the article probably says. If you retrieved only part of the content, summarize that part and label the boundary explicitly.

Read the whole thing before writing a word. Skim-summaries miss the argument and land on the topic instead.

## Match the shape of the answer to the ask

Read the request's phrasing for how much depth is wanted:

- **"tldr?" / "gist?" / "quick summary"** → Quick-hit
- **No depth cue** → Standard
- **"break this down properly" / "deep dive" / "walk me through it"** → Detailed

Input size nudges this too — a 400-word blog post can't fill the Standard format without padding, so drop to Quick-hit rather than inflating. A 90-page report asked about casually still deserves Standard. When the two signals disagree, the user's phrasing wins.

### Quick-hit

**[Title/Source]** — 1–2 sentences on the core argument. Then 2–3 bullets, only the points that would change how someone thinks or acts. Close with one line: worth it or not, and why.

**One sentence per bullet, and about 120 words for the whole thing.** That budget is the hard part, and it's easy to miss by writing five blocks that each run three sentences — which technically looks like the right shape while being twice the length. If a bullet needs a second sentence to make sense, the bullet is carrying two ideas: cut the weaker one rather than extending it. Someone who typed four characters is scanning, and going long defeats the entire point of what they asked for.

### Standard

**[Title/Source]**

**Gist:** 2–3 sentences. State the thesis, not the topic. "This argues X because Y" beats "This is about X." If the argument is weak or derivative, say that here rather than burying it.

**Key takeaways:**
- 4–6 points, ranked by significance, not by running order
- Capture the insight, not the subject matter. "AI will change hiring" is filler. "AI screening produces 3x more false negatives on non-traditional candidates" is useful.
- Anyone who reads one bullet and stops should still come away smarter

**Standout details:**
- Surprising numbers, strong quotes, contrarian claims worth remembering
- Carry enough context that each one stands on its own

**What this misses:**
Blind spots, weak reasoning, absent context, obvious counterarguments the author dodged. One or two lines. This is often the most valuable thing in the summary, because it's the part the original author will never tell you. If the piece is genuinely solid, skip this section — manufacturing criticism to fill a heading is worse than leaving it out.

**So what:**
What should they *do* with this? Be concrete and forward-looking. Not "interesting for AI practitioners" but "if you're picking between A and B, this argues for A because of X." If nothing is actionable, say "useful context, nothing to act on" — that's a real answer.

**Verdict:** One honest line on whether the original is worth their time, and specifically what the full version gives them that this summary doesn't. "Yes — the examples land harder in full" or "No — this covers it; the original is 3x longer with nothing extra."

### Detailed

Standard, plus a **Section breakdown** — a line per major section so they can jump to what interests them. Only worth adding when the content has real sections.

### Technical content (docs, papers, APIs)

Lead with what the reader needs to *use*: how to enable it, what to call, which command. Background and design rationale come after. Someone reading API docs wants "how do I implement this" before "why was this designed this way."

## Several sources at once

When handed multiple links, don't produce N summaries stacked up — that's just the reading problem again in a shorter font. Synthesize:

- Open with what they collectively establish
- Then where they agree, and more usefully, **where they contradict each other** — name which source claims what
- Flag which single one is worth reading in full, if any

Fetch what you can and note any that failed rather than silently dropping them from the set.

## Principles

Not rules to execute mechanically — the reasoning behind why good summaries work.

**Your judgment is the product.** Anyone can compress text; models are very good at it. This skill exists for what plain compression doesn't give: an editorial stance, blind-spot detection, a verdict. Output that reads like a neutral book report has failed even when every fact in it is correct.

**Extract signal, don't compress evenly.** Most content is largely filler. Covering every section in proportion is the mistake. If a 3,000-word article carries one genuinely new idea, lead with that idea and let the rest go.

**Keep the specifics that give claims their weight.** "Revenue grew significantly" is noise. "Revenue grew 34% to $4.2B" is signal. Stripping numbers, names, and dates strips the reader's reason to believe any of it.

**Separate the source's claims from yours.** When you assess, make the seam visible — "the author claims X; that conflicts with Y." A reader should always be able to tell where the summary ends and the opinion starts.

**Plain language.** Translate jargon into meaning. "Synergistic go-to-market alignment" becomes "sales and marketing working together." Their time is the scarce resource, which is the entire reason they asked.
