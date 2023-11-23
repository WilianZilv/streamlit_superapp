from typing import Literal, Optional, Union
import streamlit as st
from streamlit_superapp.navigation import Navigation

from streamlit_superapp.state import State
from streamlit.type_util import Key, LabelVisibility
from streamlit.runtime.state.common import WidgetCallback, WidgetArgs, WidgetKwargs

from streamlit_superapp.typing import Page


def experimental_text_input(
    label: str,
    value: str = "",
    max_chars: Optional[int] = None,
    key: Optional[Union[Page, str]] = None,
    type: Literal["default", "password"] = "default",
    help: Optional[str] = None,
    autocomplete: Optional[str] = None,
    on_change: Optional[WidgetCallback] = None,
    args: Optional[WidgetArgs] = None,
    kwargs: Optional[WidgetKwargs] = None,
    *,
    placeholder: Optional[str] = None,
    disabled: bool = False,
    label_visibility: LabelVisibility = "visible",
    private: Union[bool, Page] = True,
):
    key = key or label

    page = private or None

    if page is True:
        page = Navigation.current_page()

    state = State(f"widget:text_input:{key}", default_value=value, key=page)

    state.bind(
        st.text_input(
            label,
            value=state.initial_value,
            max_chars=max_chars,
            key=state.key,
            type=type,
            help=help,
            autocomplete=autocomplete,
            on_change=on_change,
            args=args,
            kwargs=kwargs,
            placeholder=placeholder,
            disabled=disabled,
            label_visibility=label_visibility,
        )
    )

    return state


__all__ = ["experimental_text_input"]
