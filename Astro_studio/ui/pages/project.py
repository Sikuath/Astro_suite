import streamlit as st
from pathlib import Path

from core.config import load_config, save_config
from core.siril_detect import detect_siril
from core.siril_version import get_siril_version



# ─────────────────────────────────
# PAGE PROJET
# ─────────────────────────────────

def show_project():

    st.title("📁 Projet")



    st.markdown(
        r"""
Configurer l'environnement de travail d'Astro Studio.

Le dossier de travail doit contenir les fichiers Ha.fit - SII.fit - OIII.fit


Astro Studio utilise deux programmes livrés avec Siril :

- **siril-cli.exe** → scripts automatiques et prétraitement
- **siril.exe** → ouverture graphique des images finales
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
    # DETECTION SIRIL
    # ─────────────────────────────

    detected_siril = detect_siril()


    detected_dir = None


    if detected_siril:


        detected_dir = Path(
            detected_siril
        ).parent


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
            "⚠ Siril non détecté automatiquement."
        )



    # ─────────────────────────────
    # CHEMINS SIRIL
    # ─────────────────────────────

    default_cli = config.get(
        "siril_cli",
        str(
            detected_dir / "siril-cli.exe"
        )
        if detected_dir
        else ""
    )


    default_gui = config.get(
        "siril_gui",
        str(
            detected_dir / "siril.exe"
        )
        if detected_dir
        else ""
    )



    with st.expander(
        "🔧 Configuration Siril"
    ):


        siril_cli = st.text_input(
            "Chemin siril-cli.exe (scripts)",
            value=default_cli
        )


        siril_gui = st.text_input(
            "Chemin siril.exe (interface graphique)",
            value=default_gui
        )


        st.caption(
            """
siril-cli.exe :
→ prétraitement automatique
→ scripts Siril (.ssf)

siril.exe :
→ ouverture des images finales
→ visualisation utilisateur
            """
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



        # dossier

        if not workdir:


            errors.append(
                "Dossier de travail non défini."
            )


        elif not Path(workdir).exists():


            errors.append(
                "Le dossier de travail n'existe pas."
            )



        # CLI

        if not siril_cli:


            errors.append(
                "Chemin siril-cli.exe absent."
            )


        elif not Path(siril_cli).exists():


            errors.append(
                "siril-cli.exe introuvable."
            )



        # GUI

        if not siril_gui:


            errors.append(
                "Chemin siril.exe absent."
            )


        elif not Path(siril_gui).exists():


            errors.append(
                "siril.exe introuvable."
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
        # VALIDATION OK
        # -------------------------

        else:



            # sauvegarde config

            config["workdir"] = workdir

            config["siril_cli"] = siril_cli

            config["siril_gui"] = siril_gui



            save_config(
                config
            )



            st.session_state.config = config



            # =====================
            # PROJET
            # =====================

            st.session_state.workdir = workdir



            # =====================
            # SIRIL CLI
            # =====================

            st.session_state.siril_cli = siril_cli



            # Compatibilité anciens modules
            # preprocessing utilise encore "siril"

            st.session_state.siril = siril_cli



            # =====================
            # SIRIL GUI
            # =====================

            st.session_state.siril_gui = siril_gui



            st.session_state.workflow_step = 1



            st.success(
                "Projet validé ✔️ Passage au prétraitement..."
            )


            st.rerun()



    st.divider()



    # ─────────────────────────────
    # ETAT PROJET
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
        "siril_cli"
    ):


        st.success(
            "⚙ Siril CLI configuré ✔"
        )


    else:


        st.warning(
            "Siril CLI non configuré"
        )



    if st.session_state.get(
        "siril_gui"
    ):


        st.success(
            "🖥 Siril graphique configuré ✔"
        )


    else:


        st.warning(
            "Siril graphique non configuré"
        )