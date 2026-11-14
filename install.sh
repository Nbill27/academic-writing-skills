#!/bin/sh
# Install all five Agent Skills and shared task resources.
set -eu

usage() {
  cat <<'HELP'
Install academic-writing-skills.
Usage: ./install.sh [--hermes|--codebuddy|--claude-code|--opencode|--codex]
Targets:
  --hermes        ~/.hermes/skills (default)
  --codebuddy     ~/.codebuddy/skills
  --claude-code   ~/.claude/skills
  --opencode      ${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills
  --codex         ~/.agents/skills
  -h, --help      Show help
HELP
}

TARGET="$HOME/.hermes/skills"
case "${1:-}" in
  ""|--hermes) ;;
  --codebuddy) TARGET="$HOME/.codebuddy/skills" ;;
  --claude-code) TARGET="$HOME/.claude/skills" ;;
  --opencode) TARGET="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills" ;;
  --codex) TARGET="$HOME/.agents/skills" ;;
  -h|--help) usage; exit 0 ;;
  *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
esac

[ -f "skills/academic-writing/SKILL.md" ] || {
  echo "Run this script from the repository root." >&2
  exit 1
}

mkdir -p "$TARGET"
for skill in academic-writing outline draft edit audit; do
  mkdir -p "$TARGET/$skill"
  cp -r "skills/$skill/." "$TARGET/$skill/"
done
mkdir -p "$TARGET/shared"
cp -r "shared/." "$TARGET/shared/"
echo "Installed skill family into $TARGET"
