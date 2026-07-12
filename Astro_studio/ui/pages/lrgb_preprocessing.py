import streamlit as st

from core.lrgb_pipeline_manager import LRGBPipelineManager



# ─────────────────────────────
# PAGE PREPARATION LRGB
# ─────────────────────────────

def show_lrgb_preprocessing():


    st.title("🔧 Préparation des couches LRGB")



    st.markdown(
        """
Cette étape prépare les quatre couches :

- L → luminance
- R → rouge
- G → vert
- B → bleu

Les couches sont alignées et normalisées avant la recomposition couleur.
        """
    )



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
    # ETAT
    # ─────────────────────────────

    if "lrgb_preprocess_done" not in st.session_state:

        st.session_state.lrgb_preprocess_done = False



    if "lrgb_preprocess_running" not in st.session_state:

        st.session_state.lrgb_preprocess_running = False




    # ─────────────────────────────
    # DEJA TERMINE
    # ─────────────────────────────

    if st.session_state.lrgb_preprocess_done:


        st.success(
            "✅ Préparation LRGB terminée"
        )


        st.info(
            """
Les fichiers préparés sont disponibles :

L_linear.fit  
R_linear.fit  
G_linear.fit  
B_linear.fit
            """
        )



        if st.button(
            "➡ Continuer vers la recomposition LRGB"
        ):


            st.session_state.workflow_step = 2

            st.rerun()



        return




    # ─────────────────────────────
    # LANCEMENT
    # ─────────────────────────────

    if not st.session_state.lrgb_preprocess_running:


        st.session_state.lrgb_preprocess_running = True



        manager = LRGBPipelineManager(

            workdir,

            siril_path

        )



        progress = st.progress(
            0
        )


        terminal = st.empty()


        logs = []



        # ─────────────────────────
        # TERMINAL
        # ─────────────────────────

        def log(line):


            line = str(line).replace(
                "\r",
                ""
            )


            logs.append(
                line
            )


            terminal.code(

                "\n".join(
                    logs[-60:]
                ),

                language=None
            )



        def callback(line):

            log(
                line
            )



        # ─────────────────────────
        # PIPELINE
        # ─────────────────────────

        ok, logs_final = manager.run_full(

            callback=callback

        )



        # ─────────────────────────
        # SUCCES
        # ─────────────────────────

        if ok:


            progress.progress(
                1.0
            )


            st.session_state.lrgb_preprocess_done = True


            st.session_state.lrgb_preprocess_running = False



            st.success(
                "🎉 Alignement et normalisation LRGB terminés"
            )



            st.session_state.workflow_step = 2


            st.rerun()



        # ─────────────────────────
        # ERREUR
        # ─────────────────────────

        else:


            st.session_state.lrgb_preprocess_running = False



            st.error(
                "❌ Erreur pendant la préparation LRGB"
            )