try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Streamlit is not installed. Please install it with `pip install streamlit`."
    )

try:
    st.experimental_get_query_params
except AttributeError:
    raise AttributeError(
        "Streamlit version is too old. Please upgrade it with `pip install streamlit --upgrade`."
    )

try:
    st.session_state
except AttributeError:
    raise AttributeError(
        "Streamlit version is too old. Please upgrade it with `pip install streamlit --upgrade`."
    )


from streamlit_superapp.navigation import Navigation
from streamlit_superapp.state import State
from streamlit_superapp.page import Page


def run(
    hide_page_title=False,
    hide_index_title=False,
    hide_sidebar_icon=False,
    hide_index_icon=False,
):
    Navigation.hide_page_title = hide_page_title
    Navigation.hide_index_title = hide_index_title
    Navigation.hide_sidebar_icon = hide_sidebar_icon
    Navigation.hide_index_icon = hide_index_icon
    Navigation.initialize()
