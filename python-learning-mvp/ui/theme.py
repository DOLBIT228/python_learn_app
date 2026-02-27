"""Global UI theme and style injection for Streamlit app."""

from __future__ import annotations

import streamlit as st


def inject_global_styles() -> None:
    """Inject custom CSS design system styles."""

    st.markdown(
        """
        <style>
        :root {
            --primary: #4F46E5;
            --secondary: #22C55E;
            --background: #F9FAFB;
            --card: #FFFFFF;
            --text: #111827;
            --muted: #6B7280;
            --danger: #DC2626;
            --radius: 12px;
            --shadow: 0 10px 24px rgba(17, 24, 39, 0.08);
        }

        .stApp {
            background: var(--background);
            color: var(--text);
        }

        div[data-testid="stVerticalBlock"] > div.ui-card {
            background: var(--card);
            border-radius: var(--radius);
            padding: 1rem 1.1rem;
            box-shadow: var(--shadow);
            border: 1px solid #EEF2F7;
            transition: transform .2s ease, box-shadow .2s ease;
            margin-bottom: .75rem;
        }

        div[data-testid="stVerticalBlock"] > div.ui-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 28px rgba(17, 24, 39, 0.12);
        }


        div[data-testid="stVerticalBlock"] > div.ui-card.ui-card-locked {
            background: #F3F4F6;
            border-color: #E5E7EB;
            box-shadow: none;
            opacity: .85;
        }

        .ui-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0;
        }

        .ui-muted {
            color: var(--muted);
            font-size: .9rem;
            margin-top: .2rem;
        }

        /* Default Streamlit button polish */
        .stButton > button {
            width: 100%;
            border-radius: var(--radius);
            border: 1px solid transparent;
            background: linear-gradient(90deg, #4F46E5, #6366F1);
            color: white;
            font-weight: 600;
            padding: .65rem .9rem;
            transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
            box-shadow: 0 6px 16px rgba(79, 70, 229, 0.25);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.02);
        }

        .stButton > button:disabled {
            background: #D1D5DB;
            color: #6B7280;
            box-shadow: none;
            cursor: not-allowed;
        }

        .ui-btn-secondary .stButton > button {
            background: linear-gradient(90deg, #16A34A, #22C55E);
            box-shadow: 0 6px 16px rgba(34, 197, 94, 0.24);
        }

        .ui-btn-danger .stButton > button {
            background: #FEE2E2;
            color: #B91C1C;
            border: 1px solid #FCA5A5;
            box-shadow: none;
        }

        /* Exercise question and option styling */
        .ui-question {
            font-size: 1.65rem;
            font-weight: 700;
            line-height: 1.35;
            margin-bottom: .6rem;
        }

        div[role="radiogroup"] > label {
            background: #fff;
            border: 1px solid #E5E7EB;
            border-radius: var(--radius);
            padding: .7rem .85rem;
            margin-bottom: .55rem;
            transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
        }

        div[role="radiogroup"] > label:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(17, 24, 39, 0.08);
            border-color: #C7D2FE;
        }

        .ui-answer-correct,
        .ui-answer-incorrect {
            border-radius: var(--radius);
            padding: .75rem .9rem;
            font-weight: 600;
            margin-top: .4rem;
            margin-bottom: .6rem;
        }

        .ui-answer-correct {
            background: #DCFCE7;
            color: #166534;
            border: 1px solid #86EFAC;
        }

        .ui-answer-incorrect {
            background: #FEE2E2;
            color: #991B1B;
            border: 1px solid #FCA5A5;
        }

        .ui-explanation {
            background: #fff;
            border-radius: var(--radius);
            border: 1px solid #E5E7EB;
            box-shadow: var(--shadow);
            padding: .85rem 1rem;
            margin-top: .55rem;
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 999px;
        }

        .stProgress > div > div > div {
            background-color: #E5E7EB;
            border-radius: 999px;
        }

        /* Character bubble */
        .ui-character-wrap {
            display: grid;
            grid-template-columns: 110px 1fr;
            gap: .75rem;
            align-items: center;
            margin-bottom: .9rem;
        }

        .ui-character-svg {
            max-width: 110px;
        }

        .ui-speech {
            background: #EEF2FF;
            border: 1px solid #C7D2FE;
            border-radius: var(--radius);
            padding: .7rem .8rem;
            color: #312E81;
            font-weight: 500;
        }

        /* XP floating animation */
        .ui-xp-pop {
            position: relative;
            display: inline-block;
            color: #16A34A;
            font-weight: 800;
            animation: ui-xp-float 1.5s ease-out forwards;
            margin-top: .25rem;
            margin-bottom: .5rem;
        }

        @keyframes ui-xp-float {
            0% { opacity: 0; transform: translateY(8px) scale(.98); }
            15% { opacity: 1; transform: translateY(0) scale(1); }
            100% { opacity: 0; transform: translateY(-18px) scale(1.03); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
