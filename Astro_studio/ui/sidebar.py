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
        st.sidebar.success("📂 Projet chargé")
        st.sidebar.caption(workdir)
    else:
        st.sidebar.warning("Aucun projet chargé")

    if siril:
        st.sidebar.info(f"⚙️ Siril détecté")

    st.sidebar.markdown("---")


    # ─────────────────────────────
    # ETAT DU WORKFLOW
    # ─────────────────────────────
    st.sidebar.markdown("## 🚀 Workflow")


    steps = [
        "📁 Projet",
        "🔧 Prétraitement",
        "🌈 Palette SHO",
        "✨ SHO Lab",
        "💾 Export"
    ]


    # Initialisation
    if "workflow_step" not in st.session_state:
        st.session_state.workflow_step = 0


    current = st.session_state.workflow_step


    for i, step in enumerate(steps):

        if i < current:
            st.sidebar.success(f"✅ {step}")

        elif i == current:
            st.sidebar.info(f"▶ {step}")

        else:
            st.sidebar.caption(f"🔒 {step}")


    st.sidebar.markdown("---")


    # ─────────────────────────────
    # ETAT TECHNIQUE
    # ─────────────────────────────
    st.sidebar.markdown("## 🧠 État")


    states = {
        "Projet": st.session_state.get("workdir") is not None,
        "Siril": st.session_state.get("siril") is not None,
        "Config": st.session_state.get("config") is not None,
    }


    for name, ok in states.items():
        if ok:
            st.sidebar.write(f"✅ {name}")
        else:
            st.sidebar.write(f"⚪ {name}")


    st.sidebar.markdown("---")

        # ─────────────────────────────
    # FOOTER SIDEBAR
    # ─────────────────────────────

    st.sidebar.markdown(
        """
        <div style="
            position: fixed;
            bottom: 8px;
            left: 15px;
            width: 220px;
            text-align: center;
            font-size: 0.55em;
            color: #888;
            line-height: 1.4;
        ">
            © 2026 <b>Sikuath</b> — Astro Studio<br>
            Logiciel distribué sous licence MIT.<br>
            Images, captures d'écran et contenus graphiques<br>
            sous licence <b>CC BY-NC-ND 4.0</b>,<br>
            sauf mention contraire.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    return st.session_state.workflow_step