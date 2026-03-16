from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from kaleidoscope.models import ProblemContext


@dataclass(frozen=True)
class QuestionSpec:
    key: str
    prompt: str


QUESTION_BANK = [
    QuestionSpec(
        "decision",
        "What decision, change, or investment are you actually weighing?",
    ),
    QuestionSpec(
        "stakeholders",
        "Who is most affected if this goes well or badly?",
    ),
    QuestionSpec(
        "constraints",
        "What constraints or non-negotiables matter here?",
    ),
    QuestionSpec(
        "success",
        "What would success look like in six months if this works?",
    ),
    QuestionSpec(
        "options",
        "What options are already on the table, including doing nothing or waiting?",
    ),
    QuestionSpec(
        "risks",
        "What risks or downstream consequences are you already worried about?",
    ),
    QuestionSpec(
        "assumptions",
        "What assumptions feel true right now, but might deserve pressure-testing?",
    ),
]


def _has_enough_context(answers: dict[str, str]) -> bool:
    must_haves = ("decision", "stakeholders", "success")
    must_have_count = sum(1 for key in must_haves if answers.get(key, "").strip())
    supporting = ("constraints", "options", "risks", "assumptions")
    supporting_count = sum(1 for key in supporting if answers.get(key, "").strip())
    return must_have_count >= 2 and supporting_count >= 2


def gather_context(
    raw_problem: str,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    max_questions: int = 6,
) -> ProblemContext:
    output_func("")
    output_func("Kaleidoscope framing")
    output_func("Answer briefly. You can skip any question with an empty response.")

    answers: dict[str, str] = {}
    questions_asked = 0

    for question in QUESTION_BANK:
        if questions_asked >= max_questions or _has_enough_context(answers):
            break

        response = input_func(f"\n{question.prompt}\n> ").strip()
        questions_asked += 1
        if response:
            answers[question.key] = response

    return ProblemContext(raw_problem=raw_problem.strip(), answers=answers)
