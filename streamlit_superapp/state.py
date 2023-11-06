from typing import Any, Generic, Optional, TypeVar, Union, cast
from uuid import uuid4
from streamlit import session_state as ss

from streamlit_superapp.typing import Page

T = TypeVar("T")


class Store:
    data = {}

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        return Store.data.get(ss.session_id, {}).get(key, default)

    @staticmethod
    def set(key: str, value: T) -> T:
        global data

        if ss.session_id not in Store.data:
            Store.data[ss.session_id] = {}
        Store.data[ss.session_id][key] = value
        ss[key] = value
        return value

    @staticmethod
    def restore(key: str, default_value: Optional[Any] = None):
        ss[key] = Store.get(key, default_value)
        return ss[key]


class State(Generic[T]):
    name: str
    default_value: Optional[T] = None

    def __init__(
        self,
        name: str,
        default_value: Optional[T] = None,
        key: Optional[Union[Page, str]] = None,
        cache: bool = True,
    ):
        if key is not None:
            if not isinstance(key, str):
                key = key.path

            name = f"{key}:{name}"

        updated_name = f"updated:{name}"
        key_name = f"key:{name}"
        previous_name = f"previous:{name}"
        default_name = f"default:{name}"
        restored_name = f"restored:{name}"

        if default_value is None:
            self.default_value = Store.get(default_name, None)

        if default_value is not None:
            self.default_value = Store.set(default_name, default_value)

        if restored_name not in ss and cache:
            Store.restore(key_name, str(uuid4()))
            Store.restore(name, default_value)
            Store.restore(updated_name, default_value)
            ss[previous_name] = ss[updated_name]

            ss[restored_name] = True

        self.key = Store.get(key_name, str(uuid4()))
        Store.set(key_name, self.key)

        self.name = name
        self.updated_name = updated_name
        self.key_name = key_name
        self.previous_name = previous_name
        self.default_name = default_name
        self.restored_name = restored_name
        self.value

    @property
    def initial_value(self) -> T:
        return cast(T, ss.get(self.name, self.default_value))

    @initial_value.setter
    def initial_value(self, value: T):
        Store.set(self.name, value)
        self.key = Store.set(self.key_name, self.key)

    @property
    def value(self) -> T:
        value = cast(T, ss.get(self.updated_name, self.default_value))

        if self.name not in ss:
            Store.set(self.name, value)

        if ss.get("page_changed", False) or ss.reloaded:
            Store.set(self.name, value)

        return value

    @value.setter
    def value(self, value: T):
        self.bind(value)

    @property
    def previous_value(self) -> T:
        return cast(T, ss.get(self.previous_name, self.default_value))

    def bind(self, value: Optional[T]):
        previous_value = self.value

        Store.set(self.previous_name, previous_value)
        Store.set(self.updated_name, value)

        return previous_value
