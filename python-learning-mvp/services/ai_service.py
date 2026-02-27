"""AI service for generating lesson exercises with OpenAI API."""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI


REQUIRED_EXERCISE_FIELDS = {
    "type",
    "question",
    "options_json",
    "correct_answer",
    "explanation",
    "difficulty",
}


def _get_openai_client() -> OpenAI:
    """Create OpenAI client from environment configuration."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def _validate_exercise_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize payload to Exercise-schema compatible shape."""

    missing = REQUIRED_EXERCISE_FIELDS - payload.keys()
    if missing:
        raise ValueError(f"AI response missing required fields: {sorted(missing)}")

    payload["type"] = str(payload["type"]).strip().upper()
    payload["question"] = str(payload["question"]).strip()
    payload["correct_answer"] = str(payload["correct_answer"]).strip()
    payload["explanation"] = str(payload["explanation"]).strip()
    payload["difficulty"] = str(payload["difficulty"]).strip().lower()

    options = payload.get("options_json")
    if options is None:
        payload["options_json"] = None
    elif isinstance(options, str):
        payload["options_json"] = options
    else:
        payload["options_json"] = json.dumps(options, ensure_ascii=False)

    return payload


def generate_exercise(topic: str, difficulty: str) -> dict[str, Any]:
    """Generate a single exercise using OpenAI API.

    Returns structure compatible with Exercise schema fields:
    type, question, options_json, correct_answer, explanation, difficulty.
    """

    client = _get_openai_client()

    system_prompt = (
        "You generate Python learning exercises for beginners. "
        "Return only valid JSON object with fields: "
        "type, question, options_json, correct_answer, explanation, difficulty. "
        "Allowed type values: MULTIPLE_CHOICE, FILL_CODE, WRITE_LINE."
    )
    user_prompt = (
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        "Create exactly one short exercise in Ukrainian. "
        "If type is MULTIPLE_CHOICE, provide options_json as a JSON array with 4 options. "
        "For other types set options_json to null."
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content or "{}"
    payload = json.loads(content)

    return _validate_exercise_payload(payload)
