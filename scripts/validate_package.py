"""Validate this repo skill metadata and portable local links.

Standard library only. This is not a general YAML or Markdown parser and does
not verify external URLs, citation truth, or agent behavior. It checks the
packaging rules the Agent Skills format needs: every skill has a SKILL.md with
frontmatter whose name matches its directory, required repo files exist, local
links resolve, and no absolute local paths leak into skill files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
ABSOLUTE = re.compile(r"(?:(?<![A-Za-z0-9])[A-Za-z]:[\\/]|file://|/Users/|/home/|/mnt/)")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def local_targets(text: str):
    for raw in LINK.findall(text):
        target = raw.strip().strip("<>")
        if target.startswith("#") or urlsplit(target).scheme:
            continue
        yield unquote(target.split("#", 1)[0])


def validate(root: Path) -> list:
    root = root.resolve()
    errors = []
    skill_dirs = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_dirs:
        return ["No skills/<name>/SKILL.md."]
    for required in ("README.md", "LICENSE", "install.sh"):
        if not (root / required).is_file():
            errors.append("Missing required file: " + required)
    for entry in skill_dirs:
        skill_root = entry.parent.resolve()
        name = skill_root.name
        text = entry.read_text(encoding="utf-8")
        fields = parse_frontmatter(text)
        if not fields:
            errors.append(name + ": frontmatter missing.")
            continue
        if fields.get("name") != name:
            errors.append(name + ": frontmatter name does not match the directory name.")
        desc = fields.get("description", "")
        if not desc:
            errors.append(name + ": description is empty.")
        elif len(desc) > 500:
            errors.append(name + ": description is over 500 characters.")
        if not fields.get("license"):
            errors.append(name + ": license is empty.")
        for target in local_targets(text):
            if ABSOLUTE.search(target):
                errors.append(name + ": absolute local link: " + target)
                continue
            full = (skill_root / target).resolve()
            if not full.is_file():
                errors.append(name + ": broken local link: " + target)
        for bad, label in ((";", "semicolon"), ("\u2014", "em dash"), ("\u2013", "en dash")):
            if bad in text:
                errors.append(name + ": contains " + label + " (house rule).")
    for preset in sorted((root / "shared" / "presets").glob("*.yml")):
        text = preset.read_text(encoding="utf-8")
        if "preset_id:" not in text:
            errors.append("Preset without preset_id: " + preset.name)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate academic-writing-skills packaging.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root to validate.")
    args = parser.parse_args()
    errors = validate(Path(args.root))
    if errors:
        print("FAIL: " + str(len(errors)) + " problems.")
        for item in errors:
            print("- " + item)
        return 1
    print("OK: package is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
