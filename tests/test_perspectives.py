"""Perspective routing, relation rules, and unknown-lens framing."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from kaleidoscope.analyzer import analyze_lenses
from kaleidoscope.lens_loader import load_lenses
from kaleidoscope.models import ProblemContext
from kaleidoscope.providers import HeuristicAnalysisProvider
from kaleidoscope.report_writer import write_reports
from kaleidoscope.synthesizer import synthesize_report

ROOT = Path(__file__).resolve().parents[1]
STRATEGY_ROADMAP = "Strategy and roadmap pull apart when the direction is named and the sequence is still open."
COMPANY_TEAM = (
    "Company and team perspectives pull apart when a wider pattern of work "
    "meets the load on the people closest to it."
)
CENTRALIZATION = (
    "Technical and operational perspectives can favor a shared path for consistency. "
    "Culture and user perspectives ask whether teams will experience that path as imposed or heavier."
)
REORG = (
    "Sharper ownership can make operations and accountability easier to see. "
    "The culture perspective asks whether people will experience the change as a status shift."
)
TIMING = (
    "The financial perspective may favor waiting for stronger evidence. "
    "The technical perspective may treat waiting as a way for complexity to compound."
)


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
        self.assertEqual(provider.synthesize(context, [analysis]).tensions, [])
        self.assertEqual(provider.synthesize(context, [analysis]).reinforcements, [])

    def test_rules_fire_only_when_named_perspectives_are_loaded(self) -> None:
        context = ProblemContext(
            raw_problem="We should centralize auth ownership across the organization.",
            answers={},
        )
        provider = HeuristicAnalysisProvider()
        selected = [
            lens
            for lens in load_lenses(ROOT / "lenses")
            if lens.name in {"Company Lens", "Team Lens"}
        ]
        analyses = analyze_lenses(context=context, lenses=selected, provider=provider)
        synthesis = synthesize_report(context=context, analyses=analyses, provider=provider)

        self.assertEqual(synthesis.tensions, [COMPANY_TEAM])
        self.assertNotIn(CENTRALIZATION, synthesis.tensions)
        self.assertNotIn(STRATEGY_ROADMAP, synthesis.tensions)

    def test_short_tokens_do_not_invent_reorg_or_timing(self) -> None:
        context = ProblemContext(
            raw_problem="The organization has a known documentation gap.",
            answers={},
        )
        provider = HeuristicAnalysisProvider()
        lenses = load_lenses(ROOT / "lenses")
        analyses = analyze_lenses(context=context, lenses=lenses, provider=provider)
        synthesis = synthesize_report(context=context, analyses=analyses, provider=provider)

        self.assertIn(STRATEGY_ROADMAP, synthesis.tensions)
        self.assertNotIn(REORG, synthesis.tensions)
        self.assertNotIn(TIMING, synthesis.tensions)

    def test_open_questions_include_a_later_perspective(self) -> None:
        context = ProblemContext(raw_problem="Auth ownership is unclear.", answers={})
        provider = HeuristicAnalysisProvider()
        lenses = load_lenses(ROOT / "lenses")
        analyses = analyze_lenses(context=context, lenses=lenses, provider=provider)
        synthesis = synthesize_report(context=context, analyses=analyses, provider=provider)

        roadmap_question = "What is already committed in the same window this would occupy?"
        self.assertIn(roadmap_question, synthesis.open_questions[:6])

    def test_cli_summary_leads_with_exploration(self) -> None:
        answers = "\n".join(
            [
                "Whether to centralize platform auth",
                "Platform and product engineering",
                "Headcount and timeline",
                "Clear ownership with no outage spike",
                "Centralize now; stay federated; phased rollout",
                "Auth drift and onboarding cost",
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "kaleidoscope",
                    "We should centralize auth, but I worry about downstream ownership.",
                    "--max-questions",
                    "6",
                    "--reports-dir",
                    tmp,
                ],
                input=answers + "\n",
                text=True,
                capture_output=True,
                cwd=ROOT,
                env=env,
                check=False,
            )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        stdout = proc.stdout
        self.assertNotIn("Suggested next steps", stdout)
        summary_at = stdout.index("Kaleidoscope summary")
        tensions_at = stdout.index("Tensions between perspectives")
        questions_at = stdout.index("Open questions")
        steps_at = stdout.index("Optional next steps")
        self.assertLess(summary_at, tensions_at)
        self.assertLess(tensions_at, questions_at)
        self.assertLess(questions_at, steps_at)
        self.assertIn(STRATEGY_ROADMAP, stdout)
