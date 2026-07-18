import streamlit as st
from pathlib import Path
import shutil
import json


from core.fits_reader import read_fits_header
from core.config import load_config
from core.optic_detector import detect_optic
from core.astro_context import (
    build_astro_context,
    inject_astro_context
)


# ==========================================================
# FORMATAGE
# ==========================================================

def format_value(value, decimals=2):

    if value is None:
        return "Inconnu"

    try:

        value = float(value)

        return (
            f"{value:.{decimals}f}"
            .replace(".", ",")
        )

    except:

        return str(value)



def format_time(seconds):

    try:

        seconds = int(seconds)

        h = seconds // 3600

        m = (seconds % 3600) // 60

        s = seconds % 60


        if h:

            return f"{h}h {m}min"

        elif m:

            return f"{m}min {s}s"

        else:

            return f"{s}s"


    except:

        return "?"



def format_ra(header):

    if header.get("OBJCTRA"):

        return header["OBJCTRA"]


    try:

        ra = float(
            header.get("RA")
        )


        total_hours = ra / 15

        h = int(total_hours)

        m = int(
            (total_hours-h)*60
        )

        s = (
            (total_hours-h)*60-m
        )*60


        return (
            f"{h:02d}h "
            f"{m:02d}m "
            f"{s:05.2f}s"
        )


    except:

        return "?"




def format_dec(header):

    if header.get("OBJCTDEC"):

        return header["OBJCTDEC"]


    try:

        dec = float(
            header.get("DEC")
        )


        sign = "+"

        if dec < 0:

            sign = "-"


        dec = abs(dec)


        d = int(dec)

        m = int(
            (dec-d)*60
        )

        s = (
            (dec-d)*60-m
        )*60


        return (
            f"{sign}{d:02d}° "
            f"{m:02d}' "
            f"{s:05.2f}\""
        )


    except:

        return "?"



# ==========================================================
# SESSION ASTRO IA
# ==========================================================


def get_latest_session(config):


    try:

        folder = Path(
            config["paths"]["data_sessions"]
        )


    except:

        return None



    if not folder.exists():

        return None



    files = sorted(

        folder.glob(
            "astro_session_*.json"
        ),

        reverse=True

    )


    if not files:

        return None



    return files[0]





def load_session_json(config):


    session_file = get_latest_session(
        config
    )


    if not session_file:

        return {}



    try:

        with open(

            session_file,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)



    except:

        return {}




# ==========================================================
# NETTOYAGE TEMP
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
# STYLE
# ==========================================================


st.markdown(

"""
<style>

.fits-info {

font-size:0.82rem;
line-height:1.5;
color:#eeeeee;

}


.fits-info b {

color:#38bdf8;

}


.fits-title {

font-size:1.1rem;
color:#facc15;

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
# CONFIG
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



session_data = load_session_json(
    config
)
# ==========================================================
# DOSSIER TEMPORAIRE
# ==========================================================

temp_dir = (

    image_root

    /

    "x_temp"

)



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
# COPIE TEMP
# ==========================================================


if fits_file:


    original_name = Path(
        fits_file.name
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


    try:


        header = read_fits_header(
            temp_path
        )


        st.session_state.fits_header = header


        # ======================================================
        # CONTEXTE CELESTE ASTRO IA
        # ======================================================

        try:

            celestial = build_astro_context(
                header
            )

            inject_astro_context(
                celestial,
                config["paths"]["data_sessions"]
            )

            st.session_state.celestial_context = celestial


        except Exception as e:

            st.warning(
                f"Contexte céleste indisponible : {e}"
            )

            st.session_state.celestial_context = {}

        
        st.success(
            "✅ FITS lu correctement"
        )



    except Exception as e:


        st.error(
            f"Erreur lecture FITS : {e}"
        )


        st.stop()




# ==========================================================
# AFFICHAGE
# ==========================================================


if st.session_state.get(
    "fits_header"
):


    header = st.session_state.fits_header



    st.divider()



    # ======================================================
    # VALIDATION AVANT AFFICHAGE DES DATAS
    # ======================================================

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
            ""
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


        st.session_state.session_data = session_data



        st.success(
            "✅ FITS validé"
        )


        st.switch_page(
            "ui/pages/02_Analyse.py"
        )



    st.caption(
        "Les données ci-dessous proviennent du header FITS "
        "et de la session Astro IA associée."
    )



    st.divider()



    st.header(
        "🔭 Informations acquisition"
    )



    col1, col2, col3, col4 = st.columns(
        4
    )



    # ======================================================
    # ACQUISITION
    # ======================================================

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
{format_value(header.get('FOCALLEN'))} mm


<br><br>


<b>Monture :</b><br>
{header.get('TELESCOP','Inconnu')}


</div>

""",

unsafe_allow_html=True

        )



    # ======================================================
    # CAMERA
    # ======================================================

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
{format_value(header.get('XPIXSZ'))}
×
{format_value(header.get('YPIXSZ'))}
µm


<br><br>


<b>Gain :</b><br>
{header.get('GAIN','?')}


<br><br>


<b>Offset :</b><br>
{header.get('OFFSET','?')}


<br><br>


<b>CCD :</b><br>
{format_value(header.get('CCD-TEMP'))} °C


</div>

""",

unsafe_allow_html=True

        )



    # ======================================================
    # FILTRES / SESSION ASTRO IA
    # ======================================================

    with col3:


        st.markdown(

"""

<div class="fits-info">

<div class="fits-title">
🌈 Filtres
</div>

""",

unsafe_allow_html=True

        )



        if session_data:


            st.write(
                f"Mode : **{session_data.get('mode','?')}**"
            )


            layers = session_data.get(
                "layers",
                {}
            )


            for name, data in layers.items():


                filt = data.get(
                    "filter",
                    name
                )


                stack = data.get(
                    "stack",
                    0
                )


                live = data.get(
                    "livetime",
                    0
                )


                unit = data.get(
                    "unit",
                    0
                )


                st.markdown(

f"""

<b>{filt}</b><br>

{stack} × {format_value(unit,0)} s

<br>

Total :
{format_time(live)}

<br><br>

""",

unsafe_allow_html=True

                )



            st.markdown(

f"""

<b>Intégration totale :</b><br>

{format_time(
    session_data.get(
        "total_livetime",
        0
    )
)}

</div>

""",

unsafe_allow_html=True

            )


        else:


            st.info(
                "Aucune session Astro IA trouvée"
            )



    # ======================================================
    # CELESTE
    # ======================================================

    with col4:


        celestial = session_data.get(
            "celestial",
            {}
        )


        ephem = celestial.get(
            "ephemeris",
            {}
        )


        obj = celestial.get(
            "object",
            {}
        )


        st.markdown(

    f"""

    <div class="fits-info">


    <div class="fits-title">
    🌌 Céleste
    </div>


    <b>Objet :</b><br>
    {obj.get("input_name","?")}


    <br><br>


    <b>Constellation :</b><br>
    {obj.get("constellation","?")}


    <br><br>


    <b>RA :</b><br>
    {format_ra(header)}


    <br><br>


    <b>DEC :</b><br>
    {format_dec(header)}


    <br><br>


    <b>Altitude :</b><br>
    {ephem.get("target",{}).get("altitude_deg","?")}°


    <br><br>


    <b>Masse d'air :</b><br>
    {ephem.get("target",{}).get("airmass","?")}


    <br><br>


    <b>Nuit astronomique :</b><br>
    {ephem.get("sun",{}).get("astronomical_night","?")}


    <br><br>


    <b>Lune / cible :</b><br>
    {ephem.get("moon",{}).get("distance_target_deg","?")}°


    </div>

    """,

    unsafe_allow_html=True

    )