# ==========================================================
# Astro IA
# Page 02 - Analyse astrophotographique
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


from core.simbad_client import query_object

from core.project_manager import (
    create_project,
    set_active_project,
    get_active_project
)


# ==========================================================
# TITRE
# ==========================================================

st.title(
    "🤖 Analyse astrophotographique"
)





# ==========================================================
# INITIALISATION SESSION
# ==========================================================


if "vision_result" not in st.session_state:

    st.session_state.vision_result = None



if "vision_preview" not in st.session_state:

    st.session_state.vision_preview = None



if "siril_result" not in st.session_state:

    st.session_state.siril_result = None



if "analysis_ready" not in st.session_state:

    st.session_state.analysis_ready = False





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

            text="Filtrage catalogue..."

        )




        st.session_state.siril_result = result




        progress.progress(

            100,

            text="Analyse Siril terminée ✅"

        )




        st.success(

            "✅ Analyse Siril terminée."

        )



    except Exception as e:


        progress.empty()



        st.error(

            f"Erreur Siril : {e}"

        )
# ==========================================================
# PREPARATION CONTEXTE IA
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



    filtered_objects = filter_catalog(

        objects,

        max_mag=16

    )





    # ======================================================
    # RESUME CATALOGUE POUR IA
    # ======================================================


    summary = create_ai_summary(

        filtered_objects

    )





    # ======================================================
    # ENRICHISSEMENT SIMBAD
    # VOCABULAIRE ASTRONOMIQUE
    # ======================================================


    simbad_vocab = []



    for obj in filtered_objects:



        name = obj.get(

            "name",

            None

        )



        if not name:

            continue



        try:



            info = query_object(

                name

            )



            if info:


                simbad_vocab.append(

                    info

                )



        except Exception:



            continue





    # ======================================================
    # CONTEXTE FINAL POUR QWEN3
    # ======================================================


    ai_context = {


        "fits":

            context,



        "fov":

            fov,



        "catalogue":

            summary,



        "simbad":

            simbad_vocab,



        "objects_count":

            len(filtered_objects)

    }




    st.session_state.objects = filtered_objects


    # ======================================================
    # AFFICHAGE RESUME CATALOGUE
    # ======================================================


    st.info(

        f"⭐ {len(filtered_objects)} objets détectés "
    "après filtrage du catalogue Siril."

    )



    with st.expander(

        "🔽 Voir les objets détectés"

    ):


        if filtered_objects:


            st.dataframe(

                filtered_objects,

                use_container_width=True

            )


        else:


            st.info(

                "Aucun objet conservé."

            )



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
            # CREATION PREVIEW LLaVA
            # ==================================================


            progress_ai.progress(

                15,

                text="Création preview LLaVA..."

            )



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





            # ==================================================
            # ANALYSE VISUELLE LLaVA
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





            # nettoyage répétitions éventuelles


            if vision_result:



                vision_result = vision_result.strip()



                vision_result = vision_result.replace(

                    "Observation visuelle uniquement.\n\n",

                    ""

                )



                vision_result = vision_result.replace(

                    "Observation visuelle uniquement.",

                    ""

                ).strip()



                st.session_state.vision_result = vision_result



            else:


                st.session_state.vision_result = None






            # ==================================================
            # ANALYSE SCIENTIFIQUE QWEN3
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



                vision_result=st.session_state.get(

                    "vision_result",

                    None

                )

            )





            progress_ai.progress(

                100,

                text="Rapport IA terminé ✅"

            )





            st.session_state.analysis_result = response
            st.session_state.analysis_context = context

            # ==================================================
            # CREATION PROJET ASTRO IA
            # ==================================================

            project_path = create_project(
                workdir,
                context["object"]
            )


            st.session_state.project_path = str(
                project_path
            )


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


vision_result = st.session_state.get(

    "vision_result",

    None

)




with st.expander(

    "👁️ Observation visuelle LLaVA"

):


    if vision_result:



        st.markdown(

            vision_result

        )



    else:



        st.info(

            "Aucune analyse visuelle LLaVA disponible."

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