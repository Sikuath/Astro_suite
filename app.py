import streamlit as st
from pathlib import Path
import base64

from tools import sho_mixer
from ui.project import sidebar_project


# ==========================================================
# CSS
# ==========================================================

from pathlib import Path

def load_css():

    css = Path("ui/style.css")

    if css.exists():
        with open(css, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="SHO Studio",
    page_icon="🌌",
    layout="wide"
)


# ==========================================================
# BACKGROUND
# ==========================================================

def set_background():

    bg = Path("ui/background.jpg")

    if not bg.exists():
        return

    with open(bg, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background:
                linear-gradient(
                    rgba(10,10,20,0.55),
                    rgba(10,10,20,0.55)
                ),
                url("data:image/jpeg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Sidebar */

        section[data-testid="stSidebar"] {{
            background: rgba(15,18,30,0.82);
            backdrop-filter: blur(12px);
        }}

        /* Zone principale */

        .main .block-container {{

            background: rgba(15,18,30,0.55);

            backdrop-filter: blur(8px);

            border-radius: 20px;

            padding: 2rem;

            margin-top: 1rem;

            margin-bottom: 1rem;
        }}

        h1,h2,h3,h4,h5,h6 {{
            color: white;
        }}

        p, label, div {{
            color: #ECECEC;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


set_background()
load_css()


# ==========================================================
# SIDEBAR
# ==========================================================

sidebar_project()

page = st.sidebar.radio(
    "Modules",
    [
        "🏠 Projet",
        "🌈 SHO Mixer",
    ]
)


# ==========================================================
# MODULES
# ==========================================================

if page == "🌈 SHO Mixer":
    sho_mixer.run()


# ==========================================================
# HOME
# ==========================================================

elif page == "🏠 Projet":

    col1, col2 = st.columns([2, 1])

    with col1:

        st.title("📁 Projet Astro Studio")

        st.write(
            """
            Configure ton dossier de travail dans la barre latérale.

            SHO Studio détectera automatiquement les fichiers :

            - SII.fit
            - HA.fit
            - OIII.fit
            """
        )

    with col2:

        st.info(
            """
💡 **Astuce**

Place les trois fichiers FITS :

- SII.fit
- HA.fit
- OIII.fit

dans le même dossier avant de lancer le mixage.
            """
        )
