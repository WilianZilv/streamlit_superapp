import streamlit as st
from streamlit import session_state as ss

from streamlit_superapp.typing import Navigation, Page


CARD = """<div style="display: flex; min-width: 250px; max-width: 300px;">
<a style="all: unset; display: block; flex: 1; font-size: 1.2rem; color: white !important; cursor: pointer; padding: 16px; border-radius: 8px; background-color: rgb(26, 28, 36);" href="?path={path}&session_id={session_id}" target="_self">{name}<br>
<span style="font-size: 1rem; font-weight: 200; color: rgb(218, 218, 218);">{description}</span></a></div>"""

SMALL = """<div style="display: flex; padding-bottom: 8px;">
<a style="all: unset; display: block; font-size: 1.2rem; color: white !important; cursor: pointer;" href="?path={path}&session_id={session_id}" target="_self">{name}<br>
</a></div>"""


def card_link(path: str, name: str, description: str, render=True):
    item = CARD.format(
        path=path, session_id=ss.session_id, name=name, description=description
    )
    if not render:
        return item
    st.markdown(item, unsafe_allow_html=True)


def small_link(path: str, name: str):
    item = SMALL.format(path=path, session_id=ss.session_id, name=name)
    st.markdown(item, unsafe_allow_html=True)


def home_link():
    navigation: Navigation = ss["navigation"]

    if navigation.current_path() in ["pages", "pages.index"]:
        return

    root = navigation.root()

    small_link(
        path=root.path,
        name="🏠 " + root.name,
    )


def go_back_link(page: Page):
    gallery = page.nearest_gallery

    if gallery is None:
        return home_link()

    small_link(path=gallery.path, name="← Go back")
