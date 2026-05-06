import json
import pandas as pd
import streamlit as st

def load_katakana(path="n5/data/katakana.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_display_text(item):
    kana = item.get("kana", "")
    romaji = item.get("romaji", "")
    return kana, romaji

@st.dialog("カ Katakana Reader", width="large")
def katakana_reader_modal(data):
    if "katakana_reader_index" not in st.session_state:
        st.session_state.katakana_reader_index = 0

    index = st.session_state.katakana_reader_index
    item = data[index]
    kana, romaji = get_display_text(item)

    st.markdown(
        f"<div style='font-size: 224px; font-weight: 700; text-align: center;'>{kana}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size: 96px; text-align: center; margin-top: 10px;'>{romaji}</div>",
        unsafe_allow_html=True
    )

    st.write("")
    st.markdown(
        f"<div style='text-align: center;'>{index + 1} / {len(data)}</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Previous", use_container_width=True, key="katakana_prev"):
            if st.session_state.katakana_reader_index > 0:
                st.session_state.katakana_reader_index -= 1
                st.rerun()

    with col2:
        if st.button("Close", use_container_width=True, key="katakana_close"):
            st.session_state.show_katakana_modal = False
            st.rerun()

    with col3:
        if st.button("Next ➡", use_container_width=True, key="katakana_next"):
            if st.session_state.katakana_reader_index < len(data) - 1:
                st.session_state.katakana_reader_index += 1
                st.rerun()

def render_katakana_study():
    st.title("カ Katakana")
    st.write("Browse katakana in a table or open the reader modal.")
    st.divider()

    katakana_data = load_katakana("n5/data/katakana.json")

    # Session state
    if "show_katakana_modal" not in st.session_state:
        st.session_state.show_katakana_modal = False
    if "katakana_search" not in st.session_state:
        st.session_state.katakana_search = ""
    if "hiragana_type_filter" not in st.session_state:
        st.session_state.hiragana_type_filter = "All"
    if "katakana_learned_filter" not in st.session_state:
        st.session_state.katakana_learned_filter = "All"

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        search_text = st.text_input(
            "Search",
            value=st.session_state.katakana_search,
            placeholder="Search by kana or romaji",
            key="katakana_search_input"
        )

    with col2:
        type_filter = st.selectbox(
            "Type",
            ["All", "standard katakana", "dakuten", "handakuten", "yōon combinations"]
        )

    with col3:
        learned_filter = st.selectbox(
            "Learned",
            ["All", "Learned", "Not learned"],
            index=0,
            key="katakana_learned_select"
        )

    st.session_state.katakana_search = search_text
    st.session_state.katakana_type_filter = type_filter
    st.session_state.katakana_learned_filter = learned_filter

    # Apply filters
    filtered_data = katakana_data

    if search_text.strip():
        query = search_text.strip().lower()
        filtered_data = [
            item for item in filtered_data
            if query in item.get("kana", "").lower()
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
        if st.button("Open Reader Modal", key="open_katakana_reader"):
            if filtered_data:
                st.session_state.show_katakana_modal = True
                st.session_state.katakana_reader_index = 0
                st.rerun()
            else:
                st.warning("No items available to open.")

    with col2:
        st.write("Use the table below to browse the full list.")

    if not filtered_data:
        st.warning("No katakana items match your filters.")
    else:
        df = pd.DataFrame(filtered_data)

        columns_to_show = []
        for col in ["kana", "romaji", "learned", "score"]:
            if col in df.columns:
                columns_to_show.append(col)

        df = df[columns_to_show]
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Open modal
    if st.session_state.show_katakana_modal and filtered_data:
        katakana_reader_modal(filtered_data)

    st.divider()

    # Back button at the bottom
    if st.button("← Back to main menu", key="back_katakana_browse"):
        st.session_state.page = "home"
        st.rerun()
