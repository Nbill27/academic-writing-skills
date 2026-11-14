"""Unit tests for the academic-writing-skills updater; no network needed.

Run from the repository root:

    python -m unittest discover -s tests -p "test_updater.py" -v
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).parents[1]
    / "skills"
    / "academic-writing"
    / "scripts"
    / "update.py"
)
SPEC = importlib.util.spec_from_file_location("academic_updater", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

SKILL_NAMES = ("academic-writing", "outline", "draft", "edit", "audit")


def _skill_md(name: str, version: str) -> str:
    return (
        f"---\nname: {name}\n"
        f"description: \"Test skill {name}.\"\n"
        f"version: {version}\n"
        f"license: MIT\n---\n\n# {name}\n"
    )


def _make_family(directory: Path, version: str) -> Path:
    """An installed family: five skills plus shared/, under a skills root."""
    root = directory / "skills"
    for name in SKILL_NAMES:
        skill = root / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(_skill_md(name, version), encoding="utf-8")
    updater_dir = root / "academic-writing" / "scripts"
    updater_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCRIPT, updater_dir / "update.py")
    (root / "shared").mkdir(parents=True, exist_ok=True)
    (root / "shared" / "marker.txt").write_text(f"shared {version}\n", encoding="utf-8")
    return root


def _make_release_zip(directory: Path, version: str, omit: str = "") -> Path:
    """A minimal release zip: a repo root with a passing stub validator."""
    root = directory / f"release-{version}"
    for name in SKILL_NAMES:
        if name == omit:
            continue
        skill = root / "skills" / name
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(_skill_md(name, version), encoding="utf-8")
    if omit != "shared":
        (root / "shared").mkdir(parents=True, exist_ok=True)
        (root / "shared" / "marker.txt").write_text(f"shared {version}\n", encoding="utf-8")
    updater_dir = root / "skills" / "academic-writing" / "scripts"
    updater_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCRIPT, updater_dir / "update.py")
    validator = root / "scripts" / "validate_package.py"
    validator.parent.mkdir(parents=True, exist_ok=True)
    validator.write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    archive = directory / f"academic-writing-skills-{version}.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(directory))
    return archive


def _env(root: Path, cache: Path) -> dict[str, str]:
    return {
        "XDG_CACHE_HOME": str(cache),
        "ACADEMIC_WRITING_UPDATER_SKILL_DIR": str(root / "academic-writing"),
    }


class VersionTests(unittest.TestCase):
    def test_parse_and_compare(self):
        self.assertEqual(MODULE.parse_version("v1.1.0"), (1, 1, 0))
        self.assertEqual(MODULE.parse_version("1.0.0"), (1, 0, 0))
        self.assertLess(MODULE.compare_versions((1, 0, 0), (1, 1, 0)), 0)
        self.assertEqual(MODULE.compare_versions((1, 1, 0), (1, 1, 0)), 0)
        self.assertGreater(MODULE.compare_versions((1, 2, 0), (1, 1, 0)), 0)
        with self.assertRaises(MODULE.UpdaterError):
            MODULE.parse_version("banana")

    def test_read_installed_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_family(Path(tmp), "1.0.0")
            self.assertEqual(MODULE.read_installed_version(root), (1, 0, 0))

    def test_disagreeing_versions_refuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_family(Path(tmp), "1.0.0")
            (root / "audit" / "SKILL.md").write_text(
                _skill_md("audit", "1.1.0"), encoding="utf-8"
            )
            with self.assertRaises(MODULE.UpdaterError):
                MODULE.read_installed_version(root)


class ExtractionTests(unittest.TestCase):
    def test_rejects_dotdot_member(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "bad.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("../evil.txt", "x")
            with self.assertRaises(MODULE.UpdaterError):
                MODULE.safe_extract_zip(archive, root / "out")

    def test_rejects_absolute_member(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "bad.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("/tmp/evil.txt", "x")
            with self.assertRaises(MODULE.UpdaterError):
                MODULE.safe_extract_zip(archive, root / "out")

    def test_accepts_normal_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "good.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("pkg/file.txt", "hello")
            out = root / "out"
            MODULE.safe_extract_zip(archive, out)
            self.assertEqual((out / "pkg" / "file.txt").read_text(), "hello")


class Sha256Tests(unittest.TestCase):
    def _release_with_sums(self, archive: Path, digest: str):
        def fake_download(url: str, destination: Path):
            destination.write_text(f"{digest}  release.zip\n", encoding="utf-8")
            return destination

        return {
            "tag": "v1.1.0",
            "version": "1.1.0",
            "version_tuple": (1, 1, 0),
            "assets": [
                {
                    "name": "SHA256SUMS.txt",
                    "browser_download_url": "https://example.invalid/SHA256SUMS.txt",
                }
            ],
        }, fake_download

    def test_verifies_matching_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "release.zip"
            archive.write_bytes(b"fake release")
            digest = hashlib.sha256(b"fake release").hexdigest()
            release, fake_download = self._release_with_sums(archive, digest)
            with patch.object(MODULE, "download_file", side_effect=fake_download):
                self.assertTrue(MODULE.verify_sha256_if_available(release, archive))

    def test_refuses_mismatched_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "release.zip"
            archive.write_bytes(b"fake release")
            release, fake_download = self._release_with_sums(archive, "0" * 64)
            with patch.object(MODULE, "download_file", side_effect=fake_download):
                with self.assertRaises(MODULE.UpdaterError):
                    MODULE.verify_sha256_if_available(release, archive)

    def test_no_asset_is_not_a_checksum_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "release.zip"
            archive.write_bytes(b"fake release")
            release = {"tag": "v1.1.0", "version": "1.1.0", "assets": []}
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertFalse(MODULE.verify_sha256_if_available(release, archive))
            self.assertIn("No SHA256SUMS.txt", stdout.getvalue())


class CheckUpdateTests(unittest.TestCase):
    def test_reports_update_available(self):
        fake = {
            "tag": "v1.1.0",
            "version": "1.1.0",
            "version_tuple": (1, 1, 0),
            "name": "v1.1.0",
            "html_url": "https://example.invalid/r",
            "zipball_url": "https://example.invalid/z",
        }
        with patch.object(MODULE, "read_installed_version", return_value=(1, 0, 0)), patch.object(
            MODULE, "fetch_latest_release", return_value=fake
        ):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = MODULE.main(["check-update"])
            self.assertEqual(code, 2)
            self.assertIn("Update available", stdout.getvalue())

    def test_reports_up_to_date(self):
        fake = {
            "tag": "v1.0.0",
            "version": "1.0.0",
            "version_tuple": (1, 0, 0),
            "name": "v1.0.0",
            "html_url": "https://example.invalid/r",
            "zipball_url": "https://example.invalid/z",
        }
        with patch.object(MODULE, "read_installed_version", return_value=(1, 0, 0)), patch.object(
            MODULE, "fetch_latest_release", return_value=fake
        ):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = MODULE.main(["check-update"])
            self.assertEqual(code, 0)
            self.assertIn("Up to date", stdout.getvalue())


class UpdateRollbackTests(unittest.TestCase):
    def test_update_then_rollback_with_local_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install_root = _make_family(root, "1.0.0")
            # An unrelated skill must survive the update untouched.
            other = install_root / "other-skill"
            other.mkdir()
            (other / "SKILL.md").write_text("unrelated\n", encoding="utf-8")
            archive = _make_release_zip(root, "1.1.0")
            env = _env(install_root, root / "cache")
            with patch.dict(os.environ, env):
                code = MODULE.main(["update", "--zip", str(archive), "--yes"])
            self.assertEqual(code, 0)
            self.assertEqual(MODULE.read_installed_version(install_root), (1, 1, 0))
            self.assertEqual(
                (install_root / "shared" / "marker.txt").read_text(),
                "shared 1.1.0\n",
            )
            self.assertEqual((other / "SKILL.md").read_text(), "unrelated\n")
            with patch.dict(os.environ, env):
                found = MODULE.list_backups()
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["from_version"], "1.0.0")
            self.assertEqual(found[0]["to_version"], "1.1.0")
            with patch.dict(os.environ, env):
                code = MODULE.main(["rollback", "--yes"])
            self.assertEqual(code, 0)
            self.assertEqual(MODULE.read_installed_version(install_root), (1, 0, 0))
            self.assertEqual(
                (install_root / "shared" / "marker.txt").read_text(),
                "shared 1.0.0\n",
            )

    def test_update_refuses_older_release_without_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install_root = _make_family(root, "1.1.0")
            archive = _make_release_zip(root, "1.0.0")
            env = _env(install_root, root / "cache")
            with patch.dict(os.environ, env):
                code = MODULE.main(["update", "--zip", str(archive), "--yes"])
            self.assertEqual(code, 1)
            self.assertEqual(MODULE.read_installed_version(install_root), (1, 1, 0))

    def test_update_validates_version_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install_root = _make_family(root, "1.0.0")
            archive = _make_release_zip(root, "1.1.0")
            env = _env(install_root, root / "cache")
            with patch.dict(os.environ, env):
                code = MODULE.main(
                    ["update", "--zip", str(archive), "--to", "1.2.0", "--yes"]
                )
            self.assertEqual(code, 1)
            self.assertEqual(MODULE.read_installed_version(install_root), (1, 0, 0))


class FamilyTests(unittest.TestCase):
    def test_update_refuses_release_missing_a_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install_root = _make_family(root, "1.0.0")
            archive = _make_release_zip(root, "1.1.0", omit="audit")
            env = _env(install_root, root / "cache")
            with patch.dict(os.environ, env):
                code = MODULE.main(["update", "--zip", str(archive), "--yes"])
            self.assertEqual(code, 1)
            self.assertEqual(MODULE.read_installed_version(install_root), (1, 0, 0))

    def test_update_refuses_release_missing_shared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install_root = _make_family(root, "1.0.0")
            archive = _make_release_zip(root, "1.1.0", omit="shared")
            env = _env(install_root, root / "cache")
            with patch.dict(os.environ, env):
                code = MODULE.main(["update", "--zip", str(archive), "--yes"])
            self.assertEqual(code, 1)
            self.assertEqual(MODULE.read_installed_version(install_root), (1, 0, 0))


if __name__ == "__main__":
    unittest.main()
