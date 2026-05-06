import streamlit as st
import css.style as style
from n5.quiz.vocab_quiz_n5 import render_vocab_quiz
from n5.quiz.kanji_quiz_n5 import render_kanji_quiz
from n5.quiz.hiragana_quiz import render_hiragana_quiz
from n5.quiz.katakana_quiz import render_katakana_quiz
from n5.study.vocab_study_n5 import render_vocab_study
from n5.study.kanji_study_n5 import render_kanji_study
from n5.study.hiragana_study import render_hiragana_study
from n5.study.katakana_study import render_katakana_study

import streamlit as st

st.set_page_config(
    page_title="Japanese N5 Trainer",
    page_icon="🇯🇵",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------------------
# Helper: card style
# ---------------------------
def render_card(title, description, emoji, button_label, button_key, target_page, bg_color):
    st.markdown(
        f"""
        <div style="
            background: {bg_color};
            border: 1px solid #d9d9d9;
            border-radius: 18px;
            padding: 22px 18px;
            min-height: 240px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
            text-align: center;
        ">
            <div style="font-size: 46px; margin-bottom: 10px;">{emoji}</div>
            <div style="font-size: 22px; font-weight: 700; margin-bottom: 10px;">
                {title}
            </div>
            <div style="font-size: 14px; color: #444; line-height: 1.5;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    style.start_button_css()
    start_button = st.button(button_label, key=button_key, use_container_width=True)
    if start_button:
        st.session_state.page = target_page
        st.rerun()


# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state.page == "home":
    st.title("🇯🇵 Japanese N5 Trainer")
    st.write("Choose what you want to practice.")

    st.markdown("## Quiz")
    st.caption("Test yourself with quizzes.")

    col1, col2, col3, col4, col5 = st.columns(
        5, vertical_alignment="center", border=True
    )

    with col1:
        render_card(
            title="Hiragana",
            description="Practice Hiragana recognition and reading.",
            emoji="ひ",
            button_label="Start Hiragana Quiz",
            button_key="start_hiragana",
            target_page="hiragana_quiz",
            bg_color="#f1fff0"
        )

    with col2:
        render_card(
            title="Katakana",
            description="Practice Katakana recognition and reading.",
            emoji="カ",
            button_label="Start Katakana Quiz",
            button_key="start_katakana",
            target_page="katakana_quiz",
            bg_color="#f8f0ff"
        )

    with col3:
        render_card(
            title="Vocabulary N5",
            description="Practice N5 words: Greek, kana, romaji.",
            emoji="📘",
            button_label="Start Vocabulary Quiz",
            button_key="start_vocab",
            target_page="vocab_quiz",
            bg_color="#eef6ff"
        )

    with col4:
        render_card(
            title="Kanji N5",
            description="Practice N5 kanji, readings, and meaning.",
            emoji="🈶",
            button_label="Start Kanji Quiz",
            button_key="start_kanji",
            target_page="kanji_quiz",
            bg_color="#fff8e8"
        )

    with col5:
        render_card(
            title="Grammar",
            description="Practice grammar.",
            emoji="文",
            button_label="Start Grammar Quiz",
            button_key="start_grammar",
            target_page="grammar_quiz",
            bg_color="#f5f5f5"
        )

    st.divider()

    st.markdown("## Study")
    st.caption("Browse the lists without quizzing yourself.")

    col1, col2, col3, col4, col5 = st.columns(
        5, vertical_alignment="center", border=True
    )

    with col1:
        render_card(
            title="Hiragana",
            description="Browse Hiragana recognition and reading.",
            emoji="ひ",
            button_label="Open Hiragana",
            button_key="open_hiragana",
            target_page="hiragana_study",
            bg_color="#f1fff0"
        )

    with col2:
        render_card(
            title="Katakana",
            description="Browse Katakana recognition and reading.",
            emoji="カ",
            button_label="Open Katakana",
            button_key="open_katakana",
            target_page="katakana_study",
            bg_color="#f8f0ff"
        )

    with col3:
        render_card(
            title="Vocabulary N5",
            description="Practice N5 words or browse the list.",
            emoji="📘",
            button_label="Open Vocabulary",
            button_key="open_vocab",
            target_page="vocab_study",
            bg_color="#eef6ff"
        )

    with col4:
        render_card(
            title="Kanji N5",
            description="Browse kanji, readings, and meanings.",
            emoji="🈶",
            button_label="Open Kanji",
            button_key="open_kanji",
            target_page="kanji_study",
            bg_color="#fff8e8"
        )

    with col5:
        render_card(
            title="Grammar",
            description="Browse grammar notes and examples.",
            emoji="文",
            button_label="Open Grammar",
            button_key="open_grammar",
            target_page="grammar_study",
            bg_color="#f5f5f5"
        )

    st.stop()


# ---------------------------
# PAGE ROUTING
# ---------------------------

elif st.session_state.page == "hiragana_quiz":
    render_hiragana_quiz()

elif st.session_state.page == "katakana_quiz":
    render_katakana_quiz()

elif st.session_state.page == "vocab_quiz":
    render_vocab_quiz()

elif st.session_state.page == "kanji_quiz":
    render_kanji_quiz()

# elif st.session_state.page == "grammar_quiz":
#     render_grammar_quiz()

elif st.session_state.page == "hiragana_study":
    render_hiragana_study()

elif st.session_state.page == "katakana_study":
    render_katakana_study()

elif st.session_state.page == "vocab_study":
    render_vocab_study()

elif st.session_state.page == "kanji_study":
    render_kanji_study()

# elif st.session_state.page == "grammar_study":
#     render_grammar_study()
