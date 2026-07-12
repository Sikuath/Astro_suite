import streamlit as st
from scipy.ndimage import zoom as spzoom
from pathlib import Path

from core.fits_io import load_fits
from core.preview import make_preview
from core.rgb_export import save_rgb_channels, save_rgb_final



# =====================================================
# CACHE FITS
# =====================================================

@st.cache_data
def load_lrgb_data(
    L_path,
    R_path,
    G_path,
    B_path
):

    L, _ = load_fits(L_path)
    R, _ = load_fits(R_path)
    G, _ = load_fits(G_path)
    B, _ = load_fits(B_path)

    return L, R, G, B



# =====================================================
# CREATION RGB LRGB
# =====================================================

def mix_lrgb(
    L,
    R,
    G,
    B,
    l_weight=1.0
):

    """
    Création RGB finale.

    La luminance est injectée
    dans les couches couleur.

    RGB = couleur × luminance

    Données conservées linéaires.
    """


    Rf = R * L * l_weight

    Gf = G * L * l_weight

    Bf = B * L * l_weight


    return Rf, Gf, Bf



# =====================================================
# PAGE LRGB MIXER
# =====================================================

def lrgb_mixer():


    st.title(
        "🌈 LRGB Mixer"
    )



    # =================================================
    # PROJET
    # =================================================

    workdir = st.session_state.get(
        "workdir"
    )


    if not workdir:

        st.warning(
            "Projet non défini."
        )

        return



    path = Path(workdir)



    L_path = path / "L_linear.fit"
    R_path = path / "R_linear.fit"
    G_path = path / "G_linear.fit"
    B_path = path / "B_linear.fit"



    if not all(
        [
            L_path.exists(),
            R_path.exists(),
            G_path.exists(),
            B_path.exists()
        ]
    ):


        st.error(
            "Fichiers LRGB_linear introuvables."
        )

        return




    # =================================================
    # CHARGEMENT
    # =================================================

    L, R, G, B = load_lrgb_data(

        L_path,
        R_path,
        G_path,
        B_path

    )




    # =================================================
    # SESSION
    # =================================================

    if "lrgb_stretch" not in st.session_state:

        st.session_state.lrgb_stretch = 3.0



    if "lrgb_zoom" not in st.session_state:

        st.session_state.lrgb_zoom = 1.0



    if "lrgb_l_weight" not in st.session_state:

        st.session_state.lrgb_l_weight = 1.0




    # =================================================
    # LAYOUT
    # =================================================

    col_left, col_right = st.columns(
        [1,2],
        gap="large"
    )



    # =================================================
    # CONTROLES
    # =================================================

    with col_left:


        st.subheader(
            "⚙️ Contrôles"
        )



        l_weight = st.slider(

            "Influence luminance",

            0.1,
            2.0,

            st.session_state.lrgb_l_weight,

            key="lrgb_l_weight"

        )



        stretch = st.slider(

            "Stretch preview",

            0.5,
            10.0,

            st.session_state.lrgb_stretch,

            key="lrgb_stretch"

        )



        zoom = st.slider(

            "Zoom",

            1.0,
            2.0,

            st.session_state.lrgb_zoom,

            key="lrgb_zoom"

        )



        st.divider()



        if st.button(
            "➡ Valider cette composition LRGB"
        ):


            R_final, G_final, B_final = mix_lrgb(

                L,
                R,
                G,
                B,

                l_weight

            )



            # export couches RGB

            save_rgb_channels(

                path,

                R_final,

                G_final,

                B_final

            )



            # export cube RGB final

            save_rgb_final(

                R_final,
                G_final,
                B_final,

                path

            )



            st.session_state.L = L


            st.session_state.R = R_final

            st.session_state.G = G_final

            st.session_state.B = B_final


            st.session_state.RGB_final = True


            st.success(
                "Composition LRGB validée ✔️"
            )




    # =================================================
    # PREVIEW
    # =================================================

    with col_right:


        st.subheader(
            "👁 Preview RGB final"
        )



        R_preview, G_preview, B_preview = mix_lrgb(

            L,
            R,
            G,
            B,

            l_weight

        )



        RGB = make_preview(

            R_preview,
            G_preview,
            B_preview,

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