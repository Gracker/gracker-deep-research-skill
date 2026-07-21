from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "scripts/publish_to_obsidian.py"
PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class PublishToObsidianTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.vault = self.root / "Vault"
        (self.vault / ".obsidian").mkdir(parents=True)
        self.materials = self.root / "topic-研究材料"
        self.materials.mkdir()
        (self.materials / "master-research.md").write_text("evidence\n")
        (self.materials / "quality-report.md").write_text("总评：通过\n")
        references = self.materials / "references"
        references.mkdir()
        (references / "source.md").write_text("source\n")
        self.report = self.root / "topic-深度调研.md"
        self.report.write_text(
            "---\ntitle: Topic\ntags:\n  - existing\n---\n\n"
            "# Topic\n\n## 执行摘要\n\n"
            "[Sources](./topic-研究材料/master-research.md)\n\n## 正文\n"
        )
        self.diagrams = []
        for name in ("mechanism", "review"):
            workdir = self.root / name
            for relative in (
                "source.md",
                "analysis.md",
                "structured-content.md",
                "copy.md",
                "prompts/infographic.md",
            ):
                target = workdir / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"{name} {relative}\n")
            (workdir / "quality-review.md").write_text("状态：通过。\n")
            image = workdir / "output/diagram.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(PNG_1X1)
            self.diagrams.append((name, image, workdir))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def command(self) -> list[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "--vault",
            str(self.vault),
            "--slug",
            "2026-07-21-无锁设计",
            "--report",
            str(self.report),
            "--materials",
            str(self.materials),
            "--tag",
            "deep-research",
        ]
        for name, image, workdir in self.diagrams:
            command.extend(("--diagram", f"{name}={image}"))
            command.extend(("--diagram-workdir", f"{name}={workdir}"))
        return command

    def test_publishes_verified_package_and_refuses_overwrite(self) -> None:
        first = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        destination = Path(json.loads(first.stdout)["destination"])
        note = (destination / self.report.name).read_text()
        self.assertIn("![[assets/mechanism.png]]", note)
        self.assertIn("![[assets/review.png]]", note)
        self.assertIn("](./research-materials/master-research.md)", note)
        self.assertIn('  - "deep-research"', note)
        self.assertLess(note.index("## 执行摘要"), note.index("## 视觉摘要"))
        self.assertLess(note.index("## 视觉摘要"), note.index("## 正文"))
        manifest = json.loads((destination / "publish-manifest.json").read_text())
        self.assertEqual(manifest["minimum_diagrams"], 2)
        self.assertEqual(len(manifest["accepted_diagrams"]), 2)

        second = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("destination already exists", second.stderr)

    def test_rejects_failed_quality_review(self) -> None:
        failed_workdir = self.diagrams[0][2]
        (failed_workdir / "quality-review.md").write_text("状态：未通过。\n")
        result = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("quality review is not accepted", result.stderr)

    def test_rejects_broken_local_link(self) -> None:
        self.report.write_text("# Topic\n\n[Missing](./missing.md)\n")
        result = subprocess.run(self.command(), text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken local link", result.stderr)


if __name__ == "__main__":
    unittest.main()
