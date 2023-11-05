from typing import List
import streamlit as st
from streamlit import session_state as ss

from streamlit_superapp import components
from streamlit_superapp.state import State
from streamlit_superapp.typing import Navigation, Page


class Sidebar:
    variants = {
        "radio": st.radio,
        "select_box": st.selectbox,
    }

    @staticmethod
    def main(page: Page):
        navigation: Navigation = ss["navigation"]

        if page.variant is None:
            raise Exception(f"Expected variant for {page.path}")

        target_path = navigation.current_path()

        children = page.children

        if not len(children):
            navigation.go(page.path)
            components.go_back_link(page)
            return Sidebar.empty_page(page)

        gallery = []
        others = []

        for child in children:
            if child.variant == "index":
                gallery.append(child)
            else:
                others.append(child)

        children = gallery + others

        index = 0

        if page.path != target_path:
            selected_path = target_path.split(page.path)[-1].split(".")[1]
            selected_path = ".".join([page.path, selected_path])

            index = Sidebar.get_page_index(selected_path, children)

        state = State("index", default_value=index, key=page, cache=False)

        with st.sidebar:
            label_visibility = "visible" if page.parent is not None else "collapsed"

            format_func = (
                str
                if navigation.hide_sidebar_icon
                else lambda page: page.icon + " " + page.name
            )

            child: Page = Sidebar.variants[page.variant](
                page.name,
                children,
                index=state.initial_value,
                key=state.key,
                label_visibility=label_visibility,
                format_func=format_func,
            )

        current_index = Sidebar.get_page_index(child.path, children)

        previous_index = state.bind(current_index)

        if previous_index != current_index or not child.variant:
            navigation.go(child.path)

        if child.variant == "index" or child.variant is None:
            components.go_back_link(child)

        if child.variant is None and not navigation.hide_page_title:
            st.header(child.name)

        navigation.render_page(child)

    @staticmethod
    def empty_page(page: Page):
        st.header(page.name)

        st.write(page.path)
        st.write("No content yet")

    @staticmethod
    def get_page_index(path, pages: List[Page]):
        for i, x in enumerate(pages):
            if x.path == path:
                return i
        return 0
