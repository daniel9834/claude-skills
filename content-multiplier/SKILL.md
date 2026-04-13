---
name: content-multiplier
version: 1.0
description: Turn one piece of content into platform-native posts across LinkedIn, X, Instagram, TikTok, YouTube, and Threads. Two-pass generation with quality filtering.
---

# Content Multiplier

One idea can reach eight audiences — but only if you rebuild it for each one. Copy-pasting a LinkedIn post to Twitter doesn't work. Reformatting a blog into a carousel doesn't work. What works is understanding the idea deeply enough to express it differently for each platform's culture, algorithm, and attention pattern.

This skill does that in two passes. First it analyzes, proposes, and gets approval. Then it generates, self-evaluates, and writes only the pieces worth publishing.

---

## Brand Context

This skill reads persistent context from `./profile/` to match the user's brand across every platform. All files are optional — the skill works without them.

**What it reads:**

| File | Purpose | Created by |
|------|---------|------------|
| `./profile/tone.md` | How the brand sounds — sentence patterns, word choices, formality | /brand-voice or similar |
| `./profile/style.md` | Visual identity — colors, fonts, logo placement, design direction | /creative or similar |
| `./profile/insights.md` | What's worked and what hasn't — platform-specific performance data | Accumulated from feedback |
| `./profile/tools.md` | Connected scheduling tools, social accounts, API keys | /setup or similar |

**On invocation, check for `./profile/` and load what exists:**

If `tone.md` exists: read it, apply per-platform voice adjustments (see Platform Tone Shifts below), and confirm what was loaded. Example: "Loaded your tone guide — direct, short sentences, proof-heavy. Adjusting per platform."

If `style.md` exists: read it and reference brand colors/fonts when writing visual content notes for carousels and thumbnails. Example: "Style guide loaded. Carousel notes will reference your visual system."

If `insights.md` exists: check for platform-specific data — which hooks worked, which formats flopped, optimal posting times. Example: "Found 4 platform insights. Applying: your audience prefers carousels over text posts on LinkedIn."

If `tools.md` exists: check for connected scheduling tools and social accounts. Example: "Buffer connected with 3 accounts."

**Show what loaded:**

```
Profile context:
  Tone guide       loaded — "direct, conversational, no jargon"
  Style guide      loaded
  Insights         4 entries (2 platform-specific)
  Tools            Buffer connected
```

---

## First Run: Setup Interview

If `./profile/` doesn't exist, or exists but is empty (no tone.md, no platforms.md), this is a first run. Before doing anything else, offer the setup interview — but let the user skip it if they want to get straight to work.

```
Looks like this is your first time running
/content-multiplier. I can ask you 5 quick
questions (~2 min) to learn your voice, platforms,
and what's worked for you before.

This makes a real difference — content that
sounds like you vs content that sounds like AI.

  1. Let's do it (recommended)
  2. Skip for now — just use defaults

You can always run the setup later by saying
"set up my profile."
```

**If they choose 1 (setup):** Run the interview below.

**If they choose 2 (skip):** Proceed immediately. Ask only which platforms they post on (that question is required — without it, you don't know what to generate). Skip tone, style, tools, and insights. Use neutral defaults. Create `./profile/platforms.md` from their answer so the platform question doesn't repeat.

After skipping, when delivering the output, add a single line at the end:

```
These were generated with default tone settings.
Run the setup ("set up my profile") anytime and
the next batch will sound like you, not like AI.
```

Do not repeat this reminder on subsequent runs — say it once.

---

### The Setup Interview

**The interview is fast — 5 questions, conversational, not a form.** Ask them one at a time. Wait for each answer before asking the next. Use their answers to build the profile files so every future run is personalized.

**Question 1 — Platforms**

```
Which platforms do you actually post on?

  1. LinkedIn
  2. Twitter / X
  3. Instagram
  4. TikTok
  5. YouTube
  6. Threads

Pick all that apply (e.g. "1, 2, 3").
I'll only generate content for these.
```

Save to `./profile/platforms.md`.

**Question 2 — Voice and tone**

```
How would you describe how you sound online?

Some examples to jog your thinking:
- "Direct and punchy, no fluff"
- "Warm and conversational, like talking to a friend"
- "Data-driven and analytical, I let the numbers talk"
- "Casual and funny, I don't take myself too seriously"

Or share a link to a post you've written that
sounds like you, and I'll reverse-engineer it.
```

If they share a link or paste content, analyze it and extract: sentence length patterns, formality level, vocabulary tendencies, use of humor, use of data/proof, how they open and close. If they describe it in words, capture that directly.

Save to `./profile/tone.md` with this structure:

```
# Tone Guide

## Voice Summary
[One-line description of how they sound]

## Patterns
- Sentence length: [short/medium/long/mixed]
- Formality: [casual/conversational/professional/academic]
- Proof style: [anecdotes/data/both/neither]
- Humor: [none/occasional/frequent]
- Opening tendency: [direct claim/question/story/data]

## Words They Use
[List of words and phrases from their content or description]

## Words They Avoid
[List of words/phrases that feel off-brand based on their description]

## Raw Input
[What they actually said, preserved for future reference]
```

**Question 3 — Visual identity (quick)**

```
Do you have brand colors, fonts, or a visual
style you use for carousels and graphics?

If yes, tell me:
- Primary colors (hex codes or descriptions)
- Fonts you use
- Any design rules (e.g. "always dark background")

If no, I'll skip visual notes for now.
You can add this later.
```

If they have visual identity, save to `./profile/style.md`. If not, skip — don't create the file.

**Question 4 — Scheduling tools**

```
Do you use a scheduling tool for posting?
(Buffer, Hootsuite, Later, or similar)

If yes, which one? If no, I'll include
recommended posting times with every piece
and you can copy-paste when ready.
```

If they use one, save to `./profile/tools.md`. If not, skip — don't create the file.

**Question 5 — What's worked before**

```
Last question — is there anything you already
know works well for your audience?

Examples:
- "Carousels crush it for me on LinkedIn"
- "My audience hates listicles"
- "Story-driven posts get the most saves on IG"
- "I have no idea yet, I'm just starting"

Anything you tell me here helps me prioritize
the right formats and angles from the start.
```

If they have insights, save to `./profile/insights.md` with dated entries. If they're just starting, skip — the file will be created naturally from feedback after the first few runs.

**After the interview, confirm what was created:**

```
Profile built:
  Tone guide       created — "[summary]"
  Style guide      [created / skipped]
  Platforms        [N] platforms selected
  Tools            [tool name / skipped]
  Insights         [N entries / starting fresh]

  Saved to ./profile/

  Ready to multiply your first piece of content.
  Paste or describe what you want to work with.
```

**On subsequent runs:** Skip the interview entirely. Load existing profile files silently. Only show the profile context summary (below).

**If profile exists but is partial:** Don't re-interview. Load what exists, note what's missing in a single line ("No tone guide yet — I'll use neutral defaults. Run /content-multiplier setup to add one."), and proceed. The user can add missing pieces whenever they want by saying "update my tone" or "add my brand colors."

**Manual re-run:** If the user says "update my profile," "redo the setup," or "change my platforms," re-run the relevant question(s) only, not the whole interview.

```
Profile context:
  Tone guide       loaded — "direct, conversational, no jargon"
  Style guide      loaded
  Insights         4 entries (2 platform-specific)
  Tools            Buffer connected
```

Or if partial:

```
Profile context:
  Tone guide       loaded — "sharp, proof-heavy"
  Style guide      not set (say "add my brand colors" anytime)
  Insights         none yet (builds automatically from feedback)
  Tools            not set
```

---

## What You Can Feed It

This skill needs something to work with. That can be a finished piece of content, a rough draft, or even just an idea. Here's how each input type works:

### Text content (paste it or point to a file)

This is the ideal input. The skill can work with it immediately.

- Blog post or article
- Newsletter edition
- Case study or whitepaper
- Written framework, process, or how-to
- YouTube script or outline
- Reel or TikTok script you've already written
- Podcast transcript
- Presentation notes or slide deck text
- Email you wrote that had a great insight in it
- Social post that performed well and deserves more mileage

**How to provide it:** Paste the text directly into the conversation, or say "use ./path/to/file.md" and the skill will read it.

### Video or audio (needs transcription first)

The skill can't watch videos or listen to audio. If the source is a Reel, TikTok, YouTube video, podcast episode, or voice memo, you need to transcribe it first and then feed the transcript.

**If someone provides a video or audio URL or file, tell them:**

```
I can't watch or listen to that directly —
I need the text to work with.

Transcribe it first using any transcription
tool (Whisper, Descript, YouTube's auto-captions,
otter.ai, etc.) and paste the transcript here.

Even a rough transcript works — I'll clean it
up during analysis.
```

Don't block on this. If they can describe the key points from the video instead of transcribing it, that's enough to work with — treat it as an "idea" input (see below).

### Just an idea (no source content yet)

If someone doesn't have a finished piece of content but has a topic, an opinion, or a rough concept, the skill can still work. It just means the analysis step generates the angles from the idea itself rather than extracting them from existing material.

**If someone provides an idea instead of content, tell them:**

```
Got it — no source content yet, just the idea.
I'll build the angles and content from scratch
instead of extracting from an existing piece.

The output will be original content for each
platform, not repurposed from a source.
```

Then run the same two-pass flow: analyze the idea (find angles, emotional core, distinct entry points), propose platform assignments, generate, evaluate, write.

The quality is slightly lower than working from a rich source (there's less material to draw from), but it's still substantially better than writing each platform post from nothing.

---

## Platform Tone Shifts

The same person sounds different on LinkedIn vs TikTok vs Threads. When a tone guide is loaded, apply these adjustments:

| Platform | Register | Energy | Default Length | What the audience expects |
|----------|----------|--------|----------------|---------------------------|
| LinkedIn | Polished but not stiff | Measured | Longer, structured | Credibility, depth |
| Twitter/X | Sharp, compressed | High | Very short | Speed, edge, conviction |
| Instagram | Visual-first, warm | Medium | Caption-length | Aesthetic, story |
| TikTok | Unfiltered, fast | Very high | Spoken-word short | Authenticity, entertainment |
| YouTube | Explanatory, natural | Medium | Script-length | Depth, personality |
| Threads | Relaxed, thoughtful | Medium-low | Medium text | Genuine conversation |

**Example — identical insight adapted eight ways:**

> **Insight:** Simple strategies outperform complex ones.

- **LinkedIn:** "A decade of marketing taught me one thing the hard way: the strategies that actually work are embarrassingly simple. Here's what I mean."
- **X:** "Complex strategy is a coping mechanism. Simple strategy is a competitive advantage."
- **Instagram:** [Visual: "Simple > Complex" in bold] + caption telling the story
- **TikTok:** "OK so I need to talk about this thing where everyone's making their marketing way harder than it needs to be..."
- **YouTube:** "If you've spent any time building campaigns, you've probably noticed a pattern..."
- **Threads:** "I keep coming back to this idea that the best strategies are the ones you can explain in one sentence. Anyone else notice this?"

---

## The Two-Pass Flow

### Pass 1: Analyze and Propose

This pass is lightweight — no full content generation. Its job is to understand the source material deeply and get alignment before committing to full generation.

**Step 1 — Confirm target platforms**

Read `./profile/platforms.md` (created during the first-run setup interview). This is the user's platform list — generate content only for these platforms.

If the user says "add [platform]" or "skip [platform]" for this run, adjust accordingly. Temporary overrides don't change the saved file — only "update my platforms" modifies the stored list.

If `platforms.md` somehow doesn't exist (e.g. user deleted it), ask which platforms they want before proceeding and recreate the file.

**Step 2 — Analyze the source**

Don't just extract bullet points. Find the angles.

For any source content (blog post, newsletter, podcast transcript, video transcript, talk, case study, research), identify:

1. **The emotional core** — What feeling does this content create? What tension does it resolve? What belief does it challenge?

2. **The argument structure** — Is it a story? A framework? A list? A comparison? A confession? An argument from evidence?

3. **Distinct entry points** — Find 3-5 genuinely different ways into the same idea. Not "point 1, point 2, point 3" from a list. Different *angles*:
   - The personal story angle (what happened to you)
   - The data/proof angle (what the numbers show)
   - The contrarian angle (why conventional wisdom is wrong)
   - The practical angle (what someone can do right now)
   - The philosophical angle (what this reveals about the bigger picture)

4. **Standalone fragments** — Individual sentences, stats, or moments that work as self-contained posts without any context from the source.

Show the analysis before proceeding:

```
Source Analysis
---

  Core: [one-sentence emotional core]

  Structure: [story / framework / argument / list / confession]

  Entry Points:
    1. [Angle name] — [one-line description]
    2. [Angle name] — [one-line description]
    3. [Angle name] — [one-line description]
    4. [Angle name] — [one-line description]

  Fragments:
    - "[standalone quote or stat]"
    - "[standalone quote or stat]"
    - "[standalone quote or stat]"
```

**Step 3 — Propose platform assignments**

For each target platform, propose which angle to use, what format works best, and the opening line. Keep proposals to ~50 words each.

```
Proposed Content
---

  LinkedIn (carousel, 8 slides)
    Angle: The framework angle
    Opens with: "[proposed hook]"

  X (thread, 7 posts)
    Angle: The contrarian angle
    Opens with: "[proposed hook]"

  Instagram (carousel + reel script)
    Angle: The personal story angle
    Opens with: "[proposed hook]"

---
Approve these? Or redirect any platform.
(Say "drop [platform]" to skip one.)
```

Wait for approval before generating. If the user redirects ("use the story angle for LinkedIn instead"), adjust and confirm.

### Pass 2: Generate and Evaluate

**Step 4 — Load platform references**

For each approved platform, read the corresponding file from `./platforms/{platform}.md`. Only load what's needed — a 3-platform run loads 3 files, not 8.

**Step 5 — Generate content**

Using the approved angles, loaded platform references, and tone guide (if available), generate full content for each platform. Apply the format templates and opening patterns from the platform files.

For each piece, ensure:
- It stands alone — someone seeing only this piece understands it
- It opens strong — the first line works without context
- It feels native — reads like it was written for this platform specifically
- It has a clear action — every piece ends with something the reader can do
- The tone shifts per platform — same person, different room

**Step 6 — Self-evaluate and filter**

After generating all pieces, score each one:

| Criteria | Question |
|----------|----------|
| Independence | Does this make sense without the source? |
| Platform fit | Would a regular user of this platform engage with this? |
| Hook strength | Does the opening line earn the second line? |
| Forced or natural | Was this a natural fit, or did I have to stretch? |

If a piece scores poorly on any dimension, flag it:

```
Quality Check
---

  LinkedIn carousel      [strong] — natural fit, hook is sharp
  X thread               [strong] — contrarian angle works here
  Instagram carousel     [strong] — visual angle is clear
  Instagram reel script  [cut] — this topic doesn't translate
                         to video naturally, dropping it
Generated 4, shipping 4. All strong.
```

Five strong pieces beat eight mediocre ones. Cut aggressively.

**Step 7 — Write files**

Write approved content to the output directory. Structure:

```
./output/{source-slug}/
  breakdown.md                  <- Source analysis from Step 2
  linkedin/
    carousel.md
    post-01.md
  twitter/
    thread.md
    tweet-01.md
    tweet-02.md
  instagram/
    carousel.md
    reel-script.md
  tiktok/
    script-01.md
  youtube/
    short-script.md
  threads/
    post-01.md
    mini-thread.md
  calendar.md                   <- Posting schedule with dates
```

**Source slug:** lowercase, hyphens, max 40 chars. "5 Pricing Mistakes That Kill SaaS Growth" becomes `pricing-mistakes-saas-growth`.

**File metadata block** (top of every content file):

```
# Meta
- Platform: LinkedIn
- Type: Carousel
- Source: "5 Pricing Mistakes That Kill SaaS Growth"
- Created: Apr 13, 2026
- State: Draft
- Post at: Tuesday 8:00 AM
```

After writing, display what was saved:

```
Saved
---

  ./output/pricing-mistakes-saas-growth/
    breakdown.md                    done
    linkedin/carousel.md            done
    linkedin/post-01.md             done
    twitter/thread.md               done
    twitter/tweet-01.md             done
    twitter/tweet-02.md             done
    instagram/carousel.md           done
    calendar.md                     done

  8 files written across 3 platforms.
  1 piece cut (Instagram reel — forced fit).
```

If `./profile/catalog.md` exists, append entries for each new piece.

---

## Posting Schedule

When writing the calendar, sequence content for maximum reach:

| Day | Why this order |
|-----|---------------|
| Day 1 | LinkedIn carousel or text post — longest shelf life, sets the narrative |
| Day 1-2 | X thread — drives discussion while the idea is fresh |
| Day 2 | Threads post — conversational take, cross-pollinates with Instagram |
| Day 2-3 | Instagram carousel — visual version, repurpose LinkedIn design direction |
| Day 3-4 | TikTok / Reel — video production takes longer, post when ready |
| Day 4-5 | YouTube Short — can repurpose TikTok footage |
| Ongoing | Individual tweets, single posts — drip from standalone fragments |

**Default posting windows** (general best practices — override with insights data if available):

| Platform | Best windows | Notes |
|----------|-------------|-------|
| LinkedIn | Tue/Thu 8-10 AM local | Quality over frequency — 2-3x/week max |
| X | Weekdays 12-1 PM local | Single tweets anytime, threads midday |
| Instagram | Mon/Wed/Fri 11 AM local | Carousels morning, Reels evening |
| TikTok | Tue/Thu 7-9 PM local | After-work consumption hours |
| YouTube | Sat 9-11 AM local | Weekend discovery window |
| Threads | Daily 9-11 AM local | Casual morning browsing |

If `./profile/insights.md` has timing data for specific platforms, use that instead.

---

## Batch Mode

When the user says "create a content calendar from this," "give me a week of posts," or "schedule this across platforms," generate a full weekly plan.

Process:
1. Run the full two-pass flow
2. Assign specific dates (not just "Day 1, Day 2")
3. Space content across the week so no platform gets hit twice in one day
4. Write all content files plus a master `calendar.md`

The calendar file format:

```
# Content Calendar

Source: "Title of Source Content"
Week: Apr 14-20, 2026
Platforms: LinkedIn, X, Instagram

---

MONDAY APR 14

  08:00 AM    LinkedIn    carousel.md
              "Opening hook preview text here"
              Format: 8-slide educational carousel

  12:00 PM    X           thread.md
              "Opening hook preview text here"
              Format: 7-post thread

---

TUESDAY APR 15

  09:00 AM    LinkedIn    post-01.md
              Deep dive on one specific angle

  01:00 PM    X           tweet-01.md
              Standalone insight from the source

---

[... continues through the week ...]

---

SUMMARY

  Total posts: 12
  Platforms: 4
  Unique pieces: 10 (some adapted across platforms)
  Cut: 1 (weak fit — Instagram reel)
```

---

## Scheduling Tools

On invocation, check `./profile/tools.md` and `.env` for scheduling tool API keys:

- `BUFFER_ACCESS_TOKEN` — Buffer
- `HOOTSUITE_API_KEY` — Hootsuite
- `LATER_API_KEY` — Later

**If a scheduler is found:** Note it and include recommended times in the calendar. Do not auto-schedule — let the user decide when to push content.

**If no scheduler is found:** Include recommended times in every content file and in the calendar. Suggest connecting one:

```
No scheduling tool detected. Content saved
with recommended post times.

To connect a scheduler, add an API key to .env:
  BUFFER_ACCESS_TOKEN=your_key_here

Then run /setup to configure connected accounts.
```

---

## Performance Tracking

After delivering content, collect feedback:

```
How did these perform?

  1) Published as-is — worked well
  2) Published with edits — needed tweaks
  3) Rewrote most of it
  4) Haven't published yet

(Answer anytime. Tell me which platforms
did best and I'll optimize next time.)
```

**Processing:**

If (1): Append to `./profile/insights.md` with platform, format, and what shipped. Example entry:
`[2026-04-13] [/content-multiplier] LinkedIn carousel published as-is. Framework angle, direct tone. Source: pricing-mistakes.`

If (2): Ask what they changed. Log the delta. If tone was the issue, suggest updating `tone.md`. Example entry:
`[2026-04-13] [/content-multiplier] X thread needed shorter sentences. Default tone may be too formal for X. User cut from 7 to 5 tweets.`

If (3): Ask for details or the final version. If it's a pattern (e.g., Instagram always needs rewriting), flag it as a recurring issue. Example entry:
`[2026-04-13] [/content-multiplier] User rewrote Threads post — shifted from observation angle to personal story. Threads audience for this niche prefers narrative over analysis.`

If (4): Note it. On next run, check if they published the last batch: "Last time I built content from your pricing post. Did any of it ship? Performance data helps me improve."

**Evolving from defaults:**

After 5+ feedback entries, check whether the user's winning patterns differ from the default opening patterns in the platform files. If they do, note it in the proposal step: "Your last 3 LinkedIn hits used personal story openers, not frameworks. Using that angle."

The defaults are scaffolding. The user's actual data replaces them over time.

---

## Catalog Registry

If `./profile/catalog.md` exists, append an entry for each piece of content created:

```
| Piece | Platform | Type | Created | Source | State |
|-------|----------|------|---------|--------|-------|
| pricing-carousel | LinkedIn | Carousel | Apr 13 | pricing-mistakes | draft |
| pricing-thread | X | Thread | Apr 13 | pricing-mistakes | draft |
```

New entries append to the bottom. Never overwrite existing rows. The user updates `State` to `published` or `retired` manually.

If the file doesn't exist, create it with the header row and the new entries.

---

## Common Mistakes

These apply across all platforms. Platform-specific pitfalls are in the individual platform files.

**Don't cross-post.** The same text on LinkedIn and X performs 40-60% worse than platform-native content on both. If you're going to post on multiple platforms, rebuild for each one. That's the entire point of this skill.

**Don't use the same opening everywhere.** A LinkedIn hook has different energy than a TikTok hook than a Threads post. The platform tone shifts table exists for a reason.

**Don't post everything at once.** Stagger across days. Each piece needs room to find its audience. Posting 8 pieces in one morning cannibalizes your own reach.

**Don't force a platform.** If the source material doesn't translate to video naturally, don't write a TikTok script just to fill the slot. The quality gate exists to prevent this. Cut weak pieces.

**Don't forget the action.** Every platform piece needs a clear next step — but make it platform-appropriate. "Save this" on Instagram. "Reply with your take" on X. "Follow for more" everywhere. "DM me [word]" when driving leads.

**Don't treat similar platforms as identical.** Threads is not X. Instagram is not LinkedIn. Each has its own culture, norms, and audience expectations. Read the platform files.

**Don't ignore what's working.** After a few runs, your `insights.md` will tell you what performs. Use that data. If carousels always outperform text posts for your audience on LinkedIn, lead with carousels. Defaults are for day one.

---

## Source Types

Different sources have different atomization potential:

| Source | Strength | Natural platforms |
|--------|----------|-------------------|
| Blog post / article | Lots of material, structured arguments | All platforms — high potential |
| Newsletter | Opinion-dense, already conversational | LinkedIn, X, Threads |
| Podcast / interview | Stories, quotes, hot takes | Short video, threads, carousels |
| Long-form video | Visual moments, teachable clips | Shorts, Reels, TikToks, carousels |
| Talk / presentation | Frameworks, key slides, audience reactions | Carousels, threads, video clips |
| Case study | Data, transformation story, proof points | LinkedIn, X threads, Threads |
| Research / data | Charts, surprising stats, implications | Carousels, data posts, LinkedIn |
| Framework / process | Step-by-step, visual flow | Carousels, threads, tutorial video |

---

## Output Presentation

Every run of this skill should feel like getting a deliverable from a senior content strategist — not a chatbot reply. The output IS the product. Presentation matters.

### Core Rules

1. **Lead with the deliverable.** No preamble ("Here's your content!"), no filler, no "Great choice!" No chatbot energy. Start with the content or the analysis.
2. **Section labels in caps, followed by `---` on the next line.** This creates a clean visual hierarchy without relying on markdown headers in terminal output.
3. **Use simple indentation (2 spaces) for nested content.** Consistent throughout.
4. **Status markers:** `done`, `cut`, `skip`, `pending` — plain text, no symbols.
5. **File paths** relative to project root with `./` prefix. Show actual paths, not placeholders.
6. **Line width under 55 characters** for terminal readability. File paths and URLs may exceed this.
7. **No emoji.** Ever. Professional restraint.
8. **No markdown formatting in output.** No `**bold**`, no `# headers`, no `` `backticks` `` in the formatted output blocks. Use caps and indentation for hierarchy instead.

### Required Sections

Every output MUST include these four sections in this order:

**1. Header** — What the user is looking at and when it was made.

```
CONTENT MULTIPLIER
---

  Source: "5 Pricing Mistakes That Kill SaaS Growth"
  Platforms: LinkedIn, X, Instagram
  Generated: Apr 13, 2026
```

**2. Content** — The actual deliverable (analysis, proposals, or generated content summary). Structure varies by which step of the flow you're in.

**3. Saved** — Every file written to disk, listed explicitly. The user should never have to hunt for output.

```
Saved
---

  ./output/pricing-mistakes-saas-growth/
    breakdown.md                    done
    linkedin/carousel.md            done
    linkedin/post-01.md             done
    twitter/thread.md               done
    twitter/tweet-01.md             done
    instagram/carousel.md           done
    calendar.md                     done

  7 files across 3 platforms.
  1 piece cut (Instagram reel — forced fit).
```

If a file was updated rather than created, note it: `done (updated)`.
If no files were written (e.g., analysis-only step), show: `No files written (analysis step)`.

**4. Next Steps** — Guide the user forward. Always offer 2-4 concrete actions.

```
Next Steps
---

  Content is saved and ready to review.

  > /creative       Build carousel graphics (~15 min)
  > Review calendar.md for posting schedule
  > "update my tone" to refine your profile

  Or tell me what to work on next.
```

### What the Proposal Step Looks Like

During Pass 1 (propose), the output is lightweight:

```
CONTENT MULTIPLIER
---

  Source: "5 Pricing Mistakes That Kill SaaS Growth"
  Platforms: LinkedIn, X, Instagram


Source Analysis
---

  Core: SaaS founders lose revenue not from bad
  products but from bad pricing decisions — and
  the mistakes are predictable.

  Structure: List with narrative (5 mistakes,
  each with a story and a fix)

  Entry Points:
    1. The confession — mistakes you made yourself
    2. The framework — how to audit your pricing
    3. The contrarian — why "premium pricing" fails
    4. The practical — 5 fixes you can do this week


Proposed Content
---

  LinkedIn (carousel, 8 slides)
    Angle: The framework
    Opens with: "I've audited 100+ SaaS pricing
    pages. The same 5 mistakes keep showing up."

  X (thread, 6 posts)
    Angle: The contrarian
    Opens with: "Premium pricing is killing more
    SaaS companies than free tiers. Here's the data."

  Instagram (carousel, 10 slides)
    Angle: The practical
    Opens with: "Fix your SaaS pricing this week"
    [Visual: bold text cover slide]


Approve these? Or redirect any platform.
Say "drop [platform]" to skip one.
```

### What the Final Output Looks Like

After generation and quality evaluation:

```
Quality Check
---

  LinkedIn carousel      strong
  LinkedIn text post     strong
  X thread               strong
  X tweet (standalone)   strong
  Instagram carousel     strong
  Instagram reel script  cut — topic doesn't
                         translate to video naturally

  Generated 6, shipping 5. Cut 1 weak piece.


Saved
---

  ./output/pricing-mistakes-saas-growth/
    breakdown.md                    done
    linkedin/carousel.md            done
    linkedin/post-01.md             done
    twitter/thread.md               done
    twitter/tweet-01.md             done
    instagram/carousel.md           done
    calendar.md                     done

  7 files across 3 platforms.


Next Steps
---

  Content is saved and ready to review.

  > /creative       Build carousel graphics (~15 min)
  > Review calendar.md for posting schedule
  > "how did these perform?" after publishing

  Or tell me what to work on next.
```

---

## Connecting to Other Skills

**Feeds into this skill:**
- Blog posts, newsletters, case studies, transcripts — any source content

**This skill feeds into:**
- Visual design tools — carousel graphics, thumbnails, video assets
- Scheduling tools — push content to Buffer, Later, etc.
- `./profile/insights.md` — performance data accumulates over time
- `./profile/catalog.md` — asset registry grows with each run

**The cycle:**
1. Create source content (blog, podcast, video)
2. Run /content-multiplier to generate platform-native pieces
3. Publish, collect performance data
4. Feed insights back into the next run
5. Over time, the skill learns what works for your audience on each platform
