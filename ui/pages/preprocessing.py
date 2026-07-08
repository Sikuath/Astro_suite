import streamlit as st

from core.pipeline_manager import PipelineManager



# ─────────────────────────────
# PAGE PRETRAITEMENT
# ─────────────────────────────

def show_preprocessing():


    st.title("🔧 Prétraitement Siril")



    workdir = st.session_state.get(
        "workdir"
    )

    siril_path = st.session_state.get(
        "siril"
    )



    if not workdir or not siril_path:

        st.warning(
            "Projet ou Siril non configuré"
        )

        return



    # ─────────────────────────────
    # ETAT PRETRAITEMENT
    # ─────────────────────────────

    if "preprocess_done" not in st.session_state:

        st.session_state.preprocess_done = False



    if "preprocess_running" not in st.session_state:

        st.session_state.preprocess_running = False



    # ─────────────────────────────
    # DEJA TERMINE
    # ─────────────────────────────

    if st.session_state.preprocess_done:


        st.success(
            "✅ Prétraitement terminé"
        )



        if st.button(
            "➡ Continuer vers la palette SHO"
        ):

            st.session_state.workflow_step = 2

            st.rerun()



        return




    # ─────────────────────────────
    # LANCEMENT AUTOMATIQUE
    # ─────────────────────────────

    if not st.session_state.preprocess_running:


        st.session_state.preprocess_running = True



        manager = PipelineManager(
            workdir,
            siril_path
        )



        progress = st.progress(
            0
        )


        terminal = st.empty()


        logs = []



        # ─────────────────────────
        # TERMINAL ASTRO STYLE
        # ─────────────────────────

        def log(line):

            # nettoyage retours ligne
            line = str(line).replace(
                "\r",
                ""
            )


            logs.append(
                line
            )


            terminal.code(
                "\n".join(
                    logs[-40:]
                ),
                language=None
            )



        def callback(line):

            log(
                line
            )



        # ─────────────────────────
        # EXECUTION PIPELINE
        # ─────────────────────────

        ok, logs_final = manager.run_full(
            callback=callback
        )



        # ─────────────────────────
        # RESULTAT OK
        # ─────────────────────────

        if ok:


            progress.progress(
                1.0
            )


            st.session_state.preprocess_done = True


            st.session_state.preprocess_running = False



            st.success(
                "🎉 Alignement et Linear Match terminés"
            )



            st.session_state.workflow_step = 2


            st.rerun()



        # ─────────────────────────
        # ERREUR
        # ─────────────────────────

        else:


            st.session_state.preprocess_running = False



            st.error(
                "❌ Erreur pendant le prétraitement"
            )