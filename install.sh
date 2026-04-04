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

# Parse file list from manifest
FILES=$(echo "$MANIFEST" | grep -o '"[^"]*"' | tr -d '"' | grep -v "^\[" | grep -v "^\]")

# Create skill directory
INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"
mkdir -p "$INSTALL_DIR"

# Download each file
echo ""
for FILE in $FILES; do
  # Create subdirectories if needed
  FILE_DIR=$(dirname "$FILE")
  if [ "$FILE_DIR" != "." ]; then
    mkdir -p "$INSTALL_DIR/$FILE_DIR"
  fi

  echo -n "  Downloading $FILE... "
  curl -fsSL "$BASE_URL/$SKILL_NAME/$FILE" -o "$INSTALL_DIR/$FILE" 2>/dev/null && {
    echo -e "${GREEN}done${NC}"
  } || {
    echo -e "${RED}failed${NC}"
  }
done

echo ""
echo "─────────────────────────────────"
echo -e "${GREEN}Installed to: $INSTALL_DIR${NC}"
echo ""

# Check for post-install instructions
if echo "$MANIFEST" | grep -q '"post_install"'; then
  POST_MSG=$(echo "$MANIFEST" | python3 -c "import sys,json; print(json.load(sys.stdin).get('post_install',''))" 2>/dev/null || echo "")
  if [ -n "$POST_MSG" ]; then
    echo -e "${YELLOW}Next step:${NC}"
    echo "  $POST_MSG"
    echo ""
  fi
fi

echo "Restart Claude Code, then type /$SKILL_NAME to get started."
echo ""
