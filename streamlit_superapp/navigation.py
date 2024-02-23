from typing import Callable, List, Optional, Union, cast
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
    hide_breadcrumbs = False
    use_query_params = True

    @staticmethod
    def initialize():
        if "session_id" not in ss:
            ss.session_id = "global_session"

        ss["navigation"] = Navigation

        PageLoader.initialize()

        path = Navigation.current_path()

        page = Navigation.find_page(path)

        if page is None:
            page = Navigation.root()
            path = page.path

        if page.index is not None:
            if not page.index:
                children = page.children
                if len(children):
                    page = children[0]
                    path = page.path

        result = handle_redirect(page)

        if isinstance(result, tuple):
            page, path = result

            if page is None:
                not_found(path)
                st.stop()
                raise Exception("Streamlit Super App not configured.")

        if page.access is not None:
            params = Navigation.discover_params(page.access, page)
            if not page.access(**params):
                page = Navigation.root()
                path = page.path

        if page.access is None:
            guard_page = page.parent

            while True:
                if guard_page is None:
                    break

                if guard_page.access is not None:
                    params = Navigation.discover_params(guard_page.access, guard_page)
                    if not guard_page.access(**params):
                        page = Navigation.root()
                        path = page.path

                    break
                guard_page = guard_page.parent

        Navigation.go(path)

        parent = page.parent

        if parent is not None:
            with st.sidebar:
                if not Navigation.hide_home_button or not Navigation.hide_back_button:
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

        if not Navigation.hide_breadcrumbs:
            components.breadcrumbs(Navigation.current_path())

        if "do_rerun" not in ss:
            ss.do_rerun = False

        if not ss.do_rerun:
            Navigation.render_page(page)

        if ss.do_rerun:
            ss.do_rerun = False
            st.rerun()

    @staticmethod
    def pages(verify_access=True) -> List["Page"]:
        pages: List[Page] = ss.pages

        if not verify_access:
            return pages

        _pages: List[Page] = []

        for page in pages:
            if page.access is True:
                continue

            if callable(page.access):
                params = Navigation.discover_params(page.access, page)

                if not page.access(**params):
                    continue

            _pages.append(page)

        return _pages

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
        page = cast(Page, path)

        if isinstance(path, str):
            page = Navigation.find_page(path)
            if page is None:
                page = Navigation.root()

        if not isinstance(path, str):
            path = path.path

        previous_path = Navigation.current_path(path)

        ss["navigation:previous_path"] = previous_path

        page_changed = previous_path != path

        if Navigation.use_query_params:
            st.query_params['path'] = path
        else:
            path_state = State("navigation:path", default_value=path)
            path_state.initial_value = path

        page_state = State("navigation:current_page", default_value=page)
        page_state.initial_value = page

        if page_changed:
            State.save_all()
            # print("go:", previous_path, "->", path)
            ss["do_rerun"] = True

    @staticmethod
    def current_path(default: str = PageLoader.root):
        if Navigation.use_query_params:
            return st.query_params.get("path", default)

        path_state = State("navigation:path", default_value=default)

        return path_state.initial_value

    @staticmethod
    def current_page():
        page_state = State[Page]("navigation:current_page", default_value=None)

        return page_state.initial_value

    @staticmethod
    def find_page(path: str):
        if "pages" not in ss:
            PageLoader.initialize()

        pages = Navigation.pages(verify_access=False)

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
    def inject(**kwargs):
        if "page" in kwargs or "navigation" in kwargs:
            raise Exception("Cannot inject 'page' or 'navigation'.")

        previous = ss.get("navigation:inject", None)

        ss["navigation:inject"] = kwargs

        if previous != kwargs:
            st.rerun()

    @staticmethod
    def discover_params(func: Callable, page: Page):
        signature = inspect.signature(func).parameters

        params = {}

        if "page" in signature:
            params["page"] = page

        if "navigation" in signature:
            params["navigation"] = Navigation

        if "navigation:inject" in ss:
            for key, value in ss["navigation:inject"].items():
                if key in signature:
                    params[key] = value

        for key, value in signature.items():
            if key not in params:
                params[key] = None

        return params

    @staticmethod
    def render_page(page: Page):
        params = Navigation.discover_params(page.main, page)

        if not Navigation.hide_page_title:
            st.header(page.icon + " " + page.name)

        return page.main(**params)


def handle_redirect(page: Page):
    if page.redirect is None:
        return

    if isinstance(page.redirect, tuple):
        func, path = page.redirect

        params = Navigation.discover_params(func, page)
        valid = func(**params)

        if valid:
            return Navigation.find_page(path), path

    func = page.redirect

    if callable(func):
        params = Navigation.discover_params(func, page)
        path = func(**params)

        if isinstance(path, str):
            return Navigation.find_page(path), path


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


def not_found(path: str):
    st.write("Page not found.")

    st.write(f"Path: `{path}`")
