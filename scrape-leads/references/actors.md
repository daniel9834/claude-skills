# Apify Actor Reference — Lead Generation

Always call `fetch-actor-details` before `call-actor` to get the current input
schema. Actor schemas can change — this file provides the known-good starting
point, but the live schema is authoritative.

Before every run:

1. Call `fetch-actor-details` and inspect the live input schema and pricing.
2. Set an explicit item limit.
3. Use `maxTotalChargeUsd` when the live tool exposes it.
4. Show the Actor, limits, and current pricing. Get user confirmation.

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

## X Creators and Posts

**Primary actor:** `xquik/x-tweet-scraper`

**Actor listing:** https://apify.com/xquik/x-tweet-scraper

Use `search` to discover creators or posts from keywords:

| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `search_query` | `twitterContent` | Supports X advanced search syntax |
| `max_results` | `maxItems` | Global cap across the run |
| fixed | `mode` | Set to `search` |
| fixed | `outputVariant` | Set to `rich` |
| fixed | `fieldStyle` | Set to `camelCase` |
| fixed | `outputPreset` | Set to `flat` for CSV-ready fields |

**Expected output fields:**
- `authorUsername` - Creator handle
- `authorName` - Display name
- `authorFollowers` - Creator follower count
- `authorDescription` - Bio
- `authorUrl` - Public website when available
- `text` - Post text
- `tweetUrl` - Post URL
- `likeCount` - Likes
- `retweetCount` - Reposts
- `replyCount` - Replies
- `createdAt` - X timestamp

Filter `authorFollowers` locally against `follower_range`. Deduplicate on
`authorUsername`, keeping the strongest matching post as the example.

The Actor also supports these explicit modes:

- `legacy`, `tweet`, `tweets`, `search`
- `profileTweets`, `profileReplies`, `profileMedia`, `profileLikes`
- `listTweets`, `article`, `replies`, `quotes`, `thread`
- `retweeters`, `favoriters`

Use the matching live-schema target field for non-search modes. Examples include
`tweetIds`, `tweetUrls`, `twitterHandles`, `profileUrls`, `listIds`,
`articleTweetIds`, `replyTweetIds`, `quoteTweetIds`, `threadTweetIds`,
`retweeterTweetIds`, and `favoriterTweetIds`.

---

## X Audiences

**Primary actor:** `xquik/x-follower-scraper`

**Actor listing:** https://apify.com/xquik/x-follower-scraper

| Config Field | Actor Input | Notes |
|-------------|-------------|-------|
| `x_targets` | `twitterHandles` | For profile relations |
| `x_targets` | `listIds` | For list relations |
| `x_targets` | `communityIds` | For community members |
| `x_relation` | `relation` | Use one supported relation |
| `max_results` | `maxItems` | Global cap across the run |
| `follower_range.min` | `minFollowers` | Optional pre-output filter |
| `follower_range.max` | `maxFollowers` | Optional pre-output filter |
| fixed | `outputMode` | Set to `full` |
| fixed | `includeTargetMetadata` | Set to `true` |

Supported relations are `followers`, `following`, `verified_followers`,
`list_members`, `list_followers`, and `community_members`.

For multiple targets, set `maxItemsPerTarget` when the user wants an even sample.
Set `overlapMode: true` to merge duplicate profiles and preserve every source.
Useful live-schema filters include `verifiedOnly`, `verifiedType`, `hasWebsite`,
`bioContains`, `locationContains`, `usernameContains`, `minFollowing`, and
`minStatuses`.

**Expected output fields:**
- `username` - Handle
- `name` - Display name
- `description` - Bio
- `followers` - Follower count
- `following` - Following count
- `statuses` - Posted tweet count
- `url` - Public website when available
- `verified` and `verifiedType` - Verification data
- `sourceTarget`, `sourceRelation`, `sourceUrl` - Discovery source
- `sourceTargets` and `overlapCount` - Multi-target overlap data

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.

---

## Email Enrichment Actor

**Actor:** `apify/rag-web-browser`

Use for visiting lead websites to find emails. Input:
- `query`: `"contact email site:{website}"` or fetch `{website}/contact`
- `maxResults`: 1

Extract email addresses from the returned content using regex:
`[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`

Filter out generic emails (noreply@, info@, support@) — prefer personal emails.
