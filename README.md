# Streamlit Super App

Enhance your Streamlit app development experience with **Streamlit Super App**! This package provides features that streamline the creation and management of multipage apps and offers improved state management for widgets.

## Features

- **Multipage/Tree Router**: Automatically generate multi-page routing based on folder structure.
- **Persistent State Management**: Seamlessly manage the state of widgets across different pages.

## Installation

Install Streamlit Super App using pip:

```sh
pip install streamlit-superapp
```

## Getting Started

### Multipage Routing

Create a `pages` folder in the root directory of your Streamlit app and organize your pages as shown below:

```
pages/
├─  __init__.py
└─  hello/__init__.py
```

- **You can go beyond that, create as many levels as you want!**

For instance, `pages/hello/__init__.py` can be:

```python
import streamlit as st

NAME = "Demo"
DESCRIPTION = "Sample page to demonstrate Streamlit Super App."
ICON = "🌍"

def main():
    st.write("Hello World!")
```

In your main file, call streamlit_superapp's "run" function

```python
import streamlit_superapp
import streamlit as st

# Your code before initialization
# Put your cool logo in the sidebar
# Customize your styles
# Insert your custom HTML
# Use your imagination

# These are the default values, no need to provide them explicitly
streamlit_superapp.run(
    hide_index_description = False,
    hide_home_button = False
)
```

### Managing DataFrame State and Editing

Easily edit and manage the state of DataFrames.

```python
import pandas as pd
import streamlit as st
from streamlit_superapp.state import State

ICON = "📊"

def main():
    state = State("df", default_value=get_base_input())


    with st.sidebar:
        if st.button("✖️ Multiply"):
            # The "state.value" is always the most updated value
            # So we can manipulate it before rendering it again
            state.initial_value = calculate(state.value)

        if st.button("🔄 Reset"):
            # Forcing a value update before rendering
            state.initial_value = get_base_input()

    # setting the "initial_value" and "key" is mandatory
    df = st.data_editor(data=state.initial_value, key=state.key, hide_index=True)

    # binding the new value to the state is mandatory!
    # plus you get the previous value for free!
    previous_df = state.bind(df)

    if not df.equals(previous_df):
        st.success("Data changed!")


def get_base_input():
    return pd.DataFrame(index=[0, 1, 2], columns=["a", "b"], dtype=float)


def calculate(df: pd.DataFrame):
    df["result"] = df["a"] * df["b"]

    return df

```

### Basic Counter

Create counters with persistent state.

```python
import streamlit as st
from streamlit_superapp import State

NAME = "Counter"
TAG = "{A:}📚 Studies" # This page will appear in a group "📚 Studies" at the top of a index page
ICON = "🔢"

def main(page):
    counter = State("counter", default_value=0, key=page)

    if st.button("Increment"):
        # This is the same as binding a new value
        counter.value += 1

    # Initial value only updates after changing pages
    # or if we update it manually
    st.write(f"initial_value:" {counter.initial_value})
    st.write(f"current value: {counter.value}")
```

### Shared State Across Pages

Maintain the state of TextInput across different pages.

```python
import streamlit as st
from streamlit_superapp import State

NAME = "Persistent Text Input"

def main():

    # You can access the state "text" on another page too!
    state = State("text", default_value="Wilian")

    text = st.text_input("Your Name", value=state.initial_value, key=state.key)

    previous_text = state.bind(text)

    if text != previous_text:
        st.success("Input changed")

    st.success(f"Hello {text}!")
```

### Page Private State

Create a persistent TextInput that is private to a page.

```python
from streamlit_superapp import State, Page
import streamlit as st

NAME = "Page Only State"

# Super app will provide the current page to your function
def main(page: Page):

    # Providing the state with the page as key will make it private
    # Even tho it has the same "text" key state
    state = State("text", default_value="", key=page)

    value = st.text_input("This is not shared between pages", value=state.initial_value)

    previous_value = state.bind(value)

    st.write(value)
```

## Contributing

We welcome contributions to Streamlit Super App! Please feel free to open issues or submit pull requests.

## License

Streamlit Super App is licensed under the [MIT License](LICENSE).

---
