import glob
from importlib import import_module
import os
import sys
from typing import List
from streamlit_superapp.index import Index
from streamlit_superapp.sidebar import Sidebar


from streamlit_superapp.page import Page
from streamlit_superapp.typing import available_variants
from streamlit import session_state as ss


class PageLoader:
    @staticmethod
    def initialize():
        paths = glob.glob("./pages/**/*.py", recursive=True)

        pages: List[Page] = []

        if "page_loader" not in ss:
            ss.page_loader = {}

        for path in paths:
            module_path = path[2:].replace(os.path.sep, ".").replace(".py", "")

            page_path = module_path.split(".")

            is__init__file = page_path[-1] == "__init__"

            if is__init__file:
                page_path = page_path[:-1]

            file_name = page_path[-1]
            page_path = ".".join(page_path)

            file_mtime = os.path.getmtime(path)
            last_mtime = ss.page_loader.get(page_path, 0)

            ss.page_loader[page_path] = file_mtime

            if module_path in sys.modules and file_mtime != last_mtime:
                del sys.modules[module_path]

            module = import_module(module_path)

            main = get_module_attr(module, "main")
            name = get_module_attr(module, "NAME", None)
            description = get_module_attr(module, "DESCRIPTION", None)
            variant = get_module_attr(module, "NAV", None)
            tag = get_module_attr(module, "TAG", None)
            icon = get_module_attr(module, "ICON", None)
            order = get_module_attr(module, "ORDER", None)

            if isinstance(order, int):
                order = str(order)

            if file_name == "index":
                variant = file_name
                main = Index.main
                name = name or "About"
                icon = icon or "📖"

            if main is None and (is__init__file or name):
                variant = variant or "select_box"
                main = Sidebar.main

            if variant is not None and variant not in available_variants:
                raise Exception(
                    f"Invalid variant {variant} for {page_path}. Expected one of {available_variants}"
                )

            if main is None:
                continue

            file_name_normalized = file_name.replace("_", " ").title()

            page = Page(
                path=page_path,
                main=main,
                variant=variant,
                name=name or file_name_normalized,
                description=description,
                tag=tag,
                icon=icon or "📄",
                order=order,
            )
            pages.append(page)

        pages = sorted(pages, key=lambda page: page.order or page.name)

        ss.pages = pages


def get_module_attr(module, attr, default=None):
    try:
        return object.__getattribute__(module, attr)
    except AttributeError:
        return default
