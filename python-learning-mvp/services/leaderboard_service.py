"""Leaderboard service for ranking users by XP."""

from __future__ import annotations

from database import SessionLocal
from models import User


def get_top_users(limit: int = 20) -> list[User]:
    """Return top users sorted by XP descending (top-N leaderboard)."""

    with SessionLocal() as db:
        return (
            db.query(User)
            .order_by(User.xp.desc(), User.level.desc(), User.created_at.asc())
            .limit(limit)
            .all()
        )
