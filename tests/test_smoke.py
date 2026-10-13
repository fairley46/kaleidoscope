"""Characterization pin for the V1 heuristic review path."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kaleidoscope.analyzer import analyze_lenses
from kaleidoscope.lens_loader import load_lenses
from kaleidoscope.providers import HeuristicAnalysisProvider
from kaleidoscope.question_flow import gather_context
from kaleidoscope.report_writer import write_reports
from kaleidoscope.synthesizer import synthesize_report

ROOT = Path(__file__).resolve().parents[1]


class ReviewPathTests(unittest.TestCase):
    def test_heuristic_run_writes_master_report(self) -> None:
        answers = iter(
            [
                "Whether to centralize platform auth",
                "Platform and product engineering",
                "Headcount and timeline",
                "Clear ownership with no outage spike",
                "Centralize now; stay federated; phased rollout",
                "Auth drift and onboarding cost",
            ]
        )

        context = gather_context(
            raw_problem="We should centralize auth, but I worry about downstream ownership.",
            input_func=lambda _prompt: next(answers),
            output_func=lambda _msg: None,
            max_questions=6,
        )
        lenses = load_lenses(ROOT / "lenses")
        self.assertGreaterEqual(len(lenses), 9)

        provider = HeuristicAnalysisProvider()
        analyses = analyze_lenses(context=context, lenses=lenses, provider=provider)
        synthesis = synthesize_report(context=context, analyses=analyses, provider=provider)

        with tempfile.TemporaryDirectory() as tmp:
            generated = write_reports(
                reports_dir=Path(tmp),
                context=context,
                analyses=analyses,
                synthesis=synthesis,
            )
            master = Path(tmp) / "Kaleidoscope_Report.md"
            self.assertTrue(master.exists())
            report = master.read_text(encoding="utf-8")
            self.assertIn("## Exploration Overview", report)
            self.assertIn("## Perspectives", report)
            self.assertIn("## Where Perspectives Reinforce", report)
            self.assertIn("## Tensions Between Perspectives", report)
            self.assertIn("## Open Questions", report)
            self.assertIn("From the company angle", report)
            self.assertIn("From the team angle", report)
            self.assertIn("From the strategy angle", report)
            self.assertIn("From the roadmap angle", report)
            self.assertGreaterEqual(len(generated), 10)


if __name__ == "__main__":
    unittest.main()
