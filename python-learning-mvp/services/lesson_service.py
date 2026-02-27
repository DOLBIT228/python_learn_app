"""Lesson service for reading learning content and validating answers."""

from __future__ import annotations

import re
from typing import Any

from database import SessionLocal
from models import Exercise, Lesson, Module


def get_modules() -> list[Module]:
    """Return all modules ordered by their configured order."""

    with SessionLocal() as db:
        return db.query(Module).order_by(Module.order.asc(), Module.id.asc()).all()


def get_lessons(module_id: int) -> list[Lesson]:
    """Return lessons for a module ordered by lesson order."""

    with SessionLocal() as db:
        return (
            db.query(Lesson)
            .filter(Lesson.module_id == module_id)
            .order_by(Lesson.order.asc(), Lesson.id.asc())
            .all()
        )


def get_exercises(lesson_id: int) -> list[Exercise]:
    """Return exercises for a lesson ordered by id."""

    with SessionLocal() as db:
        return db.query(Exercise).filter(Exercise.lesson_id == lesson_id).order_by(Exercise.id.asc()).all()


def _normalize_text(value: Any) -> str:
    """Normalize free-text/code-line answer for tolerant comparison."""

    text = str(value or "").strip().lower()
    return re.sub(r"\s+", " ", text)


def validate_answer(exercise: Exercise, user_answer: Any) -> bool:
    """Validate user answer according to exercise type rules.

    MVP rules:
    - MULTIPLE_CHOICE -> exact match to correct_answer
    - FILL_CODE -> exact string match
    - WRITE_LINE -> normalized text match
    """

    exercise_type = (exercise.type or "").strip().upper()
    correct_answer = exercise.correct_answer or ""

    if exercise_type == "MULTIPLE_CHOICE":
        return str(user_answer) == str(correct_answer)

    if exercise_type == "FILL_CODE":
        return str(user_answer) == str(correct_answer)

    if exercise_type == "WRITE_LINE":
        return _normalize_text(user_answer) == _normalize_text(correct_answer)

    raise ValueError(f"Unsupported exercise type: {exercise.type}")
