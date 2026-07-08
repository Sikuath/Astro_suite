import streamlit as st

from tools.sho_lab import (
    make_luminance,
    apply_luminance
)

from core.preview import make_preview


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
        "O"
    ]


    if not all(
        key in st.session_state
        for key in required
    ):

        st.warning(
            "Aucune composition SHO disponible."
        )

        return



    # récupération données

    R = st.session_state.R
    G = st.session_state.G
    B = st.session_state.B

    S = st.session_state.S
    H = st.session_state.H
    O = st.session_state.O



    # ─────────────────────────────
    # LAYOUT
    # ─────────────────────────────

    left, right = st.columns(
        [1, 2],
        gap="large"
    )



    # valeurs par défaut

    mode = "Ha"

    coeffs = (
        0.25,
        0.60,
        0.15
    )

    strength = 1.0
    stretch = 3.0



    # =====================================================
    # COLONNE GAUCHE
    # =====================================================

    with left:


        st.subheader(
            "✨ Luminance"
        )


        mode = st.radio(
            "Source",
            [
                "Aucune",
                "Ha",
                "SHO synthétique",
                "L externe"
            ],
            index=1
        )



        # -------------------------
        # Informations
        # -------------------------

        if mode == "Aucune":

            st.info(
                """
                Aucune luminance.

                Les couches RGB seront envoyées
                directement vers Siril pour une
                recomposition couleur.
                """
            )


        elif mode == "L externe":

            st.info(
                """
                Une luminance réalisée dans Siril
                sera utilisée pour une recomposition LRGB.
                """
            )



        # -------------------------
        # Curseurs SHO
        # -------------------------

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



        st.divider()



        strength = st.slider(
            "Force luminance",
            0.0,
            1.0,
            1.0
        )


        stretch = st.slider(
            "Stretch",
            0.5,
            10.0,
            3.0
        )


        st.divider()



        # =================================================
        # CALCUL AVANT VALIDATION
        # =================================================

        L = None
        R2 = R
        G2 = G
        B2 = B


        if mode not in [
            "Aucune",
            "L externe"
        ]:


            L = make_luminance(
                S,
                H,
                O,
                mode,
                coeffs
            )


            R2, G2, B2 = apply_luminance(
                R,
                G,
                B,
                L,
                strength
            )



        # =================================================
        # VALIDATION
        # =================================================

        if st.button(
            "➡ Valider le traitement luminance"
        ):


            # -------------------------
            # RGB direct
            # -------------------------

            if mode == "Aucune":

                st.session_state.workflow_step = 4
                st.session_state.luminance_mode = mode

                st.rerun()



            # -------------------------
            # L externe
            # -------------------------

            elif mode == "L externe":

                st.session_state.workflow_step = 5
                st.session_state.luminance_mode = mode

                st.rerun()



            # -------------------------
            # L Python
            # -------------------------

            else:


                st.session_state.R_lrgb = R2
                st.session_state.G_lrgb = G2
                st.session_state.B_lrgb = B2

                st.session_state.L_lrgb = L

                st.session_state.luminance_mode = mode


                st.session_state.workflow_step = 6


                st.rerun()



    # =====================================================
    # PREVIEW
    # =====================================================

    with right:


        st.subheader(
            "👁 Résultat SHO Lab"
        )


        RGB = make_preview(
            R2,
            G2,
            B2,
            stretch
        )


        st.image(
            RGB,
            use_container_width=True
        )