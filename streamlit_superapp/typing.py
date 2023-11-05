from typing import Callable, List, Literal, Optional, Protocol, Union

Variant = Literal["select_box", "radio", "index"]
available_variants = ["select_box", "radio", "index"]


class Page(Protocol):
    path: str
    main: Callable
    name: str
    icon: str
    description: Optional[str] = None
    variant: Optional[Variant] = None
    tag: Optional[str] = None
    order: Optional[str] = None

    @property
    def is_active(self) -> bool:
        ...

    @property
    def parent(self) -> Optional["Page"]:
        ...

    @property
    def children(self) -> List["Page"]:
        ...

    @property
    def neighbors(self) -> List["Page"]:
        ...

    @property
    def nearest_gallery(self) -> Optional["Page"]:
        ...


class Navigation(Protocol):
    hide_page_title: bool
    hide_index_title: bool
    hide_sidebar_icon: bool
    hide_index_icon: bool

    @staticmethod
    def find_page(path: str) -> Optional[Page]:
        ...

    @staticmethod
    def root() -> Page:
        ...

    @staticmethod
    def render_page(page: Page) -> None:
        ...

    @staticmethod
    def go(path: Union[str, Page]) -> None:
        ...

    @staticmethod
    def current_path(default: str = "pages") -> str:
        ...
