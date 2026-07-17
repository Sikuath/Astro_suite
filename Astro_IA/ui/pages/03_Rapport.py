# ==========================================================
# Astro IA
# Page 03 - Rapport astrophotographique
# PARTIE 1/2
# ==========================================================


import streamlit as st

import json
from datetime import datetime


from pathlib import Path
from core.project_manager import (
    create_project,
    set_active_project,
    get_active_project
)
from core.workflow_manager import get_workflow


# ==========================================================
# TITRE
# ==========================================================


st.title(

    "📋 Rapport astrophotographique"

)
### debug a suppier les 3 lignes dessous
#st.write(
#    "DEBUG SESSION",
#    st.session_state
#)



# ==========================================================
# VERIFICATION
# ==========================================================


if not st.session_state.get(

    "analysis_ready",

    False

):


    st.warning(

        "Aucune analyse disponible."

    )


    st.stop()






# ==========================================================
# WORKFLOW
# ==========================================================


# ==========================================================
# CREATION PROJET SI NECESSAIRE
# ==========================================================


project_path = get_active_project()



if not project_path:


    st.warning(
        "📂 Aucun projet associé à cette analyse."
    )


    st.subheader(
        "Créer le projet astrophotographique"
    )



    header = st.session_state.get(
        "fits_header",
        {}
    )



    default_object = header.get(
        "OBJECT",
        "Objet_inconnu"
    )



    project_name = st.text_input(

        "Nom du projet",

        value=default_object

    )


    object_name = st.text_input(

        "Objet astronomique",

        value=default_object

    )



    if st.button(

        "🚀 Créer le projet",

        type="primary"

    ):


        workdir = st.session_state.get(
            "workdir"
        )


        if not workdir:


            st.error(
                "Aucun dossier de traitement disponible."
            )

            st.stop()



        project_path = create_project(

            workdir,

            project_name,

            object_name

        )



        set_active_project(

            project_path

        )


        st.success(

            f"✅ Projet créé : {project_path}"

        )


        st.rerun()



    st.stop()



if project_path:


    workflow = get_workflow(

        project_path

    )


    report_done = False


    for section in workflow:

        for step in section.get("steps", []):

            if step["id"] == "report":

                report_done = step["done"]



    if report_done:


        st.success(

            "✅ Rapport déjà validé dans le workflow."

        )


    else:


        if st.button(

            "✅ Valider le rapport dans le workflow"

        ):


            toggle_step(

                project_path,

                "report"

            )


            st.success(

                "Rapport ajouté au workflow."

            )


            st.rerun()







# ==========================================================
# RECUPERATION DONNEES
# ==========================================================


header = st.session_state.get(

    "fits_header",

    {}

)



analysis = st.session_state.get(

    "analysis_result",

    ""

)



vision_result = st.session_state.get(

    "vision_result",

    None

)



fov = st.session_state.get(

    "fov",

    {}

)



objects = st.session_state.get(

    "objects",

    []

)







# ==========================================================
# INFORMATIONS ACQUISITION
# ==========================================================


st.header(

    "📷 Acquisition"

)





col1, col2 = st.columns(2)





with col1:


    st.write(

        f"**Objet :** {header.get('OBJECT','?')}"

    )


    st.write(

        f"**Instrument indiqué FITS :** {header.get('INSTRUME','?')}"

    )


    st.write(

        f"**Télescope / système :** {header.get('TELESCOP','?')}"

    )


    st.write(

        f"**Focale :** {header.get('FOCALLEN','?')} mm"

    )





with col2:


    st.write(

        f"**Pose :** {header.get('EXPTIME','?')} s"

    )


    st.write(

        f"**Gain :** {header.get('GAIN','?')}"

    )


    st.write(

        f"**Température capteur :** {header.get('CCD-TEMP','?')} °C"

    )


    st.write(

        f"**Caméra :** {header.get('INSTRUME','?')}"

    )





st.info(

"""
Les informations ci-dessus proviennent des métadonnées FITS.

Elles constituent les données d'acquisition de référence.
"""

)








# ==========================================================
# POSITION DU CHAMP
# ==========================================================


st.header(

    "🌌 Position du champ"

)





c1, c2 = st.columns(2)





with c1:


    st.write(

        f"RA : {header.get('RA','?')}"

    )




with c2:


    st.write(

        f"DEC : {header.get('DEC','?')}"

    )





st.info(

"""
Les coordonnées proviennent directement du header FITS.

Elles sont utilisées comme référence pour l'analyse.
"""

)






# ==========================================================
# CHAMP OPTIQUE
# ==========================================================


st.header(

    "📐 Champ photographié"

)





if fov:


    c1, c2, c3 = st.columns(3)




    with c1:


        st.metric(

            "Largeur",

            f"{fov.get('fov_horizontal_deg')}°"

        )



    with c2:


        st.metric(

            "Hauteur",

            f"{fov.get('fov_vertical_deg')}°"

        )



    with c3:


        st.metric(

            "Échantillonnage",

            f"{fov.get('sampling_arcsec_pixel')}\"/pix"

        )
# ==========================================================
# OBJETS CATALOGUES SIRIL
# ==========================================================


st.header(

    "⭐ Objets catalogués dans le champ"

)



st.write(

    f"{len(objects)} objets conservés après filtrage Siril."

)





with st.expander(

    "🔎 Voir les objets et informations SIMBAD"

):


    if objects:


        for obj in objects:


            st.markdown(

                f"""
### {obj.get('name','?')}

Type catalogue :
{obj.get('type','?')}

"""

            )



            if "vocabulary" in obj:


                st.write(

                    "Vocabulaire astronomique :"

                )


                for word in obj["vocabulary"]:


                    st.write(

                        f"- {word}"

                    )



            st.divider()



    else:


        st.info(

            "Aucun objet."

        )






st.caption(

"""
Les objets proviennent du catalogue Siril.

Ils indiquent uniquement des sources cataloguées
présentes dans le champ.

Ils ne constituent pas une preuve de qualité d'image.
"""

)








# ==========================================================
# ANALYSE VISUELLE LLAVA
# ==========================================================


st.header(

    "👁️ Analyse visuelle LLaVA"

)





if vision_result:


    st.info(

"""
Cette analyse est réalisée par LLaVA.

Elle correspond uniquement à une observation visuelle.
Elle ne remplace pas les mesures scientifiques :
FWHM, HFR, SNR, excentricité, suivi ou photométrie.
"""

    )


    st.markdown(

        vision_result

    )



else:


    st.info(

        "Aucune analyse visuelle LLaVA disponible."

    )








# ==========================================================
# ANALYSE IA ASTRO (QWEN3)
# ==========================================================


st.header(

    "🤖 Analyse scientifique Astro IA"

)





if analysis:


    st.markdown(

        analysis

    )


else:


    st.warning(

        "Aucun rapport Astro IA généré."

    )








# ==========================================================
# RESUME MODELES UTILISES
# ==========================================================


st.header(

    "🧠 Modèles utilisés"

)





models_info = [

    "✅ Astro IA scientifique : modèle Ollama principal (Qwen3)"

]





if vision_result:


    models_info.append(

        "✅ Analyse visuelle : LLaVA 7B"

    )


else:


    models_info.append(

        "❌ Analyse visuelle : non utilisée"

    )





for item in models_info:


    st.write(

        item

    )








st.info(

"""
Architecture Astro IA :

- Qwen3 analyse les métadonnées FITS,
  le FOV, le catalogue et les règles scientifiques.

- LLaVA analyse uniquement l'aspect visuel
  de l'image.

- Les deux analyses restent séparées.

- Une interprétation visuelle ne peut jamais
  devenir une mesure scientifique.
"""

)








# ==========================================================
# EXPORT RAPPORT TXT
# ==========================================================


st.divider()



st.header(

    "💾 Export"

)





report_text = f"""

=====================================
Rapport Astro IA
=====================================


Date :

{datetime.now()}



=====================================
ACQUISITION FITS
=====================================


Objet :

{header.get('OBJECT','?')}



Instrument indiqué :

{header.get('INSTRUME','?')}



Télescope :

{header.get('TELESCOP','?')}



Focale :

{header.get('FOCALLEN','?')} mm



Temps de pose :

{header.get('EXPTIME','?')} s



Gain :

{header.get('GAIN','?')}



Température :

{header.get('CCD-TEMP','?')} °C





=====================================
POSITION
=====================================


RA :

{header.get('RA','?')}



DEC :

{header.get('DEC','?')}





=====================================
CHAMP OPTIQUE
=====================================


Largeur :

{fov.get('fov_horizontal_deg','?')} °



Hauteur :

{fov.get('fov_vertical_deg','?')} °



Echantillonnage :

{fov.get('sampling_arcsec_pixel','?')} arcsec/pixel






=====================================
CATALOGUE SIRIL
=====================================


Nombre objets conservés :

{len(objects)}



Le catalogue Siril est utilisé uniquement

comme référence de champ.

Il ne constitue pas une mesure

de qualité d'image.





=====================================
ANALYSE VISUELLE LLAVA
=====================================


{vision_result if vision_result else "Aucune analyse visuelle disponible."}






=====================================
ANALYSE ASTRO IA QWEN3
=====================================


{analysis}






=====================================
FIN DU RAPPORT

"""






st.download_button(

    "⬇ Télécharger le rapport TXT",

    report_text,

    file_name=

        f"rapport_{header.get('OBJECT','astro')}.txt",

    mime="text/plain"

)

# ==========================================================
# NAVIGATION
# ==========================================================


st.divider()


col1, col2 = st.columns(2)



with col1:


    if st.button(

        "⬅ Retour FITS"

    ):


        st.switch_page(

            "ui/pages/01_FITS.py"

        )





with col2:


    if st.button(

        "🧭 Ouvrir Workflow"

    ):


        # ==================================================
        # SAUVEGARDE RAPPORT AVANT WORKFLOW
        # ==================================================


        project_path = st.session_state.get(
            "project_path"
        )


        analysis = st.session_state.get(
            "analysis_result",
            None
        )


        if project_path and analysis:


            reports_dir = Path(project_path) / "reports"


            reports_dir.mkdir(
                parents=True,
                exist_ok=True
            )



            # -----------------------------
            # TXT
            # -----------------------------


            txt_file = reports_dir / "rapport_IA.txt"


            with open(
                txt_file,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    analysis
                )



            # -----------------------------
            # JSON
            # -----------------------------
            context = st.session_state.get(
                "analysis_context",
                {}
            )

            json_file = reports_dir / "rapport_IA.json"



            report_data = {


                "date":

                    datetime.now().isoformat(),



                "objet":

                    context.get(
                        "object",
                        "Inconnu"
                    ),



                "fits":

                    context,



                "fov":

                    fov,



                "vision":

                    st.session_state.get(
                        "vision_result",
                        None
                    ),



                "rapport":

                    analysis

            }



            with open(
                json_file,
                "w",
                encoding="utf-8"
            ) as f:


                json.dump(

                    report_data,

                    f,

                    indent=4,

                    ensure_ascii=False

                )



            st.success(
                "💾 Rapport sauvegardé dans le projet."
            )


        else:


            st.warning(
                "⚠️ Aucun rapport IA à sauvegarder."
            )



        st.switch_page(

            "ui/pages/04_Workflow.py"

        )