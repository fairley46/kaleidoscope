"""Perspective routing and unknown-lens framing."""

from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from kaleidoscope.lens_loader import load_lenses
from kaleidoscope.models import ProblemContext
from kaleidoscope.providers import HeuristicAnalysisProvider
from kaleidoscope.report_writer import write_reports


def _write_lens(directory: Path, filename: str, body: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).write_text(textwrap.dedent(body).strip() + "\n", encoding="utf-8")


class PerspectiveRoutingTests(unittest.TestCase):
    def test_first_token_in_the_name_selects_the_perspective(self) -> None:
        context = ProblemContext(raw_problem="Move auth ownership to one team.", answers={})
        provider = HeuristicAnalysisProvider()

        with tempfile.TemporaryDirectory() as tmp:
            lenses_dir = Path(tmp)
            _write_lens(
                lenses_dir,
                "Mixed_Lens.md",
                """
                # Mixed Lens

                ## Lens Name
                Culture User Lens

                ## Purpose
                Unused purpose text for a named perspective.
                """,
            )
            lenses = load_lenses(lenses_dir)
            analysis = provider.analyze_lens(context, lenses[0])

        self.assertEqual(
            analysis.summary,
            "From the culture angle, the open question is whether people, incentives, and trust will carry this change.",
        )

    def test_unknown_lens_frames_purpose_without_authoring_instructions(self) -> None:
        context = ProblemContext(raw_problem="Auth ownership is unclear.", answers={})
        provider = HeuristicAnalysisProvider()

        with tempfile.TemporaryDirectory() as tmp:
            lenses_dir = Path(tmp) / "lenses"
            reports_dir = Path(tmp) / "reports"
            _write_lens(
                lenses_dir,
                "Security_Lens.md",
                """
                # Security Lens

                ## Lens Name
                Security Lens

                ## Purpose
                Explore how the problem changes exposure, access, and recovery.

                ## Key Questions
                - Who can reach the sensitive path today?

                ## What This Lens Looks For
                - Access that is wider than the problem statement admits.

                ## Common Risks / Failure Modes
                - A shared path that quietly widens access.

                ## Signals or Evidence to Consider
                - Who can reach the system today.

                ## Recommendation Style
                Shape recommendations in this tone: skeptical and specific.
                """,
            )
            lenses = load_lenses(lenses_dir)
            analysis = provider.analyze_lens(context, lenses[0])
            write_reports(
                reports_dir=reports_dir,
                context=context,
                analyses=[analysis],
                synthesis=provider.synthesize(context, [analysis]),
            )
            review = (reports_dir / "Security_Review.md").read_text(encoding="utf-8")

        self.assertEqual(
            analysis.summary,
            "From this perspective, the aim is to explore how the problem changes exposure, access, and recovery.",
        )
        self.assertNotIn("Shape recommendations in this tone", review)
        self.assertIn("Who can reach the sensitive path today?", review)
