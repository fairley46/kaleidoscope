from __future__ import annotations

import argparse
from pathlib import Path

from kaleidoscope.analyzer import analyze_lenses
from kaleidoscope.lens_loader import load_lenses
from kaleidoscope.providers import HeuristicAnalysisProvider
from kaleidoscope.question_flow import gather_context
from kaleidoscope.report_writer import write_reports
from kaleidoscope.synthesizer import synthesize_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kaleidoscope",
        description="Pressure-test an ambiguous engineering decision through multiple diagnostic lenses.",
    )
    parser.add_argument(
        "problem",
        nargs="?",
        help="A rough problem statement, decision prompt, or messy working thought.",
    )
    parser.add_argument(
        "--lenses-dir",
        type=Path,
        default=_project_root() / "lenses",
        help="Directory containing markdown lens files.",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=_project_root() / "reports",
        help="Directory where markdown reports will be written.",
    )
    parser.add_argument(
        "--max-questions",
        type=int,
        default=6,
        help="Maximum number of clarifying questions to ask before analysis.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    raw_problem = args.problem.strip() if args.problem else input("What problem are you working through?\n> ").strip()
    if not raw_problem:
        parser.error("A problem statement is required.")

    context = gather_context(raw_problem=raw_problem, max_questions=max(1, args.max_questions))
    lenses = load_lenses(args.lenses_dir)
    if not lenses:
        parser.error(f"No lens markdown files found in {args.lenses_dir}")

    provider = HeuristicAnalysisProvider()
    analyses = analyze_lenses(context=context, lenses=lenses, provider=provider)
    synthesis = synthesize_report(context=context, analyses=analyses, provider=provider)
    generated = write_reports(
        reports_dir=args.reports_dir,
        context=context,
        analyses=analyses,
        synthesis=synthesis,
    )

    print("")
    print("Kaleidoscope summary")
    print(synthesis.executive_synthesis)
    print("")
    print("Suggested next steps")
    for item in synthesis.recommendations[:3]:
        print(f"- {item}")
    print("")
    print("Generated reports")
    for path in generated:
        print(f"- {path}")

    return 0


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]
