from typing import Callable, List, Literal, Optional, Protocol, Union


class Page(Protocol):
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

    def serializable_dict(self) -> dict:
        ...

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
    hide_index_description: bool
    hide_home_button: bool
    hide_back_button: bool

    @staticmethod
    def previous_path() -> str:
        ...

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
