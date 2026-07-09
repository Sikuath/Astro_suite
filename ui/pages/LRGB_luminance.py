import streamlit as st
from pathlib import Path
import subprocess

from core.fits_io import save_fits
from tools.siril_live_runner import run_siril_live_script



def show_lrgb_luminance():


    st.title("✨ Recomposition LRGB")



    # ─────────────────────────────
    # VERIFICATION DONNEES
    # ─────────────────────────────

    required = [
        "R_lrgb",
        "G_lrgb",
        "B_lrgb",
        "L_lrgb",
        "workdir",
        "siril"
    ]


    if not all(
        key in st.session_state
        for key in required
    ):

        st.error(
            "Données LRGB absentes."
        )

        st.info(
            "Retournez dans SHO Lab."
        )

        return



    R = st.session_state.R_lrgb
    G = st.session_state.G_lrgb
    B = st.session_state.B_lrgb
    L = st.session_state.L_lrgb


    workdir = Path(
        st.session_state.workdir
    )


    siril_path = Path(
        st.session_state.siril
    )


    mode = st.session_state.get(
        "luminance_mode",
        "inconnue"
    )



    # ─────────────────────────────
    # INFOS
    # ─────────────────────────────

    st.info(
        f"""
        Source luminance :

        ⭐ {mode}


        Astro Studio va préparer :

        ✔ la couche de luminance et l'injecter dans les trois fichiers RGB  
        ✔ creér le fichier RGB_final.fit  
        ✔ ouvrir le fichier RGB_final.fit avec Siril  
       
        """
    )



    # ─────────────────────────────
    # SCRIPT SIRIL
    # ─────────────────────────────

    script_path = (
        Path(__file__)
        .parents[2]
        /
        "scripts"
        /
        "04_RGB.ssf"
    )



    st.divider()



    if st.button(
        "🚀 Lancer recomposition LRGB"
    ):



        # =========================
        # EXPORT FITS
        # =========================

        with st.spinner(
            "Création des couches FITS..."
        ):


            save_fits(
                workdir / "R.fit",
                R
            )

            save_fits(
                workdir / "G.fit",
                G
            )

            save_fits(
                workdir / "B.fit",
                B
            )

          
        st.success(
            "Couches LRGB créées ✔"
        )



        # =========================
        # VERIFICATION SCRIPT
        # =========================

        if not script_path.exists():

            st.error(
                f"Script Siril introuvable :\n{script_path}"
            )

            return



        # =========================
        # TERMINAL LIVE SIRIL
        # =========================

        terminal = st.empty()



        with st.spinner(
            "Recomposition LRGB dans Siril..."
        ):


            ok = run_siril_live_script(
                script_path,
                terminal
            )



        if not ok:

            st.error(
                "Erreur pendant la recomposition Siril."
            )

            return



        st.success(
            "Recomposition LRGB terminée ✔"
        )



        # =========================
        # OUVERTURE SIRIL GRAPHIQUE
        # =========================

        image_finale = (
            workdir
            /
            "RGB_final.fit"
        )


        if not image_finale.exists():

            st.warning(
                "RGB_final.fit introuvable après recomposition."
            )

            return



        try:


            siril_gui = (
                siril_path.parent
                /
                "siril.exe"
            )


            if not siril_gui.exists():

                st.error(
                    f"Siril graphique introuvable : {siril_gui}"
                )

                return



            subprocess.Popen(
                [
                    str(siril_gui),
                    str(image_finale)
                ],
                cwd=str(workdir)
            )


            st.success(
                "Siril ouvert avec RGB_final.fit ✔"
            )


        except Exception as e:

            st.error(
                f"Impossible d'ouvrir Siril : {e}"
            )



    st.divider()



    col1, col2 = st.columns(2)



    with col1:


        if st.button(
            "⬅ Retour SHO Lab"
        ):

            st.session_state.workflow_step = 3

            st.rerun()



    with col2:


        if st.button(
            "❌ Quitter"
        ):


            st.session_state.workflow_step = 0


            st.session_state.pop(
                "luminance_mode",
                None
            )


            st.session_state.pop(
                "R_lrgb",
                None
            )


            st.session_state.pop(
                "G_lrgb",
                None
            )


            st.session_state.pop(
                "B_lrgb",
                None
            )


            st.session_state.pop(
                "L_lrgb",
                None
            )


            st.success(
                "Retour à l'accueil"
            )


            st.rerun()