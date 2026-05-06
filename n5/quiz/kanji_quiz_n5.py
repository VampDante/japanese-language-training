import json
import random
import css.style as style
import streamlit as st

def load_kanji(path="n5_n5quiz/data/kanji_n5.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return text.strip().lower()

def get_question_and_answer(item, mode):
    if mode == "Kanji → Greek":
        return item["kanji"], item["greek"]
    elif mode == "Kanji → Romaji":
        return item["kanji"], item["romaji"]
    elif mode == "Greek → Kanji":
        return item["greek"], item["kanji"]
    elif mode == "Romaji → Kanji":
        return item["romaji"], item["kanji"]
    else:
        return item["kanji"], item["greek"]
    
def reset_kanji_quiz():
    keys_to_reset = [
        "kanji_questions",
        "kanji_index",
        "kanji_score",
        "kanji_started",
        "kanji_failed_items",
        "kanji_feedback",
        "kanji_feedback_type",
        "kanji_mode",
        "kanji_quiz_size"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def render_kanji_quiz():
    st.title("🈶 Kanji N5 Quiz")
    st.divider()

    # Application
    st.set_page_config(
        page_title="Japanese N5 Quiz", 
        page_icon="🇯🇵", 
        layout="centered")
    st.write("Practice your N5 Kanji.")

    kanji_data = load_kanji("n5/data/kanji_n5.json")

    # Quiz settings
    st.sidebar.header("Quiz Settings")
    mode = st.sidebar.radio(
        "Quiz mode",
        ["Kanji → Greek", "Kanji → Romaji", "Greek → Kanji", "Romaji → Kanji"],
        key="kanji_mode"
    )

    quiz_size = st.sidebar.slider(
        "Number of questions",
        1,
        len(kanji_data),
        min(5, len(kanji_data)),
        key="kanji_quiz_size"
    )

    # Session state
    if "kanji_questions" not in st.session_state:
        st.session_state.kanji_questions = []
    if "kanji_index" not in st.session_state:
        st.session_state.kanji_index = 0
    if "kanji_score" not in st.session_state:
        st.session_state.kanji_score = 0
    if "kanji_started" not in st.session_state:
        st.session_state.kanji_started = False
    if "kanji_failed_items" not in st.session_state:
        st.session_state.kanji_failed_items = []
    if "kanji_feedback" not in st.session_state:
        st.session_state.kanji_feedback = ""
    if "kanji_feedback_type" not in st.session_state:
        st.session_state.kanji_feedback_type = None

    # Start/restart quiz
    start_btn = st.button("Start / Restart Kanji Quiz", key="start_kanji_quiz")
    if start_btn:
        st.session_state.kanji_questions = random.sample(kanji_data, quiz_size)
        st.session_state.kanji_index = 0
        st.session_state.kanji_score = 0
        st.session_state.kanji_failed_items = []
        st.session_state.kanji_feedback = ""
        st.session_state.kanji_feedback_type = None
        st.session_state.kanji_started = True
        st.rerun()

    # If quiz not started
    if not st.session_state.kanji_started:
        st.info("Click **Start / Restart Kanji Quiz** to begin.")
        st.divider()
        if st.button("← Back to main menu", key="back_kanji_home"):
            reset_kanji_quiz()
            st.session_state.page = "home"
            st.rerun()
        st.stop()

    # Finish quiz
    if st.session_state.kanji_index >= len(st.session_state.kanji_questions):
        st.success(
            f"Quiz finished! Final score: {st.session_state.kanji_score}/{len(st.session_state.kanji_questions)}"
        )

        if st.session_state.kanji_failed_items:
            st.subheader("Failed items")
            for item in st.session_state.kanji_failed_items:
                question, correct_answer = get_question_and_answer(item, mode)
                st.write(f"- **{question}** → {correct_answer}")
        else:
            st.success("Perfect score! No failed items.")
        
        st.divider()
        if st.button("← Back to main menu", key="back_vocab_end"):
            reset_kanji_quiz()
            st.session_state.page = "home"
            st.rerun()
            
        st.stop()
    
        st.divider()
        if st.button("← Back to main menu", key="back_kanji_end"):
            reset_kanji_quiz()
            st.session_state.page = "home"
            st.rerun()
        return
    
    # Show feedback from previous answer
    if st.session_state.kanji_feedback:
        if st.session_state.kanji_feedback_type == "success":
            st.success(st.session_state.kanji_feedback)
        elif st.session_state.kanji_feedback_type == "error":
            st.error(st.session_state.kanji_feedback)
    
    # Current question
    current_item = st.session_state.kanji_questions[st.session_state.kanji_index]
    question, correct_answer = get_question_and_answer(current_item, mode)

    st.metric("Score", f"{st.session_state.kanji_score}/{len(st.session_state.kanji_questions)}")
    st.subheader(f"Question {st.session_state.kanji_index + 1}/{len(st.session_state.kanji_questions)}")

    with st.form("kanji_answer_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(
                f"<div style='font-size: 150px; font-weight: 100;'>{question}</div>",
                unsafe_allow_html=True
            )
        with col2:
            user_answer = st.text_input("Your answer")
        
        style.add_button_css()
        submitted = st.form_submit_button("Submit", 
                                          use_container_width=True)
    
    if submitted and normalize(user_answer) != "":
        if normalize(user_answer) in normalize(correct_answer):
            st.session_state.kanji_score += 1
            st.session_state.kanji_feedback = f"Correct! ✅ {question} → {correct_answer}"
            st.session_state.kanji_feedback_type = "success"
        else:
            st.session_state.kanji_failed_items.append(current_item)
            st.session_state.kanji_feedback = f"Wrong ❌ Correct answer: {correct_answer}"
            st.session_state.kanji_feedback_type = "error"

        st.session_state.kanji_index += 1
        st.rerun()
    
    st.divider()
    if st.button("← Back to main menu", key="back_kanji"):
        reset_kanji_quiz()
        st.session_state.page = "home"
        st.rerun()