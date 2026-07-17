# ==========================================================
# Astro IA
# Page 00 - Configuration
# Gestion configuration + projet actif
# ==========================================================


import streamlit as st

from pathlib import Path



from core.config import (
    load_config,
    save_config,
    restore_default
)



from core.project_manager import (
    create_project,
    list_projects,
    set_active_project,
    get_active_project,
    get_projects_root
)





# ==========================================================
# TITRE
# ==========================================================


st.title(
    "⚙️ Configuration Astro IA"
)


# ==========================================================
# CHARGEMENT CONFIG
# ==========================================================


config = load_config()



# ==========================================================
# DOSSIER DE TRAVAIL ACTIF
# ==========================================================


workdir = st.session_state.get(
    "workdir"
)

if not workdir:

    temp_dir = st.session_state.get("temp_dir")


    if temp_dir:

        workdir = str(
            Path(temp_dir).parent
        )

        st.session_state.workdir = workdir



# ==========================================================
# GESTION PROJET
# ==========================================================


st.header(
    "📂 Projet astrophotographique"
)





# ==========================================================
# DOSSIER PROJETS
# ==========================================================


projects_root = None



if workdir:


    projects_root = get_projects_root(

        workdir

    )


if projects_root:


    st.caption(

        f"📁 Les projets sont stockés ici : {projects_root}"

    )


else:


    st.info(

        """
📂 Aucun dossier de traitement actif.

Choisissez d'abord vos images dans la page FITS.
Le dossier x_projects sera créé automatiquement
à côté du dossier de traitement.
"""

    )





active_project = get_active_project()





if active_project:


    st.success(

        f"📂 Projet actif : {active_project}"

    )


else:


    st.info(

        "Aucun projet actif."

    )







tab1, tab2 = st.tabs(

    [

        "➕ Nouveau projet",

        "📁 Ouvrir un projet"

    ]

)







# ==========================================================
# CREATION NOUVEAU PROJET
# ==========================================================


with tab1:



    project_name = st.text_input(

        "Nom du projet",

        placeholder="NGC6871_20260716"

    )



    object_name = st.text_input(

        "Objet astronomique",

        placeholder="NGC6871"

    )






    if st.button(

        "🚀 Créer le projet",

        type="primary"

    ):



        if project_name:



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



        else:



            st.warning(

                "Nom de projet obligatoire."

            )









# ==========================================================
# OUVERTURE PROJET EXISTANT
# ==========================================================


with tab2:


    if not workdir:


        st.info(

            "📷 Sélectionnez d'abord un dossier FITS."

        )


        projects = []


    else:


        projects = list_projects(

            workdir

        )


    if projects:



        selected = st.selectbox(

            "Projet disponible",

            projects

        )




        if st.button(

            "📂 Ouvrir le projet"

        ):



            project_path = (

                projects_root

                /

                selected

            )



            set_active_project(

                project_path

            )



            st.success(

                f"✅ Projet chargé : {project_path}"

            )



            st.rerun()





    else:



        st.info(

            "Aucun projet existant."

        )





st.divider()
# ==========================================================
# FIN CONFIGURATION
# ==========================================================


# ==========================================================
# INFORMATIONS PROJET
# ==========================================================


st.divider()



if active_project:


    st.subheader(
        "📌 Informations projet actif"
    )


    st.write(
        f"**Chemin :** {active_project}"
    )


    st.write(
        """
Le projet contient :

- les données FITS associées
- les rapports IA
- les exports
- le workflow sauvegardé

La reprise d'une session ne relance pas
les analyses IA automatiquement.
"""
    )



# ==========================================================
# RETOUR WORKFLOW
# ==========================================================


st.divider()



if active_project:


    if st.button(
        "🧭 Ouvrir le workflow"
    ):


        st.switch_page(

            "ui/pages/04_Workflow.py"

        )



# ==========================================================
# RETOUR FITS
# ==========================================================


if st.button(

    "📷 Aller vers FITS"

):


    st.switch_page(

        "ui/pages/01_FITS.py"

    )