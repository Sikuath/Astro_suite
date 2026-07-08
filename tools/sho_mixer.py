import streamlit as st
from scipy.ndimage import zoom as spzoom
from pathlib import Path

from core.fits_io import load_fits
from core.processing import mix_sho, apply_palette
from core.preview import make_preview


# ─────────────────────────────────────
# CACHE FITS
# ─────────────────────────────────────

@st.cache_data
def load_sho_data(S_path, H_path, O_path):

    S, _ = load_fits(S_path)
    H, _ = load_fits(H_path)
    O, _ = load_fits(O_path)

    return S, H, O



# ─────────────────────────────────────
# PAGE SHO MIXER
# ─────────────────────────────────────

def sho_mixer():

    st.title("🌈 SHO Mixer")


    # =========================
    # PROJET
    # =========================

    workdir = st.session_state.get("workdir")


    if not workdir:

        st.warning(
            "Projet non défini — retourne dans l'étape Projet."
        )

        return


    path = Path(workdir)


    S_path = path / "SII_linear.fit"
    H_path = path / "HA_linear.fit"
    O_path = path / "OIII_linear.fit"


    if not (
        S_path.exists()
        and H_path.exists()
        and O_path.exists()
    ):

        st.error(
            "Fichiers SHO introuvables dans le dossier."
        )

        return



    # =========================
    # CHARGEMENT DONNEES
    # =========================

    S, H, O = load_sho_data(
        S_path,
        H_path,
        O_path
    )



    # =========================
    # INITIALISATION ETAT
    # =========================

    if "sho_palette" not in st.session_state:
        st.session_state.sho_palette = "Hubble SHO"


    if "sho_stretch" not in st.session_state:
        st.session_state.sho_stretch = 3.0


    if "sho_zoom" not in st.session_state:
        st.session_state.sho_zoom = 1.0



    # =========================
    # LAYOUT
    # =========================

    col_left, col_right = st.columns(
        [1, 2],
        gap="large"
    )



    # =====================================================
    # CONTROLES
    # =====================================================

    with col_left:


        st.subheader("⚙️ Contrôles")



        # -------------------------
        # PALETTE
        # -------------------------

        palette = st.selectbox(

            "Palette",

            [
                "Manual",
                "Hubble SHO",
                "HOO Boost",
                "HOO Natural",
                "Hα Rich",
                "OIII Rich",
                "Foraxx Pro",
                "Gold & Blue",
                "Teal & Orange"
            ],

            key="sho_palette"
        )



        if palette == "Manual":


            r_s = st.slider(
                "R SII",
                0.0,
                1.0,
                0.8,
                key="sho_r_s"
            )


            r_h = st.slider(
                "R Hα",
                0.0,
                1.0,
                0.2,
                key="sho_r_h"
            )


            g_h = st.slider(
                "G Hα",
                0.0,
                1.0,
                0.7,
                key="sho_g_h"
            )


            g_o = st.slider(
                "G OIII",
                0.0,
                1.0,
                0.3,
                key="sho_g_o"
            )


            b_o = st.slider(
                "B OIII",
                0.0,
                1.0,
                1.0,
                key="sho_b_o"
            )


        else:

            r_s, r_h, g_h, g_o, b_o = apply_palette(
                palette
            )



        st.divider()



        # -------------------------
        # IMAGE
        # -------------------------

        stretch = st.slider(

            "Stretch",

            0.5,
            10.0,

            st.session_state.sho_stretch,

            key="sho_stretch"
        )


        zoom = st.slider(

            "Zoom",

            1.0,
            2.0,

            st.session_state.sho_zoom,

            key="sho_zoom"
        )



        st.divider()



        # -------------------------
        # VALIDATION WORKFLOW
        # -------------------------

        st.subheader("✨ Continuer")


        if st.button(
            "➡ Valider cette composition SHO"
        ):


            R, G, B = mix_sho(

                S,
                H,
                O,

                r_s,
                r_h,
                g_h,
                g_o,
                b_o
            )


            # stockage workflow

            st.session_state.S = S
            st.session_state.H = H
            st.session_state.O = O


            st.session_state.R = R
            st.session_state.G = G
            st.session_state.B = B


            st.session_state.palette = palette


            # étape suivante

            st.session_state.workflow_step = 3


            st.success(
                "Composition validée → ouverture SHO Lab"
            )


            st.rerun()



    # =====================================================
    # PREVIEW
    # =====================================================

    with col_right:


        st.subheader("👁 Preview")



        R, G, B = mix_sho(

            S,
            H,
            O,

            r_s,
            r_h,
            g_h,
            g_o,
            b_o
        )


        RGB = make_preview(

            R,
            G,
            B,

            stretch

        )



        if zoom > 1:

            RGB = spzoom(

                RGB,

                (
                    zoom,
                    zoom,
                    1
                ),

                order=1

            )



        st.image(

            RGB,

            use_container_width=True

        )