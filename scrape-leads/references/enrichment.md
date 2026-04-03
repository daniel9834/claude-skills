# Enrichment Workflows

## Level 1: Raw Data Only

No enrichment. Output whatever the Apify scraper returns, mapped to clean
column names. This is the default for users who just want a list.

---

## Level 2: Find Emails

Goal: visit each lead's website and extract email addresses.

### Process

1. Filter leads that have a `website` or `externalUrl` field
2. Process in batches of 5 (to manage Apify costs and avoid rate limits)
3. For each website:
   a. Use `call-actor` with `apify/rag-web-browser`:
      - `query`: `"{website}/contact"` (try contact page first)
      - `maxResults`: 1
   b. Search the returned content for email patterns:
      `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   c. If no email found on /contact, try the homepage and /about page
4. Prioritize emails in this order:
   - Personal emails (name@domain.com)
   - Role-based emails (sales@, hello@, info@)
   - Skip: noreply@, no-reply@, support@, admin@
5. Add `Email` column to results
6. Update the CSV file

### Reporting

After enrichment, tell the user:
- "Found emails for X of Y leads (Z%)"
- If low hit rate: "Many sites didn't have public emails. Consider LinkedIn
  outreach instead, or try a different enrichment tool."

---

## Level 3: Full Enrichment

Everything from Level 2, plus lead scoring and outreach draft generation.

### Lead Scoring (1-10)

Score each lead based on available signals. The rubric varies by lead type:

**Local businesses:**
| Signal | Points |
|--------|--------|
| Has email | +2 |
| Has phone | +1 |
| Has website | +1 |
| Rating >= 4.0 | +2 |
| Reviews >= 50 | +2 |
| Reviews < 10 (new/small) | +1 |
| Category matches search exactly | +1 |

**Creators:**
| Signal | Points |
|--------|--------|
| Has email (public or found) | +2 |
| Has website/link in bio | +1 |
| Followers in target range | +2 |
| Bio mentions relevant keywords | +2 |
| Verified account | +1 |
| Posts regularly (>2/week) | +1 |
| Engagement rate > 2% | +1 |

**Online businesses:**
| Signal | Points |
|--------|--------|
| Has email | +2 |
| Has phone | +1 |
| Has active website | +2 |
| Website loads fast | +1 |
| Description matches search | +2 |
| Has social media links | +1 |
| Has blog/content | +1 |

Cap at 10. Sort results by score (highest first).

### Outreach Drafts

For each lead, generate a 2-sentence personalized outreach message.

**Requirements:**
1. Read the project's CLAUDE.md for the user's business name and offering
2. Reference something specific about the lead (their rating, niche, content, etc.)
3. Keep it casual and human — not salesy
4. End with a question to invite a reply
5. Under 50 words total

**Example for a local business:**
"Hey! I noticed [Business Name] has great reviews in [City]. I help businesses
like yours [what you do from CLAUDE.md] — would you be open to a quick chat
about it?"

**Example for a creator:**
"Hey [username]! Love your content on [topic from bio]. I'm building [what you
do from CLAUDE.md] and think there could be a cool collab — interested?"

Add `Score` and `Outreach Draft` columns to the results and CSV.
