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


def run(hide_index_description: bool = False, hide_home_button: bool = False):
    Navigation.hide_index_description = hide_index_description
    Navigation.hide_home_button = hide_home_button

    Navigation.initialize()
