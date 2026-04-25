---
name: client-proposal
description: "Generate client proposals from intro call transcripts. Takes a meeting transcript, researches the prospect's business, extracts pain points and team details, calculates pricing, and generates a one-page branded HTML proposal + send-with email. Use this skill whenever the user says 'proposal', 'write up the proposal', 'generate proposal', 'put together the proposal', references an intro call transcript, or mentions a new prospect meeting. Also trigger when the user pastes a meeting transcript and wants deliverables from it."
---

# Client Proposal Generator

Generates two deliverables from a single intro call transcript:
1. **Branded HTML Proposal** — one-page A4, print-to-PDF ready
2. **Send-with Email** — ready to copy and send with the proposal attached

---

## Step 0: Load Config

Read `~/.claude/skills/client-proposal/references/config.md`.

- **If the file cannot be read:** Stop and say: "The config file is missing from this skill. Go back to the guide page, fill in your details, and reinstall a fresh copy."
- **If any line's value contains `[YOUR_` (a literal placeholder):** Stop and say: "This skill hasn't been personalized yet. Go back to the guide page, fill in your details, and download a configured copy before installing."
- **Otherwise:** Load all values and proceed to Step 1.

---

## Workflow

### Step 1: Find the Transcript

Work through these sources in order — stop as soon as you have the transcript.

**1. Try the connected meeting tool first.**
If a meeting connector is available (Granola, Fireflies, Circleback, Fellow.ai, or Zoom), ask: "What's the client's company name? I'll pull the transcript from your meeting notes."

Search the connector for meetings matching that name. Then:
- **If one match is found:** show the meeting title and date, and confirm: "Found: [meeting title] on [date] — is this the right one?" Proceed only on confirmation.
- **If multiple matches are found:** list them (title + date) and ask the user to pick one.
- **If no match is found:** say so and fall through to source 2 or 3.

**2. Check the proposals folder.**
Look in `[proposals_folder]` for a folder matching the business name. Check for `intro-call-transcript.md` or `session-context.md` inside it. If `session-context.md` exists, use it as the primary source — only return to the raw transcript for missing details.

**3. Ask the user to paste.**
If neither source yields a transcript, ask: "I can't find a transcript for that client. Can you paste it here?"

### Step 2: Research the Prospect

Extract the business name and website from the transcript or session context. Use WebSearch to research:
- What the business does
- Team size
- Key people mentioned
- Location and any specialisations

If no website is mentioned, search for the business name + location + industry.

### Step 3: Extract from the Transcript

If `session-context.md` exists, use it as the primary source — only return to the raw transcript for missing details.

Extract:
- **Business name**
- **Key contacts** (names, roles)
- **Team size** (total headcount)
- **Number of practitioners / billable staff** (for ROI math)
- **Current tool stack**
- **Pain points** (specific complaints, frustrations, bottlenecks)
- **What they said success looks like** (their own words where possible)
- **Growth plans**
- **Meeting date**

### Step 4: Confirm the Price

Use the pricing from config to determine the recommended price.

**If a price was already stated on the call**, use that price. Confirm once: "Based on the call, I'll use $[X][tax_label] — does that still work?" If confirmed or no objection, proceed.

**If no price was mentioned**, present the recommendation and ask: "Based on [X] team members, I'd recommend $[Z][tax_label]. Does that work, or would you like to adjust?"

Never generate the proposal with an unconfirmed price.

### Step 5: Generate the Proposal HTML

Use the template in `references/proposal-template.html` as the exact HTML/CSS structure. Do not change the styling or layout. Only replace content and brand tokens.

**Every `[PLACEHOLDER]` in the template must be replaced. Nothing should remain as a literal bracket token in the saved file.**

**From config — same on every proposal:**

| Placeholder | Source |
|---|---|
| `[YOUR_ACCENT_COLOR]` | `accent_color` |
| `[YOUR_ACCENT_LIGHT]` | `accent_light` |
| `[YOUR_BUSINESS]` | `business` |
| `[YOUR_SERVICE_TAGLINE]` | `service_tagline` |
| `[TAX_LABEL]` | `tax_label` |
| `[YOUR_NAME]` | `name` |
| `[YOUR_PHONE]` | `phone` |
| `[YOUR_EMAIL]` | `email` |
| `[YOUR_WEBSITE]` | `website` |
| `[DELIVERABLE_1_TITLE]` | `deliverable_1_title` |
| `[DELIVERABLE_1_DESC]` | `deliverable_1_desc` — replace `[TOOL_STACK]` with tools from the call |
| `[DELIVERABLE_2_TITLE]` | `deliverable_2_title` |
| `[DELIVERABLE_2_DESC]` | `deliverable_2_desc` — replace `[TOOL_STACK]` if present |
| `[DELIVERABLE_3_TITLE]` | `deliverable_3_title` |
| `[DELIVERABLE_3_DESC]` | `deliverable_3_desc` — replace `[TOOL_STACK]` if present |
| `[DELIVERABLE_4_TITLE]` | `deliverable_4_title` |
| `[DELIVERABLE_4_DESC]` | `deliverable_4_desc` — replace `[TOOL_STACK]` if present |
| `[STEP_1_TITLE]` | `step_1_title` |
| `[STEP_2_TITLE]` | `step_2_title` |
| `[STEP_2_DESC]` | `step_2_desc` |
| `[STEP_3_TITLE]` | `step_3_title` |
| `[STEP_3_DESC]` | `step_3_desc` |
| `[STEP_4_TITLE]` | `step_4_title` |
| `[STEP_4_DESC]` | `step_4_desc` |
| `[TIMELINE]` | `default_timeline` |
| `[DELIVERY_FORMAT]` | `delivery_format` |

**From the page `<title>` tag:** `[service_name] | [business]`

**Per proposal — generated from transcript and call context:**

| Placeholder | Source |
|---|---|
| `[CLIENT_BUSINESS_NAME]` | Business name from transcript |
| `[DATE]` | Today's date |
| `[SERVICE_NAME_PART_1]` | First part of `service_name`, split naturally across two lines |
| `[SERVICE_NAME_PART_2]` | Second part of `service_name` — goes in the `<span>` for accent colour |
| `[INTRO_PARAGRAPH]` | 2–3 sentences on their specific situation. Mirror their language. 3 lines max. |
| `[KEY_CONTACTS]` | Names from transcript, used inside `step_1_desc` |
| `[STEP_1_DESC]` | `step_1_desc` from config with `[KEY_CONTACTS]` replaced from transcript |
| `[INVESTMENT_AMOUNT]` | Confirmed price |
| `[START_WEEK]` | Next available start week — ask the user if unsure |
| `[CONTEXT_BOX_TEXT]` | ROI math: [practitioners] × 30 min/day × 5 days × 48 weeks = hours/year × `billing_rate` = dollar figure. 2–3 sentences, conversational, specific to their numbers. |

**Content length rules — critical for single-page fit:**
- Intro paragraph: 3 lines max
- Deliverable descriptions: 1-2 lines each
- Context box: 2-3 sentences max
- If you're writing a fourth line anywhere, cut a sentence — do not expand CSS spacing

Save to: `[proposals_folder][business-name]/proposal.html`

### Step 6: Generate the Email

**Subject:** [Client Business] x [business] — [service_name] Proposal

**Body:**

> Hi [first names],
>
> Good to meet you today.
>
> I've attached the proposal based on our discussion. It covers a kickoff session, working sessions with [key ops/admin person by name, or "your team" if unclear], and a findings presentation in two to four weeks. Everything ranked by impact, with a dollar figure on each opportunity.
>
> I've got availability to kick off the first week of [next available month].
>
> I'll follow up with you early next week. If you have any questions in the meantime, please let me know.
>
> [name]

**Rules:**
- No recap of the call. The proposal carries the detail.
- No "happy to", "just checking in", or hedging language.
- Availability: use a specific week (e.g., "first week of May"). Ask the user if unsure.
- Do not add anything else. This template is final.

Save to: `[proposals_folder][business-name]/email.md`

---

## Writing Rules

Apply to all copy in the proposal and email:

- No em-dashes. Use commas, colons, or periods.
- No exclamation points.
- Contractions throughout (you're, we're, that's, don't).
- Name actual tasks, tools, and hours — never say "manual processes" when you can say "chasing invoices."
- Quantify in hours, not revenue.
- Lead with the problem, not the technology.
- No AI jargon (LLM, RAG, agent, neural network) unless the client specifically used it. Say "automation" or "systems."
- Never use: leverage, comprehensive, robust, streamline, cutting-edge, transform, empower, solution, landscape, crucial, delve, game-changer, unlock, unleash, elevate, harness, thrive.

For a richer voice guide, see `references/voice-profile.md` — fill it in once for more detailed tone control.

---

## File Structure

```
[proposals_folder]
└── [business-name]/
    ├── proposal.html
    └── email.md
```

---

## Important Notes

- The proposal must fit on one A4 page when printed to PDF (Cmd+P → Save as PDF with "Print backgrounds" on). The template is already calibrated. Adding content means something else must shrink.
- Always confirm the price before generating. Never auto-generate with an unconfirmed price.
- To update your setup details, go back to the guide page, fill in your updated values, download a new zip, and reinstall the skill.
