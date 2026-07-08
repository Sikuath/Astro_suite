import streamlit as st
from pathlib import Path
import base64

from ui.sidebar import sidebar

from ui.pages.project import show_project
from ui.pages.preprocessing import show_preprocessing

from tools.sho_mixer import sho_mixer

from ui.pages.sho_lab import show_sho_lab
from ui.pages.aucune_luminance import show_aucune_luminance
from ui.pages.external_luminance import show_external_luminance
from ui.pages.LRGB_luminance import show_lrgb_luminance

# ─────────────────────────────────────
# CONFIG STREAMLIT
# ─────────────────────────────────────

st.set_page_config(
    page_title="Astro Studio",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ─────────────────────────────────────
# CSS + BACKGROUND
# ─────────────────────────────────────

def load_css():

    css_path = Path("ui/style.css")

    if css_path.exists():

        st.markdown(
            f"""
            <style>
            {css_path.read_text(encoding="utf-8")}
            </style>
            """,
            unsafe_allow_html=True
        )



def set_background():

    img_path = Path("ui/background.jpg")

    if img_path.exists():

        with open(img_path, "rb") as f:

            encoded = base64.b64encode(
                f.read()
            ).decode()


        st.markdown(
            f"""
            <style>

            .stApp {{

                background-image:

                linear-gradient(
                    rgba(0,0,0,0.20),
                    rgba(0,0,0,0.20)
                ),

                url(
                "data:image/png;base64,{encoded}"
                );


                background-size:cover;
                background-position:center;
                background-attachment:fixed;

            }}

            </style>
            """,

            unsafe_allow_html=True
        )



# ─────────────────────────────────────
# INITIALISATION WORKFLOW
# ─────────────────────────────────────

def init_state():

    defaults = {


        # étape workflow

        "workflow_step": 0,


        # projet

        "workdir": None,

        "siril": None,

        "config": None,



        # SHO

        "palette": None,

        "rgb_ready": False,


        # luminance

        "luminance_mode": None,


        # résultats

        "R_final": None,

        "G_final": None,

        "B_final": None,


    }


    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value




# ─────────────────────────────────────
# INIT APPLICATION
# ─────────────────────────────────────

init_state()

load_css()

set_background()



# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────

step = sidebar()



# ─────────────────────────────────────
# ROUTING WORKFLOW
# ─────────────────────────────────────


if step == 0:

    # Projet

    show_project()



elif step == 1:

    # Prétraitement Siril

    show_preprocessing()



elif step == 2:

    # Palette SHO

    sho_mixer()



elif step == 3:

    # Luminance

    show_sho_lab()



elif step == 4:

    # Branche sans luminance

    show_aucune_luminance()



elif step == 5:

    # Branche luminance externe

    show_external_luminance()



elif step == 6:
    show_lrgb_luminance()



else:

    st.error(
        "Étape workflow inconnue"
    )
