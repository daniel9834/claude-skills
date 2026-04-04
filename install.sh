#!/bin/bash
# Claude Skills Installer — github.com/daniel9834/claude-skills
# Usage: curl -fsSL https://raw.githubusercontent.com/daniel9834/claude-skills/main/install.sh | bash -s <skill-name>

set -e

SKILL_NAME="${1:-}"
REPO="daniel9834/claude-skills"
BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/$REPO/$BRANCH"
SKILLS_DIR="$HOME/.claude/skills"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$SKILL_NAME" ]; then
  echo -e "${RED}Error: No skill name provided.${NC}"
  echo ""
  echo "Usage:"
  echo "  curl -fsSL $BASE_URL/install.sh | bash -s <skill-name>"
  echo ""
  echo "Available skills:"
  echo "  scrape-leads    — Generate leads from Google Maps, Instagram, TikTok, YouTube"
  echo ""
  exit 1
fi

echo ""
echo -e "${GREEN}Installing skill: $SKILL_NAME${NC}"
echo "─────────────────────────────────"

# Check if skill exists in the repo by fetching the manifest
MANIFEST_URL="$BASE_URL/$SKILL_NAME/manifest.json"
MANIFEST=$(curl -fsSL "$MANIFEST_URL" 2>/dev/null) || {
  echo -e "${RED}Skill '$SKILL_NAME' not found.${NC}"
  echo "Check available skills at: https://github.com/$REPO"
  exit 1
}

# Parse file list from manifest using python3 JSON parser
FILES=$(echo "$MANIFEST" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for f in data['files']:
    print(f)
" 2>/dev/null)

if [ -z "$FILES" ]; then
  echo -e "${RED}Failed to parse manifest. Ensure python3 is installed.${NC}"
  exit 1
fi

# Create skill directory
INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"
mkdir -p "$INSTALL_DIR"

# Download each file
echo ""
while IFS= read -r FILE; do
  [ -z "$FILE" ] && continue
  # Create subdirectories if needed
  FILE_DIR=$(dirname "$FILE")
  if [ "$FILE_DIR" != "." ]; then
    mkdir -p "$INSTALL_DIR/$FILE_DIR"
  fi

  echo -n "  Downloading $FILE... "
  if curl -fsSL "$BASE_URL/$SKILL_NAME/$FILE" -o "$INSTALL_DIR/$FILE" 2>/dev/null; then
    echo -e "${GREEN}done${NC}"
  else
    echo -e "${RED}failed${NC}"
  fi
done <<< "$FILES"

echo ""
echo "─────────────────────────────────"
echo -e "${GREEN}Installed to: $INSTALL_DIR${NC}"
echo ""

# Check for post-install instructions
POST_MSG=$(echo "$MANIFEST" | python3 -c "
import sys, json
data = json.load(sys.stdin)
msg = data.get('post_install', '')
if msg:
    print(msg)
" 2>/dev/null || echo "")

if [ -n "$POST_MSG" ]; then
  echo -e "${YELLOW}Next step:${NC}"
  echo "  $POST_MSG"
  echo ""
fi

echo "Restart Claude Code, then type /$SKILL_NAME to get started."
echo ""
