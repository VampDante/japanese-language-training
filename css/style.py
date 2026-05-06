import streamlit as st

def add_button_css():
    st.markdown(
        """
        <style>
        div[data-testid="stFormSubmitButton"] button {
            background-color: #1f77b4;
            color: white;
            border: none;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background-color: #155a8a;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def start_button_css():
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            background-color: #1f77b4;
            color: white;
            border: none;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #155a8a;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
