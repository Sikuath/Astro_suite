import streamlit as st
from pathlib import Path

from core.fits_io import save_fits



def show_external_luminance():

    st.title("⭐ Luminance externe")


    st.info(
        """
        Mode Luminance externe.

        Astro Studio prépare la couche couleur SHO.
        La création de la luminance sera réalisée dans Siril.
        """
    )


    # ─────────────────────────────
    # VERIFICATION DONNEES RGB
    # ─────────────────────────────

    required = [
        "R",
        "G",
        "B",
        "workdir"
    ]


    if not all(
        key in st.session_state
        for key in required
    ):

        st.error(
            "Les couches RGB ne sont pas disponibles."
        )

        st.info(
            "Retournez dans SHO Mixer pour valider la palette."
        )

        return



    R = st.session_state.R
    G = st.session_state.G
    B = st.session_state.B


    workdir = Path(
        st.session_state.workdir
    )



    # ─────────────────────────────
    # CREATION FICHIERS
    # ─────────────────────────────

    if not st.session_state.get(
        "rgb_saved",
        False
    ):


        with st.spinner(
            "Création des couches RGB..."
        ):


            save_fits(
                workdir / "R.fit",
                R
            )


            save_fits(
                workdir / "G.fit",
                G
            )


            save_fits(
                workdir / "B.fit",
                B
            )


            st.session_state.rgb_saved = True



        st.success(
            "Couches RGB créées dans le dossier Travail ✔"
        )



    st.divider()



    st.subheader(
        "📷 Procédure dans Siril"
    )


    st.markdown(
        """
### 1️⃣ Ouvrir Siril

Les fichiers suivants sont disponibles :

R.fit
G.fit
B.fit

### 2️⃣ Préparer la luminance

Dans Siril :

- traiter vos images L
- empiler
- aligner
- appliquer les traitements nécessaires


### 3️⃣ Recomposition LRGB

Utiliser :

- Luminance → détails
- RGB SHO → couleurs


La luminance apporte :

✨ contraste  
✨ finesse  
✨ structures

La couche SHO apporte :

🌈 couleurs
        """
    )



    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "⬅ Retour SHO Lab"
        ):

            st.session_state.workflow_step = 3
            st.rerun()



    with col2:

        if st.button(
            "❌ Quitter"
        ):

            st.session_state.workflow_step = 0

            # nettoyage état luminance externe
            st.session_state.pop(
                "rgb_saved",
                None
            )

            st.session_state.pop(
                "luminance_mode",
                None
            )

            st.success(
                "Retour à l'accueil"
            )

            st.rerun()