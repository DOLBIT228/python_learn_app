"""Hearts engine for lesson attempt availability.

MVP rules:
- Max hearts: 5
- Non-premium users lose 1 heart on mistake
- Hearts regenerate by 1 every 4 hours
- Premium users effectively have unlimited hearts
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Protocol


MAX_HEARTS = 5
REGEN_INTERVAL = timedelta(hours=4)


class HeartsUserLike(Protocol):
    """Minimal user contract required by hearts engine functions."""

    hearts: int
    premium: bool


def _now() -> datetime:
    return datetime.utcnow()


def _get_regen_anchor(user: HeartsUserLike) -> datetime | None:
    """Read regen anchor timestamp from user if available."""

    return getattr(user, "hearts_regen_at", None)


def _set_regen_anchor(user: HeartsUserLike, value: datetime) -> None:
    """Persist regen anchor timestamp on user object."""

    setattr(user, "hearts_regen_at", value)


def remove_heart(user: HeartsUserLike) -> int:
    """Remove one heart for non-premium users and return current hearts."""

    if user.premium:
        return MAX_HEARTS

    regenerate_hearts(user)

    if user.hearts > 0:
        user.hearts -= 1
        if user.hearts < MAX_HEARTS and _get_regen_anchor(user) is None:
            _set_regen_anchor(user, _now())

    return user.hearts


def regenerate_hearts(user: HeartsUserLike) -> int:
    """Regenerate hearts based on 4-hour intervals and return current hearts."""

    if user.premium:
        return MAX_HEARTS

    if user.hearts >= MAX_HEARTS:
        user.hearts = MAX_HEARTS
        return user.hearts

    anchor = _get_regen_anchor(user)
    now = _now()

    if anchor is None:
        _set_regen_anchor(user, now)
        return user.hearts

    elapsed = now - anchor
    hearts_to_regen = int(elapsed.total_seconds() // REGEN_INTERVAL.total_seconds())

    if hearts_to_regen <= 0:
        return user.hearts

    user.hearts = min(MAX_HEARTS, user.hearts + hearts_to_regen)

    if user.hearts >= MAX_HEARTS:
        _set_regen_anchor(user, now)
    else:
        _set_regen_anchor(user, anchor + (REGEN_INTERVAL * hearts_to_regen))

    return user.hearts


def can_start_lesson(user: HeartsUserLike) -> bool:
    """Return whether the user can start a lesson right now."""

    if user.premium:
        return True

    regenerate_hearts(user)
    return user.hearts > 0
