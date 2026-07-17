# ==========================================================
# Astro IA
# Gestionnaire de projets astrophotographiques
# ==========================================================


from pathlib import Path
import json
from datetime import datetime




# ==========================================================
# RACINE DES PROJETS
# A côté de x_temp / images
# ==========================================================


from pathlib import Path


def get_projects_root(workdir):

    if not workdir:
        return None


    workdir = Path(workdir).resolve()


    # Si on est dans x_temp, remonter automatiquement
    if workdir.name == "x_temp":

        root = workdir.parent / "x_projects"

    else:

        root = workdir / "x_projects"


    root.mkdir(
        parents=True,
        exist_ok=True
    )


    return root





# ==========================================================
# NETTOYAGE NOM PROJET
# ==========================================================


def sanitize_name(name):


    forbidden = [

        "\\",
        "/",
        ":",
        "*",
        "?",
        "\"",
        "<",
        ">",
        "|"

    ]


    for char in forbidden:

        name = name.replace(

            char,

            "_"

        )


    return name.strip()





# ==========================================================
# CREATION PROJET
# ==========================================================


def create_project(

    workdir,

    name,

    object_name=None

):

    """
    Création :

    Traitement/x_projects/NOM_PROJET

    """

    name = sanitize_name(name)



    projects_root = get_projects_root(

        workdir

    )



    project_path = (

        projects_root

        /

        name

    )



    if project_path.exists():

        return project_path





    folders = [

        "fits",

        "previews",

        "reports",

        "exports",

        "logs"

    ]



    for folder in folders:


        (

            project_path

            /

            folder

        ).mkdir(

            parents=True,

            exist_ok=True

        )





    # fichier projet


    project = {


        "name":

            name,


        "object":

            object_name
            or
            "Inconnu",



        "created":

            datetime.now()
            .isoformat(),



        "status":

            "created",



        "workdir":

            str(workdir)

    }




    save_project_file(

        project_path,

        project

    )



    return project_path





# ==========================================================
# PROJECT.JSON
# ==========================================================


def get_project_file(project_path):


    return (

        Path(project_path)

        /

        "project.json"

    )






def save_project_file(

    project_path,

    data

):


    file = get_project_file(

        project_path

    )


    with open(

        file,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )






def load_project_file(

    project_path

):


    file = get_project_file(

        project_path

    )


    if not file.exists():

        return {}



    try:


        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)



    except Exception:


        return {}







# ==========================================================
# LISTE DES PROJETS
# ==========================================================


# ==========================================================
# LISTE DES PROJETS
# ==========================================================


def list_projects(workdir):


    """
    Retourne les projets existants
    associés au dossier de traitement.
    """


    root = get_projects_root(

        workdir

    )



    if root is None:


        return []



    projects = []



    for folder in root.iterdir():


        if folder.is_dir():


            projects.append(

                folder.name

            )



    return sorted(projects)


# ==========================================================
# CHEMINS INTERNES PROJET
# ==========================================================


def get_project_paths(

    project_path

):


    project_path = Path(

        project_path

    )



    return {


        "root":

            project_path,



        "fits":

            project_path / "fits",



        "previews":

            project_path / "previews",



        "reports":

            project_path / "reports",



        "exports":

            project_path / "exports",



        "logs":

            project_path / "logs",



        "workflow":

            project_path / "workflow.json"

    }








# ==========================================================
# PROJET ACTIF
# SESSION STREAMLIT + PERSISTANCE
# ==========================================================


def get_active_file(workdir):


    return (

        get_projects_root(workdir)

        /

        ".active_project.json"

    )






def save_active_project(

    workdir,

    project_path

):


    file = get_active_file(

        workdir

    )


    data = {


        "project":

            str(project_path)

    }



    with open(

        file,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )







def load_active_project(

    workdir

):


    file = get_active_file(

        workdir

    )


    if not file.exists():

        return None




    try:


        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:


            data = json.load(f)



        project = Path(

            data.get(

                "project",

                ""

            )

        )



        if project.exists():

            return project



    except Exception:


        pass



    return None






def set_active_project(

    project_path,

    workdir=None

):


    import streamlit as st



    project_path = Path(

        project_path

    ).resolve()



    st.session_state.project_path = str(

        project_path

    )



    if workdir:


        save_active_project(

            workdir,

            project_path

        )







def get_active_project():


    import streamlit as st



    return st.session_state.get(

        "project_path",

        None

    )







# ==========================================================
# RESTAURATION AU DEMARRAGE
# ==========================================================


def restore_active_project(

    workdir

):


    import streamlit as st



    project = load_active_project(

        workdir

    )



    if project:


        st.session_state.project_path = str(

            project

        )



        return project



    return None