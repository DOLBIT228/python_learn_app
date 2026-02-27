"""Service layer that orchestrates gamification engines.

This module combines XP, hearts, and streak logic for common user actions.
"""

from __future__ import annotations

from typing import Any

from core.hearts_engine import can_start_lesson, remove_heart
from core.streak_engine import check_streak_milestones, update_streak
from core.xp_engine import PERFECT_LESSON_BONUS, calculate_xp, check_level_up


def _apply_xp(user: Any, xp_delta: int) -> dict[str, Any]:
    """Apply XP to user and resolve level-up carry-over."""

    if xp_delta < 0:
        raise ValueError("xp_delta must be >= 0")

    new_level, remaining_xp, leveled_up = check_level_up(user.xp + xp_delta, user.level)
    user.level = new_level
    user.xp = remaining_xp

    return {
        "xp_gained": xp_delta,
        "new_level": user.level,
        "current_xp": user.xp,
        "leveled_up": leveled_up,
    }


def process_correct_answer(user: Any, difficulty: str) -> dict[str, Any]:
    """Handle reward flow for a correct answer."""

    earned_xp = calculate_xp(difficulty)
    xp_result = _apply_xp(user, earned_xp)

    return {
        **xp_result,
        "hearts": user.hearts,
        "can_continue": can_start_lesson(user),
    }


def process_wrong_answer(user: Any) -> dict[str, Any]:
    """Handle penalty flow for a wrong answer."""

    hearts_left = remove_heart(user)
    return {
        "hearts": hearts_left,
        "can_continue": can_start_lesson(user),
    }


def complete_lesson(user: Any, lesson_score: int) -> dict[str, Any]:
    """Handle lesson completion rewards (perfect bonus + streak milestones)."""

    bonus_xp = PERFECT_LESSON_BONUS if lesson_score >= 100 else 0

    update_streak(user)
    streak_rewards = check_streak_milestones(user)
    bonus_xp += int(streak_rewards["xp_bonus"])

    xp_result = _apply_xp(user, bonus_xp)

    badges = list(streak_rewards["badges"])
    if badges:
        existing_badges = getattr(user, "badges", []) or []
        merged = list(existing_badges)
        for badge in badges:
            if badge not in merged:
                merged.append(badge)
        setattr(user, "badges", merged)

    return {
        **xp_result,
        "streak": user.streak,
        "badges": badges,
        "perfect_bonus_applied": lesson_score >= 100,
    }
