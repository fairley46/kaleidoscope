from __future__ import annotations

from kaleidoscope.models import LensAnalysis, LensDefinition, ProblemContext
from kaleidoscope.providers import AnalysisProvider


def analyze_lenses(
    context: ProblemContext,
    lenses: list[LensDefinition],
    provider: AnalysisProvider,
) -> list[LensAnalysis]:
    return [provider.analyze_lens(context, lens) for lens in lenses]
