# Claude Code Skills

Skills for Claude Code by [@askdandonovan](https://instagram.com/askdandonovan).

## Install any skill

```bash
curl -fsSL https://raw.githubusercontent.com/askdandonovan/claude-skills/main/install.sh | bash -s <skill-name>
```

## Available Skills

| Skill | What it does | Install |
|-------|-------------|---------|
| `scrape-leads` | Generate leads from Google Maps, Instagram, TikTok, YouTube. Finds emails and writes outreach. | `curl -fsSL https://raw.githubusercontent.com/askdandonovan/claude-skills/main/install.sh \| bash -s scrape-leads` |

## How it works

Each skill is a set of instructions that teach Claude Code how to do something specific. When you install a skill, it copies the files into `~/.claude/skills/` on your computer. Next time you open Claude Code, the skill is available.

## Requirements

- [Claude Code](https://claude.ai/code) with a Pro or Max plan
- Node.js 18+ (for skills that use MCP servers)
