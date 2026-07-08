import streamlit as st
from pathlib import Path

from core.config import load_config, save_config


def show_project():

    st.title("📁 Projet")

    st.markdown(
        """
        Configure l'environnement de travail d'Astro Studio.

        Le dossier doit contenir ou recevoir les données SHO :
        - SII
        - Ha
        - OIII
        """
    )


    # ─────────────────────────────
    # CHARGEMENT CONFIG
    # ─────────────────────────────

    if "config" not in st.session_state or st.session_state.config is None:
        st.session_state.config = load_config()

    config = st.session_state.config


    # ─────────────────────────────
    # DOSSIER TRAVAIL
    # ─────────────────────────────

    workdir = st.text_input(
        "📂 Dossier de travail",
        value=config.get("workdir", "")
    )


    # ─────────────────────────────
    # SIRIL
    # ─────────────────────────────

    siril = st.text_input(
        "🔭 Chemin siril-cli.exe",
        value=config.get("siril_path", "")
    )


    st.divider()


    # ─────────────────────────────
    # VALIDATION
    # ─────────────────────────────

    if st.button("🚀 Valider le projet"):


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
                st.error(error)


        # -------------------------
        # OK
        # -------------------------

        else:

            config["workdir"] = workdir
            config["siril_path"] = siril

            save_config(config)


            st.session_state.config = config
            st.session_state.workdir = workdir
            st.session_state.siril = siril


            # passage étape suivante
            st.session_state.workflow_step = 1


            st.success(
                "Projet validé ✔️ Passage au prétraitement..."
            )

            st.rerun()



    st.divider()


    # ─────────────────────────────
    # ETAT
    # ─────────────────────────────

    st.subheader("📊 État du projet")


    if st.session_state.workdir:

        st.success(
            f"📂 {st.session_state.workdir}"
        )

    else:

        st.warning(
            "Aucun dossier validé"
        )


    if st.session_state.siril:

        st.success(
            "🔭 Siril détecté"
        )

    else:

        st.warning(
            "Siril non configuré"
        )