import streamlit as st
from pathlib import Path

from core.config import load_config, save_config
from core.siril_detect import detect_siril
from core.siril_version import get_siril_version



def show_project():

    st.title("📁 Projet")


    st.markdown(
        r"""
        Configurer l'environnement de travail d'Astro Studio.  

        Le **Dossier de travail** doit contenir les trois fichiers :

        - Ha.fit
        - SII.fit
        - OIII.fit


        Astro Studio détecte automatiquement le logiciel Siril installé sur votre ordinateur.
        
        """,
        unsafe_allow_html=True
    )



    # ─────────────────────────────
    # CHARGEMENT CONFIG
    # ─────────────────────────────

    if (
        "config" not in st.session_state
        or st.session_state.config is None
    ):

        st.session_state.config = load_config()


    config = st.session_state.config



    # ─────────────────────────────
    # DETECTION AUTOMATIQUE SIRIL
    # ─────────────────────────────

    detected_siril = detect_siril()


    if detected_siril:


        siril_version = get_siril_version(
            detected_siril
        )


        st.success(
            "🔭 Siril détecté automatiquement ✔"
        )


        st.info(
            f"Version : {siril_version}"
        )


    else:


        st.warning(
            "⚠ Siril n'a pas été détecté automatiquement."
        )



    # ─────────────────────────────
    # INFORMATIONS TECHNIQUES
    # ─────────────────────────────

    with st.expander(
        "🔧 Informations techniques"
    ):


        siril = st.text_input(

            "Chemin siril-cli.exe",

            value=config.get(
                "siril_path",
                detected_siril or ""
            )

        )



        if siril:

            st.caption(
                "Ce chemin peut être modifié si Siril est installé dans un autre dossier."
            )



    # ─────────────────────────────
    # DOSSIER TRAVAIL
    # ─────────────────────────────

    workdir = st.text_input(

        "📂 Dossier de travail",

        value=config.get(
            "workdir",
            ""
        )

    )



    st.divider()



    # ─────────────────────────────
    # VALIDATION
    # ─────────────────────────────

    if st.button(
        "🚀 Valider le projet"
    ):


        errors = []



        if not workdir:


            errors.append(
                "Le dossier de travail n'est pas défini."
            )


        elif not Path(workdir).exists():


            errors.append(
                "Le dossier de travail n'existe pas."
            )



        if not siril:


            errors.append(
                "Le chemin Siril n'est pas défini."
            )


        elif not Path(siril).exists():


            errors.append(
                "Le programme Siril est introuvable."
            )



        # -------------------------
        # ERREURS
        # -------------------------

        if errors:


            for error in errors:

                st.error(
                    error
                )



        # -------------------------
        # OK
        # -------------------------

        else:


            config["workdir"] = workdir

            config["siril_path"] = siril


            save_config(
                config
            )



            st.session_state.config = config

            st.session_state.workdir = workdir

            st.session_state.siril = siril



            st.session_state.workflow_step = 1



            st.success(
                "Projet validé ✔️ Passage au prétraitement..."
            )


            st.rerun()



    st.divider()



    # ─────────────────────────────
    # ETAT DU PROJET
    # ─────────────────────────────

    st.subheader(
        "📊 État du projet"
    )



    if st.session_state.get(
        "workdir"
    ):


        st.success(
            f"📂 {st.session_state.workdir}"
        )


    else:


        st.warning(
            "Aucun dossier validé"
        )



    if st.session_state.get(
        "siril"
    ):


        st.success(
            "🔭 Siril configuré ✔"
        )


    else:


        st.warning(
            "Siril non configuré"
        )