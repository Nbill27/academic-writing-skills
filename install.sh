#!/bin/sh
# Install academic-writing-skills into an agent skills directory.
# Default target is Hermes (~/.hermes/skills).
set -e

usage() {
  cat <<'EOF'
Install academic-writing-skills (outline, draft, edit, audit).

Usage:
  ./install.sh [TARGET]

Targets:
  --hermes        ~/.hermes/skills                              (default)
  --codebuddy     ~/.codebuddy/skills
  --claude-code   ~/.claude/skills
  --opencode      ${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills
  --codex         ~/.agents/skills
  -h, --help      Show this help.

Run from the repo root. The four skill folders are copied next to a shared/
folder, because the skill text refers to shared/campus-presets.md and
shared/presets/ relative to the skills root.

For project scope, copy the same folders into the project directory instead:
  .claude/skills  .opencode/skills  .codebuddy/skills  .agents/skills
EOF
}

TARGET="$HOME/.hermes/skills"
AGENT="Hermes"
VERIFY="hermes skills list"

case "$1" in
  --hermes)
    ;;
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
    TARGET="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills"
    AGENT="OpenCode"
    VERIFY="opencode --help"
    ;;
  --codex)
    TARGET="$HOME/.agents/skills"
    AGENT="Codex"
    VERIFY="codex --help"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  "")
    ;;
  *)
    echo "Unknown option: $1" >&2
    echo "Run ./install.sh --help for usage." >&2
    exit 1
    ;;
esac

if [ ! -f "skills/outline/SKILL.md" ]; then
  echo "Run this script from the repo root." >&2
  exit 1
fi

mkdir -p "$TARGET"
for skill in outline draft edit audit; do
  mkdir -p "$TARGET/$skill"
  cp -r "skills/$skill/." "$TARGET/$skill/"
done

mkdir -p "$TARGET/shared"
cp -r "shared/." "$TARGET/shared/"

echo "Installed into $TARGET ($AGENT):"
ls "$TARGET" | sed 's/^/  /'
echo "Verify with: $VERIFY"
