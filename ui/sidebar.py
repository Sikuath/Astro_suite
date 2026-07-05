import streamlit as st


def sidebar():

    st.sidebar.title("🔭 Astro Studio")

    # ─────────────────────────────
    # PROJET ACTIF
    # ─────────────────────────────
    st.sidebar.markdown("## 📁 Projet actif")

    workdir = st.session_state.get("workdir")
    siril = st.session_state.get("siril")

    if workdir:
        st.sidebar.success(f"📂 {workdir}")
    else:
        st.sidebar.warning("Aucun dossier sélectionné")

    if siril:
        st.sidebar.info(f"⚙️ Siril : {siril}")

    st.sidebar.markdown("---")

    # ─────────────────────────────
    # STATUS
    # ─────────────────────────────
    st.sidebar.markdown("## 🧠 État")

    st.sidebar.write(
        "Config :",
        "OK" if st.session_state.get("config") else "Non chargée"
    )

    st.sidebar.write("Session :", "active")

    st.sidebar.markdown("---")

    # ─────────────────────────────
    # NAVIGATION
    # ─────────────────────────────
    st.sidebar.markdown("## 🚀 Workflow")

    pages = [
        "Accueil",
        "Projet",
        "Prétraitement",
        "Traitement",
        "Résultats"
    ]

    # 🔥 source unique de vérité
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"

    st.session_state.page = st.sidebar.radio(
        "Aller à",
        pages,
        index=pages.index(st.session_state.page)
    )

    st.sidebar.markdown("---")

    # ─────────────────────────────
    # AIDE
    # ─────────────────────────────
    st.sidebar.markdown("## ❓ Aide")

    st.sidebar.caption(
        "Configure ton projet dans l’onglet Projet.\n"
        "Puis lance le pipeline dans Prétraitement."
    )

    return st.session_state.page