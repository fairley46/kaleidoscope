from __future__ import annotations

import re
import textwrap
from typing import Protocol

from kaleidoscope.lens_loader import extract_bullets
from kaleidoscope.models import LensAnalysis, LensDefinition, ProblemContext, SynthesisReport

PERSPECTIVE_TOKENS: tuple[str, ...] = (
    "company",
    "team",
    "culture",
    "strategy",
    "roadmap",
    "technical",
    "operational",
    "financial",
    "user",
)


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
    def __init__(self) -> None:
        by_token = {
            "company": self._company_analysis,
            "team": self._team_analysis,
            "culture": self._culture_analysis,
            "strategy": self._strategy_analysis,
            "roadmap": self._roadmap_analysis,
            "technical": self._technical_analysis,
            "operational": self._operational_analysis,
            "financial": self._financial_analysis,
            "user": self._user_analysis,
        }
        self._analyzers = {token: by_token[token] for token in PERSPECTIVE_TOKENS}

    def analyze_lens(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        normalized_name = lens.name.lower()
        for token, method in self._analyzers.items():
            if token in normalized_name:
                return method(context, lens)
        return self._generic_analysis(context, lens)

    def synthesize(
        self,
        context: ProblemContext,
        analyses: list[LensAnalysis],
    ) -> SynthesisReport:
        themes = _detect_themes(context.combined_text)
        perspectives = [
            f"**{analysis.lens_name}:** {analysis.summary}" for analysis in analyses
        ]

        present = _present_tokens(analyses)
        blind_spots = _build_blind_spots(context, themes)
        tensions = _build_tensions(themes, analyses, present)
        reinforcements = _build_reinforcements(themes, present)

        exploration_overview = _compose_exploration_overview(context, analyses, themes)
        problem_overview = _compose_problem_overview(context)
        confidence_note = _build_confidence_note(context, analyses)

        return SynthesisReport(
            problem_overview=problem_overview,
            exploration_overview=exploration_overview,
            perspectives=perspectives,
            reinforcements=reinforcements,
            tensions=tensions,
            blind_spots=blind_spots,
            open_questions=_interleave(analyses, "open_questions", 8),
            recommendations=_interleave(analyses, "recommendations", 6),
            tradeoffs=_interleave(analyses, "tradeoffs", 6),
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
            summary="From the technical angle, the open question is whether the chosen shape reduces future complexity or mainly concentrates it.",
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
            summary="From the culture angle, the open question is whether people, incentives, and trust will carry this change.",
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
            summary="From the operational angle, the open question is who runs this, supports it, and absorbs failures after the first push.",
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
            summary="From the financial angle, the open question is whether the effort returns leverage relative to the work and disruption it displaces.",
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
            summary="From the user angle, the open question is whether the people who feel this change will notice a real improvement.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=evidence_to_consider,
        )

    def _company_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        themes = _detect_themes(context.combined_text)
        observations = [
            "From the company angle, the useful question is which pattern of work this problem would make more normal.",
            _theme_line(
                themes,
                "centralization",
                "A shared capability changes who sets the default way of working, and that default shows up in later choices across teams.",
            ),
            _theme_line(
                themes,
                "reorg",
                "An ownership or structure change reads, at company scale, as a statement about which work the organization wants to keep close.",
            ),
            "If the framing stays inside one team, this perspective still asks whether that local shape matches a wider pattern.",
        ]
        risks = [
            "A local fix can harden an operating pattern the organization did not mean to keep.",
            "Language about alignment can outrun any real change in how work moves.",
            "Concentrating a capability without a reason other teams would recognize can read as control.",
        ]
        tradeoffs = [
            "A shared company pattern versus room for local variation.",
            "Moving on a pattern now versus waiting until more teams have felt the same problem.",
        ]
        recommendations = [
            "Name the company pattern this would reinforce, in one sentence a team outside the project would recognize.",
            "Ask two neighboring teams whether they would describe the same problem.",
        ]
        open_questions = [
            "What pattern of work would this make normal across the organization?",
            "Who, outside the team closest to the problem, would have to live with that pattern?",
            "If this became the default, which later choices would get easier and which would get harder?",
        ]
        return _build_analysis(
            context=context,
            lens=lens,
            summary="From the company angle, this problem sits inside how the organization sets direction and concentrates work.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=_evidence_from_lens(
                lens,
                fallback=[
                    "How neighboring teams describe the same problem.",
                    "Earlier changes that became an unstated default.",
                    "Stated operating principles, and where current work matches them.",
                ],
            ),
        )

    def _team_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        themes = _detect_themes(context.combined_text)
        observations = [
            "From the team angle, the useful question is who would carry this after the first push, and what that does to their week.",
            _theme_line(
                themes,
                "reorg",
                "Moving ownership changes the team that gets interrupted, asked, and blamed when the work slips or breaks.",
            ),
            _theme_line(
                themes,
                "centralization",
                "A shared path can remove local variation and still add handoffs for the team that has to wait on the shared owner.",
            ),
            "If the proposal names a team and does not name the load, the team perspective still treats the load as part of the problem.",
        ]
        risks = [
            "Long-term ownership can land on a team that was not in the original framing.",
            "A path that looks simpler on a diagram can add coordination for the people who use it.",
            "The work can depend on one person's context, with no path for anyone else to hold it.",
        ]
        tradeoffs = [
            "Local speed for the team closest to the work versus a shared path others can join.",
            "Clear ownership on one team versus spreading the load across teams that already have commitments.",
        ]
        recommendations = [
            "Name the team that would own this six months out, and the load that comes with that ownership.",
            "Ask the receiving team what they would keep doing the old way if the new path is heavier.",
        ]
        open_questions = [
            "Which team would carry the ongoing work, and do they have room for it?",
            "What gets easier in the day-to-day, and what gets heavier?",
            "Which local workaround would teams keep if the new path is harder than the old one?",
        ]
        return _build_analysis(
            context=context,
            lens=lens,
            summary="From the team angle, the open question is how the people closest to the work would carry the load, the ownership, and the coordination.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=_evidence_from_lens(
                lens,
                fallback=[
                    "How the affected team describes its current load.",
                    "Handoffs and waiting that already shape the work.",
                    "Who gets interrupted when this area breaks today.",
                ],
            ),
        )

    def _strategy_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        themes = _detect_themes(context.combined_text)
        observations = [
            "From the strategy angle, the useful question is which longer direction this problem serves.",
            _theme_line(
                themes,
                "centralization",
                "Centralizing a capability is a direction choice. It makes one shared path easier to repeat and makes divergent local paths harder to defend.",
            ),
            _theme_line(
                themes,
                "timing",
                "Starting, waiting, or narrowing the scope would teach the organization different lessons about which direction actually matters.",
            ),
            "A framing that sounds like a local fix can still set aside another direction by taking the attention that direction needed.",
        ]
        risks = [
            "A preference with a long time horizon can get called a strategy before anyone names the direction it serves.",
            "A direction that needs every team to adopt it can proceed with no evidence that they will.",
            "Attention can move toward one arc while the problem statement never names the arc that lost room.",
        ]
        tradeoffs = [
            "A lasting commitment to one direction versus a smaller probe that teaches whether the direction is real.",
            "Serving the stated arc versus spending attention on a bet that sits beside it.",
        ]
        recommendations = [
            "Name the longer direction this serves, and name one direction that would lose room.",
            "Describe a smaller slice that would teach something about that direction before the whole path is treated as settled.",
        ]
        open_questions = [
            "Which longer direction does this problem serve?",
            "What becomes easier to repeat if this path holds?",
            "Which other direction loses attention or room if this proceeds?",
        ]
        return _build_analysis(
            context=context,
            lens=lens,
            summary="From the strategy angle, the open question is which longer direction this problem serves.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=_evidence_from_lens(
                lens,
                fallback=[
                    "The direction the organization already says it is pursuing.",
                    "Paths that were set aside, and why.",
                    "A smaller slice that would teach something about the direction.",
                ],
            ),
        )

    def _roadmap_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        themes = _detect_themes(context.combined_text)
        observations = [
            "From the roadmap angle, the useful question is where this sits among work already in motion.",
            _theme_line(
                themes,
                "migration",
                "A migration is a sequence. The destination matters less, on a roadmap, than who carries the coexistence period and when the old path stops.",
            ),
            _theme_line(
                themes,
                "timing",
                "Waiting and starting now are different sequences. Each one changes what else can move in the same window.",
            ),
            "If the framing names a direction and does not name what slips, the roadmap perspective still treats the slip as part of the problem.",
        ]
        risks = [
            "The work can land on a roadmap as if the people on the critical path were free.",
            "A coexistence period can start with no owner and no point where the old path stops.",
            "Other commitments can slip without being named.",
        ]
        tradeoffs = [
            "A smaller first slice that fits the current sequence versus a full cutover that displaces other commitments.",
            "Starting while the critical people are already committed versus waiting for a window that may not arrive cleanly.",
        ]
        recommendations = [
            "Place this beside the commitments already in the same window, and name what would shrink or wait.",
            "Describe the coexistence period, including who owns it and what has to be true before the old path stops.",
        ]
        open_questions = [
            "What is already committed in the same window this would occupy?",
            "What has to happen first, and what can wait until after a smaller slice?",
            "What would waiting change about the sequence, and what would starting now change?",
        ]
        return _build_analysis(
            context=context,
            lens=lens,
            summary="From the roadmap angle, the open question is where this sits among work already in motion.",
            observations=observations,
            risks=risks,
            tradeoffs=tradeoffs,
            recommendations=recommendations,
            open_questions=open_questions,
            evidence_to_consider=_evidence_from_lens(
                lens,
                fallback=[
                    "Work already committed for the same people and the same window.",
                    "Dependencies that gate the first useful slice.",
                    "What would slip or wait if this entered the sequence.",
                ],
            ),
        )

    def _generic_analysis(self, context: ProblemContext, lens: LensDefinition) -> LensAnalysis:
        key_questions = extract_bullets(lens.section("key questions"))
        what_it_looks_for = extract_bullets(lens.section("what this lens looks for"))
        common_risks = extract_bullets(lens.section("common risks / failure modes"))
        signals = extract_bullets(lens.section("signals or evidence to consider"))
        purpose = lens.section("purpose")

        aim = purpose.strip().splitlines()[0].strip().rstrip(".") if purpose else ""
        if aim:
            lowered_aim = aim[0].lower() + aim[1:]
            summary = textwrap.shorten(
                f"From this perspective, the aim is to {lowered_aim}.",
                width=220,
                placeholder="...",
            )
        else:
            summary = "This perspective looks at the problem from an angle the named lenses may leave aside."
        observations = [
            "Read the problem through this perspective on its own, in case the named lenses do not cover it.",
        ]
        observations.extend(
            f"This perspective looks for {item.rstrip('.')}."
            for item in what_it_looks_for[:3]
        )

        risks = common_risks[:3] or [
            "This perspective can be named in the framing and still never turned into a concrete question.",
        ]
        tradeoffs = [
            "Time spent on this perspective versus time spent gathering evidence for the perspectives already in the room.",
            "Moving with the current frame versus waiting until this perspective has something specific to say.",
        ]
        recommendations = [
            "Ask what this perspective notices that the others have not asked yet.",
        ]
        open_questions = key_questions[:4] or [
            "What would this perspective notice that the named lenses might miss?",
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
        lines.append(f"The problem or change being explored appears to be: {context.get('decision')}")
    if context.get("stakeholders"):
        lines.append(f"The most affected stakeholders appear to be: {context.get('stakeholders')}")
    if context.get("success"):
        lines.append(f"Current success framing: {context.get('success')}")
    return " ".join(lines)


def _compose_exploration_overview(
    context: ProblemContext,
    analyses: list[LensAnalysis],
    themes: set[str],
) -> str:
    if {"centralization", "reorg"} & themes:
        shape = (
            "This problem is less about a single technical move and more about the operating model "
            "the organization is reinforcing."
        )
    elif "migration" in themes:
        shape = (
            "This problem is as much about migration path and reversibility as about the destination architecture."
        )
    elif "timing" in themes:
        shape = (
            "Timing and scope are part of the problem itself, not only whether the idea sounds right."
        )
    else:
        shape = (
            "Across the loaded perspectives, the framing is useful enough to explore and still open enough to stay provisional."
        )

    caution = (
        "Ambiguity remains around execution shape, stakeholder impact, and what success would look like in practice."
    )
    if context.answered_count() >= 5:
        caution = (
            "The clarifying answers give a usable frame. The perspectives below are for exploration, not a verdict."
        )

    if analyses:
        value = " ".join(analysis.summary for analysis in analyses[:2])
    else:
        value = "No perspectives were loaded."

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


def _present_tokens(analyses: list[LensAnalysis]) -> set[str]:
    present: set[str] = set()
    for analysis in analyses:
        lowered = analysis.lens_name.lower()
        for token in PERSPECTIVE_TOKENS:
            if token in lowered:
                present.add(token)
                break
    return present


def _build_tensions(
    themes: set[str],
    analyses: list[LensAnalysis],
    present: set[str],
) -> list[str]:
    tensions: list[str] = []
    if "centralization" in themes and {"technical", "culture"} & present:
        tensions.append(
            "Technical and operational consistency may improve with centralization, while culture and user lenses warn that adoption can suffer if teams experience the change as imposed or heavier-weight."
        )
    if "reorg" in themes and {"culture", "operational"} & present:
        tensions.append(
            "Sharper ownership can help operations and accountability, while culture concerns rise if the change is felt as a status shift or disruption rather than a clearer way to work."
        )
    if "migration" in themes and {"technical", "operational"} & present:
        tensions.append(
            "The technical lens may favor the long-term destination, while operational and financial lenses emphasize migration drag, transition risk, and delayed payoff."
        )
    if "timing" in themes and {"financial", "technical", "strategy", "roadmap"} & present:
        tensions.append(
            "Financial discipline may push toward waiting for stronger evidence, while technical debt, strategy direction, or roadmap pressure may argue that waiting compounds the eventual cost."
        )
    if {"strategy", "roadmap"}.issubset(present):
        tensions.append(
            "Strategy and roadmap can diverge when the directional bet is clear but the sequence, capacity, and what moves on the roadmap stay unresolved."
        )
    if {"company", "team"}.issubset(present):
        tensions.append(
            "Company and team perspectives can diverge when enterprise mandate and local capacity are both real and not yet reconciled."
        )
    if "reliability" in themes and {"operational", "roadmap"} & present:
        tensions.append(
            "Operational readiness concerns can sit in tension with roadmap pressure to land a first slice before support and recovery paths are clear."
        )

    if not tensions and analyses:
        tensions.extend(
            analysis.tradeoffs[0]
            for analysis in analyses
            if analysis.tradeoffs
        )

    return _dedupe(tensions)[:6]


def _build_reinforcements(themes: set[str], present: set[str]) -> list[str]:
    reinforcements: list[str] = []
    if "centralization" in themes and {"technical", "operational"}.issubset(present):
        reinforcements.append(
            "Technical and operational perspectives reinforce each other when centralization is framed as reducing duplicated patterns and clarifying day-two ownership of the shared path."
        )
    if {"culture", "user"}.issubset(present):
        reinforcements.append(
            "Culture and user perspectives reinforce each other when adoption depends on whether people experience the change as relief rather than heavier process."
        )
    if {"company", "strategy"}.issubset(present):
        reinforcements.append(
            "Company and strategy perspectives reinforce each other when the problem is tied to a named company outcome and an explicit strategic bet."
        )
    if "migration" in themes and {"roadmap", "operational"}.issubset(present):
        reinforcements.append(
            "Roadmap and operational perspectives reinforce each other when migration success is treated as a sequenced coexistence problem, not only a destination architecture."
        )
    if "reorg" in themes and {"team", "operational"}.issubset(present):
        reinforcements.append(
            "Team and operational perspectives reinforce each other when sharper ownership is paired with an explicit sustainment and escalation model."
        )
    return _dedupe(reinforcements)[:6] or [
        "No strong cross-perspective reinforcement stood out from the current framing."
    ]


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


def _interleave(analyses: list[LensAnalysis], field_name: str, limit: int) -> list[str]:
    buckets = [list(getattr(analysis, field_name)) for analysis in analyses]
    chosen: list[str] = []
    seen: set[str] = set()
    depth = 0
    while len(chosen) < limit:
        progressed = False
        for bucket in buckets:
            if depth >= len(bucket):
                continue
            progressed = True
            item = bucket[depth].strip()
            key = item.lower()
            if item and key not in seen:
                seen.add(key)
                chosen.append(item)
                if len(chosen) >= limit:
                    break
        if not progressed:
            break
        depth += 1
    return chosen


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
        "centralization": (
            r"\bcentralize\b",
            r"\bcentralized\b",
            r"shared platform",
            r"platform capability",
            r"\bstandardize\b",
        ),
        "reorg": (
            r"\bre-?org\b",
            r"\bownership\b",
            r"\borg\b",
            r"\borganization\b",
            r"team boundary",
        ),
        "migration": (
            r"\bmigration\b",
            r"\bmigrate\b",
            r"\bcutover\b",
            r"\bsunset\b",
            r"\breplace\b",
        ),
        "timing": (
            r"\bwait\b",
            r"\bdefer\b",
            r"\blater\b",
            r"\bnow\b",
            r"\btiming\b",
            r"\binvestment\b",
            r"phased rollout",
        ),
        "reliability": (
            r"\bincident\b",
            r"\breliability\b",
            r"\boutage\b",
            r"\bresilience\b",
            r"support burden",
        ),
    }
    themes: set[str] = set()
    for theme, patterns in theme_map.items():
        if any(re.search(pattern, lowered) for pattern in patterns):
            themes.add(theme)
    return themes


def _theme_line(themes: set[str], theme: str, line: str) -> str:
    return line if theme in themes else ""
