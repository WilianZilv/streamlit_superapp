from dataclasses import dataclass

from typing import Callable, List, Literal, Optional, cast
from streamlit import session_state as ss

from streamlit_superapp.typing import Navigation


@dataclass
class Page:
    path: str
    main: Callable
    name: str
    icon: str
    description: Optional[str] = None
    tag: Optional[str] = None
    order: Optional[str] = None
    sidebar: Optional[Literal["selectbox", "radio"]] = None
    index: Optional[bool] = None
    search: Optional[bool] = None
    hidden: bool = False

    def serializable_dict(self):
        return {
            "path": self.path,
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "tag": self.tag,
            "order": self.order,
            "index": self.index,
            "hidden": self.hidden,
        }

    @property
    def is_active(self):
        navigation: Navigation = ss["navigation"]
        return navigation.current_path() == self.path

    @property
    def parent(self):
        navigation: Navigation = ss["navigation"]

        parent_path = ".".join(self.path.split(".")[:-1])
        return navigation.find_page(parent_path)

    @property
    def children(self):
        pages: List[Page] = ss.pages
        target = self.path + "."

        def is_child(page: Page):
            if page.path == self.path:
                return False

            if not page.path.startswith(target):
                return False

            return "." not in page.path[len(target) :]

        return [page for page in pages if is_child(page)]

    @property
    def neighbors(self) -> List["Page"]:
        parent = self.parent

        if parent is None:
            return []

        return cast(
            List[Page], [page for page in parent.children if page.path != self.path]
        )

    def __str__(self) -> str:
        return self.name or self.path
