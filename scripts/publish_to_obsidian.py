#!/usr/bin/env python3
"""Publish a verified research package into an Obsidian vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit


SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")
SAFE_SLUG = re.compile(r"^[\w.-]+$")
REQUIRED_DIAGRAM_FILES = (
    "source.md",
    "analysis.md",
    "structured-content.md",
    "copy.md",
    "prompts/infographic.md",
    "quality-review.md",
    "output/diagram.png",
)


def parse_mapping(value: str) -> tuple[str, Path]:
    name, separator, raw_path = value.partition("=")
    if not separator or not SAFE_NAME.fullmatch(name) or not raw_path:
        raise argparse.ArgumentTypeError("expected SAFE_NAME=/path/to/file")
    return name, Path(raw_path).expanduser().resolve()


def unique_mappings(entries: list[tuple[str, Path]], label: str) -> dict[str, Path]:
    mappings = dict(entries)
    if len(mappings) != len(entries):
        raise ValueError(f"duplicate {label} name")
    return mappings


def require_file(path: Path, label: str) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"{label} must be a non-empty file: {path}")


def require_png(path: Path, label: str) -> None:
    require_file(path, label)
    with path.open("rb") as handle:
        signature = handle.read(8)
    if signature != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{label} must be a PNG file: {path}")


def require_directory(path: Path, label: str) -> None:
    if not path.is_dir():
        raise ValueError(f"{label} must be a directory: {path}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_diagram_workdir(path: Path, image: Path, name: str) -> None:
    require_directory(path, f"diagram workdir {name}")
    for relative in REQUIRED_DIAGRAM_FILES:
        require_file(path / relative, f"diagram {name} {relative}")
    review = (path / "quality-review.md").read_text(encoding="utf-8")
    accepted = re.search(
        r"(?im)^\s*(?:[-*]\s*)?(?:状态|status)\s*[:：]\s*(?:通过|accepted)\b",
        review,
    )
    if not accepted:
        raise ValueError(f"diagram {name} quality review is not accepted")
    if sha256(path / "output/diagram.png") != sha256(image):
        raise ValueError(f"diagram {name} does not match its reviewed output")


def add_tags(markdown: str, tags: list[str]) -> str:
    if not tags:
        return markdown
    unique_tags = list(dict.fromkeys(tags))
    tag_lines = "".join(
        f"\n  - {json.dumps(tag, ensure_ascii=False)}" for tag in unique_tags
    )
    if markdown.startswith("---\n"):
        closing = markdown.find("\n---\n", 4)
        if closing != -1:
            frontmatter = markdown[4:closing]
            body = markdown[closing + 5 :]
            if re.search(r"(?m)^tags:\s*$", frontmatter):
                frontmatter = re.sub(
                    r"(?m)^tags:\s*$", f"tags:{tag_lines}", frontmatter, count=1
                )
            elif re.search(r"(?m)^tags:\s*\[", frontmatter):
                frontmatter += f"\nresearch_delivery_tags:{tag_lines}"
            else:
                frontmatter += f"\ntags:{tag_lines}"
            return f"---\n{frontmatter}\n---\n{body}"
    tag_block = f"---\ntags:{tag_lines}"
    return f"{tag_block}\n---\n\n{markdown}"


def add_visual_summary(markdown: str, image_names: list[str]) -> str:
    embeds = "\n".join(f"![[assets/{name}.png]]" for name in image_names)
    section = f"\n\n## 视觉摘要\n\n{embeds}\n"
    summary = re.search(r"(?im)^## (?:执行摘要|summary)\s*$", markdown)
    if summary:
        next_section = re.search(r"(?m)^## .+$", markdown[summary.end() :])
        insertion = (
            len(markdown)
            if not next_section
            else summary.end() + next_section.start()
        )
        return markdown[:insertion].rstrip() + section + "\n" + markdown[insertion:]
    heading = re.search(r"(?m)^# .+$", markdown)
    if not heading:
        return markdown.rstrip() + section
    line_end = markdown.find("\n", heading.end())
    insertion = len(markdown) if line_end == -1 else line_end
    return markdown[:insertion] + section + markdown[insertion:]


def rewrite_material_links(markdown: str, source_directory_name: str) -> str:
    markdown = markdown.replace(
        f"](./{source_directory_name}/", "](./research-materials/"
    )
    return markdown.replace(
        f"]({source_directory_name}/", "](research-materials/"
    )


def validate_local_links(markdown: str, package_root: Path) -> None:
    targets = re.findall(r"\]\(([^)]+)\)", markdown)
    targets.extend(re.findall(r"!\[\[([^]|]+)(?:\|[^]]+)?\]\]", markdown))
    package_root = package_root.resolve()
    for raw_target in targets:
        target = raw_target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        relative = Path(unquote(parsed.path))
        if relative.is_absolute():
            raise ValueError(f"absolute local link is not portable: {raw_target}")
        resolved = (package_root / relative).resolve()
        if not resolved.is_relative_to(package_root) or not resolved.exists():
            raise ValueError(f"broken local link in published note: {raw_target}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--collection", default="DeepResearch")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--materials", type=Path, required=True)
    parser.add_argument("--diagram", action="append", type=parse_mapping, default=[])
    parser.add_argument(
        "--diagram-workdir", action="append", type=parse_mapping, default=[]
    )
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--minimum-diagrams", type=int, default=2)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    vault = args.vault.expanduser().resolve()
    report = args.report.expanduser().resolve()
    materials = args.materials.expanduser().resolve()

    require_directory(vault / ".obsidian", "vault marker")
    require_file(report, "report")
    require_directory(materials, "research materials")
    require_file(materials / "master-research.md", "master research")
    require_file(materials / "quality-report.md", "quality report")
    references = materials / "references"
    require_directory(references, "references archive")
    if not any(path.is_file() and path.stat().st_size for path in references.rglob("*")):
        raise ValueError(f"references archive must contain a non-empty file: {references}")
    if not SAFE_SLUG.fullmatch(args.slug):
        raise ValueError(
            "slug may contain only Unicode letters, numbers, dot, underscore, and dash"
        )

    diagrams = unique_mappings(args.diagram, "diagram")
    workdirs = unique_mappings(args.diagram_workdir, "diagram-workdir")
    if args.minimum_diagrams < 1:
        raise ValueError("minimum-diagrams must be at least 1")
    if len(diagrams) < args.minimum_diagrams:
        raise ValueError(
            f"at least {args.minimum_diagrams} accepted diagrams are required"
        )
    if set(diagrams) != set(workdirs):
        raise ValueError("every diagram must have one matching diagram-workdir")
    for name, image in diagrams.items():
        require_png(image, f"diagram {name}")
        validate_diagram_workdir(workdirs[name], image, name)

    collection = Path(args.collection)
    if collection.is_absolute() or ".." in collection.parts:
        raise ValueError("collection must be a safe relative path")
    destination_parent = vault / collection
    destination = destination_parent / args.slug
    destination_parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not args.overwrite:
        raise FileExistsError(f"destination already exists: {destination}")

    staging = Path(tempfile.mkdtemp(prefix=f".{args.slug}-", dir=destination_parent))
    try:
        assets_dir = staging / "assets"
        diagram_root = staging / "gracker-diagrams"
        assets_dir.mkdir()
        diagram_root.mkdir()
        shutil.copytree(materials, staging / "research-materials")

        copied_images = []
        for name, image in diagrams.items():
            target_image = assets_dir / f"{name}.png"
            shutil.copy2(image, target_image)
            shutil.copytree(workdirs[name], diagram_root / name)
            copied_images.append(
                {
                    "name": name,
                    "path": f"assets/{name}.png",
                    "sha256": sha256(target_image),
                }
            )

        note = report.read_text(encoding="utf-8")
        note = add_tags(note, args.tag)
        note = rewrite_material_links(note, materials.name)
        note = add_visual_summary(note, list(diagrams))
        note_path = staging / report.name
        note_path.write_text(note, encoding="utf-8")
        validate_local_links(note, staging)

        manifest = {
            "schema_version": 1,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "report": report.name,
            "research_materials": "research-materials",
            "minimum_diagrams": args.minimum_diagrams,
            "accepted_diagrams": copied_images,
        }
        (staging / "publish-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        if destination.exists():
            shutil.rmtree(destination)
        staging.rename(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    print(json.dumps({"destination": str(destination)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
