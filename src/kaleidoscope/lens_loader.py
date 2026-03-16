from __future__ import annotations

import re
from pathlib import Path

from kaleidoscope.models import LensDefinition


def _slugify(name: str) -> str:
    cleaned = name.replace("Lens", "").strip()
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", cleaned).strip("_")
    return slug or "Lens"


def _normalize_heading(text: str) -> str:
    return text.strip().lower()


def parse_lens_file(path: Path) -> LensDefinition:
    raw_content = path.read_text(encoding="utf-8").strip()
    title = path.stem.replace("_", " ")
    sections: dict[str, str] = {}
    current_heading: str | None = None
    bucket: list[str] = []

    for line in raw_content.splitlines():
        if line.startswith("# "):
            if title == path.stem.replace("_", " "):
                title = line[2:].strip()
            continue

        if line.startswith("## "):
            if current_heading is not None:
                sections[_normalize_heading(current_heading)] = "\n".join(bucket).strip()
            current_heading = line[3:].strip()
            bucket = []
            continue

        if current_heading is not None:
            bucket.append(line)

    if current_heading is not None:
        sections[_normalize_heading(current_heading)] = "\n".join(bucket).strip()

    name = sections.get("lens name", title).splitlines()[0].strip() if sections.get("lens name") else title
    return LensDefinition(
        name=name,
        slug=_slugify(name),
        path=path,
        title=title,
        sections=sections,
        raw_content=raw_content,
    )


def load_lenses(lenses_dir: Path) -> list[LensDefinition]:
    lenses: list[LensDefinition] = []
    for path in sorted(lenses_dir.glob("*.md")):
        if path.name.startswith("."):
            continue
        lenses.append(parse_lens_file(path))
    return lenses


def extract_bullets(markdown_section: str) -> list[str]:
    bullets: list[str] = []
    for line in markdown_section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            bullets.append(stripped[2:].strip())
    return bullets
