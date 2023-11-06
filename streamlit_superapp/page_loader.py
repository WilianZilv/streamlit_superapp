import glob
from importlib import import_module
import os
import sys
from typing import List
from streamlit_superapp.index import Index


from streamlit_superapp.page import Page
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
            tag = get_module_attr(module, "TAG", None)
            icon = get_module_attr(module, "ICON", None)
            order = get_module_attr(module, "ORDER", None)
            file_name_normalized = file_name.replace("_", " ").title()
            sidebar = get_module_attr(module, "SIDEBAR", None)

            if isinstance(order, int):
                order = str(order)

            if main is None:
                main = Index.main
                name = name or file_name_normalized
                icon = icon or "📖"

            if main is None:
                continue

            page = Page(
                path=page_path,
                main=main,
                name=name or file_name_normalized,
                description=description,
                tag=tag,
                icon=icon or "📄",
                order=order,
                sidebar=sidebar,
            )
            pages.append(page)

        pages = sorted(pages, key=lambda page: page.order or page.name)

        ss.pages = pages


def get_module_attr(module, attr, default=None):
    try:
        return object.__getattribute__(module, attr)
    except AttributeError:
        return default
