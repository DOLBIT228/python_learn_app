"""Streak engine for daily learning consistency.

MVP rules from PRODUCT MASTER DOCUMENT:
- If user completed a lesson today -> streak +1 (once per calendar day)
- If user missed 1 day -> streak reset
- Milestones:
  - 7-day streak -> +50 XP reward
  - 30-day streak -> badge reward
"""

from __future__ import annotations

from datetime import date
from typing import Protocol


SEVEN_DAY_XP_BONUS = 50
BADGE_30_DAY = "streak_30_days"


class StreakUserLike(Protocol):
    """Minimal user contract required by streak engine functions."""

    streak: int
    last_activity_date: date | None


def _today() -> date:
    return date.today()


def update_streak(user: StreakUserLike) -> int:
    """Update streak for today's lesson completion and return streak value."""

    today = _today()
    last_activity = user.last_activity_date

    if last_activity is None:
        user.streak = 1
    else:
        days_diff = (today - last_activity).days
        if days_diff == 0:
            return user.streak
        if days_diff == 1:
            user.streak += 1
        else:
            user.streak = 1

    user.last_activity_date = today
    return user.streak


def reset_streak(user: StreakUserLike) -> int:
    """Reset streak to zero and return updated streak."""

    user.streak = 0
    return user.streak


def check_streak_milestones(user: StreakUserLike) -> dict[str, object]:
    """Check streak milestones and return reward metadata.

    Returns a dict containing:
    - xp_bonus: int
    - badges: list[str]
    """

    rewards = {
        "xp_bonus": 0,
        "badges": [],
    }

    if user.streak > 0 and user.streak % 7 == 0:
        rewards["xp_bonus"] = SEVEN_DAY_XP_BONUS

    if user.streak >= 30 and user.streak % 30 == 0:
        rewards["badges"].append(BADGE_30_DAY)

    return rewards
