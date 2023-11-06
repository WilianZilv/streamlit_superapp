import streamlit as st
from streamlit import session_state as ss

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

    label = label or parent.name

    if variant == "selectbox":
        value = st.sidebar.selectbox(
            label, index=index, options=paths, format_func=format_func
        )

    if variant == "radio":
        value = st.sidebar.radio(
            label, index=index, options=paths, format_func=format_func
        )

    if value is None:
        return

    if value != page.path:
        navigation: Navigation = ss["navigation"]
        navigation.go(value)


_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        "page_index",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("page_index", path=build_dir)


def page_index(pages: List[Page], key=None):
    _pages = [page.serializable_dict() for page in pages]
    return _component_func(pages=_pages, key=key)
