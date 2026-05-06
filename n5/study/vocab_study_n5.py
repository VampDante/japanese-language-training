import json
import pandas as pd
import streamlit as st

def load_vocab(path="n5/data/vocab_n5.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_display_text(item):
    word = item.get("kana", "") or item.get("kanji", "")
    meaning = item.get("greek", "")
    return word, meaning

@st.dialog("📘 Vocabulary Reader", width="large")
def vocab_reader_modal(data):
    if "vocab_reader_index" not in st.session_state:
        st.session_state.vocab_reader_index = 0

    index = st.session_state.vocab_reader_index
    item = data[index]
    word, meaning = get_display_text(item)

    st.markdown(
        f"<div style='font-size: 224px; font-weight: 700; text-align: center;'>{word}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size: 96px; text-align: center; margin-top: 10px;'>{meaning}</div>",
        unsafe_allow_html=True
    )

    st.write("")
    st.markdown(
        f"<div style='text-align: center;'>{index + 1} / {len(data)}</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅ Previous", use_container_width=True, key="vocab_prev"):
            if st.session_state.vocab_reader_index > 0:
                st.session_state.vocab_reader_index -= 1
                st.rerun()

    with col2:
        if st.button("Close", use_container_width=True, key="vocab_close"):
            st.session_state.show_vocab_modal = False
            st.rerun()

    with col3:
        if st.button("Next ➡", use_container_width=True, key="vocab_next"):
            if st.session_state.vocab_reader_index < len(data) - 1:
                st.session_state.vocab_reader_index += 1
                st.rerun()

def render_vocab_study():
    st.title("📘 Vocabulary N5")
    st.write("Browse vocabulary in a table or open the reader modal.")
    st.divider()

    vocab = load_vocab("n5/data/vocab_n5.json")

    # Session state
    if "show_vocab_modal" not in st.session_state:
        st.session_state.show_vocab_modal = False
    if "vocab_search" not in st.session_state:
        st.session_state.vocab_search = ""
    if "vocab_type_filter" not in st.session_state:
        st.session_state.vocab_type_filter = "All"
    if "vocab_learned_filter" not in st.session_state:
        st.session_state.vocab_learned_filter = "All"
    
    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        search_text = st.text_input(
            "Search",
            value=st.session_state.vocab_search,
            placeholder="Search by Greek, kana, romaji",
            key="vocab_search_input"
        )

    with col2:
        type_filter = st.selectbox(
            "Type",
            ["All", "noun", "verb", "adjective", "adverb", "particle", "other"],
            index=0,
            key="vocab_type_select"
        )

    with col3:
        learned_filter = st.selectbox(
            "Learned",
            ["All", "Learned", "Not learned"],
            index=0,
            key="vocab_learned_select"
        )

    st.session_state.vocab_search = search_text
    st.session_state.vocab_type_filter = type_filter
    st.session_state.vocab_learned_filter = learned_filter

    # Apply filters
    filtered_data = vocab

    if search_text.strip():
        query = search_text.strip().lower()
        filtered_data = [
            item for item in filtered_data
            if query in item.get("greek", "").lower()
            or query in item.get("kana", "").lower()
            or query in item.get("romaji", "").lower()
        ]

    if type_filter != "All":
        filtered_data = [
            item for item in filtered_data
            if item.get("type", "").lower() == type_filter.lower()
        ]

    if learned_filter == "Learned":
        filtered_data = [item for item in filtered_data if item.get("learned") is True]
    elif learned_filter == "Not learned":
        filtered_data = [item for item in filtered_data if item.get("learned") is False]

    st.write(f"**Results:** {len(filtered_data)} item(s) found")

    # Button above table
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Open Reader Modal", key="open_vocab_reader"):
            if filtered_data:
                st.session_state.show_vocab_modal = True
                st.session_state.vocab_reader_index = 0
                st.rerun()
            else:
                st.warning("No items available to open.")   

    with col2:
        st.write("Use the table below to browse the full list.")

    if not filtered_data:
        st.warning("No vocabulary items match your filters.")

    else:
        # Create a clean dataframe
        df = pd.DataFrame(filtered_data)

        # Ensure useful columns exist
        columns_to_show = []
        for col in ["kana", "romaji", "greek", "type", "learned", "score"]:
            if col in df.columns:
                columns_to_show.append(col)

        df = df[columns_to_show]

        # Pretty display
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Open modal
    if st.session_state.show_vocab_modal and filtered_data:
        vocab_reader_modal(filtered_data)

    st.divider()

    # Back button at the bottom
    if st.button("← Back to main menu", key="back_vocab_browse"):
        st.session_state.page = "home"
        st.rerun()