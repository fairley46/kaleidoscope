from __future__ import annotations

import textwrap
from collections import Counter
from typing import Protocol

from kaleidoscope.lens_loader import extract_bullets
from kaleidoscope.models import LensAnalysis, LensDefinition, ProblemContext, SynthesisReport


class AnalysisProvider(Protocol):
    def analyze_lens(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        ...

    def synthesize(
        self,
        context: ProblemContext,
        analyses: list[LensAnalysis],
    ) -> SynthesisReport:
        ...


class HeuristicAnalysisProvider:
    def analyze_lens(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        normalized_name = lens.name.lower()
        if "technical" in normalized_name:
            return self._technical_analysis(context, lens)
        if "culture" in normalized_name:
            return self._culture_analysis(context, lens)
        if "operational" in normalized_name:
            return self._operational_analysis(context, lens)
        if "financial" in normalized_name:
            return self._financial_analysis(context, lens)
        if "user" in normalized_name:
            return self._user_analysis(context, lens)
        return self._generic_analysis(context, lens)

    def synthesize(
        self,
        context: ProblemContext,
        analyses: list[LensAnalysis],
    ) -> SynthesisReport:
        themes = _detect_themes(context.combined_text)
        lens_highlights = [
            f"**{analysis.lens_name}:** {analysis.summary}" for analysis in analyses
        ]

        repeated_open_questions = _top_items(
            item
            for analysis in analyses
            for item in analysis.open_questions
        )
        aggregated_tradeoffs = _top_items(
            item
            for analysis in analyses
            for item in analysis.tradeoffs
        )
        aggregated_recommendations = _top_items(
            item
            for analysis in analyses
            for item in analysis.recommendations
        )

        blind_spots = _build_blind_spots(context, themes)
        cross_lens_tensions = _build_cross_lens_tensions(themes, analyses)

        executive_synthesis = _compose_executive_synthesis(context, analyses, themes)
        problem_overview = _compose_problem_overview(context)
        confidence_note = _build_confidence_note(context, analyses)

        return SynthesisReport(
            problem_overview=problem_overview,
            executive_synthesis=executive_synthesis,
            lens_highlights=lens_highlights,
            blind_spots=blind_spots,
            cross_lens_tensions=cross_lens_tensions,
            tradeoffs=aggregated_tradeoffs[:6],
            recommendations=aggregated_recommendations[:6],
            open_questions=repeated_open_questions[:6],
            confidence_note=confidence_note,
        )

    def _technical_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        themes = _detect_themes(context.combined_text)
        observations = [
            "The decision has meaningful architecture consequences, so the technical shape should be evaluated for both immediate fit and the system it nudges the organization toward over time.",
            _theme_line(
                themes,
                "centralization",
                "Centralization could reduce duplicated patterns, but it will only pay off if the shared capability stays narrow enough to remain understandable and supportable.",
            ),
            _theme_line(
                themes,
                "migration",
                "The technical soundness of a migration is likely to depend less on the destination state and more on compatibility, rollout sequencing, and reversibility.",
            ),
            _theme_line(
                themes,
                "reorg",
                "Ownership changes can clarify technical accountability, but they rarely resolve brittle interfaces unless contracts, boundaries, and decision rights also become explicit.",
            ),
            "Missing technical detail is itself a signal: if implementation paths, dependencies, or failure boundaries are still vague, the initiative may be directionally right but not yet decision-ready.",
        ]
        risks = [
            "Hidden dependencies could make the true implementation cost materially higher than the current framing suggests.",
            "A technically elegant solution may still increase long-term maintenance burden if it creates a new coordination hotspot or bespoke platform surface.",
            "If success criteria are not tied to measurable engineering outcomes, the work may look complete while still failing to reduce complexity.",
        ]
        tradeoffs = [
            "Standardization and leverage versus local team autonomy and speed.",
            "Long-term architectural coherence versus near-term delivery drag and migration overhead.",
            "Designing the durable abstraction now versus waiting for more usage evidence and risking additional sprawl in the meantime.",
        ]
        recommendations = [
            "Map the top dependencies, integration points, and rollback boundaries before committing to the final technical path.",
            "Describe at least one smaller reversible slice that could validate the direction without forcing full adoption.",
            "Define the technical success measures up front, such as complexity removed, incidents reduced, or implementation paths simplified.",
        ]
        open_questions = [
            "Which technical assumptions would become expensive if they turn out to be wrong?",
            "What would the rollout, coexistence period, or rollback path look like in practice?",
            "Does this reduce system complexity for most teams, or does it mostly relocate complexity into a shared layer?",
        ]
        evidence_to_consider = _evidence_from_lens(
            lens,
            fallback=[
                "Dependency maps, architecture diagrams, and known brittle interfaces.",
                "Current support burden, defect patterns, and maintenance hotspots.",
                "Past migrations or platform efforts with similar scope.",
            ],
        )
        return _build_analysis(
            context=context,
            lens=lens,
            summary="Technically plausible, but the real question is whether the chosen shape reduces future complexity instead of simply concentrating it.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )

    def _culture_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        observations = [
            "The proposal will land differently depending on whether people experience it as support, control, or another source of ambiguity.",
            "Adoption risk is often cultural before it is technical: people need to understand why the change exists, how it helps them, and which frustrations it removes.",
            "If the initiative changes ownership, standards, or ways of working, trust and clarity are likely to matter as much as the decision itself.",
            "A decision that looks efficient from leadership altitude can still create resentment if the day-to-day impact on teams is underexplained or unevenly distributed.",
        ]
        risks = [
            "Teams may comply publicly but resist in practice if the decision feels imposed or misaligned with local realities.",
            "Unclear communication could turn a strategic change into a morale problem, especially if it is perceived as loss of autonomy or status.",
            "If incentives do not change with the new direction, the organization may unintentionally preserve the old behavior beneath new language.",
        ]
        tradeoffs = [
            "Faster directional alignment versus the slower work of building durable buy-in.",
            "Consistency in how teams operate versus room for local context and judgment.",
            "Clear central ownership versus the perception that decision-making has moved farther away from the work.",
        ]
        recommendations = [
            "Identify whose behavior must change for this to work, then test whether the proposed change actually makes that behavior easier.",
            "Pressure-test the narrative with a small set of affected leaders or teams before finalizing the recommendation.",
            "Make stakeholder expectations explicit: what gets easier, what changes, and what support the organization will provide during the transition.",
        ]
        open_questions = [
            "Who is most likely to see this as helpful, and who is most likely to see it as a constraint?",
            "What new behavior is required for success, and what currently rewards the opposite behavior?",
            "How will leadership explain the why behind this change in a way that feels credible to teams close to the work?",
        ]
        evidence_to_consider = _evidence_from_lens(
            lens,
            fallback=[
                "Team sentiment, prior change-management lessons, and stakeholder feedback.",
                "Where similar directives have succeeded or quietly stalled in the organization.",
                "Known points of friction between teams, functions, or leadership layers.",
            ],
        )
        return _build_analysis(
            context=context,
            lens=lens,
            summary="The idea may be strategically reasonable, but it will only stick if the people dynamics and incentives around it are deliberately handled.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )

    def _operational_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        observations = [
            "Day-two ownership matters here. The operational burden after launch may be more important than the initial delivery plan.",
            "If the change introduces a new shared dependency, the reliability and support expectations for that dependency rise immediately.",
            "Operational readiness is usually where strategic proposals reveal their hidden cost: alerting, on-call ownership, handoffs, runbooks, and failure recovery all need a home.",
            "If turnover or organizational churn is likely, the operating model should survive people changes rather than depend on heroic institutional memory.",
        ]
        risks = [
            "Support load may quietly accumulate in a team that was not staffed or chartered for long-term sustainment.",
            "Failure modes can become more severe if a centralized or shared capability becomes a single point of operational friction.",
            "Without explicit ownership boundaries, incidents and escalations may get slower and more political rather than more reliable.",
        ]
        tradeoffs = [
            "Operational simplicity for consuming teams versus higher responsibility for the owning team.",
            "Improved consistency in steady state versus greater blast radius when the shared path fails.",
            "Shipping a technically valid solution now versus delaying until observability and readiness are good enough to trust it in production.",
        ]
        recommendations = [
            "Name the long-term owner and describe what support, observability, and escalation expectations come with that ownership.",
            "List the likely failure modes and confirm whether the proposed operating model can detect, triage, and recover from them.",
            "Treat day-two sustainment as part of the decision, not as a follow-up task after implementation.",
        ]
        open_questions = [
            "Who owns this six months after delivery, and do they actually want that ownership?",
            "What new operational toil might this create even if implementation goes smoothly?",
            "How would an incident involving this change be detected, escalated, and resolved?",
        ]
        evidence_to_consider = _evidence_from_lens(
            lens,
            fallback=[
                "On-call load, incident history, support queues, and operational dashboards.",
                "Ownership maps and escalation paths for adjacent systems.",
                "Readiness gaps in logging, metrics, alerting, and rollback procedures.",
            ],
        )
        return _build_analysis(
            context=context,
            lens=lens,
            summary="The proposal should be judged partly on who will run it, support it, and absorb its failures after the initial project energy fades.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )

    def _financial_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        observations = [
            "The real financial question is not just direct spend; it is whether this is the best use of limited engineering attention compared with the credible alternatives.",
            "A strategic initiative can be directionally right and still be mistimed if the payoff horizon is too slow relative to current constraints.",
            "Hidden cost usually shows up in migration effort, enablement work, temporary duplication, and leadership attention that cannot be spent elsewhere.",
            "Value should be tested against a realistic adoption path. Savings or leverage that require broad organizational behavior change often arrive later than expected.",
        ]
        risks = [
            "The initiative may consume high-leverage people and stall other work without producing proportional value soon enough.",
            "Projected ROI may be overstated if benefits are speculative, delayed, or dependent on adoption that has not been validated.",
            "Costs can be mis-scoped if analysis focuses on build effort but excludes migration, support, and transition overhead.",
        ]
        tradeoffs = [
            "Investing now to prevent future waste versus preserving capacity for more urgent work today.",
            "Funding the durable solution versus using a cheaper local workaround that may compound over time.",
            "Chasing long-term leverage versus accepting near-term opportunity cost and organizational disruption.",
        ]
        recommendations = [
            "Frame the decision against at least one credible alternative, including deferment, so the opportunity cost is explicit.",
            "Estimate value in ranges rather than precise numbers when uncertainty is still high.",
            "Separate one-time implementation cost from recurring support, migration, and coordination cost before declaring the investment attractive.",
        ]
        open_questions = [
            "What work would be delayed, deprioritized, or made harder if this proceeds now?",
            "How much of the expected value depends on broad adoption rather than direct technical change?",
            "What is the earliest point at which the organization should expect meaningful payback?",
        ]
        evidence_to_consider = _evidence_from_lens(
            lens,
            fallback=[
                "Headcount allocation, roadmap tradeoffs, and estimated migration effort.",
                "Baseline costs, wasted effort today, and the scale of repeated work being addressed.",
                "The likely time horizon for adoption and realized benefit.",
            ],
        )
        return _build_analysis(
            context=context,
            lens=lens,
            summary="Financially, the case depends on whether this produces meaningful leverage relative to the work and disruption it displaces.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )

    def _user_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        observations = [
            "A decision can be internally coherent and still underdeliver if the consuming team or end user experiences it as extra friction.",
            "The user-facing value should be tested directly: what gets simpler, faster, clearer, or more reliable for the people on the receiving end?",
            "Internal proxy metrics can obscure real experience. If the proposal mainly improves internal architecture, the user payoff still needs to be articulated honestly.",
            "Adoption is easier when the improvement is felt quickly and the new path is easier than the old one, not merely more compliant.",
        ]
        risks = [
            "The initiative may solve an internal coordination problem while adding new user-facing friction or confusion.",
            "A theoretically better path may go unused if it requires too much migration effort, training, or workflow change from consuming teams.",
            "If the problem statement is framed mostly from the builder's perspective, genuine user needs may be underspecified.",
        ]
        tradeoffs = [
            "Improving internal consistency versus preserving a low-friction experience for users and consuming teams.",
            "Building the complete ideal solution versus delivering the smallest user-visible improvement sooner.",
            "Pushing teams toward the preferred path versus earning adoption by making the path clearly better.",
        ]
        recommendations = [
            "Name the primary user or consuming team explicitly and define what improves for them in concrete terms.",
            "Validate the proposal with people who will experience the change directly before treating the current framing as sufficient.",
            "Prefer rollout shapes that let users feel value early rather than asking them to absorb upfront migration cost for delayed benefit.",
        ]
        open_questions = [
            "Whose experience improves first if this succeeds, and how will they notice?",
            "Does this solve a real user problem or mainly an internal proxy problem?",
            "What new friction might the consuming team inherit even if the core strategy is sound?",
        ]
        evidence_to_consider = _evidence_from_lens(
            lens,
            fallback=[
                "Customer feedback, support themes, workflow pain points, and adoption behavior.",
                "Current UX or DX friction for internal or external consumers.",
                "Evidence that the proposed change removes a problem users actually feel.",
            ],
        )
        return _build_analysis(
            context=context,
            lens=lens,
            summary="User value is plausible but should be proven in terms the consuming team can actually feel, not just in internal architecture language.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )

    def _generic_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        key_questions = extract_bullets(lens.section("key questions"))
        what_it_looks_for = extract_bullets(lens.section("what this lens looks for"))
        common_risks = extract_bullets(lens.section("common risks / failure modes"))
        signals = extract_bullets(lens.section("signals or evidence to consider"))
        recommendation_style = lens.section("recommendation style")
        purpose = lens.section("purpose")

        summary = textwrap.shorten(
            purpose or f"This lens provides an additional perspective on the decision.",
            width=180,
            placeholder="...",
        )
        observations = [
            f"This lens matters because {summary[0].lower() + summary[1:] if summary else 'it introduces a distinct point of view.'}",
            "The current problem framing should be tested against this lens directly rather than assumed to be covered by the default set of concerns.",
        ]
        observations.extend(
            f"From this lens, pay attention to {item.rstrip('.')}."
            for item in what_it_looks_for[:3]
        )

        risks = common_risks[:3] or [
            "The decision could be under-evaluated if this perspective is acknowledged but not translated into concrete questions or evidence.",
        ]
        tradeoffs = [
            "Depth from this specialized lens versus the time and coordination needed to gather the right evidence.",
            "Acting on directional confidence now versus delaying for sharper evidence from this perspective.",
        ]
        recommendations = [
            "Use this lens to challenge the current framing, not just to confirm what the other lenses already suggest.",
        ]
        if recommendation_style:
            recommendations.append(
                f"Shape recommendations in this tone: {textwrap.shorten(recommendation_style, width=140, placeholder='...')}"
            )
        open_questions = key_questions[:4] or [
            "What would this lens notice that the default lenses might miss?",
        ]
        evidence_to_consider = signals[:4] or [
            "Any direct evidence or stakeholder input that specifically grounds this lens.",
        ]

        return _build_analysis(
            context=context,
            lens=lens,
            summary=summary,
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )


def _build_analysis(
    context: ProblemContext,
    lens: LensDefinition,
    summary: str,
    observations: list[str],
    risks: list[str],
    tradeoffs: list[str],
    recommendations: list[str],
    open_questions: list[str],
    evidence_to_consider: list[str],
) -> LensAnalysis:
    enriched_observations = _dedupe(
        [item for item in observations if item]
        + _context_observations(context)
    )
    enriched_risks = _dedupe([item for item in risks if item] + _context_risks(context))
    enriched_questions = _dedupe([item for item in open_questions if item] + _context_questions(context))

    return LensAnalysis(
        lens_name=lens.name,
        slug=lens.slug,
        lens_path=lens.path,
        summary=summary,
        observations=enriched_observations[:6],
        risks=enriched_risks[:6],
        tradeoffs=_dedupe(item for item in tradeoffs if item)[:5],
        recommendations=_dedupe(item for item in recommendations if item)[:5],
        open_questions=enriched_questions[:6],
        evidence_to_consider=_dedupe(item for item in evidence_to_consider if item)[:5],
        confidence_note=_lens_confidence_note(context),
    )


def _compose_problem_overview(context: ProblemContext) -> str:
    lines = [f"The starting problem statement is: \"{context.raw_problem.strip()}\""]
    if context.get("decision"):
        lines.append(f"The concrete decision being weighed appears to be: {context.get('decision')}")
    if context.get("stakeholders"):
        lines.append(f"The most affected stakeholders appear to be: {context.get('stakeholders')}")
    if context.get("success"):
        lines.append(f"Current success framing: {context.get('success')}")
    return " ".join(lines)


def _compose_executive_synthesis(
    context: ProblemContext,
    analyses: list[LensAnalysis],
    themes: set[str],
) -> str:
    if {"centralization", "reorg"} & themes:
        shape = "The decision is less about a single technical move and more about what operating model the organization wants to reinforce."
    elif "migration" in themes:
        shape = "The decision appears strategically promising, but the migration path and reversibility may matter more than the destination architecture alone."
    elif "timing" in themes:
        shape = "The biggest question is not simply whether the idea is good, but whether this is the right time and scope for it."
    else:
        shape = "Across the lenses, the idea looks directionally plausible but still benefits from tighter framing before a firm commitment."

    caution = "The strongest pattern across reviews is that ambiguity remains around execution shape, stakeholder impact, and what success would concretely look like."
    if context.answered_count() >= 5:
        caution = "The clarifying answers create a more usable frame, but the reviews still suggest pressure-testing the plan before locking into a single course."

    value = "The likely value of moving forward will depend on whether the chosen path makes complexity, coordination, and user impact better in practice rather than better only on paper."
    if analyses:
        summary_lines = [analysis.summary for analysis in analyses[:2]]
        value = " ".join(summary_lines)

    return f"{shape} {caution} {value}"


def _build_blind_spots(context: ProblemContext, themes: set[str]) -> list[str]:
    blind_spots = [
        f"The current framing does not yet fully specify {item}."
        for item in context.missing_dimensions()[:4]
    ]

    if "centralization" in themes:
        blind_spots.append(
            "The case for centralization may be stronger in principle than in practice unless the consuming teams' migration burden and autonomy concerns are surfaced early."
        )
    if "reorg" in themes:
        blind_spots.append(
            "Org or ownership changes can overestimate what structural moves alone will fix if decision rights, service boundaries, and incentives stay fuzzy."
        )
    if "migration" in themes:
        blind_spots.append(
            "The destination state may be clearer than the coexistence and rollback plan, which is often where migration risk actually lives."
        )

    return _dedupe(blind_spots)[:6] or [
        "No major blind spots were surfaced, but this likely reflects the limits of the current heuristics rather than complete certainty."
    ]


def _build_cross_lens_tensions(
    themes: set[str],
    analyses: list[LensAnalysis],
) -> list[str]:
    tensions: list[str] = []
    if "centralization" in themes:
        tensions.append(
            "Technical and operational consistency may improve with centralization, while culture and user lenses warn that adoption can suffer if teams experience the change as imposed or heavier-weight."
        )
    if "reorg" in themes:
        tensions.append(
            "Sharper ownership can help operations and accountability, while culture concerns rise if the change is felt as a status shift or disruption rather than a clearer way to work."
        )
    if "migration" in themes:
        tensions.append(
            "The technical lens may favor the long-term destination, while operational and financial lenses emphasize migration drag, transition risk, and delayed payoff."
        )
    if "timing" in themes:
        tensions.append(
            "Financial discipline may push toward waiting for stronger evidence, while technical debt or platform direction may argue that waiting compounds the eventual cost."
        )

    if not tensions and analyses:
        tensions.extend(
            analysis.tradeoffs[0]
            for analysis in analyses
            if analysis.tradeoffs
        )

    return _dedupe(tensions)[:5]


def _build_confidence_note(context: ProblemContext, analyses: list[LensAnalysis]) -> str:
    if context.answered_count() >= 5:
        return "Moderate confidence. The problem has enough context for useful pressure-testing, but several conclusions remain conditional because the analysis is heuristic and the evidence base is still local and incomplete."
    if context.answered_count() >= 3:
        return "Moderate-to-low confidence. The framing is good enough to surface tensions and blind spots, but recommendations should be treated as prompts for discussion rather than firm guidance."
    return "Low confidence. The tool can still surface useful questions, but ambiguity in the framing means the outputs should be read as exploratory scaffolding."


def _context_observations(context: ProblemContext) -> list[str]:
    observations: list[str] = []
    if context.get("constraints"):
        observations.append(f"Relevant constraints already in play: {context.get('constraints')}")
    if context.get("options"):
        observations.append(f"Current option set: {context.get('options')}")
    if context.get("success"):
        observations.append(f"Success is currently framed as: {context.get('success')}")
    return observations


def _context_risks(context: ProblemContext) -> list[str]:
    risks: list[str] = []
    if context.get("risks"):
        risks.append(f"Known suspected risk: {context.get('risks')}")
    if not context.get("stakeholders"):
        risks.append("Stakeholder impact is still underspecified, which increases the risk of solving the wrong problem for the wrong audience.")
    if not context.get("success"):
        risks.append("Success is not yet concrete, so downstream evaluation may drift toward activity instead of outcome.")
    return risks


def _context_questions(context: ProblemContext) -> list[str]:
    questions: list[str] = []
    if context.get("assumptions"):
        questions.append(f"Which part of this assumption needs the most pressure-testing: {context.get('assumptions')}?")
    if not context.get("options"):
        questions.append("What credible alternative paths, including waiting or limiting scope, should be compared against the current direction?")
    if not context.get("constraints"):
        questions.append("What non-negotiables could materially narrow the solution space once they are made explicit?")
    return questions


def _lens_confidence_note(context: ProblemContext) -> str:
    if context.answered_count() >= 5:
        return "Moderate confidence from a local heuristic pass. Useful for framing and challenge, but still worth validating with evidence and stakeholder input."
    if context.answered_count() >= 3:
        return "Moderate-to-low confidence because the lens is working from partial context and no external validation."
    return "Low confidence because the analysis is extrapolating from a very rough initial framing."


def _evidence_from_lens(lens: LensDefinition, fallback: list[str]) -> list[str]:
    bullets = extract_bullets(lens.section("signals or evidence to consider"))
    return bullets[:4] or fallback


def _top_items(items) -> list[str]:
    ordered_unique: list[str] = []
    counter = Counter(item for item in items if item)
    for item, _ in counter.most_common():
        ordered_unique.append(item)
    return ordered_unique


def _dedupe(items) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(normalized)
    return result


def _detect_themes(text: str) -> set[str]:
    lowered = text.lower()
    theme_map = {
        "centralization": ("centralize", "centralized", "shared platform", "platform capability", "standardize"),
        "reorg": ("re-org", "reorg", "ownership", "org", "team boundary"),
        "migration": ("migration", "migrate", "cutover", "sunset", "replace"),
        "timing": ("wait", "defer", "later", "now", "timing", "investment"),
        "reliability": ("incident", "reliability", "outage", "resilience", "support burden"),
    }
    themes = {
        theme
        for theme, keywords in theme_map.items()
        if any(keyword in lowered for keyword in keywords)
    }
    return themes


def _theme_line(themes: set[str], theme: str, line: str) -> str:
    return line if theme in themes else ""
