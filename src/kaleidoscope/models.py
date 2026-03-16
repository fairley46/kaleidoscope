from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ProblemContext:
    raw_problem: str
    answers: dict[str, str]
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def combined_text(self) -> str:
        parts = [self.raw_problem.strip()]
        parts.extend(
            f"{key.replace('_', ' ').title()}: {value.strip()}"
            for key, value in self.answers.items()
            if value.strip()
        )
        return "\n".join(parts).strip()

    def get(self, key: str, default: str = "") -> str:
        return self.answers.get(key, default).strip()

    def answered_count(self) -> int:
        return sum(1 for value in self.answers.values() if value.strip())

    def missing_dimensions(self) -> list[str]:
        dimensions = [
            ("decision", "the concrete decision or change being weighed"),
            ("stakeholders", "who is most affected"),
            ("constraints", "the meaningful constraints or non-negotiables"),
            ("success", "what success looks like"),
            ("options", "which options are already being considered"),
            ("risks", "the risks already suspected"),
            ("assumptions", "the assumptions that still need pressure-testing"),
        ]
        return [label for key, label in dimensions if not self.get(key)]


@dataclass
class LensDefinition:
    name: str
    slug: str
    path: Path
    title: str
    sections: dict[str, str]
    raw_content: str

    def section(self, title: str) -> str:
        return self.sections.get(title.lower(), "").strip()


@dataclass
class LensAnalysis:
    lens_name: str
    slug: str
    lens_path: Path
    summary: str
    observations: list[str]
    risks: list[str]
    tradeoffs: list[str]
    recommendations: list[str]
    open_questions: list[str]
    evidence_to_consider: list[str]
    confidence_note: str


@dataclass
class SynthesisReport:
    problem_overview: str
    executive_synthesis: str
    lens_highlights: list[str]
    blind_spots: list[str]
    cross_lens_tensions: list[str]
    tradeoffs: list[str]
    recommendations: list[str]
    open_questions: list[str]
    confidence_note: str
