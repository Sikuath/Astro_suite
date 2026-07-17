import streamlit as st
from pathlib import Path
import shutil

from core.fits_reader import read_fits_header
from core.config import load_config
from core.optic_detector import detect_optic

# ==========================================================
# FORMATAGE AFFICHAGE
# ==========================================================

def format_value(value, decimals=2):

    try:

        value = float(value)

        return f"{value:.{decimals}f}".replace(".", ",")

    except Exception:

        return value

# ==========================================================
# NETTOYAGE DOSSIER TEMPORAIRE
# ==========================================================

def clean_temp_folder(temp_dir):


    if temp_dir.exists():


        for item in temp_dir.iterdir():


            try:


                if item.is_file():

                    item.unlink()


                elif item.is_dir():

                    shutil.rmtree(item)


            except Exception as e:


                st.warning(
                    f"Impossible de supprimer {item}: {e}"
                )


    else:


        temp_dir.mkdir(
            parents=True,
            exist_ok=True
        )



# ==========================================================
# STYLE LOCAL PAGE FITS
# ==========================================================

st.markdown(
    """
    <style>

    .fits-info {
        font-size: 0.82rem;
        line-height: 1.5;
        color: #eeeeee;
    }

    .fits-info b {
        color: #38bdf8;
    }

    .fits-title {
        font-size: 1.1rem;
        color: #facc15;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# ==========================================================
# PAGE
# ==========================================================

st.title(
    "📷 Analyse FITS"
)


st.write(
    "Chargement et lecture des métadonnées astrophotographiques."
)



# ==========================================================
# CONFIGURATION
# ==========================================================

config = load_config()


image_root = Path(
    config["paths"]["images"]
)



if not image_root.exists():

    st.error(
        f"Dossier images introuvable : {image_root}"
    )

    st.stop()



# ==========================================================
# DOSSIER TEMPORAIRE
# ==========================================================

temp_dir = (

    image_root

    /

    "x_temp"

)



# nettoyage au premier passage uniquement

if "temp_cleaned" not in st.session_state:


    clean_temp_folder(
        temp_dir
    )


    st.session_state.temp_cleaned = True



# ==========================================================
# SELECTION FITS
# ==========================================================

st.header(
    "📂 Sélection du fichier"
)



fits_file = st.file_uploader(
    "Choisir une image FITS",
    type=[
        "fit",
        "fits",
        "fts"
    ]
)



# ==========================================================
# COPIE DANS X_TEMP
# ==========================================================

if fits_file:


    original_name = Path(
        fits_file.name
    )



    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )



    temp_path = (

        temp_dir

        /

        original_name.name

    )



    with open(
        temp_path,
        "wb"
    ) as f:


        f.write(
            fits_file.getbuffer()
        )



    st.session_state.image_path = str(
        temp_path.resolve()
    )


    st.session_state.image_name = (

        original_name.name

    )


    st.session_state.temp_dir = str(
        temp_dir.resolve()
    )



    try:


        header = read_fits_header(
            temp_path
        )


        st.session_state.fits_header = header



        st.success(
            "✅ FITS lu correctement"
        )


        st.caption(
            f"📁 Travail temporaire : {temp_path}"
        )



    except Exception as e:


        st.error(
            f"Erreur lecture FITS : {e}"
        )

        st.stop()



# ==========================================================
# AFFICHAGE HEADER
# ==========================================================

if st.session_state.get(
    "fits_header",
    {}
):


    header = st.session_state.fits_header



    st.divider()


    st.header(
        "🔭 Informations acquisition"
    )



    col1, col2, col3 = st.columns(3)



    with col1:


        st.markdown(
            f"""

<div class="fits-info">

<div class="fits-title">
🔭 Acquisition
</div>

<b>Objet :</b><br>
{header.get('OBJECT','Inconnu')}

<br><br>

<b>Optique :</b><br>
{
detect_optic(
    header.get(
        "FOCALLEN",
        0
    )
)
}

<br><br>

<b>Focale :</b><br>
{header.get('FOCALLEN','?')} mm

<br><br>

<b>Temps pose :</b><br>
{header.get('EXPTIME','?')} s

</div>

            """,
            unsafe_allow_html=True
        )



    with col2:


        st.markdown(
            f"""

<div class="fits-info">

<div class="fits-title">
📷 Caméra
</div>

<b>Instrument :</b><br>
{header.get('INSTRUME','Inconnu')}

<br><br>

<b>Pixel :</b><br>
{header.get('XPIXSZ','?')} × {header.get('YPIXSZ','?')} µm

<br><br>

<b>Gain :</b><br>
{header.get('GAIN','?')}

<br><br>

<b>Offset :</b><br>
{header.get('OFFSET','?')}

<br><br>

<b>CCD :</b><br>
{header.get('CCD-TEMP','?')} °C

</div>

            """,
            unsafe_allow_html=True
        )



    with col3:


        st.markdown(
            f"""

<div class="fits-info">

<div class="fits-title">
🌌 Céleste
</div>

<b>RA :</b><br>
{header.get('RA','?')}

<br><br>

<b>DEC :</b><br>
{header.get('DEC','?')}

<br><br>

<b>Date :</b><br>
{header.get('DATE-OBS','?')}

<br><br>

<b>Filtre :</b><br>
{header.get('FILTER','Inconnu')}

</div>

            """,
            unsafe_allow_html=True
        )



# ==========================================================
# HEADER COMPLET
# ==========================================================

    with st.expander(
        "Afficher le header FITS complet"
    ):


        st.json(
            dict(header)
        )



# ==========================================================
# VALIDATION
# ==========================================================

    st.divider()



    if st.button(
        "✅ Valider cette image",
        type="primary"
    ):


        st.session_state.fits_loaded = True


        st.session_state.object_name = header.get(
            "OBJECT",
            "Inconnu"
        )


        st.session_state.camera = header.get(
            "INSTRUME",
            "Inconnue"
        )


        st.session_state.focal_length = header.get(
            "FOCALLEN",
            ""
        )


        st.session_state.exposure = header.get(
            "EXPTIME",
            ""
        )


        st.session_state.gain = header.get(
            "GAIN",
            ""
        )


        st.session_state.ccd_temp = header.get(
            "CCD-TEMP",
            ""
        )


        st.session_state.ra = header.get(
            "RA",
            ""
        )


        st.session_state.dec = header.get(
            "DEC",
            ""
        )


        st.success(
            "✅ FITS validé"
        )


        st.switch_page(
            "ui/pages/02_Analyse.py"
        )