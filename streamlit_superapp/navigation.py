from typing import List, Union
from uuid import uuid4
from streamlit import session_state as ss
import streamlit as st

import inspect
from streamlit_superapp import components
from streamlit_superapp.page_loader import PageLoader
from streamlit_superapp.typing import Page


class Navigation:
    hide_page_title = False
    hide_index_title = False
    hide_sidebar_icon = False
    hide_index_icon = False

    @staticmethod
    def initialize():
        if "reloaded" not in ss:
            ss.reloaded = True

        if "session_id" not in ss:
            ss.session_id = str(uuid4())  # TODO: GET FROM COOKIES

        ss["navigation"] = Navigation

        Navigation.go(Navigation.current_path())

        PageLoader.initialize()

        with st.sidebar:
            components.home_link()

        Navigation.render_page(Navigation.root())

        ss.reloaded = False

    @staticmethod
    def go(path: Union[str, Page]):
        if not isinstance(path, str):
            path = path.path

        previous_path = Navigation.current_path(path)

        st.session_state.page_changed = previous_path != path
        st.experimental_set_query_params(path=path)

        if previous_path != path:
            print("go:", previous_path, "->", path)

    @staticmethod
    def current_path(default="pages"):
        return st.experimental_get_query_params().get("path", [default])[0]

    @staticmethod
    def find_page(path: str):
        pages: List[Page] = ss.pages

        for page in pages:
            if page.path == path:
                return page

    @staticmethod
    def root():
        root = Navigation.find_page("pages")
        if root is None:
            not_configured()
            st.stop()
            raise Exception("Streamlit Super App not configured.")

        return root

    @staticmethod
    def render_page(page: Page):
        signature = inspect.signature(page.main).parameters

        params = {}

        if "page" in signature:
            params["page"] = page

        if "navigation" in signature:
            params["navigation"] = Navigation

        return page.main(**params)


def not_configured():
    st.write("Streamlit Super App needs to be configured.")

    st.write(
        "Please create a `pages` folder in the root directory of your Streamlit app."
    )

    st.code(
        """
        pages/
        ├─  __init__.py
        ├─  index/__init__.py
        └─  hello/__init__.py
    """
    )

    st.write("add this to")
    st.code("pages/hello/__init__.py")

    st.code(
        """
        import streamlit as st

        NAME = "Demo" # Optional
        DESCRIPTION = "Sample page to demonstrate Streamlit Super App."  # Optional
        ICON = "🌍" # Optional

        # main function is required
        def main():
            st.write("Hello World!")

    """
    )
