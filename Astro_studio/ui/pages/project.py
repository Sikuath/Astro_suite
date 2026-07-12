import streamlit as st
from pathlib import Path

from core.config import load_config, save_config
from core.siril_detect import detect_siril
from core.siril_version import get_siril_version
from core.project_detector import detect_project



# ─────────────────────────────────
# PAGE PROJET
# ─────────────────────────────────

def show_project():


    # =============================
    # CSS LOCAL
    # =============================

    st.markdown(
        """
        <style>

        .astro-text {

            color:#eeeeee;
            font-size:1rem;

        }


        .detect-title {

            color:white;
            font-size:1.3rem;
            font-weight:600;

        }


        </style>
        """,
        unsafe_allow_html=True
    )



    # =============================
    # TITRE
    # =============================

    st.title("📁 Projet")


    st.markdown(
        """
        <div class="astro-text">

        Configurez le dossier de travail et l'environnement Siril.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="astro-text">

        <b>siril-cli.exe</b> → scripts automatiques et prétraitement

        <br>

        <b>siril.exe</b> → ouverture graphique des images finales

        </div>
        """,
        unsafe_allow_html=True
    )



    # =============================
    # CHARGEMENT CONFIG
    # =============================

    if (
        "config" not in st.session_state
        or st.session_state.config is None
    ):

        st.session_state.config = load_config()



    config = st.session_state.config



    # =============================
    # DETECTION SIRIL
    # =============================

    detected_siril = detect_siril()

    detected_dir = None



    if detected_siril:


        detected_dir = Path(
            detected_siril
        ).parent



        version = get_siril_version(
            detected_siril
        )


        st.success(
            "🔭 Siril détecté automatiquement ✔"
        )


        st.info(
            f"Version : {version}"
        )


    else:


        st.warning(
            "⚠ Siril non détecté automatiquement."
        )



    # =============================
    # CONFIGURATION SIRIL
    # =============================

    default_cli = config.get(
        "siril_cli",
        str(detected_dir / "siril-cli.exe")
        if detected_dir else ""
    )


    default_gui = config.get(
        "siril_gui",
        str(detected_dir / "siril.exe")
        if detected_dir else ""
    )



    with st.expander(
        "🔧 Configuration Siril"
    ):


        siril_cli = st.text_input(
            "Chemin siril-cli.exe",
            value=default_cli
        )


        siril_gui = st.text_input(
            "Chemin siril.exe",
            value=default_gui
        )



    # =============================
    # DOSSIER TRAVAIL
    # =============================

    workdir = st.text_input(
        "📂 Dossier de travail",
        value=config.get(
            "workdir",
            ""
        )
    )



    # =============================
    # DETECTION + VALIDATION
    # =============================

    st.divider()


    col_title, col_analyse, col_valide = st.columns(
        [4,1,1],
        vertical_alignment="center"
    )


    with col_title:

        st.markdown(
            '<div class="detect-title">🔍 Détection du projet</div>',
            unsafe_allow_html=True
        )


    with col_analyse:

        analyse_clicked = st.button(
            "🔍 Analyser"
        )


    with col_valide:

        validate_clicked = st.button(
            "🚀 Valider"
        )



    # =============================
    # ANALYSE PROJET
    # =============================

    if analyse_clicked:


        if not workdir:


            st.error(
                "Choisissez d'abord un dossier."
            )


        else:


            detection = detect_project(
                workdir
            )


            st.session_state.project_detection = detection



            if detection["valid"]:


                st.success(
                    f"Projet détecté : {detection['type']} ✔"
                )


                for file in detection["detected"]:

                    st.write(
                        f"✅ {file}"
                    )



            elif detection["type"]:


                st.warning(
                    f"Projet {detection['type']} incomplet"
                )


                for file in detection["missing"]:

                    st.write(
                        f"❌ {file}"
                    )



            else:


                st.error(
                    "Aucun projet SHO ou LRGB reconnu."
                )
    # =============================
    # VALIDATION PROJET
    # =============================

    if validate_clicked:


        errors = []


        detection = st.session_state.get(
            "project_detection"
        )



        if not workdir:


            errors.append(
                "Dossier de travail non défini."
            )


        elif not Path(workdir).exists():


            errors.append(
                "Le dossier de travail n'existe pas."
            )



        if not siril_cli or not Path(siril_cli).exists():


            errors.append(
                "siril-cli.exe introuvable."
            )



        if not siril_gui or not Path(siril_gui).exists():


            errors.append(
                "siril.exe introuvable."
            )



        if not detection or not detection["valid"]:


            errors.append(
                "Projet SHO/LRGB non détecté."
            )



        if errors:


            for error in errors:

                st.error(
                    error
                )



        else:


            # =============================
            # ENREGISTREMENT PROJET
            # =============================

            project_type = detection["type"]


            config["workdir"] = workdir

            config["siril_cli"] = siril_cli

            config["siril_gui"] = siril_gui

            config["project_type"] = project_type



            save_config(
                config
            )



            st.session_state.config = config


            st.session_state.workdir = workdir

            st.session_state.siril_cli = siril_cli

            st.session_state.siril = siril_cli

            st.session_state.siril_gui = siril_gui

            st.session_state.project_type = project_type



            # =============================
            # RESET PIPELINE
            # =============================

            st.session_state.preprocess_done = False

            st.session_state.preprocess_running = False


            st.session_state.lrgb_preprocess_done = False

            st.session_state.lrgb_preprocess_running = False


            st.session_state.pipeline_logs = []



            # Passage étape suivante

            st.session_state.workflow_step = 1



            st.success(
                f"Projet {project_type} validé ✔️ Passage au prétraitement..."
            )


            st.rerun()



    st.divider()



    # =============================
    # ETAT PROJET
    # =============================

    st.subheader(
        "📊 État du projet"
    )



    if st.session_state.get(
        "project_type"
    ):


        st.success(
            f"🛰 Type : {st.session_state.project_type}"
        )


    else:


        st.warning(
            "Type de projet non défini"
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