import json
import pandas as pd
import streamlit as st


def load_kanji(path="n5/data/kanji_n5.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_display_text(item):
    kanji = item.get("kanji", "")
    greek = item.get("greek", "")
    romaji = item.get("romaji", "")
    return kanji, greek, romaji


@st.dialog("🈶 Kanji Reader", width="large")
def kanji_reader_modal(data):
    if "kanji_reader_index" not in st.session_state:
        st.session_state.kanji_reader_index = 0

    index = st.session_state.kanji_reader_index
    item = data[index]
    kanji, greek, romaji = get_display_text(item)

    st.markdown(
        f"<div style='font-size: 224px; font-weight: 700; text-align: center;'>{kanji}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size: 96px; text-align: center; margin-top: 10px;'>{greek}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size: 48px; text-align: center; margin-top: 10px; color: gray;'>{romaji}</div>",
        unsafe_allow_html=True
    )

    st.write("")
    st.markdown(
        f"<div style='text-align: center;'>{index + 1} / {len(data)}</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Previous", use_container_width=True, key="kanji_prev"):
            if st.session_state.kanji_reader_index > 0:
                st.session_state.kanji_reader_index -= 1
                st.rerun()

    with col2:
        if st.button("Close", use_container_width=True, key="kanji_close"):
            st.session_state.show_kanji_modal = False
            st.rerun()

    with col3:
        if st.button("Next ➡", use_container_width=True, key="kanji_next"):
            if st.session_state.kanji_reader_index < len(data) - 1:
                st.session_state.kanji_reader_index += 1
                st.rerun()


def render_kanji_study():
    st.title("🈶 Kanji N5")
    st.write("Browse kanji in a table or open the reader modal.")
    st.divider()

    kanji_data = load_kanji("n5/data/kanji_n5.json")

    # Session state
    if "show_kanji_modal" not in st.session_state:
        st.session_state.show_kanji_modal = False
    if "kanji_search" not in st.session_state:
        st.session_state.kanji_search = ""
    if "kanji_learned_filter" not in st.session_state:
        st.session_state.kanji_learned_filter = "All"

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        search_text = st.text_input(
            "Search",
            value=st.session_state.kanji_search,
            placeholder="Search by kanji, Greek, or romaji",
            key="kanji_search_input"
        )

    with col2:
        learned_filter = st.selectbox(
            "Learned",
            ["All", "Learned", "Not learned"],
            index=0,
            key="kanji_learned_select"
        )

    st.session_state.kanji_search = search_text
    st.session_state.kanji_learned_filter = learned_filter

    # Apply filters
    filtered_data = kanji_data

    if search_text.strip():
        query = search_text.strip().lower()
        filtered_data = [
            item for item in filtered_data
            if query in item.get("kanji", "").lower()
            or query in item.get("greek", "").lower()
            or query in item.get("romaji", "").lower()
            or query in item.get("kana", "").lower()
        ]

    if learned_filter == "Learned":
        filtered_data = [item for item in filtered_data if item.get("learned") is True]
    elif learned_filter == "Not learned":
        filtered_data = [item for item in filtered_data if item.get("learned") is False]

    st.write(f"**Results:** {len(filtered_data)} item(s) found")

    # Button above table
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Open Reader Modal", key="open_kanji_reader"):
            if filtered_data:
                st.session_state.show_kanji_modal = True
                st.session_state.kanji_reader_index = 0
                st.rerun()
            else:
                st.warning("No items available to open.")

    with col2:
        st.write("Use the table below to browse the full list.")

    if not filtered_data:
        st.warning("No kanji items match your filters.")
    else:
        # Create a clean dataframe
        df = pd.DataFrame(filtered_data)

        # Ensure useful columns exist
        columns_to_show = []
        for col in ["kanji", "kana", "romaji", "greek", "learned", "score"]:
            if col in df.columns:
                columns_to_show.append(col)

        df = df[columns_to_show]

        # Pretty display
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Open modal
    if st.session_state.show_kanji_modal and filtered_data:
        kanji_reader_modal(filtered_data)

    st.divider()

    # Back button at the bottom
    if st.button("← Back to main menu", key="back_kanji_browse"):
        st.session_state.page = "home"
        st.rerun()
