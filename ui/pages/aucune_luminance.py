import streamlit as st
from pathlib import Path
import subprocess

from core.fits_io import save_fits
from tools.siril_runner import run_siril_script



def show_aucune_luminance():

    st.title("🌈 RGB sans luminance")


    st.info(
        """
        Mode RGB direct.

        Astro Studio crée les trois couches couleur
        issues de la palette SHO puis demande à Siril
        de réaliser uniquement la recomposition RVB.
        """
    )


    required = [
        "R",
        "G",
        "B",
        "workdir",
        "siril"
    ]


    if not all(
        key in st.session_state
        for key in required
    ):

        st.error(
            "Les couches RGB ou Siril ne sont pas disponibles."
        )

        st.info(
            "Retournez dans SHO Mixer pour valider la palette."
        )

        return



    R = st.session_state.R
    G = st.session_state.G
    B = st.session_state.B


    workdir = Path(
        st.session_state.workdir
    )


    siril_path = Path(
        st.session_state.siril
    )


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
        "🚀 Créer RGB et ouvrir Siril"
    ):


        # -------------------------
        # CREATION RGB
        # -------------------------

        with st.spinner(
            "Création des couches RGB..."
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
            "Couches RGB créées dans Travail ✔"
        )



        # -------------------------
        # VERIFICATION SCRIPT
        # -------------------------

        if not script_path.exists():

            st.error(
                f"Script Siril introuvable :\n{script_path}"
            )

            return



        # -------------------------
        # LANCEMENT SIRIL CLI
        # -------------------------

        with st.spinner(
            "Recomposition RVB dans Siril..."
        ):

            ok = run_siril_script(
                script_path
            )



        if ok:

            st.success(
                "Recomposition RVB terminée ✔"
            )


            # -------------------------
            # OUVERTURE SIRIL GRAPHIQUE
            # -------------------------

            image_finale = (
                workdir
                /
                "RGB_final.fit"
            )


            if image_finale.exists():

                try:

                    # Siril graphique
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
                        f"Impossible d'ouvrir Siril graphique : {e}"
                    )


            else:

                st.warning(
                    "RGB_final.fit introuvable après recomposition."
                )


        else:

            st.error(
                "Erreur pendant la recomposition Siril."
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

            # nettoyage état luminance externe
            st.session_state.pop(
                "rgb_saved",
                None
            )

            st.session_state.pop(
                "luminance_mode",
                None
            )

            st.success(
                "Retour à l'accueil"
            )

            st.rerun()