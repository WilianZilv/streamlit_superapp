try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Streamlit is not installed. Please install it with `pip install streamlit`."
    )

try:
    st.query_params
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
from streamlit_superapp.page_loader import PageLoader
from streamlit_superapp.state import State
from streamlit_superapp.page import Page
from streamlit_superapp.widgets import *

PageLoader.initialize()

inject = Navigation.inject


def run(
    hide_index_description: bool = False,
    hide_home_button: bool = False,
    hide_back_button: bool = False,
    hide_page_title: bool = False,
    hide_breadcrumbs: bool = False,
    use_query_params: bool = True,
):
    Navigation.hide_index_description = hide_index_description
    Navigation.hide_home_button = hide_home_button
    Navigation.hide_back_button = hide_back_button
    Navigation.hide_page_title = hide_page_title
    Navigation.hide_breadcrumbs = hide_breadcrumbs
    Navigation.use_query_params = use_query_params

    Navigation.initialize()
