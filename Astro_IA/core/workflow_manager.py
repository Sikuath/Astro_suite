# ==========================================================
# Astro IA
# Gestion du workflow astrophotographique
# ==========================================================


from datetime import datetime


from core.project_state import (
    load_project_state,
    save_project_state
)





# ==========================================================
# WORKFLOW ASTROPHOTO
# ==========================================================


DEFAULT_WORKFLOW = [


    {
        "section": "A - Siril",

        "steps": [


            {
                "id": "siril_crop",
                "name": "Recadrer l’image",
                "done": False
            },


            {
                "id": "siril_astrometry",
                "name": "Résolution astrométrique",
                "done": False
            },


            {
                "id": "siril_gradient",
                "name": "Extraction de gradient",
                "done": False
            },


            {
                "id": "siril_green",
                "name": "Suppression du bruit vert",
                "done": False
            },


            {
                "id": "siril_photometry",
                "name": "Etalonnage des couleurs par photométrie",
                "done": False
            },


            {
                "id": "abberration_remover",
                "name": "Abberration Remover (script Python)",
                "done": False
            },


            {
                "id": "cosmicclarity",
                "name": "CosmicClartity_Sharpen (script Python)",
                "done": False
            },


            {
                "id": "veralux",
                "name": "Veralux_Silentium (script Python)",
                "done": False
            },


            {
                "id": "starless_creation",
                "name": "Création de la starless",
                "done": False
            },


            {
                "id": "starless_stretch",
                "name": "Etirement de la Starless",
                "done": False
            }

        ]
    },



    {
        "section": "B - Gimp",

        "steps": [


            {
                "id": "gimp_starless",
                "name": "Traitement de la starless",
                "done": False
            },


            {
                "id": "gimp_levels",
                "name": "Ajuster le niveau des couleurs",
                "done": False
            },


            {
                "id": "gimp_noise",
                "name": "Réduction du bruit",
                "done": False
            },


            {
                "id": "gimp_colors",
                "name": "Renforcer les couleurs",
                "done": False
            },


            {
                "id": "gimp_saturation",
                "name": "Rehausser les couleurs",
                "done": False
            },


            {
                "id": "gimp_curve",
                "name": "Traitement par courbe",
                "done": False
            },


            {
                "id": "gimp_highpass",
                "name": "Filtre passe haut",
                "done": False
            },


            {
                "id": "gimp_balance",
                "name": "Balance des couleurs",
                "done": False
            }

        ]
    },



    {
        "section": "C - Siril",

        "steps": [


            {
                "id": "stars_mask",
                "name": "Travailler le masque d’étoiles",
                "done": False
            },


            {
                "id": "purple_remove",
                "name": "Suppression zones violettes (inversion / bruit vert / inversion)",
                "done": False
            },


            {
                "id": "recompose",
                "name": "Recomposition starless / masque d’étoiles",
                "done": False
            },


            {
                "id": "deconvolution",
                "name": "Déconvolution éventuelle",
                "done": False
            }


        ]
    },



    {
        "section": "D - Gimp",

        "steps": [


            {
                "id": "gimp_finish",
                "name": "Finition",
                "done": False
            },
            {
                "id": "report",
                "name": "Rapport astrophotographique validé",
                "done": False
        }

        ]
    }

]





# ==========================================================
# INITIALISATION
# ==========================================================


def init_workflow(project_path):


    data = load_project_state(project_path)


    if "workflow" not in data:


        data["workflow"] = DEFAULT_WORKFLOW


        data["workflow_updated"] = datetime.now().isoformat()


        save_project_state(

            project_path,

            data

        )


    return data["workflow"]







# ==========================================================
# RECUPERATION
# ==========================================================


def get_workflow(project_path):


    data = load_project_state(project_path)


    workflow = data.get(

        "workflow"

    )


    if not workflow:


        workflow = init_workflow(

            project_path

        )


    return workflow







# ==========================================================
# MODIFICATION
# ==========================================================


def set_step(

    project_path,

    step_id,

    state

):


    data = load_project_state(project_path)


    workflow = data.get(

        "workflow",

        []

    )



    for section in workflow:


        for step in section.get("steps", []):


            if step["id"] == step_id:


                step["done"] = state



    data["workflow"] = workflow


    data["workflow_updated"] = datetime.now().isoformat()


    save_project_state(

        project_path,

        data

    )







# ==========================================================
# INVERSION
# ==========================================================


def toggle_step(

    project_path,

    step_id

):


    workflow = get_workflow(project_path)



    for section in workflow:


        for step in section.get("steps", []):


            if step["id"] == step_id:


                set_step(

                    project_path,

                    step_id,

                    not step["done"]

                )


                return







# ==========================================================
# PROGRESSION
# ==========================================================


def workflow_summary(project_path):


    workflow = get_workflow(project_path)


    total = 0

    done = 0



    for section in workflow:


        for step in section.get("steps", []):


            total += 1


            if step["done"]:

                done += 1



    progress = 0


    if total:

        progress = int(done / total * 100)



    return {


        "total": total,

        "done": done,

        "progress": progress

    }