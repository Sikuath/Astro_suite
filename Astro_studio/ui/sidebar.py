import streamlit as st



def sidebar():


    st.sidebar.title(
        "🔭 Astro Studio"
    )



    # ─────────────────────────────
    # INITIALISATION NAVIGATION
    # ─────────────────────────────

    if "page" not in st.session_state:

        st.session_state.page = "workflow"



    # ─────────────────────────────
    # PROJET ACTIF
    # ─────────────────────────────

    st.sidebar.markdown(
        "## 📁 Projet actif"
    )


    workdir = st.session_state.get(
        "workdir"
    )


    siril = st.session_state.get(
        "siril"
    )


    project_type = st.session_state.get(
        "project_type"
    )



    if workdir:

        st.sidebar.success(
            "📂 Projet chargé"
        )

        st.sidebar.caption(
            workdir
        )

    else:

        st.sidebar.warning(
            "Aucun projet chargé"
        )



    if project_type == "SHO":

        st.sidebar.info(
            "🌈 Projet SHO détecté"
        )


    elif project_type == "LRGB":

        st.sidebar.info(
            "🌈 Projet LRGB détecté"
        )




    if siril:

        st.sidebar.info(
            "⚙️ Siril détecté"
        )



    st.sidebar.markdown(
        "---"
    )



    # ─────────────────────────────
    # OUTILS
    # ─────────────────────────────

    st.sidebar.markdown(
        "## 🛠️ Outils"
    )



    if st.sidebar.button(
        "🎨 Gestion des palettes personnelles",
        use_container_width=True
    ):

        st.session_state.page = "palettes"



    if st.sidebar.button(
        "🚀 Retour workflow",
        use_container_width=True
    ):

        st.session_state.page = "workflow"




    st.sidebar.markdown(
        "---"
    )



    # ─────────────────────────────
    # WORKFLOW
    # ─────────────────────────────

    st.sidebar.markdown(
        "## 🚀 Workflow"
    )



    steps = [

        "📁 Projet",

        "🔧 Prétraitement",

        "🌈 Recomposition RGB",

        "✨ Traitement final",

        "💾 Export"

    ]



    if "workflow_step" not in st.session_state:

        st.session_state.workflow_step = 0



    current = st.session_state.workflow_step



    for i, step in enumerate(steps):


        if i < current:


            st.sidebar.success(
                f"✅ {step}"
            )


        elif i == current:


            st.sidebar.info(
                f"▶ {step}"
            )


        else:


            st.sidebar.caption(
                f"🔒 {step}"
            )



    st.sidebar.markdown(
        "---"
    )



    # ─────────────────────────────
    # FOOTER SIDEBAR
    # ─────────────────────────────

    st.sidebar.markdown(

        """

        <style>

        section[data-testid="stSidebar"] {

            position: relative;

        }


        .astro-footer {

            position: fixed;

            bottom: 10px;

            width: 260px;

            text-align: center;

            font-size: 0.55em;

            color: #888;

            line-height: 1.4;

            z-index: 999;

        }


        section[data-testid="stSidebar"] > div:first-child {

            padding-bottom: 90px;

        }


        </style>


        <div class="astro-footer">

        © 2026 <b>Sikuath</b> — Astro Suite<br>
        Logiciel distribué sous licence MIT.<br>
        Images, captures d'écran et contenus graphiques<br>
        sous licence <b>CC BY-NC-ND 4.0</b>,<br>
        sauf mention contraire.

        </div>

        """,

        unsafe_allow_html=True

    )



    return st.session_state.workflow_step