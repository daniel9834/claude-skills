# Apify Actor Reference — Lead Generation

Always call `fetch-actor-details` before `call-actor` to get the current input
schema. Actor schemas can change — this file provides the known-good starting
point, but the live schema is authoritative.

---

## Local Businesses

**Primary actor:** `compass/crawler-google-places`

**Input mapping:**
| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `search_query` | `searchStringsArray` | Wrap in array: `["yoga studios"]` |
| `location` | `locationQuery` | e.g., `"Austin, TX"` |
| `max_results` | `maxCrawledPlacesPerSearch` | Direct mapping |

**Expected output fields:**
- `title` — Business name
- `address` — Full address
- `phone` — Phone number
- `website` — Website URL
- `totalScore` — Google rating (1-5)
- `reviewsCount` — Number of reviews
- `categoryName` — Business category
- `url` — Google Maps URL

**Fallback actor:** `nwua/google-maps-scraper`

---

## Online / SaaS Companies

**Strategy:** Two-step — search Google for company lists, then scrape the results.

**Step 1 — Find company lists:**
Use `apify/google-search-scraper`

| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `search_query` | `queries` | e.g., `"top Shopify stores selling pet products"` |
| `max_results` | `maxPagesPerQuery` | Set to 1-2 pages |

**Step 2 — Extract company info:**
Use `apify/rag-web-browser` on the top search results to extract company names,
websites, and descriptions.

**Expected output fields from Google Search:**
- `title` — Page title
- `url` — Result URL
- `description` — Snippet

---

## Instagram Creators

**Primary actor:** `apify/instagram-profile-scraper`

**Input mapping:**
| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `search_query` | `search` | Keyword search for profiles |
| `max_results` | `resultsLimit` | Direct mapping |

**Expected output fields:**
- `username` — Handle
- `fullName` — Display name
- `followersCount` — Follower count
- `biography` — Bio text
- `externalUrl` — Website link
- `businessEmail` — Public email (if set)
- `isVerified` — Verified badge
- `postsCount` — Number of posts

**Fallback actor:** `apify/instagram-scraper`

**Filtering by follower range:** After getting results, filter locally by
`follower_range.min` and `follower_range.max` from config.

---

## TikTok Creators

**Primary actor:** `clockworks/tiktok-profile-scraper`

**Input mapping:**
| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `search_query` | `profiles` | May need username list — use search first |
| `max_results` | `resultsPerPage` | Direct mapping |

**Strategy:** TikTok profile scrapers often need usernames, not keywords.
Consider using `apify/rag-web-browser` to search
`"top [niche] TikTok creators"` first, extract handles, then scrape profiles.

**Expected output fields:**
- `uniqueId` — Username
- `nickname` — Display name
- `followerCount` — Followers
- `signature` — Bio
- `bioLink` — Website

**Fallback:** Use `search-actors` with query `"tiktok profile scraper"` and pick
the highest-rated result.

---

## YouTube Creators

**Primary actor:** `streamers/youtube-channel-scraper`

**Input mapping:**
| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `search_query` | `searchKeywords` | Keyword search for channels |
| `max_results` | `maxResults` | Direct mapping |

**Expected output fields:**
- `channelName` — Channel name
- `subscriberCount` — Subscribers
- `description` — Channel description
- `channelUrl` — YouTube URL
- `website` — External link (if available)

**Fallback:** Use `search-actors` with query `"youtube channel scraper"`.

---

## Email Enrichment Actor

**Actor:** `apify/rag-web-browser`

Use for visiting lead websites to find emails. Input:
- `query`: `"contact email site:{website}"` or fetch `{website}/contact`
- `maxResults`: 1

Extract email addresses from the returned content using regex:
`[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`

Filter out generic emails (noreply@, info@, support@) — prefer personal emails.
