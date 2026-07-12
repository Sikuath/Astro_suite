import streamlit as st
from scipy.ndimage import zoom as spzoom
from pathlib import Path

from core.fits_io import load_fits
from core.processing import mix_sho, apply_palette
from core.preview import make_preview
from core.rgb_export import save_rgb_channels

from core.palette_manager import (
    load_custom_palettes,
    save_custom_palette,
    delete_custom_palette
)



# ─────────────────────────────────────
# CACHE FITS
# ─────────────────────────────────────

@st.cache_data
def load_sho_data(
    S_path,
    H_path,
    O_path
):

    S, _ = load_fits(S_path)
    H, _ = load_fits(H_path)
    O, _ = load_fits(O_path)

    return S, H, O



# ─────────────────────────────────────
# PALETTES NATIVES
# ─────────────────────────────────────

DEFAULT_PALETTES = [

    "Manual",
    "Hubble SHO",
    "HOO Boost",
    "HOO Natural",
    "Hα Rich",
    "OIII Rich",
    "Foraxx Pro",
    "Gold & Blue",
    "Teal & Orange"

]



# ─────────────────────────────────────
# PAGE SHO MIXER
# ─────────────────────────────────────

def sho_mixer():


    st.title(
        "🌈 SHO Mixer"
    )



    # =========================
    # PROJET
    # =========================

    workdir = st.session_state.get(
        "workdir"
    )


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
    # CHARGEMENT FITS
    # =========================

    S, H, O = load_sho_data(
        S_path,
        H_path,
        O_path
    )
    # =========================
    # PALETTES PERSONNELLES
    # =========================

    custom_palettes = load_custom_palettes()



    palette_names = [

        "Manual",
        "Hubble SHO",
        "HOO Boost",
        "HOO Natural",
        "Hα Rich",
        "OIII Rich",
        "Foraxx Pro",
        "Gold & Blue",
        "Teal & Orange"

    ]



    # ajout palettes utilisateur

    for name in custom_palettes.keys():

        if name not in palette_names:

            palette_names.append(name)




    # =========================
    # ETAT SESSION
    # =========================

    if "sho_palette" not in st.session_state:

        st.session_state.sho_palette = "Hubble SHO"



    if "sho_stretch" not in st.session_state:

        st.session_state.sho_stretch = 3.0



    if "sho_zoom" not in st.session_state:

        st.session_state.sho_zoom = 1.0



    if "sho_manual_values" not in st.session_state:

        st.session_state.sho_manual_values = (

            0.8,
            0.2,
            0.7,
            0.3,
            1.0

        )




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


        st.subheader(

            "⚙️ Contrôles"

        )



        palette = st.selectbox(

            "Choisir une palette SHO",

            palette_names,

            key="sho_palette"

        )



        # =================================================
        # CHARGEMENT PALETTE PERSONNELLE
        # =================================================

        custom = None


        if palette in custom_palettes:

            custom = custom_palettes[palette]



        if custom:


            st.info(

                f"""
### 🎨 Palette personnelle

**Nom :**
{palette}


**Objet :**
{custom.get("objet","")}


**Notes :**

{custom.get("description","")}


📅 Créée le :
{custom.get("date","")}

"""

            )



            r_s, r_h, g_h, g_o, b_o = (

                tuple(
                    custom["coefficients"]
                )

            )



        elif palette != "Manual":


            r_s, r_h, g_h, g_o, b_o = apply_palette(

                palette

            )



        else:


            r_s, r_h, g_h, g_o, b_o = (

                st.session_state.sho_manual_values

            )
        # =================================================
        # DOCUMENTATION PALETTES SHO
        # =================================================

        with st.expander(
            "📚 Référence des palettes SHO"
        ):

            st.markdown(
"""
## Paramètres des palettes SHO

| Palette | R:SII | R:Hα | G:Hα | G:OIII | B:OIII |
|---|---:|---:|---:|---:|---:|
| 🌌 Hubble SHO | 0.8 | 0.2 | 0.7 | 0.3 | 1.0 |
| 🔥 HOO Boost | 0.0 | 0.15 | 0.3 | 0.7 | 1.0 |
| 🌿 HOO Natural | 0.0 | 0.10 | 0.6 | 0.4 | 1.0 |
| ❤️ Hα Rich | 0.2 | 0.8 | 0.8 | 0.2 | 0.8 |
| 🔵 OIII Rich | 0.0 | 0.10 | 0.0 | 1.0 | 1.0 |
| 🟡 Foraxx Pro | 0.6 | 0.4 | 0.4 | 0.6 | 1.0 |
| 🌅 Gold & Blue | 1.0 | 0.0 | 0.5 | 0.5 | 1.0 |
| 🟠 Teal & Orange | 0.9 | 0.1 | 0.3 | 0.7 | 1.0 |

---

### Lecture rapide

🔴 Rouge :
- SII augmente les tons rouges chauds
- Hα renforce les zones d'émission

🟢 Vert :
- Ha dominant = SHO classique
- ajout OIII = tons cyan

🔵 Bleu :
- OIII dominant = nébuleuses bleutées

"""
            )



        # =================================================
        # MODE MANUEL
        # =================================================

        if palette == "Manual":


            st.markdown(
                "### 🎛 Réglages manuels"
            )


            r_s = st.slider(

                "R SII",

                0.0,
                1.0,

                r_s

            )


            r_h = st.slider(

                "R Hα",

                0.0,
                1.0,

                r_h

            )


            g_h = st.slider(

                "G Hα",

                0.0,
                1.0,

                g_h

            )


            g_o = st.slider(

                "G OIII",

                0.0,
                1.0,

                g_o

            )


            b_o = st.slider(

                "B OIII",

                0.0,
                1.0,

                b_o

            )



            st.session_state.sho_manual_values = (

                r_s,
                r_h,
                g_h,
                g_o,
                b_o

            )



            # =================================================
            # SAUVEGARDE PALETTE PERSONNELLE
            # =================================================

            st.divider()


            with st.expander(
                "💾 Enregistrer cette palette personnelle"
            ):


                palette_name = st.text_input(

                    "Nom de la palette",

                    placeholder=
                    "Ex : M42 rouge profond"

                )


                palette_object = st.text_input(

                    "Objet",

                    placeholder=
                    "Ex : M42, NGC7000..."

                )


                palette_description = st.text_area(

                    "Notes",

                    placeholder=
"""
Exemples :

- bon équilibre sur nébuleuses HII
- réduit les étoiles vertes
- contraste intéressant sur OIII
- traitement préféré pour Newton 200/1000
"""

                )



                if st.button(

                    "💾 Sauvegarder palette"

                ):


                    if palette_name.strip():


                        save_custom_palette(

                            palette_name,

                            (
                                r_s,
                                r_h,
                                g_h,
                                g_o,
                                b_o
                            ),

                            description=palette_description,

                            objet=palette_object

                        )


                        st.success(

                            "Palette enregistrée ✔️"

                        )


                        st.rerun()


                    else:


                        st.warning(

                            "Donne un nom à la palette."

                        )
        # =================================================
        # STRETCH / ZOOM
        # =================================================

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



        # =================================================
        # VALIDATION COMPOSITION SHO
        # =================================================

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



            # =====================
            # EXPORT COUCHES RGB
            # =====================

            save_rgb_channels(

                path,

                R,
                G,
                B

            )



            # =====================
            # STOCKAGE WORKFLOW
            # =====================

            st.session_state.S = S

            st.session_state.H = H

            st.session_state.O = O



            st.session_state.R = R

            st.session_state.G = G

            st.session_state.B = B



            st.session_state.palette = palette



            # passage SHO Lab

            st.session_state.workflow_step = 3



            st.success(

                "Composition SHO validée ✔️ Passage au SHO Lab"

            )


            st.rerun()
    # =====================================================
    # PREVIEW
    # =====================================================


    with col_right:


        st.subheader(

            "👁 Preview"

        )



        # recalcul dynamique

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



        # =========================
        # ZOOM INSPECTION
        # =========================

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
        # =========================
        # INFORMATIONS COURANTES
        # =========================

        st.divider()


        st.caption(

            f"""
🎨 Palette active : **{palette}**

Valeurs :

R:SII = {r_s:.2f}

R:Hα = {r_h:.2f}

G:Hα = {g_h:.2f}

G:OIII = {g_o:.2f}

B:OIII = {b_o:.2f}

"""

        )