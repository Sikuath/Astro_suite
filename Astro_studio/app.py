import streamlit as st
from pathlib import Path
import base64

from ui.sidebar import sidebar

from ui.pages.project import show_project
from ui.pages.preprocessing import show_preprocessing
from ui.pages.lrgb_preprocessing import show_lrgb_preprocessing

from tools.sho_mixer import sho_mixer
from tools.lrgb_mixer import lrgb_mixer

from ui.pages.sho_lab import show_sho_lab
from ui.pages.rgb_lab import show_rgb_lab

from ui.pages.palette_manager import show_palette_manager



# ─────────────────────────────────────
# CONFIG STREAMLIT
# ─────────────────────────────────────

BASE_DIR = Path(__file__).parent

ICON = BASE_DIR / "assets" / "Astro_suite.ico"


st.set_page_config(
    page_title="Astro Studio",
    page_icon=str(ICON),
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


        # Navigation

        "page": "workflow",


        # Workflow

        "workflow_step": 0,


        # Projet

        "workdir": None,

        "siril": None,

        "siril_cli": None,

        "siril_gui": None,

        "config": None,

        "project_type": None,

        "project_detection": None,



        # Prétraitement

        "preprocess_done": False,

        "preprocess_running": False,


        "lrgb_preprocess_done": False,

        "lrgb_preprocess_running": False,



        # SHO

        "S": None,

        "H": None,

        "O": None,



        # LRGB

        "L": None,

        "R_lrgb": None,

        "G_lrgb": None,

        "B_lrgb": None,



        # RGB

        "R": None,

        "G": None,

        "B": None,

        "rgb_ready": False,



        # Palette

        "palette": None,



        # LAB

        "luminance_mode": None,



        # Résultats

        "R_final": None,

        "G_final": None,

        "B_final": None,

        "RGB_final": None,



        # Terminal

        "pipeline_logs": [],

    }



    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value




# ─────────────────────────────────────
# INIT
# ─────────────────────────────────────

init_state()

load_css()

set_background()



# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────

step = sidebar()



# ─────────────────────────────────────
# PAGE OUTIL INDEPENDANTE
# ─────────────────────────────────────

if st.session_state.page == "palettes":

    show_palette_manager()

    st.stop()



# ─────────────────────────────────────
# WORKFLOW
# ─────────────────────────────────────


# ================================
# ETAPE 0
# ================================

if step == 0:

    show_project()



# ================================
# ETAPE 1
# ================================

elif step == 1:


    project_type = st.session_state.get(
        "project_type"
    )


    if project_type == "SHO":

        show_preprocessing()


    elif project_type == "LRGB":

        show_lrgb_preprocessing()


    else:

        st.warning(
            "Type de projet non détecté."
        )



# ================================
# ETAPE 2
# ================================

elif step == 2:


    project_type = st.session_state.get(
        "project_type"
    )


    if project_type == "SHO":

        sho_mixer()


    elif project_type == "LRGB":

        lrgb_mixer()


    else:

        st.warning(
            "Aucun type de projet confirmé."
        )



# ================================
# ETAPE 3
# ================================

elif step == 3:


    project_type = st.session_state.get(
        "project_type"
    )


    if project_type == "SHO":

        show_sho_lab()


    elif project_type == "LRGB":

        show_rgb_lab()


    else:

        st.warning(
            "Projet non défini."
        )



# ================================
# ERREUR
# ================================

else:

    st.error(
        "Étape workflow inconnue"
    )