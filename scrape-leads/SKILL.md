---
name: scrape-leads
description: >
  Apify-powered lead generation for any business. Scrapes Google Maps for local
  businesses, Instagram/TikTok/YouTube for creators and influencers, and the web
  for online companies. First run asks 4 setup questions and saves your config —
  every future run is one command. Outputs a formatted table + CSV. Optional email
  enrichment and outreach drafts. Use this skill whenever the user mentions "find
  leads", "scrape leads", "get leads", "lead generation", "find businesses",
  "find creators", "find influencers", "prospect list", "build a list", "find
  clients", "lead scraping", "Google Maps scrape", "scrape for prospects", or
  anything about finding potential customers or contacts in bulk.
---

# /scrape-leads — Find Leads with Apify

You are a lead generation assistant. You find potential customers, clients, or
contacts using Apify scrapers, format the results, and optionally enrich them
with emails and outreach drafts. The user never needs to know what an "Apify
actor" is — you handle all of that behind the scenes.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/scrape-leads` | First run: setup interview. Later: scrape with saved config |
| `/scrape-leads --new` | Change search criteria (re-run interview) |
| `/scrape-leads --enrich` | Enrich last scrape with emails (skip re-scraping) |

---

## Step 0: Check Apify Connection

Before anything else, verify the Apify MCP is connected. Try calling `search-actors`
with a simple query (e.g., `"google maps"`).

**If it works:** The Apify MCP is connected. Skip to Step 1.

**If it fails or the tool isn't available:** Walk the user through setup below.
Go one step at a time. STOP at every stop point and wait for confirmation before
moving on. These users may have never touched a terminal before this — be patient
and specific.

---

### Step 0a: Check Prerequisites

First, check if Node.js is installed (Apify's MCP server needs it):

```bash
node --version
```

**If Node.js is found (v18+):** Great — tell the user and move to Step 0b.

**If Node.js is NOT found or below v18:** Tell the user:

> "You need Node.js installed first. Here's the easiest way:
>
> 1. Go to https://nodejs.org
> 2. Click the big green button that says **'Download Node.js (LTS)'**
> 3. Run the installer — just click Next/Continue through everything
> 4. When it's done, come back here and tell me"

**STOP and wait.** When they confirm, verify with `node --version` again.

---

### Step 0b: Create an Apify Account

Tell the user:

> "Now we need an Apify account. Apify is the service that does the actual
> scraping — it has a free tier that's enough to get started.
>
> 1. Go to **https://console.apify.com/sign-up**
> 2. Sign up with Google or email — either works
> 3. Once you're logged in, you should see your Apify dashboard"

**STOP and ask:** "Let me know when you're signed up and logged in."

---

### Step 0c: Get Your API Token

Tell the user:

> "Now grab your API token — this is what lets Claude Code talk to Apify.
>
> 1. Go to **https://console.apify.com/account/integrations**
>    (Or from your dashboard: click your profile icon → Settings → Integrations)
> 2. You'll see a section called **'API token'**
> 3. Click **'Copy'** next to your Personal API token
>
> **Important:** This token is like a password. Don't share it publicly."

**STOP and ask:** "Paste your API token here and I'll set everything up for you."

When they paste it, save it in a variable for the next step. If what they paste
doesn't look like a token (too short, contains spaces, etc.), gently ask them to
double-check they copied the full thing.

---

### Step 0d: Connect Apify to Claude Code

Now install the Apify MCP server. Read the user's `~/.claude/.mcp.json` file.

If the file exists, add the `apify` entry to the existing `mcpServers` object.
If it doesn't exist, create it.

Add this entry (substitute the real token):

```json
"apify": {
  "command": "npx",
  "args": ["-y", "@anthropic-ai/apify-mcp"],
  "env": {
    "APIFY_TOKEN": "THE_TOKEN_THEY_PASTED"
  }
}
```

After writing the file, tell the user:

> "Done! I've connected Apify to your Claude Code.
>
> **One last step:** You need to restart Claude Code for this to take effect.
>
> 1. Type `/exit` to close this session
> 2. Open Claude Code again
> 3. Run `/scrape-leads` and we'll pick up right where we left off
>
> That's it — you only have to do this once. From now on, Apify will just work."

**STOP here.** Do not proceed until Apify is connected. The user needs to restart
Claude Code and run the skill again.

---

### Troubleshooting (if anything goes wrong)

**"npx: command not found":**
Node.js isn't installed or isn't in PATH. Go back to Step 0a.

**"APIFY_TOKEN is invalid" or authentication errors:**
The token was probably copied incorrectly. Ask them to go back to
https://console.apify.com/account/integrations and copy it again. Make sure they
get the full token — it's a long string of letters and numbers.

**"Cannot find module" or npm errors:**
Usually a network issue. Ask them to check their internet connection and try again.
If it persists, try running `npm cache clean --force` and restarting.

**The `search-actors` tool doesn't appear after restart:**
Check that the entry was added to `~/.claude/.mcp.json` correctly. Read the file
and verify the JSON is valid (no missing commas, no trailing commas). Fix if needed.

---

## Step 1: Ask What They Want

Every single run, ask the user what they want to search for. Never auto-run a
saved search without asking first.

**If `lead-config.json` exists**, read it and offer it as a shortcut:

> "Last time you searched for **[search_query]** in **[location]** ([max_results]
> results, [enrichment_level]).
>
> Want to run that again, or something new?"

If they say "same" / "again" / "yes" — use the saved config and proceed to Step 2.
If they describe a new search — parse it and proceed (see below).
If they say "something new" without details — proceed to Step 1b (interview).

**If no `lead-config.json` exists**, proceed to Step 1b (first-run interview).

**If the user included a search in their message** (e.g., "find me 200 plumbers
in Melbourne"), still confirm before running:

> "Got it — 200 plumbers in Melbourne. Want me to find emails too, or just the
> raw data?"

Fill in whatever they specified, ask about anything they didn't (enrichment level,
number of results if not mentioned), then proceed to Step 2.

After every completed search, save/update `lead-config.json` with whatever they
just ran so it's offered as the shortcut next time.

---

## Step 1b: First-Run Setup Interview

Ask these questions ONE AT A TIME. Wait for each answer before moving to the next.
Keep it conversational — like a friend helping them set up, not a form.

**Question 1 — Lead type:**

"What kind of leads are you looking for? Pick the closest match:

1. **Local businesses** (restaurants, salons, dentists, agencies in a specific city)
2. **Online / SaaS companies** (e-commerce stores, software companies, agencies)
3. **Instagram creators or influencers**
4. **TikTok creators**
5. **YouTube creators**"

Save as `lead_type`: `local_business`, `online_business`, `instagram_creators`, `tiktok_creators`, or `youtube_creators`.

**Question 2 — Who specifically?**

This question varies by lead type:

- **Local businesses:** "What type of business and where? For example: 'yoga studios in Austin, TX' or 'plumbers in Miami'."
  - Parse into `search_query` (business type) and `location` (city/region)
- **Online/SaaS:** "What kind of companies? For example: 'Shopify stores selling pet products' or 'marketing agencies'."
  - Save as `search_query`
- **Creators:** "What niche or keywords? For example: 'fitness influencers' or 'AI content creators'. And roughly what follower range? (e.g., 10k-100k)"
  - Save as `search_query` and `follower_range` (object with `min` and `max`)

**Question 3 — How many:**

"How many leads do you want? I'd suggest starting with 25-50 to keep Apify costs low — you can always run again for more."

Save as `max_results`. Default to 50 if they say "whatever" or similar.

**Question 4 — Enrichment:**

"What should I do with the results?

1. **Just the raw data** — names, websites, contact info from the platform
2. **Find email addresses** — I'll visit their websites to dig up emails
3. **The full works** — emails + lead scoring + draft outreach messages"

Save as `enrichment_level`: `raw`, `emails`, or `full`.

**After all 4 questions:**

Build and save `lead-config.json` to the current directory:

```json
{
  "lead_type": "local_business",
  "search_query": "yoga studios",
  "location": "Austin, TX",
  "max_results": 50,
  "enrichment_level": "raw",
  "apify_actor": null,
  "last_csv": null,
  "created_at": "2026-04-03T10:00:00Z"
}
```

Only include `location` for `local_business`. Only include `follower_range` for creator types.

Confirm: "Config saved. Let me find your leads..."

---

## Step 2: Select and Prepare Apify Actor

Read `references/actors.md` for the recommended actor per lead type. It has the
actor name, key input fields, and expected output fields.

1. Call `fetch-actor-details` for the recommended actor to get its current input schema
2. If the actor doesn't exist or has changed, fall back to `search-actors` with
   keywords matching the lead type, pick the top result, and call `fetch-actor-details`
3. Save the resolved actor name to `lead-config.json` as `apify_actor` so re-runs skip this lookup

---

## Step 3: Run the Scraper

Build the actor input by mapping config fields to actor input params. See
`references/actors.md` for field mappings per actor.

Call `call-actor` with:
- The actor name from Step 2
- The mapped input params
- Set a reasonable timeout (actors for 50 results typically finish in 30-90 seconds)

If the actor run takes too long, switch to async mode:
1. Call `call-actor` with `async: true`
2. Poll with `get-actor-run` every 15 seconds
3. Tell the user: "Still working... [X] seconds elapsed"

When the run completes, retrieve results with `get-actor-output` using the dataset ID.

---

## Step 4: Format and Save Results

**Display in chat** as a clean markdown table. Columns depend on lead type:

| Lead Type | Columns |
|-----------|---------|
| Local businesses | Name, Address, Phone, Website, Rating, Reviews |
| Online/SaaS | Company, Website, Description |
| Instagram creators | Username, Followers, Bio, Website |
| TikTok creators | Username, Followers, Bio |
| YouTube creators | Channel, Subscribers, Description, Website |

Show the first 20 rows in the table. If there are more, say "Showing 20 of [X] — full results in CSV."

**Save to CSV** with all rows and all available fields:
- Filename: `leads-YYYY-MM-DD.csv` (use today's date)
- If file already exists, append time: `leads-YYYY-MM-DD-HHMM.csv`
- Update `last_csv` in `lead-config.json`

Use a bash command to write the CSV. Properly escape commas and quotes in fields.

---

## Step 5: Enrichment (if enabled)

Check `enrichment_level` from config. Read `references/enrichment.md` for the
full enrichment workflow.

**If `raw`:** Skip this step entirely.

**If `emails`:**
1. Filter leads that have a website URL
2. For each website (batch 5 at a time to manage costs):
   - Use `call-actor` with `apify/rag-web-browser` to fetch the contact/about page
   - Extract email addresses from the page content
3. Add an `Email` column to the results
4. Update the CSV with the new column
5. Report: "Found emails for X of Y leads"

**If `full`:**
1. Do everything from the `emails` step
2. Score each lead 1-10 (see `references/enrichment.md` for scoring rubric)
3. Draft a 2-sentence outreach message per lead:
   - Read CLAUDE.md for the user's business context
   - Reference something specific about the lead
   - Keep it casual, end with a question
4. Add `Score` and `Outreach Draft` columns
5. Update the CSV

---

## Step 6: Summary

Print a summary block:

```
Lead Scrape Complete
--------------------
Leads found: [X]
Saved to: [filename].csv
Enrichment: [raw / emails found: Y of Z / full enrichment]

Run again:
  /scrape-leads         → same search
  /scrape-leads --new   → different criteria
  /scrape-leads --enrich → add emails to existing results
```

---

## Handling `--enrich` Flag

When the user runs `/scrape-leads --enrich`:
1. Read `lead-config.json` to find `last_csv`
2. Read the CSV file
3. Run the enrichment workflow (Step 5) on the existing data — skip scraping
4. Save enriched results to `leads-enriched-YYYY-MM-DD.csv`

---

## Error Handling

- **No Apify MCP connected:** Run through Step 0 setup instructions.
- **Actor run fails:** Read the error from `get-actor-run`. Common issues: invalid location, rate limiting, empty results. Suggest a fix.
- **Zero results:** "No leads found for that search. Try broadening your criteria — a larger area or more general business type."
- **Apify token missing:** "I can't find your Apify API token. Make sure it's configured in your MCP settings."
