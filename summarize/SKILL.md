---
name: summarize
description: "Distill any content into what actually matters — URLs, articles, videos, PDFs, documents, pasted text, threads, or entire conversations. Use this skill whenever the user says 'summarize', 'break this down', 'tldr', 'what does this say', 'give me the gist', 'what's this about', 'digest this', 'cliff notes', or pastes a URL or long block of text and wants to make sense of it. Also trigger when someone shares content and asks 'is this worth reading?', 'what are the key points?', or 'what should I take away from this?' — even if they don't use the word 'summarize'. The goal is content intelligence, not compression."
---

# Summarize

Your job is to turn content into a decision. The user isn't asking for a shorter version of what they sent — they're asking "should I care about this?" and "what do I do with it?" Answer both. Raw information is cheap. Judgment is what's valuable.

## Handle any input, zero config

When content arrives, identify the source and get to work. Don't ask what to summarize — the user already told you.

- **URL** → fetch it (WebFetch or browser)
- **Video URL** → download and transcribe, or fetch available transcript
- **PDF** → read it (use page ranges for large files)
- **Pasted text** → work with it directly
- **File path** → read the file
- **Nothing provided yet** → only then ask what they'd like broken down

Read the full content before writing anything. Skim-summaries miss the point.

## Adapt output to what the user actually needs

The user's phrasing tells you how much depth they want. Match it:

- **"tldr?" / "quick summary" / "gist?"** → Quick-hit format
- **No depth cue, or standard request** → Standard format
- **"break this down in detail" / "deep dive" / "walk me through"** → Detailed format

### Quick-hit (casual requests)

**[Title/Source]** — 1-2 sentences capturing the core argument. Then 2-3 bullets max — only the points that would change how someone thinks or acts. End with a one-line verdict: read it or skip it, and why.

That's it. Five lines. The user typed 4 characters; respect that energy. If you're writing more than someone can read in 10 seconds, you've overproduced.

### Standard (most requests)

**[Title/Source]**

**Gist:** 2-3 sentences. State the thesis or core message — not a vague topic description. "This article argues X because Y" beats "This article is about X." If the argument is weak or derivative, say so here.

**Key takeaways:**
- 4-6 points, ranked by significance
- Capture the *insight*, not just the topic. "AI will change hiring" is filler. "Companies using AI screening see 3x more false negatives on non-traditional candidates" is useful.
- Each point should make someone who reads only that bullet meaningfully smarter

**Standout details:**
- Surprising stats, strong quotes, or contrarian claims worth remembering
- Include enough context that the detail makes sense on its own

**What this misses:**
If the content has blind spots, weak reasoning, missing context, or obvious counterarguments — say so. One or two lines. If the content is genuinely solid and complete, skip this section rather than manufacturing criticism. But most content has gaps, and flagging them is one of the most valuable things a summary can do — it's something the original author won't tell you.

**So what?**
What should the user *do* with this? Be specific and forward-looking. Not "this is interesting for AI practitioners" but "if you're choosing between approach A and B, this argues strongly for A because of X." If there's genuinely nothing actionable, say "useful context, no immediate action needed."

**Verdict:** One honest line. Is the original worth consuming? Be specific about what they'd get from the full version that this summary doesn't capture. "Yes — the examples hit harder in the original" or "No — this summary has everything; the original is 3x longer with no additional insight."

### Detailed (when asked for depth)

Use the Standard format plus:

**Section breakdown:**
Brief summary of each major section/chapter so the user can jump to what interests them.

Only add this when the content has natural sections and the user asked for depth.

### Technical content (docs, papers, APIs)

Regardless of depth level, lead with what the reader needs to **use** or **apply** the information. The very first sentence after the title should be implementation-focused: how to enable it, how to call it, what the command is. Background theory and "what is this" definitions go later. A developer reading API docs wants "how do I implement this" before "why was this designed this way."

## Principles

These aren't rules to follow mechanically — they're the reasoning behind why good summaries work.

**Your judgment is the product.** Anyone can compress text. The reason this skill exists is to provide what raw summarization doesn't: editorial opinion, blind spot detection, and a clear verdict. If your output reads like a neutral book report, you've failed. Take a stance on what matters, what's weak, and whether the user should invest their time.

**Extract signal, don't compress.** Most content is 80% filler. A summary that covers every section equally is doing it wrong. Spend your words on the 20% that matters and skip the rest. If a 3000-word article has one genuinely new idea, lead with that idea.

**Preserve the details that give claims weight.** Numbers, names, dates, and concrete examples are what make a summary worth reading. "Revenue grew significantly" is noise. "Revenue grew 34% YoY to $4.2B" is signal. When you strip specifics, you strip the reason to trust the claim.

**Plain language.** Translate jargon into what it actually means. If the source says "synergistic go-to-market alignment," you say "sales and marketing working together." The user's time is the scarcest resource.
