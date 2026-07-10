import streamlit as st
from scipy.ndimage import zoom as spzoom
from pathlib import Path

from core.fits_io import load_fits
from core.processing import mix_sho, apply_palette
from core.preview import make_preview
from core.rgb_export import save_rgb_channels



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
    # CHARGEMENT
    # =========================

    S, H, O = load_sho_data(
        S_path,
        H_path,
        O_path
    )



    # =========================
    # ETAT SESSION
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



        palette = st.selectbox(

            "Choisir une palette SHO",

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



        descriptions = {

            "Manual":
            """
            Palette personnalisée.

            Réglage manuel SII / Ha / OIII.
            """,

            "Hubble SHO":
            """
            Palette SHO classique.

            SII → Rouge
            Ha → Vert
            OIII → Bleu
            """,

            "HOO Boost":
            """
            Palette HOO renforcée.

            Ha + OIII dominants.
            """,

            "HOO Natural":
            """
            Palette HOO naturelle.

            Ha rouge,
            OIII cyan/bleu.
            """,

            "Hα Rich":
            """
            Accentuation du H-alpha.
            """,

            "OIII Rich":
            """
            Accentuation de l'OIII.
            """,

            "Foraxx Pro":
            """
            Palette avancée inspirée Foraxx.
            """,

            "Gold & Blue":
            """
            Palette artistique chaud/froid.
            """,

            "Teal & Orange":
            """
            Palette artistique cyan/orange.
            """
        }



        st.info(
            descriptions[palette]
        )



        # =========================
        # REGLAGES
        # =========================

        if palette == "Manual":


            r_s = st.slider(
                "R SII",
                0.0,
                1.0,
                0.8
            )


            r_h = st.slider(
                "R Ha",
                0.0,
                1.0,
                0.2
            )


            g_h = st.slider(
                "G Ha",
                0.0,
                1.0,
                0.7
            )


            g_o = st.slider(
                "G OIII",
                0.0,
                1.0,
                0.3
            )


            b_o = st.slider(
                "B OIII",
                0.0,
                1.0,
                1.0
            )


        else:


            r_s, r_h, g_h, g_o, b_o = apply_palette(
                palette
            )



        st.divider()



        stretch = st.slider(
            "Stretch preview",
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



        # =========================
        # VALIDATION
        # =========================

        if st.button(
            "➡ Valider cette composition SHO"
        ):


            # création RGB linéaire

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



            # =========================
            # EXPORT RGB
            # =========================

            save_rgb_channels(
                path,
                R,
                G,
                B
            )



            # =========================
            # STOCKAGE WORKFLOW
            # =========================

            st.session_state.S = S
            st.session_state.H = H
            st.session_state.O = O


            st.session_state.R = R
            st.session_state.G = G
            st.session_state.B = B


            st.session_state.palette = palette


            st.session_state.workflow_step = 3



            st.success(
                "Composition SHO validée ✔️ Passage au traitement luminance"
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