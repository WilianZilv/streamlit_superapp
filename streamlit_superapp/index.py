from streamlit_superapp.components import page_index
from streamlit_superapp.typing import Navigation, Page
import streamlit as st
from streamlit import session_state as ss


class Index:
    @staticmethod
    def main(page: Page):
        navigation: Navigation = ss["navigation"]

        pages = page.children

        if page.description and not navigation.hide_index_description:
            st.write(page.description)

        path = page_index(pages)

        if path is not None:
            navigation.go(path)
