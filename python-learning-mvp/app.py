"""Main Streamlit app for Python Learning MVP.

UI layer responsibilities:
- render pages (Login, Home, Lesson, Exercise)
- call service layer for business logic
- avoid implementing XP/heart/streak math in UI
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from database import SessionLocal, init_db
from models import Exercise, Lesson, Module, User
from services.gamification_service import complete_lesson, process_correct_answer, process_wrong_answer
from services.lesson_service import get_exercises, get_lessons, get_modules, validate_answer
from services.leaderboard_service import get_top_users
from ui.character import render_character
from ui.character_state_manager import CharacterStateManager
from ui.layout import render_layout
from ui.theme import inject_global_styles


BASE_DIR = Path(__file__).resolve().parent
CHARACTER_ASSETS_DIR = BASE_DIR / "assets" / "characters"

init_db()


def _get_character_manager() -> CharacterStateManager:
    if "character_manager" not in st.session_state:
        st.session_state.character_manager = CharacterStateManager(assets_dir=CHARACTER_ASSETS_DIR)
    return st.session_state.character_manager


def _render_character() -> None:
    manager = _get_character_manager()
    render_character(manager.current_state.value)


def _xp_pop_animation(xp_value: int) -> None:
    st.markdown(f'<div class="ui-xp-pop">+{xp_value} XP</div>', unsafe_allow_html=True)


def _get_or_create_user(email: str) -> User:
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            user = User(
                email=email,
                password_hash="mvp-placeholder-hash",
                xp=0,
                level=1,
                streak=0,
                hearts=5,
                premium=False,
                created_at=datetime.utcnow(),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user


def _get_current_user() -> User | None:
    user_id = st.session_state.get("user_id")
    if not user_id:
        return None
    with SessionLocal() as db:
        return db.query(User).filter(User.id == user_id).first()


def _seed_demo_content() -> None:
    with SessionLocal() as db:
        if db.query(Module.id).first():
            return
        module = Module(title="Python Basics", order=1)
        db.add(module)
        db.flush()
        lesson = Lesson(module_id=module.id, title="Variables 101", order=1, difficulty="easy")
        db.add(lesson)
        db.flush()
        db.add_all(
            [
                Exercise(
                    lesson_id=lesson.id,
                    type="MULTIPLE_CHOICE",
                    question="Яке ключове слово використовується для створення змінної в Python?",
                    options_json='["var", "let", "(не потрібне ключове слово)", "define"]',
                    correct_answer="(не потрібне ключове слово)",
                    explanation="У Python змінна створюється простим присвоєнням.",
                    difficulty="easy",
                ),
                Exercise(
                    lesson_id=lesson.id,
                    type="WRITE_LINE",
                    question="Напиши рядок коду, що присвоює x значення 10.",
                    options_json=None,
                    correct_answer="x = 10",
                    explanation="Використовуємо оператор '=' для присвоєння.",
                    difficulty="easy",
                ),
            ]
        )
        db.commit()


def _render_login_page() -> None:
    _get_character_manager().set_idle()
    st.title("🔐 Login")
    _render_character()
    email = st.text_input("Email", placeholder="you@example.com")
    if st.button("Login"):
        if not email.strip():
            st.error("Введіть email.")
            return
        user = _get_or_create_user(email.strip().lower())
        st.session_state.user_id = user.id
        st.session_state.page = "home"
        st.rerun()


def _render_home_page(user: User) -> None:
    _get_character_manager().set_idle()
    st.title("🏠 Home")
    _render_character()
    st.caption(f"User: {user.email}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Level", user.level)
    c2.metric("XP", user.xp)
    c3.metric("Hearts", user.hearts)

    modules = get_modules()
    if not modules:
        st.info("Модулі поки відсутні.")
        return

    st.subheader("Modules")
    for index, module in enumerate(modules):
        is_unlocked = index == 0
        card_class = "ui-card" if is_unlocked else "ui-card ui-card-locked"
        st.markdown(
            (
                f'<div class="{card_class}">'
                f'<p class="ui-title">{module.title}</p>'
                f'<p class="ui-muted">{"Unlocked" if is_unlocked else "Locked"}</p>'
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        progress_value = 100 if is_unlocked else 0
        st.progress(progress_value)
        if st.button(
            "Open module" if is_unlocked else "Locked",
            key=f"open_module_{module.id}",
            disabled=not is_unlocked,
        ):
            st.session_state.selected_module_id = module.id
            st.session_state.page = "lesson"
            st.rerun()

    st.subheader("🏆 Leaderboard (Top 20 by XP)")
    leaderboard = get_top_users(limit=20)
    if leaderboard:
        st.dataframe(
            [
                {
                    "Rank": idx + 1,
                    "Email": row.email,
                    "XP": row.xp,
                    "Level": row.level,
                    "Streak": row.streak,
                }
                for idx, row in enumerate(leaderboard)
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("Leaderboard порожній.")


def _render_lesson_page(user: User) -> None:
    _get_character_manager().set_loading()
    st.title("📘 Lesson Page")
    _render_character()

    module_id = st.session_state.get("selected_module_id")
    if not module_id:
        st.warning("Спочатку оберіть модуль на Home сторінці.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()
        return

    lessons = get_lessons(module_id)
    if not lessons:
        st.info("У цьому модулі поки немає уроків.")
        return

    for lesson in lessons:
        with st.container(border=True):
            st.write(f"**{lesson.title}**")
            st.caption(f"Difficulty: {lesson.difficulty}")
            if st.button("Start lesson", key=f"start_lesson_{lesson.id}"):
                st.session_state.selected_lesson_id = lesson.id
                st.session_state.exercise_index = 0
                st.session_state.lesson_correct = 0
                st.session_state.lesson_total = 0
                _get_character_manager().set_loading()
                st.session_state.page = "exercise"
                st.rerun()

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


def _save_user_updates(user: User) -> User:
    with SessionLocal() as db:
        db_user = db.query(User).filter(User.id == user.id).first()
        if db_user is None:
            return user
        db_user.xp = user.xp
        db_user.level = user.level
        db_user.hearts = user.hearts
        db_user.streak = user.streak
        db_user.last_activity_date = user.last_activity_date
        db.commit()
        db.refresh(db_user)
        return db_user


def _render_exercise_page(user: User) -> None:
    st.title("🧩 Exercise Page")
    _render_character()

    lesson_id = st.session_state.get("selected_lesson_id")
    if not lesson_id:
        st.warning("Спочатку оберіть урок.")
        if st.button("Back to Lesson Page"):
            st.session_state.page = "lesson"
            st.rerun()
        return

    exercises = get_exercises(lesson_id)
    if not exercises:
        st.info("Для цього уроку немає вправ.")
        return

    idx = st.session_state.get("exercise_index", 0)
    if idx >= len(exercises):
        total = max(st.session_state.get("lesson_total", 0), 1)
        correct = st.session_state.get("lesson_correct", 0)
        lesson_score = int((correct / total) * 100)
        updated_user = _get_current_user()
        if updated_user is not None:
            prev_level = updated_user.level
            lesson_result = complete_lesson(updated_user, lesson_score)
            _save_user_updates(updated_user)
            if lesson_result["new_level"] > prev_level:
                _get_character_manager().set_level_up()
            else:
                _get_character_manager().set_lesson_completed()
            _render_character()
            st.success("Урок завершено!")
            st.write(f"Score: {lesson_score}%")
            st.write(f"XP gained: {lesson_result['xp_gained']}")
            st.write(f"Current level: {lesson_result['new_level']}")
            st.write(f"Current XP: {lesson_result['current_xp']}")
        if st.button("Back to Home"):
            _get_character_manager().set_idle()
            st.session_state.page = "home"
            st.rerun()
        return

    _get_character_manager().set_loading()
    exercise = exercises[idx]
    result_state_key = f"exercise_result_{idx}"
    answer_state_key = f"answer_{idx}"
    st.subheader(f"Exercise {idx + 1}/{len(exercises)}")
    st.markdown(f'<div class="ui-question">{exercise.question}</div>', unsafe_allow_html=True)

    previous_result = st.session_state.get(result_state_key)
    if previous_result:
        if previous_result["is_correct"]:
            st.markdown('<div class="ui-answer-correct">✅ Correct answer!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="ui-answer-incorrect">❌ Невірно. Спробуємо наступне завдання.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-explanation"><b>Explanation:</b><br>{exercise.explanation}</div>', unsafe_allow_html=True)
        if st.button("Next", key=f"next_{idx}"):
            st.session_state.exercise_index = idx + 1
            st.session_state.pop(result_state_key, None)
            st.session_state.pop(answer_state_key, None)
            st.rerun()
        return

    if exercise.type == "MULTIPLE_CHOICE":
        options = json.loads(exercise.options_json or "[]")
        user_answer = st.radio("Виберіть відповідь", options=options, key=answer_state_key, label_visibility="collapsed")
    else:
        user_answer = st.text_input("Ваша відповідь", key=answer_state_key)

    if st.button("Submit answer", key=f"submit_{idx}"):
        is_correct = validate_answer(exercise, user_answer)
        st.session_state.lesson_total = st.session_state.get("lesson_total", 0) + 1

        live_user = _get_current_user()
        if live_user is None:
            st.error("Користувач не знайдений. Залогіньтесь знову.")
            st.session_state.page = "login"
            st.rerun()

        if is_correct:
            result = process_correct_answer(live_user, exercise.difficulty)
            st.session_state.lesson_correct = st.session_state.get("lesson_correct", 0) + 1
            _get_character_manager().set_correct_answer()
            st.success("✅ Correct!")
            _xp_pop_animation(result["xp_gained"])
        else:
            result = process_wrong_answer(live_user)
            _get_character_manager().set_error()
            st.error("❌ Невірно")
            st.caption(f"Hearts left: {result['hearts']}")

        _save_user_updates(live_user)
        _render_character()

        if not result["can_continue"]:
            st.warning("У вас закінчилися hearts. Спробуйте пізніше.")
            if st.button("Back to Home", key="hearts_back_home"):
                _get_character_manager().set_idle()
                st.session_state.page = "home"
                st.rerun()
            return

        st.session_state[result_state_key] = {
            "is_correct": is_correct,
            "xp_gained": result.get("xp_gained", 0),
        }
        st.rerun()

    if st.button("Back to Lesson Page"):
        _get_character_manager().set_idle()
        st.session_state.page = "lesson"
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Python Learning MVP", page_icon="🐍", layout="centered")
    inject_global_styles()
    _seed_demo_content()

    if "page" not in st.session_state:
        st.session_state.page = "login"

    user = _get_current_user()
    if st.session_state.page != "login" and user is None:
        st.session_state.page = "login"

    def _render_page_content() -> None:
        if st.session_state.page == "login":
            _render_login_page()
        elif st.session_state.page == "home" and user:
            _render_home_page(user)
        elif st.session_state.page == "lesson" and user:
            _render_lesson_page(user)
        elif st.session_state.page == "exercise" and user:
            _render_exercise_page(user)

    render_layout(_render_page_content)


if __name__ == "__main__":
    main()
