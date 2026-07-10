import streamlit as st
from pathlib import Path
import base64

from ui.sidebar import sidebar

from ui.pages.project import show_project
from ui.pages.preprocessing import show_preprocessing

from tools.sho_mixer import sho_mixer

from ui.pages.sho_lab import show_sho_lab



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
# CSS
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



# ─────────────────────────────────────
# BACKGROUND
# ─────────────────────────────────────

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
# SESSION STATE
# ─────────────────────────────────────

def init_state():

    defaults = {


        # workflow

        "workflow_step": 0,



        # projet

        "workdir": None,

        "siril_cli": None,

        "siril_gui": None,

        "config": None,



        # SHO source

        "S": None,

        "H": None,

        "O": None,



        # RGB généré

        "R": None,

        "G": None,

        "B": None,


        "rgb_ready": False,


        "palette": None,



        # luminance SHO Lab

        "luminance_mode": None,

        "L": None,



        # résultats finaux

        "R_final": None,

        "G_final": None,

        "B_final": None,

        "RGB_final": None,


        # sécurité

        "siril_opened": False,

    }



    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value




# ─────────────────────────────────────
# INITIALISATION
# ─────────────────────────────────────

init_state()

load_css()

set_background()



# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────

step = sidebar()



# ─────────────────────────────────────
# WORKFLOW
# ─────────────────────────────────────

if step == 0:

    show_project()



elif step == 1:

    show_preprocessing()



elif step == 2:

    sho_mixer()



elif step == 3:

    show_sho_lab()



else:

    st.error(
        "Étape workflow inconnue"
    )