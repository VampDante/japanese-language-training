import json
import random
import css.style as style
import streamlit as st

# Helpers
def load_vocab(path="n5/data/vocab_n5.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return text.strip().lower()

def get_question_and_answer(item, mode):
    if mode == "Greek → Romaji":
        return item["greek"], item["romaji"]
    elif mode == "Romaji → Greek":
        return item["romaji"], item["greek"]
    else:
        return item["greek"], item["romaji"]

def filter_items(data, type_filter):
    if type_filter == "Verbs only":
        return [item for item in data if item.get("type") == "verb"]
    elif type_filter == "Nouns only":
        return [item for item in data if item.get("type") == "noun"]
    elif type_filter == "Adjectives only":
        return [item for item in data if item.get("type") == "adjective"]
    elif type_filter == "Other":
        return [item for item in data if item.get("type") == "other"]
    return data

def reset_vocab_quiz():
    keys_to_reset = [
        "vocab_questions",
        "vocab_index",
        "vocab_score",
        "vocab_started",
        "vocab_failed_items",
        "vocab_feedback",
        "vocab_feedback_type",
        "vocab_mode",
        "vocab_quiz_size"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def render_vocab_quiz():
    st.title("📘 Vocabulary N5 Quiz")
    st.divider()

    # Application
    st.set_page_config(
        page_title="Japanese N5 Quiz", 
        page_icon="🇯🇵", 
        layout="centered")

    st.write("Practice your N5 vocabulary with Greek and Romaji.")

    vocab = load_vocab("n5/data/vocab_n5.json")

    # Quiz settings
    st.sidebar.header("Quiz Settings")
    mode = st.sidebar.radio(
        "Quiz direction", 
        ["Greek → Romaji", "Romaji → Greek"],
        key="vocab_mode"
    )
    
    type_filter = st.sidebar.radio(
        "Type",
        ["All", "Verbs only", "Nouns only", "Adjectives only", "Other"],
        index=0
    )
    filtered_vocab = filter_items(vocab, type_filter)

    if not filtered_vocab:
        st.warning("No items available for the selected filter.")
        st.stop()

    quiz_size = st.sidebar.slider(
        "Number of questions",
        1, 
        len(filtered_vocab),
        min(5, len(filtered_vocab)) if len(filtered_vocab) > 0 else 1,
        key="vocab_quiz_size")
    
    # Session state
    if "vocab_questions" not in st.session_state:
        st.session_state.vocab_questions = []
    if "vocab_index" not in st.session_state:
        st.session_state.vocab_index = 0
    if "vocab_score" not in st.session_state:
        st.session_state.vocab_score = 0
    if "vocab_started" not in st.session_state:
        st.session_state.vocab_started = False
    if "vocab_failed_items" not in st.session_state:
        st.session_state.vocab_failed_items = []
    if "vocab_feedback" not in st.session_state:
        st.session_state.vocab_feedback = ""
    if "vocab_feedback_type" not in st.session_state:
        st.session_state.vocab_feedback_type = None

    # Start/restart quiz
    start_btn=st.button("Start / Restart Quiz", key="start_restart_button")
    if start_btn:
        st.session_state.vocab_questions = random.sample(
            filtered_vocab, 
            min(quiz_size, len(filtered_vocab)))
        st.session_state.vocab_index = 0
        st.session_state.vocab_score = 0
        st.session_state.vocab_failed_items = []
        st.session_state.vocab_feedback = ""
        st.session_state.vocab_feedback_type = None
        st.session_state.vocab_started = True
        st.rerun()

    # If quiz not started
    if not st.session_state.vocab_started:
        st.info("Click **Start / Restart Quiz** to begin.")
        st.divider()
        if st.button("← Back to main menu", key="back_kanji_home"):
            reset_vocab_quiz()
            st.session_state.page = "home"
            st.rerun()
        st.stop()

    # Finish quiz
    if st.session_state.vocab_index >= len(st.session_state.vocab_questions):
        st.success(f"Quiz finished! Final score: {st.session_state.vocab_score}/{len(st.session_state.vocab_questions)}")

        if st.session_state.vocab_failed_items:
            st.subheader("Failed items")
            for item in st.session_state.vocab_failed_items:
                question, correct_answer = get_question_and_answer(item, mode)
                st.write(f"- **{question}** → {correct_answer}")
        else:
            st.success("Perfect score! No failed items.")

        st.divider()
        if st.button("← Back to main menu", key="back_vocab_end"):
            reset_vocab_quiz()
            st.session_state.page = "home"
            st.rerun()

        st.stop()

        st.divider()
        if st.button("← Back to main menu", key="back_vocab_end"):
            reset_vocab_quiz()
            st.session_state.page = "home"
            st.rerun()
        return

    # Show feedback from previous submission
    if st.session_state.vocab_feedback:
        if st.session_state.vocab_feedback_type == "success":
            st.success(st.session_state.vocab_feedback)
        elif st.session_state.vocab_feedback_type == "error":
            st.error(st.session_state.vocab_feedback)

    # Current question
    current_item = st.session_state.vocab_questions[st.session_state.vocab_index]
    question, correct_answer = get_question_and_answer(current_item, mode)

    st.metric("Score", f"{st.session_state.vocab_score}/{len(st.session_state.vocab_questions)}")
    st.subheader(f"Question {st.session_state.vocab_index + 1}/{len(st.session_state.vocab_questions)}")
    

    with st.form("vocab_answer_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 1])

        with col1:
            with col1:
                st.markdown(
                    f"<div style='font-size: 50px; font-weight: 100;'>{question}</div>",
                    unsafe_allow_html=True
                )

        with col2:
            user_answer = st.text_input("Your answer", )
        
        style.add_button_css()
        submitted = st.form_submit_button("Submit", 
                                          use_container_width=True)

    if submitted and normalize(user_answer) != "":
        if normalize(user_answer) == normalize(correct_answer):
            st.success("Correct!")
            st.session_state.vocab_score += 1
            st.session_state.vocab_feedback = f"Correct! ✅ {question} → {correct_answer}"
            st.session_state.vocab_feedback_type = "success"
        else:
            st.error(f"Wrong. Correct answer: **{correct_answer}**")
            st.session_state.vocab_failed_items.append(current_item)
            st.session_state.vocab_feedback = f"Wrong ❌ Correct answer: {correct_answer}"
            st.session_state.vocab_feedback_type = "error"

        st.session_state.vocab_index += 1
        st.rerun()

    st.divider()
    if st.button("← Back to main menu", key="back_vocab_quiz"):
        reset_vocab_quiz()
        st.session_state.page = "home"
        st.rerun()