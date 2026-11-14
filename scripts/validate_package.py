"""Validate Agent Skills packaging and local repository references.

This checks packaging only, not academic correctness, source truth or runtime
behavior. Standard library only; intentionally not a general YAML parser.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
YAML_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):", re.M)
REF_PATH = re.compile(r"references/[A-Za-z0-9_./-]+")
ABSOLUTE = re.compile(r"(?:(?<![A-Za-z0-9])[A-Za-z]:[\\/]|file://|/Users/|/home/|/mnt/)")
SKILLS = ("academic-writing", "outline", "draft", "edit", "audit")
ROOT_FILES = ("README.md", "LICENSE", "install.sh")
PRESET_KEYS = ("preset_id", "chapter_count", "problem_statement_location", "chapter2_name",
    "conceptual_framework_location", "results_discussion_structure", "subchapter_numbering",
    "max_heading_depth", "citation_style", "abstract_languages", "special_front_matter",
    "figure_table_numbering", "mandatory_output", "writing_systematics", "similarity_limit",
    "paper_size", "margin_top", "margin_bottom", "margin_left", "margin_right", "font_family",
    "font_size", "line_spacing")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if not line or line.startswith((" ", "#")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def local_link_targets(text: str):
    for raw in LINK.findall(text):
        target = raw.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield unquote(parsed.path)


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    for filename in ROOT_FILES:
        if not (root / filename).is_file():
            errors.append("Missing required file: " + filename)
    for name in SKILLS:
        entry = root / "skills" / name / "SKILL.md"
        if not entry.is_file():
            errors.append("Missing skill entrypoint: " + str(entry.relative_to(root)))
            continue
        content = entry.read_text(encoding="utf-8")
        meta = parse_frontmatter(content)
        if not meta:
            errors.append(name + ": malformed frontmatter")
            continue
        if meta.get("name") != name:
            errors.append(name + ": frontmatter name does not match directory")
        if not meta.get("description") or len(meta["description"]) > 500:
            errors.append(name + ": missing or overlong description")
        for required in ("license", "compatibility", "allowed-tools"):
            if not meta.get(required):
                errors.append(name + ": missing frontmatter field " + required)
        if name != "academic-writing" and "## References" not in content:
            errors.append(name + ": missing References section")
        if ABSOLUTE.search(content):
            errors.append(name + ": contains absolute local path")
        for target in set(REF_PATH.findall(content)):
            target = target.rstrip(".,;:)")
            if not (entry.parent / target).is_file():
                errors.append(name + ": missing reference " + target)
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        try:
            content = document.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append("Unreadable Markdown: " + str(document.relative_to(root)))
            continue
        for target in local_link_targets(content):
            candidate = (document.parent / target).resolve()
            if not candidate.is_file() and not candidate.is_dir():
                errors.append(str(document.relative_to(root)) + ": broken link " + target)
    preset_dir = root / "shared" / "presets"
    presets = sorted(preset_dir.glob("*.yml")) if preset_dir.is_dir() else []
    if not presets:
        errors.append("No shared preset found")
    for preset in presets:
        keys = YAML_KEY.findall(preset.read_text(encoding="utf-8"))
        missing = [key for key in PRESET_KEYS if key not in keys]
        if missing:
            errors.append(preset.name + ": missing keys " + ", ".join(missing))
        duplicates = sorted({key for key in keys if keys.count(key) > 1})
        if duplicates:
            errors.append(preset.name + ": duplicate keys " + ", ".join(duplicates))
    installer = root / "install.sh"
    if installer.is_file():
        body = installer.read_text(encoding="utf-8")
        for name in SKILLS:
            if name not in body:
                errors.append("install.sh does not include " + name)
        if "shared/" not in body:
            errors.append("install.sh does not copy shared/")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill packaging and local references.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    args = parser.parse_args()
    problems = validate(Path(args.root))
    if problems:
        print(f"FAIL: {len(problems)} packaging issue(s).")
        for problem in problems:
            print("- " + problem)
        return 1
    print("OK: package structure, metadata, and local references are valid.")
    print("NOTE: academic content, source truth, and agent runtime behavior are not tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
