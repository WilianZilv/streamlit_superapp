from typing import List, Union
from uuid import uuid4
from streamlit import session_state as ss
import streamlit as st

import inspect
from streamlit_superapp import components
from streamlit_superapp.page_loader import PageLoader
from streamlit_superapp.state import State
from streamlit_superapp.typing import Page


class Navigation:
    hide_page_title = False
    hide_home_button = False
    hide_back_button = False
    hide_index_description = False

    @staticmethod
    def initialize():
        if "reloaded" not in ss:
            ss.reloaded = True

        if "session_id" not in ss:
            ss.session_id = str(uuid4())  # TODO: GET FROM COOKIES

        ss["navigation"] = Navigation

        PageLoader.initialize()

        path = Navigation.current_path()

        page = Navigation.find_page(path)

        if page is None:
            return

        if page.index is not None:
            if not page.index:
                children = page.children
                if len(children):
                    page = children[0]
                    path = page.path

        Navigation.go(path)

        parent = page.parent

        if parent is not None:
            with st.sidebar:
                c1, c2 = st.columns(2)

                if not Navigation.hide_home_button:
                    with c1:
                        components.go_home_link()

                if not Navigation.hide_back_button:
                    with c2:
                        components.go_back_link()

            if parent.search:
                components.search(page)

            if parent.sidebar is not None:
                components.sidebar(page, variant=parent.sidebar)

        if not ss.get("page_changed", False):
            Navigation.render_page(page)

        ss.reloaded = False

        rerun = ss.get("do_rerun", False)

        if rerun:
            ss["do_rerun"] = False
            st.rerun()

    @staticmethod
    def previous_path(path: Optional[str] = None):
        current_path = path
        if current_path is None:
            current_path = Navigation.current_path()

        if "." not in current_path:
            return current_path

        tree = current_path.split(".")
        path = ".".join(tree[:-1])

        page = Navigation.find_page(path)

        if page is None:
            return current_path

        if page.index is not None:
            if not page.index:
                return Navigation.previous_path(page.path)

        return path

    @staticmethod
    def go(path: Union[str, Page]):
        if not isinstance(path, str):
            path = path.path

        previous_path = Navigation.current_path(path)
        page_changed = previous_path != path

        st.session_state.page_changed = page_changed
        st.experimental_set_query_params(path=path)
        if page_changed:
            State.save_all()
            # print("go:", previous_path, "->", path)
            ss["do_rerun"] = True

    @staticmethod
    def current_path(default: str = PageLoader.root):
        return st.experimental_get_query_params().get("path", [default])[0]

    @staticmethod
    def find_page(path: str):
        if "pages" not in ss:
            PageLoader.initialize()

        pages: List[Page] = ss.pages

        for page in pages:
            if page.path == path:
                return page

    @staticmethod
    def root():
        root = Navigation.find_page(PageLoader.root)
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

        if not Navigation.hide_page_title:
            st.header(page.icon + " " + page.name)

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
