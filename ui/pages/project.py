import streamlit as st
from core.config import load_config, save_config

def show_project():

    st.title("⚙️ Projet")

    # ─────────────────────────────
    # LOAD CONFIG UNE SEULE FOIS
    # ─────────────────────────────
    if "config" not in st.session_state or st.session_state.config is None:
        st.session_state.config = load_config()

    config = st.session_state.config

    # ─────────────────────────────
    # WORKDIR
    # ─────────────────────────────
    workdir = st.text_input(
        "Dossier de travail",
        value=config.get("workdir", "")
    )

    # ─────────────────────────────
    # SIRIL
    # ─────────────────────────────
    siril = st.text_input(
        "Chemin du fichier siril-cli.exe (ex : C:\\Program Files\\Siril\\bin\\siril-cli.exe)",
        value=config.get("siril_path", "")
    )

    st.markdown("---")

    # ─────────────────────────────
    # SAUVEGARDE CONTROLLEE
    # ─────────────────────────────
    if st.button("💾 Sauvegarder le projet"):

        config["workdir"] = workdir
        config["siril_path"] = siril

        save_config(config)
        st.session_state.config = config

        st.session_state.workdir = workdir
        st.session_state.siril = siril

        st.success("Projet sauvegardé ✔️")

    st.markdown("---")

    st.subheader("📊 État actuel")

    st.write("Workdir :", workdir or "Non défini")
    st.write("Siril :", siril or "Non défini")