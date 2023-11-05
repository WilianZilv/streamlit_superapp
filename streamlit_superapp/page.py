from dataclasses import dataclass

from typing import Callable, List, Optional, cast
from streamlit import session_state as ss

from streamlit_superapp.typing import Navigation, Variant


@dataclass
class Page:
    path: str
    main: Callable
    name: str
    icon: str
    description: Optional[str] = None
    variant: Optional[Variant] = None
    tag: Optional[str] = None
    order: Optional[str] = None

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

    @property
    def nearest_gallery(self):
        target = self
        while True:
            gallery = [n for n in target.neighbors if n.variant == "index"]
            if len(gallery):
                return gallery[0]

            target = target.parent

            if target is None:
                return None

    def __str__(self) -> str:
        return self.name or self.path
