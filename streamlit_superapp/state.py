from typing import Any, Generic, Optional, TypeVar, Union, cast
from uuid import uuid4
from streamlit import session_state as ss

from streamlit_superapp.typing import Page

T = TypeVar("T")

STATES_KEY = "streamlit_superapp:states"


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

        if STATES_KEY not in ss:
            ss[STATES_KEY] = {}

        ss[STATES_KEY][name] = self

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

    @staticmethod
    def save_all():
        if STATES_KEY not in ss:
            return

        [state.save() for state in ss[STATES_KEY].values()]

    def save(self):
        Store.set(self.name, ss.get(self.updated_name, self.default_value))

    @property
    def initial_value(self) -> T:
        return cast(T, ss.get(self.name, self.default_value))

    @initial_value.setter
    def initial_value(self, value: T):
        Store.set(self.name, value)
        Store.set(self.updated_name, value)

        self.key = Store.set(self.key_name, str(uuid4()))

    @property
    def value(self) -> T:
        return cast(T, ss.get(self.updated_name, ss.get(self.name, self.default_value)))

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
