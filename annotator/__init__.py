import streamlit.components.v1 as components

_component_func = components.declare_component(
    "custom_annotator",
    url="http://localhost:3001",
)

def custom_annotator(text: str, tags: list, key=None):
    # Pass min and max from Python to the frontend component
    component_value = _component_func(text=text, tags=tags, key=key)
    return component_value
