import streamlit as st
import time

from core.fits_loader import find_fits
from core.preview import fits_preview
from core.reject import reject_file
from core.config import load_config

from streamlit_shortcuts import shortcut_button


# ==========================
# Configuration page
# ==========================

st.set_page_config(
    page_title="Astro Preview",
    page_icon="🔭",
    layout="wide"
)


st.title("🔭 Preview Lights")


# ==========================
# Chargement configuration
# ==========================

if "rejected_folder" not in st.session_state:

    config = load_config()

    st.session_state["rejected_folder"] = config.get(
        "rejected_folder",
        ""
    )


# ==========================
# Vérification projet
# ==========================

if "lights_folder" not in st.session_state:

    st.warning(
        "Choisissez d'abord un projet"
    )

    st.stop()



files = find_fits(
    st.session_state["lights_folder"]
)



if not files:

    st.error(
        "Aucun fichier FITS trouvé"
    )

    st.stop()



# ==========================
# Initialisation session
# ==========================

if "index" not in st.session_state:

    st.session_state.index = 0



if "reject_count" not in st.session_state:

    st.session_state.reject_count = 0



if "reject_requested" not in st.session_state:

    st.session_state.reject_requested = False



if "last_action_time" not in st.session_state:

    st.session_state.last_action_time = 0



# ==========================
# Anti répétition clavier
# ==========================

def can_execute(delay=0.3):

    now = time.time()


    if now - st.session_state.last_action_time < delay:

        return False


    st.session_state.last_action_time = now

    return True



# ==========================
# Sécurité index
# ==========================

st.session_state.index = max(
    0,
    min(
        st.session_state.index,
        len(files)-1
    )
)



current = files[
    st.session_state.index
]



# ==========================
# Traitement rejet
# ==========================

if st.session_state.reject_requested:


    reject_file(
        current,
        st.session_state["rejected_folder"]
    )


    st.session_state.reject_count += 1


    st.session_state.reject_requested = False


    st.session_state.index = min(
        st.session_state.index + 1,
        len(files)-1
    )



# ==========================
# Actions navigation
# ==========================

def previous():

    st.session_state.index = max(
        0,
        st.session_state.index - 1
    )



def next_image():

    st.session_state.index = min(
        len(files)-1,
        st.session_state.index + 1
    )



# ==========================
# En-tête
# ==========================

col_a, col_b = st.columns(
    [4,1]
)


with col_a:

    st.subheader(
        current.name
    )


with col_b:

    st.metric(
        "🗑️ Rejets",
        st.session_state.reject_count
    )



# ==========================
# Commandes clavier
# ==========================

nav1, trash, nav2 = st.columns(
    [1,1,1]
)



with nav1:

    if shortcut_button(
        "⬅️ Précédente",
        "ArrowLeft"
    ):

        if can_execute():

            previous()

            st.rerun()



with trash:

    if shortcut_button(
        "⬆️ Rejeter",
        "ArrowUp"
    ):

        if can_execute(0.8):

            st.session_state.reject_requested = True



with nav2:

    if shortcut_button(
        "Suivante ➡️",
        "ArrowRight"
    ):

        if can_execute():

            next_image()

            st.rerun()



# ==========================
# Affichage image
# ==========================

image = fits_preview(
    current
)



if image:

    st.image(
        image,
        width=900
    )



# ==========================
# Bouton souris rejet
# ==========================

st.divider()


if st.button(
    "🗑️ Rejeter cette image",
    use_container_width=True
):

    if can_execute(0.8):

        st.session_state.reject_requested = True



# ==========================
# Informations
# ==========================

info1, info2 = st.columns(2)



with info1:

    st.info(
        f"📷 Image {st.session_state.index + 1} / {len(files)}"
    )



with info2:

    st.success(
        f"📂 Lights disponibles : {len(files)}"
    )



# ==========================
# Aide
# ==========================

st.caption(
    "⬅️ précédent   |   ➡️ suivant   |   ⬆️ rejeter"
)