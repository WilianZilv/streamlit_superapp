from typing import List, Optional
from streamlit_superapp.typing import Navigation, Page
import streamlit_superapp.components as components
import streamlit as st
from streamlit import session_state as ss


class Index:
    CONTAINER = (
        """<div style="display: flex; flex-wrap: wrap; gap: 8px;">{item}</div>"""
    )

    TAG_SORT_PATTERN = r"\{([^}]+):\}"

    @staticmethod
    def main(page: Page):
        navigation: Navigation = ss["navigation"]

        pages = page.neighbors

        if not navigation.hide_index_title:
            parent = page.parent
            if parent is not None:
                st.header(parent.icon + " " + parent.name)

        Index.render_gallery(pages)

    @staticmethod
    def render_gallery(pages: List[Page], split=True):
        if not split:
            return Index.render_pages(pages, None)

        tags = set([page.tag for page in pages])

        import re

        def key(tag):
            if not tag:
                tag = "{ZZZ:}"

            match = re.search(Index.TAG_SORT_PATTERN, tag)
            if match is None:
                return tag

            return match.group(1)

        tags = sorted(tags, key=key)

        def resolve_tag(tag: Optional[str]):
            if tag is None:
                return None

            match = re.search(Index.TAG_SORT_PATTERN, tag)
            if match is None:
                return tag

            return tag.replace(match.group(0), "")

        groups = {
            resolve_tag(tag): [page for page in pages if page.tag == tag]
            for tag in tags
        }

        untagged = "🏷️ Untagged" if len(tags) > 1 else None

        [Index.render_pages(pages, tag or untagged) for tag, pages in groups.items()]

    @staticmethod
    def render_pages(pages: List[Page], header):
        items = []

        for child in pages:
            if child.is_active:
                continue

            description = ""

            if child.description:
                description = "<br>".join(child.description.split("\n"))

            navigation: Navigation = ss["navigation"]

            name = (
                (child.name)
                if navigation.hide_index_icon
                else (child.icon + " " + child.name)
            )

            item = components.card_link(
                path=child.path,
                name=name,
                description=description or "",
                render=False,
            )

            items.append(item)

        if header is not None:
            st.text(header)

        container = Index.CONTAINER.format(item="".join(items))
        st.markdown(container, unsafe_allow_html=True)
        st.write("\n")
