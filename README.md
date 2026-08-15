# Claude Code Skills

Skills for Claude Code by [@askdandonovan](https://instagram.com/askdandonovan).

## Install any skill

```bash
curl -fsSL https://raw.githubusercontent.com/daniel9834/claude-skills/main/install.sh | bash -s <skill-name>
```

## Available Skills

| Skill | What it does | Install |
|-------|-------------|---------|
| `content-multiplier` | Turn one piece of content into platform-native posts across LinkedIn, X, Instagram, TikTok, YouTube, and Threads. | `curl -fsSL https://raw.githubusercontent.com/daniel9834/claude-skills/main/install.sh \| bash -s content-multiplier` |
| `scrape-leads` | Generate leads from Google Maps, Instagram, TikTok, YouTube. Finds emails and writes outreach. | `curl -fsSL https://raw.githubusercontent.com/daniel9834/claude-skills/main/install.sh \| bash -s scrape-leads` |
| `summarize` | Turn a URL, article, YouTube video, or PDF into a decision — a verdict and the gaps, not a neutral recap. Pulls video transcripts automatically, and refuses to summarise anything it couldn't actually read. | `curl -fsSL https://raw.githubusercontent.com/daniel9834/claude-skills/main/install.sh \| bash -s summarize` |

## How it works

Each skill is a set of instructions that teach Claude Code how to do something specific. When you install a skill, it copies the files into `~/.claude/skills/` on your computer. Next time you open Claude Code, the skill is available.

## Requirements

- [Claude Code](https://claude.ai/code) with a Pro or Max plan
- Node.js 18+ (for skills that use MCP servers)

### Optional, for `summarize`

Nothing extra is required — articles, PDFs and pasted text work out of the box. These two only widen what it can reach, and it degrades gracefully without them:

- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) (`brew install yt-dlp`) — lets it pull transcripts from YouTube, Vimeo, Loom and friends
- `mlx-whisper` + `ffmpeg` — only used as a last resort, when a video has no captions at all

Without `yt-dlp`, video links fail with a clear message rather than a made-up summary.
