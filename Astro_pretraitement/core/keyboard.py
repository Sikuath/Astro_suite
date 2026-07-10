from pathlib import Path
import streamlit.components.v1 as components


_component_path = (
    Path(__file__).parent.parent
    / "components"
    / "keyboard"
    / "frontend"
)


_keyboard_component = components.declare_component(
    "astro_keyboard",
    path=str(_component_path)
)



def get_key():

    return _keyboard_component(
        default="",
        key="keyboard"
    )