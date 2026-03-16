from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from kaleidoscope.models import LensAnalysis, ProblemContext, SynthesisReport


def write_reports(
    reports_dir: Path,
    context: ProblemContext,
    analyses: list[LensAnalysis],
    synthesis: SynthesisReport,
) -> list[Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    for analysis in analyses:
        report_path = reports_dir / _review_filename(analysis.lens_name)
        report_path.write_text(_lens_review_markdown(context, analysis), encoding="utf-8")
        generated.append(report_path)

    synthesis_path = reports_dir / "Kaleidoscope_Report.md"
    synthesis_path.write_text(_synthesis_markdown(context, synthesis), encoding="utf-8")
    generated.append(synthesis_path)
    return generated


def _review_filename(lens_name: str) -> str:
    base = re.sub(r"\bLens\b", "", lens_name, flags=re.IGNORECASE).strip()
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", base).strip("_") or "Lens"
    return f"{safe}_Review.md"


def _lens_review_markdown(context: ProblemContext, analysis: LensAnalysis) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# {analysis.lens_name} Review",
        "",
        f"_Generated: {timestamp}_",
        "",
        "## Problem Snapshot",
        f"- Raw problem: {context.raw_problem}",
    ]

    if context.answers:
        lines.append("- Clarified context:")
        for key, value in context.answers.items():
            if value.strip():
                lines.append(f"  - {key.replace('_', ' ').title()}: {value.strip()}")

    lines.extend(
        [
            "",
            "## Lens Summary",
            analysis.summary,
            "",
            "## Observations",
        ]
    )
    lines.extend(f"- {item}" for item in analysis.observations)
    lines.extend(["", "## Risks"])
    lines.extend(f"- {item}" for item in analysis.risks)
    lines.extend(["", "## Tradeoffs"])
    lines.extend(f"- {item}" for item in analysis.tradeoffs)
    lines.extend(["", "## Recommendations"])
    lines.extend(f"- {item}" for item in analysis.recommendations)
    lines.extend(["", "## Open Questions"])
    lines.extend(f"- {item}" for item in analysis.open_questions)
    lines.extend(["", "## Signals or Evidence to Consider"])
    lines.extend(f"- {item}" for item in analysis.evidence_to_consider)
    lines.extend(
        [
            "",
            "## Confidence / Ambiguity",
            analysis.confidence_note,
            "",
            f"_Source lens file: {analysis.lens_path}_",
            "",
        ]
    )
    return "\n".join(lines)


def _synthesis_markdown(context: ProblemContext, synthesis: SynthesisReport) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Kaleidoscope Report",
        "",
        f"_Generated: {timestamp}_",
        "",
        "## Problem Overview",
        synthesis.problem_overview,
        "",
        "## Executive Synthesis",
        synthesis.executive_synthesis,
        "",
        "## Lens Highlights",
    ]
    lines.extend(f"- {item}" for item in synthesis.lens_highlights)
    lines.extend(["", "## Blind Spots"])
    lines.extend(f"- {item}" for item in synthesis.blind_spots)
    lines.extend(["", "## Cross-Lens Tensions"])
    lines.extend(f"- {item}" for item in synthesis.cross_lens_tensions)
    lines.extend(["", "## Tradeoffs"])
    lines.extend(f"- {item}" for item in synthesis.tradeoffs)
    lines.extend(["", "## Recommendations / Ideas"])
    lines.extend(f"- {item}" for item in synthesis.recommendations)
    lines.extend(["", "## Open Questions"])
    lines.extend(f"- {item}" for item in synthesis.open_questions)
    lines.extend(
        [
            "",
            "## Confidence / Ambiguity Notes",
            synthesis.confidence_note,
            "",
            "## Session Context",
            f"- Raw problem: {context.raw_problem}",
        ]
    )
    for key, value in context.answers.items():
        if value.strip():
            lines.append(f"- {key.replace('_', ' ').title()}: {value.strip()}")
    lines.append("")
    return "\n".join(lines)
