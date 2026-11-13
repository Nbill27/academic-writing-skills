#!/bin/sh
# Install the academic-writing-skills skills into an agent skills directory.
# Default target is Hermes (~/.hermes/skills).
# Pass --codebuddy for CodeBuddy, --claude-code for Claude Code,
# --opencode for OpenCode, --codex for Codex, --hermes for Hermes.
set -e

TARGET="$HOME/.hermes/skills"
AGENT="Hermes"
VERIFY="hermes skills list"

case "$1" in
  --codebuddy)
    TARGET="$HOME/.codebuddy/skills"
    AGENT="CodeBuddy"
    VERIFY="codebuddy skills list"
    ;;
  --claude-code)
    TARGET="$HOME/.claude/skills"
    AGENT="Claude Code"
    VERIFY="claude --help"
    ;;
  --opencode)
    TARGET="$HOME/.config/opencode/skills"
    AGENT="OpenCode"
    VERIFY="opencode --help"
    ;;
  --codex)
    TARGET="$HOME/.codex/skills"
    AGENT="Codex"
    VERIFY="codex --help"
    ;;
  --hermes)
    TARGET="$HOME/.hermes/skills"
    AGENT="Hermes"
    VERIFY="hermes skills list"
    ;;
  "")
    ;;
  *)
    echo "Unknown option: $1" >&2
    echo "Usage: $0 [--codebuddy|--claude-code|--opencode|--codex|--hermes]" >&2
    exit 1
    ;;
esac

if [ ! -d "skills" ]; then
  echo "Run this script from the repo root." >&2
  exit 1
fi

mkdir -p "$TARGET"
cp -r skills/* "$TARGET/"

echo "Installed into $TARGET ($AGENT):"
ls "$TARGET" | grep -E "^(outline|draft|edit|audit)$"
echo "Verify with: $VERIFY"
