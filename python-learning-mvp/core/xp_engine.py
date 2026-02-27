"""XP engine for gamification rules.

Implements MVP rules from the PRODUCT MASTER DOCUMENT:
- XP per difficulty: easy=10, medium=20, hard=30
- Perfect lesson bonus: +15 XP
- XP required per level: 100 * current_level
- XP carries over across levels
"""

from typing import Tuple


DIFFICULTY_XP = {
    "easy": 10,
    "medium": 20,
    "hard": 30,
}
PERFECT_LESSON_BONUS = 15


def calculate_xp(difficulty: str, perfect_bonus: bool = False) -> int:
    """Calculate XP reward for a lesson/exercise result.

    Args:
        difficulty: Difficulty label (easy, medium, hard).
        perfect_bonus: Whether to add perfect completion bonus.

    Returns:
        Total XP to award.

    Raises:
        ValueError: If difficulty is unsupported.
    """

    normalized = difficulty.strip().lower()
    if normalized not in DIFFICULTY_XP:
        allowed = ", ".join(sorted(DIFFICULTY_XP.keys()))
        raise ValueError(f"Unsupported difficulty '{difficulty}'. Allowed: {allowed}.")

    xp = DIFFICULTY_XP[normalized]
    if perfect_bonus:
        xp += PERFECT_LESSON_BONUS
    return xp


def get_xp_required(level: int) -> int:
    """Return XP required to pass the provided current level."""

    if level < 1:
        raise ValueError("Level must be >= 1.")
    return 100 * level


def check_level_up(current_xp: int, current_level: int) -> Tuple[int, int, bool]:
    """Resolve level-up progression using carry-over XP.

    Args:
        current_xp: XP currently stored toward the next level.
        current_level: User's current level.

    Returns:
        Tuple of (new_level, remaining_xp, leveled_up).
    """

    if current_xp < 0:
        raise ValueError("current_xp must be >= 0.")
    if current_level < 1:
        raise ValueError("current_level must be >= 1.")

    new_level = current_level
    remaining_xp = current_xp

    while remaining_xp >= get_xp_required(new_level):
        remaining_xp -= get_xp_required(new_level)
        new_level += 1

    return new_level, remaining_xp, new_level > current_level
