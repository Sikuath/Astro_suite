# ==========================================================
# Astro IA
# Page 02 - Analyse acquisition
# PARTIE 1/2
# ==========================================================


import streamlit as st
from pathlib import Path


from core.fov_calculator import calculate_fov
from core.siril_runner import SirilRunner
from core.siril_analyser import SirilAnalyser


from core.catalog_filter import (
    filter_catalog,
    create_ai_summary
)


from core.ollama_client import ask_ollama
from core.config import load_config


from core.vision_client import analyse_image
from core.vision_preview import create_vision_preview



# ==========================================================
# TITRE
# ==========================================================

st.title(
    "🤖 Analyse astrophotographique"
)



# ==========================================================
# VERIFICATION FITS
# ==========================================================

if not st.session_state.get(
    "fits_loaded",
    False
):

    st.warning(
        "⚠️ Aucun FITS validé."
    )

    st.stop()



header = st.session_state.get(
    "fits_header",
    {}
)



# ==========================================================
# CONFIGURATION
# ==========================================================

config = load_config()



siril_path = (

    config
    .get(
        "paths",
        {}
    )
    .get(
        "siril"
    )

)



if not siril_path:

    st.error(
        "Chemin Siril absent du config.json"
    )

    st.stop()



# ==========================================================
# IMAGE FITS
# ==========================================================

fits_path = st.session_state.get(
    "image_path"
)



if not fits_path:

    st.error(
        "Aucun FITS temporaire trouvé."
    )

    st.stop()



fits_path = Path(
    fits_path
).resolve()



if not fits_path.exists():

    st.error(
        "Le fichier FITS n'existe plus."
    )

    st.stop()



workdir = fits_path.parent




# ==========================================================
# OUTILS
# ==========================================================

def safe_float(
    value,
    default=0
):

    try:

        return float(value)

    except Exception:

        return default




# ==========================================================
# DONNEES ACQUISITION FITS
# ==========================================================

context = {


    "object":

        header.get(
            "OBJECT",
            "Inconnu"
        ),



    "ra":

        safe_float(
            header.get(
                "RA",
                0
            )
        ),



    "dec":

        safe_float(
            header.get(
                "DEC",
                0
            )
        ),



    "instrument":

        header.get(
            "INSTRUME",
            "Inconnu"
        ),



    "telescope":

        header.get(
            "TELESCOP",
            "Inconnu"
        ),



    "focal":

        safe_float(
            header.get(
                "FOCALLEN",
                0
            )
        ),



    "pixel":

        safe_float(
            header.get(
                "XPIXSZ",
                3.76
            ),
            3.76
        ),



    "fits_exposure":

    safe_float(
        header.get(
            "EXPTIME",
            0
        )
    ),



    "gain":

        header.get(
            "GAIN",
            "?"
        ),



    "temperature":

        header.get(
            "CCD-TEMP",
            "?"
        )

}




# ==========================================================
# CALCUL FOV
# ==========================================================

st.header(
    "📐 Champ photographié"
)



fov = calculate_fov(

    focal_length=context["focal"],

    pixel_size=context["pixel"],

    sensor_width=23.5,

    sensor_height=15.7

)



st.session_state.fov = fov




c1, c2, c3 = st.columns(3)



with c1:

    st.metric(
        "Horizontal",
        f"{fov['fov_horizontal_deg']}°"
    )



with c2:

    st.metric(
        "Vertical",
        f"{fov['fov_vertical_deg']}°"
    )



with c3:

    st.metric(
        "Échantillonnage",
        f"{fov['sampling_arcsec_pixel']} arcsec/pixel"
    )





# ==========================================================
# ANALYSE SIRIL
# ==========================================================

st.header(
    "🌌 Analyse du champ"
)



if "siril_result" not in st.session_state:

    st.session_state.siril_result = None




if st.button(
    "🚀 Lancer analyse Siril",
    type="primary"
):


    progress = st.progress(
        0,
        text="Préparation..."
    )



    def update_log(line):

        pass



    try:


        progress.progress(
            20,
            text="Préparation image..."
        )



        runner = SirilRunner(
            siril_path
        )



        analyser = SirilAnalyser(
            runner
        )



        progress.progress(
            40,
            text="Analyse astrométrique Siril..."
        )



        result = analyser.analyse_field(

            workdir,

            fits_path,

            callback=update_log

        )



        progress.progress(
            80,
            text="Lecture catalogue..."
        )



        st.session_state.siril_result = result



        progress.progress(
            100,
            text="Analyse terminée ✅"
        )



        count = len(

            result.get(
                "objects",
                []
            )

        )



        st.success(

            f"✅ Analyse terminée ({count} objets détectés)"

        )



    except Exception as e:


        progress.empty()


        st.error(

            f"Erreur Siril : {e}"

        )





# ==========================================================
# RESULTATS CATALOGUE
# ==========================================================

result = st.session_state.get(
    "siril_result",
    None
)



filtered_objects = []



if result:


    objects = result.get(
        "objects",
        []
    )



    st.subheader(

        f"⭐ Objets détectés par Siril : {len(objects)}"

    )



    if objects:


        filtered_objects = filter_catalog(

            objects,

            max_mag=16

        )



        st.write(

            f"Objets retenus pour analyse IA : "
            f"{len(filtered_objects)}"

        )



        st.dataframe(

            filtered_objects,

            width="stretch"

        )



    else:


        st.info(

            "Aucun objet retourné par Siril."

        )



    st.session_state.objects = filtered_objects






# ==========================================================
# PREPARATION CONTEXTE IA
# ==========================================================

st.divider()


st.header(
    "🧠 Analyse IA"
)



if result:


    summary = create_ai_summary(

        filtered_objects

    )



    ai_context = {


        "fits":

            context,


        "fov":

            fov,


        "objects":

            summary,


        "siril":

            {


                "csv":

                    result.get(
                        "csv",
                        ""
                    ),



                "objects_detected":

                    len(
                        result.get(
                            "objects",
                            []
                        )
                    ),



                "objects_selected":

                    len(
                        filtered_objects
                    )

            }

    }



    st.session_state.ai_context = ai_context
    # ======================================================
    # GENERATION RAPPORT IA
    # ======================================================


    if st.button(

        "🤖 Générer rapport IA",

        type="primary"

    ):


        ollama_config = config.get(

            "ollama",

            {}

        )



        progress_ai = st.progress(

            0,

            text="Préparation IA..."

        )



        try:



            # ==================================================
            # ETAPE 1
            # CREATION UNIQUE PREVIEW VISION
            # ==================================================


            progress_ai.progress(

                15,

                text="Création preview couleur pour LLaVA..."

            )


            #
            # UN SEUL APPEL ICI
            #
            vision_path = create_vision_preview(

                fits_path

            )



            vision_path = Path(

                vision_path

            ).resolve()



            if not vision_path.exists():

                raise FileNotFoundError(

                    f"Preview absente : {vision_path}"

                )



            st.session_state.vision_preview = str(

                vision_path

            )



            st.success(

                f"✅ Preview créée : {vision_path}"

            )



            # DEBUG IMAGE ENVOYEE
            with st.expander(

                "🖼️ Debug image envoyée à LLaVA"

            ):


                st.write(

                    "FITS source :"

                )


                st.code(

                    str(fits_path)

                )



                st.write(

                    "PNG envoyé :"

                )


                st.code(

                    str(vision_path)

                )



                st.write(

                    "Existe :",

                    vision_path.exists()

                )



                st.write(

                    "Taille :",

                    vision_path.stat().st_size

                )



                st.image(

                    vision_path,

                    width=800

                )





            # ==================================================
            # ETAPE 2
            # ANALYSE LLaVA
            # ==================================================


            progress_ai.progress(

                35,

                text="Analyse visuelle LLaVA..."

            )



            vision_model = ollama_config.get(

                "vision_model",

                "llava:7b"

            )



            vision_result = analyse_image(

                vision_path,

                model=vision_model

            )



            st.session_state.vision_result = vision_result

        
            # ==================================================
            # ETAPE 3
            # ANALYSE SCIENTIFIQUE QWEN
            # ==================================================


            progress_ai.progress(

                60,

                text="Analyse scientifique Astro IA..."

            )



            response = ask_ollama(

                model=ollama_config.get(

                    "default_model",

                    "astro-expert:latest"

                ),



                acquisition=context,



                fov=fov,



                simbad_data=ai_context,



                workflow=st.session_state.get(

                    "workflow",

                    None

                ),



                vision_result=vision_result

            )





            progress_ai.progress(

                100,

                text="Rapport IA terminé ✅"

            )



            st.session_state.analysis_result = response



            st.session_state.analysis_ready = True



            st.success(

                "✅ Rapport IA généré."

            )



        except Exception as e:


            progress_ai.empty()


            st.error(

                f"Erreur IA : {e}"

            )






# ==========================================================
# AFFICHAGE PREVIEW LLaVA
# ==========================================================


vision_preview = st.session_state.get(

    "vision_preview",

    None

)



if vision_preview:


    with st.expander(

        "🖼️ Preview utilisée par LLaVA"

    ):


        st.image(

            vision_preview,

            width=800

        )





# ==========================================================
# AFFICHAGE RESULTAT LLaVA
# ==========================================================


if st.session_state.get(

    "vision_result",

    None

):


    with st.expander(

        "👁️ Observation visuelle LLaVA"

    ):


        st.write(

            st.session_state.vision_result

        )





# ==========================================================
# RAPPORT FINAL
# ==========================================================


if st.session_state.get(

    "analysis_ready",

    False

):


    st.success(

        "✅ Rapport prêt."

    )



    if st.button(

        "➡ Voir le rapport"

    ):


        st.switch_page(

            "ui/pages/03_Rapport.py"

        )