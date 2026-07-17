# ==========================================================
# Astro IA
# Page 04 - Workflow astrophotographique
# ==========================================================


import streamlit as st


from core.workflow_manager import (
    get_workflow,
    toggle_step,
    workflow_summary
)


from core.project_state import (
    load_project_state
)



# ==========================================================
# TITRE
# ==========================================================


st.title(
    "🧭 Workflow astrophotographique"
)



# ==========================================================
# VERIFICATION PROJET
# ==========================================================


project_path = st.session_state.get(
    "project_path"
)



if not project_path:


    st.warning(
        "⚠️ Aucun projet actif."
    )


    st.stop()





# ==========================================================
# CHARGEMENT
# ==========================================================


project_state = load_project_state(

    project_path

)



workflow = get_workflow(

    project_path

)



summary = workflow_summary(

    project_path

)





# ==========================================================
# AVANCEMENT
# ==========================================================


st.header(
    "📊 Avancement"
)



st.progress(

    summary["progress"] / 100

)



st.write(

    f"**{summary['done']} / {summary['total']} étapes terminées**"

)





if project_state.get(
    "workflow_updated"
):


    st.caption(

        "Dernière modification : "

        + project_state["workflow_updated"]

    )





st.divider()





# ==========================================================
# AFFICHAGE WORKFLOW PAR SECTION
# ==========================================================


st.header(
    "🔭 Étapes de traitement"
)



for section in workflow:


    section_name = section.get(

        "section",

        "Workflow"

    )


    st.subheader(

        section_name

    )



    for step in section.get(

        "steps",

        []

    ):


        step_id = step["id"]

        current = step["done"]

        label = step["name"]



        value = st.checkbox(

            label,

            value=current,

            key=f"workflow_{step_id}"

        )



        if value != current:


            toggle_step(

                project_path,

                step_id

            )


            st.rerun()



    st.divider()







# ==========================================================
# MESSAGE
# ==========================================================


st.info(
"""
Le workflow est enregistré dans le projet.

Cette page sert uniquement au suivi manuel
des étapes de traitement astrophotographique.

Aucune analyse Siril, LLaVA ou Qwen3
n'est relancée automatiquement.

Vous pouvez fermer Astro IA et reprendre
plus tard exactement à cette étape.
"""
)






# ==========================================================
# RETOUR
# ==========================================================


if st.button(

    "⬅ Retour analyse"

):


    st.switch_page(

        "ui/pages/02_Analyse.py"

    )