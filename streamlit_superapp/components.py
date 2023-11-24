import streamlit as st
from streamlit import session_state as ss
from streamlit_superapp.state import State

from streamlit_superapp.typing import Navigation, Page


import os
from typing import List, Literal
import streamlit.components.v1 as components


def small_link(path: str, name: str, use_container_width=False):
    if st.button(
        name, key="link:" + path + ":" + name, use_container_width=use_container_width
    ):
        ss["navigation"].go(path)


def go_home_link():
    navigation: Navigation = ss["navigation"]

    root = navigation.root()

    small_link(
        path=root.path,
        name="🏠 Home",
        use_container_width=True,
    )


def go_back_link():
    navigation: Navigation = ss["navigation"]

    small_link(
        path=navigation.previous_path(), name="← Go back", use_container_width=True
    )


def sidebar(page: Page, variant: Literal["selectbox", "radio"] = "radio", label=None):
    parent = page.parent

    if not parent:
        return

    pages = parent.children

    if len(pages) == 1:
        return

    text = [page.icon + " " + page.name for page in pages]
    paths = [page.path for page in pages]

    index = paths.index(page.path)

    def format_func(path: str):
        return text[paths.index(path)]

    value = None

    state = State("page_index", default_value=index, key=parent)

    if state.initial_value != index:
        state.initial_value = index

    label = label or parent.name

    if variant == "selectbox":
        value = st.sidebar.selectbox(
            label,
            index=state.initial_value,
            options=paths,
            format_func=format_func,
            key=state.key + ":selectbox",
        )

    if variant == "radio":
        value = st.sidebar.radio(
            label,
            index=state.initial_value,
            options=paths,
            format_func=format_func,
            key=state.key + ":radio",
        )

    if value is None:
        return

    if value != page.path:
        state.initial_value = paths.index(value)
        navigation: Navigation = ss["navigation"]
        navigation.go(value)


def search(page):
    sidebar(page, variant="selectbox", label="Search")


_RELEASE = True


def declare_component(name: str):
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    if not _RELEASE:
        with open(os.path.join(parent_dir, "web", name, ".env"), "r") as f:
            _env = f.readlines()
            port = [line for line in _env if line.startswith("PORT=")][0].split("=")[1]

        return components.declare_component(
            name,
            url=f"http://localhost:{port}",
        )

    build_dir = os.path.join(parent_dir, f"web/{name}/build")
    return components.declare_component(name, path=build_dir)


def page_index(pages: List[Page], key=None):
    _component_func = declare_component("page_index")

    _pages = [page.serializable_dict() for page in pages]
    return _component_func(pages=_pages, key=key)


def breadcrumbs(current_path: str):
    _component_func = declare_component("breadcrumbs")

    navigation: Navigation = ss["navigation"]

    current_path = navigation.current_path()

    current_page = navigation.find_page(current_path)

    if current_page is None:
        return

    ancestors = []

    while True:
        if current_page is None:
            break

        ancestors = [current_page, *ancestors]

        current_page = current_page.parent

    pages = [page.serializable_dict() for page in ancestors]

    k = "navigation:breadcrumbs:path"

    previous_value = ss.get(k, None)

    next_value = _component_func(pages=pages, current_path=current_path, default=None)

    ss[k] = next_value

    if previous_value == next_value:
        return

    if next_value is not None:
        navigation.go(next_value)
        st.rerun()
