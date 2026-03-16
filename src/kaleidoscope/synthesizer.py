from __future__ import annotations

from kaleidoscope.models import LensAnalysis, ProblemContext, SynthesisReport
from kaleidoscope.providers import AnalysisProvider


def synthesize_report(
    context: ProblemContext,
    analyses: list[LensAnalysis],
    provider: AnalysisProvider,
) -> SynthesisReport:
    return provider.synthesize(context, analyses)
