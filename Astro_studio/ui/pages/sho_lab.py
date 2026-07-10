import streamlit as st
from pathlib import Path

from tools.sho_lab import (
    make_luminance,
    apply_luminance
)

from core.preview import make_preview

from core.rgb_export import (
    save_rgb_final,
    open_with_siril
)



# ─────────────────────────────────
# PAGE SHO LAB
# ─────────────────────────────────

def show_sho_lab():

    st.title("✨ SHO Lab")



    # ─────────────────────────────
    # VERIFICATION DONNEES
    # ─────────────────────────────

    required = [
        "R",
        "G",
        "B",
        "S",
        "H",
        "O",
        "workdir"
    ]


    if not all(
        key in st.session_state
        for key in required
    ):

        st.warning(
            "Aucune composition SHO disponible."
        )

        return



    R = st.session_state.R
    G = st.session_state.G
    B = st.session_state.B


    S = st.session_state.S
    H = st.session_state.H
    O = st.session_state.O


    workdir = Path(
        st.session_state.workdir
    )



    # ─────────────────────────────
    # LAYOUT
    # ─────────────────────────────

    left, right = st.columns(
        [1, 2],
        gap="large"
    )



    mode = "Aucune"

    coeffs = (
        0.25,
        0.60,
        0.15
    )

    strength = 1.0

    stretch = 3.0



    # =================================================
    # CONTROLES
    # =================================================

    with left:


        st.subheader(
            "✨ Luminance"
        )


        mode = st.radio(

            "Choisir la luminance",

            [
                "Aucune",
                "Ha",
                "SHO synthétique"
            ],

            index=0

        )



        if mode == "Aucune":

            st.info(
                """
                Aucun ajout de luminance.

                Le RGB SHO sera exporté directement.
                """
            )


        elif mode == "Ha":

            st.info(
                """
                H-alpha utilisée comme luminance.
                """
            )


        elif mode == "SHO synthétique":

            st.info(
                """
                Luminance créée à partir du mélange SHO.
                """
            )



        if mode == "SHO synthétique":


            st.markdown(
                "### Coefficients luminance"
            )


            s = st.slider(
                "SII",
                0.0,
                1.0,
                0.25
            )


            h = st.slider(
                "Ha",
                0.0,
                1.0,
                0.60
            )


            o = st.slider(
                "OIII",
                0.0,
                1.0,
                0.15
            )


            coeffs = (
                s,
                h,
                o
            )



        strength = st.slider(
            "Force luminance",
            0.0,
            1.0,
            1.0
        )


        stretch = st.slider(
            "Stretch preview",
            0.5,
            10.0,
            3.0
        )



        # =================================================
        # CALCUL
        # =================================================

        R_final = R
        G_final = G
        B_final = B


        if mode != "Aucune":


            L = make_luminance(
                S,
                H,
                O,
                mode,
                coeffs
            )


            R_final, G_final, B_final = apply_luminance(
                R,
                G,
                B,
                L,
                strength
            )



        st.divider()



        # =================================================
        # EXPORT + SIRIL
        # =================================================

        if st.button(
            "💾 Générer RGB_final.fit et ouvrir Siril"
        ):


            with st.spinner(
                "Création RGB_final.fit..."
            ):


                image_finale = save_rgb_final(
                    R_final,
                    G_final,
                    B_final,
                    workdir
                )



            st.success(
                f"RGB_final.fit créé ✔\n\n{image_finale}"
            )



            # sauvegarde session

            st.session_state.R_final = R_final
            st.session_state.G_final = G_final
            st.session_state.B_final = B_final

            st.session_state.luminance_mode = mode



            # =========================
            # OUVERTURE SIRIL GUI
            # =========================

            try:


                siril_gui = st.session_state.get(
                    "siril_gui"
                )


                if not siril_gui:

                    raise Exception(
                        "siril_gui absent de la configuration"
                    )



                siril_exe = Path(
                    siril_gui
                )



                if not siril_exe.exists():

                    raise FileNotFoundError(
                        siril_exe
                    )



                # =====================
                # VERROU ANTI DOUBLE
                # =====================

                if st.session_state.get(
                    "siril_opened",
                    False
                ):


                    st.info(
                        "Siril est déjà ouvert pour cette image."
                    )


                else:


                    open_with_siril(
                        image_finale,
                        siril_exe
                    )


                    st.session_state.siril_opened = True


                    st.success(
                        "Siril ouvert avec RGB_final.fit ✔"
                    )



            except Exception as e:


                st.error(
                    f"Impossible d'ouvrir Siril graphique : {e}"
                )



    # =================================================
    # PREVIEW
    # =================================================

    with right:


        st.subheader(
            "👁 Résultat"
        )


        RGB = make_preview(
            R_final,
            G_final,
            B_final,
            stretch
        )


        st.image(
            RGB,
            width="stretch"
        )



    # =================================================
    # NAVIGATION
    # =================================================

    st.divider()


    col1, col2 = st.columns(2)



    with col1:


        if st.button(
            "⬅ Retour SHO Mixer"
        ):


            st.session_state.workflow_step = 2


            st.session_state.pop(
                "siril_opened",
                None
            )


            st.rerun()



    with col2:


        if st.button(
            "❌ Quitter"
        ):


            st.session_state.workflow_step = 0


            for key in [
                "R_final",
                "G_final",
                "B_final",
                "luminance_mode",
                "siril_opened"
            ]:


                st.session_state.pop(
                    key,
                    None
                )


            st.success(
                "Retour accueil"
            )


            st.rerun()