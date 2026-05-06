import json
import random
import css.style as style
import streamlit as st

st.set_page_config(
    page_title="Katakana Quiz",
    page_icon="🇯🇵",
    layout="centered"
)

def load_katakana(path="n5/data/katakana.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return text.strip().lower()


def get_question_and_answer(item, mode):
    if mode == "Kana → Romaji":
        return item["kana"], item["romaji"]
    elif mode == "Romaji → Kana":
        return item["romaji"], item["kana"]
    return item["kana"], item["romaji"]

def filter_items(data, type_filter):
    if type_filter == "Standard":
        return [item for item in data if item.get("type") == "standard katakana"]
    elif type_filter == "Dakuten":
        return [item for item in data if item.get("type") == "dakuten"]
    elif type_filter == "Handakuten":
        return [item for item in data if item.get("type") == "handakuten"]
    elif type_filter == "Yōon":
        return [item for item in data if item.get("type") == "yōon combinations"]
    return data

def reset_katakana_quiz():
    keys_to_reset = [
        "katakana_questions",
        "katakana_index",
        "katakana_score",
        "katakana_started",
        "katakana_failed_items",
        "katakana_feedback",
        "katakana_feedback_type",
        "katakana_mode",
        "katakana_quiz_size"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def render_katakana_quiz():
    st.title("カ Katakana Quiz")
    st.divider()

    # Application
    st.set_page_config(
        page_title="Japanese N5 Quiz", 
        page_icon="🇯🇵", 
        layout="centered")
    st.write("Practice your Katakana.")

    katakana_data = load_katakana("n5/data/katakana.json")

    # Quiz settings
    mode = st.sidebar.radio(
        "Quiz direction",
        ["Greek → Romaji", "Romaji → Greek"], 
        key="katakana_mode"
    )    
    
    type_filter = st.sidebar.radio(
        "Type",
        ["All", "Standard", "Dakuten", "Handakuten", "Yōon"],
        index=0
    )
    filtered_katakana = filter_items(katakana_data, type_filter)

    if not filtered_katakana:
        st.warning("No items available for the selected filter.")
        st.stop()

    quiz_size = st.sidebar.slider(
        "Number of questions",
        1,
        len(filtered_katakana),
        min(5, len(filtered_katakana)),
        key="katakana_quiz_size"
    )

    # Session state
    if "katakana_questions" not in st.session_state:
        st.session_state.katakana_questions = []
    if "katakana_index" not in st.session_state:
        st.session_state.katakana_index = 0
    if "katakana_score" not in st.session_state:
        st.session_state.katakana_score = 0
    if "katakana_started" not in st.session_state:
        st.session_state.katakana_started = False
    if "katakana_failed_items" not in st.session_state:
        st.session_state.katakana_failed_items = []
    if "katakana_feedback" not in st.session_state:
        st.session_state.katakana_feedback = ""
    if "katakana_feedback_type" not in st.session_state:
        st.session_state.katakana_feedback_type = None

    # Start/restart quiz
    start_btn = st.button("Start / Restart Katakana Quiz", key="start_katakana_quiz")

    if start_btn:
        st.session_state.katakana_questions = random.sample(
            filtered_katakana,
            min(quiz_size, len(filtered_katakana))
        )
        st.session_state.katakana_index = 0
        st.session_state.katakana_score = 0
        st.session_state.katakana_failed_items = []
        st.session_state.katakana_feedback = ""
        st.session_state.katakana_feedback_type = None
        st.session_state.katakana_started = True
        st.rerun()

    if not st.session_state.katakana_started:
        st.info("Click **Start / Restart Katakana Quiz** to begin.")
        st.divider()
        if st.button("← Back to main menu", key="back_katakana_home"):
            reset_katakana_quiz()
            st.session_state.page = "home"
            st.rerun()
        st.stop()

    # Finish quiz
    if st.session_state.katakana_index >= len(st.session_state.katakana_questions):
        st.success(
            f"Quiz finished! Final score: {st.session_state.katakana_score}/{len(st.session_state.katakana_questions)}"
        )

        if st.session_state.katakana_failed_items:
            st.subheader("Failed items")
            for item in st.session_state.katakana_failed_items:
                q, a = get_question_and_answer(item, mode)
                st.write(f"- **{q}** → {a}")
        else:
            st.success("Perfect score! No failed items.")

        st.divider()
        if st.button("← Back to main menu", key="back_katakana_end"):
            reset_katakana_quiz()
            st.session_state.page = "home"
            st.rerun()

        st.stop()
    
        st.divider()
        if st.button("← Back to main menu", key="back_kanji_end"):
            reset_katakana_quiz()
            st.session_state.page = "home"
            st.rerun()
        return

    # Show feedback from previous answer
    if st.session_state.katakana_feedback:
        if st.session_state.katakana_feedback_type == "success":
            st.success(st.session_state.katakana_feedback)
        elif st.session_state.katakana_feedback_type == "error":
            st.error(st.session_state.katakana_feedback)

    # Current question
    current_item = st.session_state.katakana_questions[st.session_state.katakana_index]
    question, correct_answer = get_question_and_answer(current_item, mode)

    st.metric("Score", f"{st.session_state.katakana_score}/{len(st.session_state.katakana_questions)}")
    st.subheader(f"Question {st.session_state.katakana_index + 1}/{len(st.session_state.katakana_questions)}")

    with st.form("katakana_answer_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(
                f"<div style='font-size: 28px; font-weight: 700;'>Translate: {question}</div>",
                unsafe_allow_html=True
            )

        with col2:
            user_answer = st.text_input("Your answer")

        style.add_button_css()
        submitted = st.form_submit_button("Submit", 
                                          use_container_width=True)
    
    if submitted and normalize(user_answer) != "":
        if normalize(user_answer) in normalize(correct_answer):
            st.success("Correct!")
            st.session_state.katakana_score += 1
            st.session_state.katakana_feedback = f"Correct! ✅ {question} → {correct_answer}"
            st.session_state.katakana_feedback_type = "success"
        else:
            st.error(f"Wrong. Correct answer: **{correct_answer}**")
            st.session_state.katakana_failed_items.append(current_item)
            st.session_state.katakana_feedback = f"Wrong ❌ Correct answer: {correct_answer}"
            st.session_state.katakana_feedback_type = "error"

        st.session_state.katakana_index += 1
        st.rerun()

    st.divider()
    if st.button("← Back to main menu", key="back_katakana_quiz"):
        reset_katakana_quiz()
        st.session_state.page = "home"
        st.rerun()
