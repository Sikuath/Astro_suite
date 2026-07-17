# ==========================================================
# Astro IA
# Page 00 - Configuration
# Gestion configuration + projet actif
# ==========================================================


import streamlit as st

from pathlib import Path



from core.config import (
    load_config
)



from core.project_manager import (
    list_projects,
    set_active_project,
    get_active_project,
    get_projects_root,
    delete_project
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
# RESTAURATION JSON + SESSION
# ==========================================================


workdir = st.session_state.get(
    "workdir"
)



# Si absent, chercher dans la configuration

if not workdir:


    workdir = config.get(
        "paths",
        {}
    ).get(
        "images",
        None
    )



    if workdir:


        st.session_state.workdir = workdir





# ==========================================================
# PROJET ASTROPHOTOGRAPHIQUE
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

Sélectionnez d'abord vos images dans la page FITS.
Les projets seront créés automatiquement lors
de la génération d'un rapport IA.
"""

    )







# ==========================================================
# PROJET ACTIF
# ==========================================================


active_project = get_active_project()





if active_project:


    st.success(

        f"📂 Projet actif : {active_project}"

    )


else:


    st.info(

        "Aucun projet actif."

    )







st.divider()





# ==========================================================
# OUVERTURE PROJET EXISTANT
# ==========================================================


st.subheader(

    "📁 Ouvrir un projet existant"

)





if workdir:


    projects = list_projects(

        workdir

    )


else:


    projects = []





if projects:



    selected = st.selectbox(

        "Projet disponible",

        projects

    )





    if st.button(

        "📂 Charger ce projet"

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







# ==========================================================
# SUPPRESSION PROJETS
# ==========================================================


st.divider()



st.subheader(

    "🧹 Supprimer des projets"

)





if projects:



    delete_list = []



    for project in projects:


        if st.checkbox(

            project,

            key=f"delete_{project}"

        ):


            delete_list.append(

                project

            )





    if delete_list:


        st.warning(

            f"{len(delete_list)} projet(s) sélectionné(s)"

        )





        if st.button(

            "🗑️ Supprimer les projets sélectionnés",

            type="primary"

        ):



            deleted = 0



            for project in delete_list:



                project_path = (

                    projects_root

                    /

                    project

                )



                if delete_project(

                    project_path

                ):


                    deleted += 1





            st.success(

                f"✅ {deleted} projet(s) supprimé(s)"

            )



            st.rerun()





else:


    st.info(

        "Aucun projet à supprimer."

    )







# ==========================================================
# INFORMATIONS PROJET ACTIF
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
automatiquement les analyses IA.
"""

    )







# ==========================================================
# NAVIGATION WORKFLOW
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

    "📷 Nouveau Projet"

):


    st.switch_page(

        "ui/pages/01_FITS.py"

    )