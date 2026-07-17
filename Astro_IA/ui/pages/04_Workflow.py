# ==========================================================
# Astro IA
# Page 04 - Workflow astrophotographique
# ==========================================================


import streamlit as st

from pathlib import Path


from core.workflow_manager import (
    get_workflow,
    toggle_step,
    workflow_summary
)


from core.project_state import (
    load_project_state
)

# ==========================================================
# STYLE RAPPORT IA TRANSPARENT
# ==========================================================

st.markdown(
    """
<style>

/* Zone texte rapport IA */
div[data-testid="stTextArea"] textarea {

    background:

        rgba(10,15,30,0.55) !important;


    color:

        white !important;


    border-radius:

        12px;


    border:

        1px solid rgba(255,255,255,0.25);


    backdrop-filter:

        blur(8px);

}


/* Expander rapport */
div[data-testid="stExpander"] {


    background:

        rgba(10,15,30,0.35);


    border-radius:

        15px;


    border:

        1px solid rgba(255,255,255,0.15);

}



div[data-testid="stExpander"] details summary {


    color:

        white;

}


</style>
""",
    unsafe_allow_html=True
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
# DISPOSITION 2 COLONNES
# ==========================================================


left_col, right_col = st.columns(

    [2, 3],

    gap="large"

)





# ==========================================================
# COLONNE GAUCHE
# WORKFLOW
# ==========================================================


with left_col:


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


            value = st.checkbox(

                step["name"],

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
# COLONNE DROITE
# RAPPORT IA
# ==========================================================


with right_col:


    st.header(
        "🤖 Rapport IA"
    )


    report_file = (

        Path(project_path)

        /

        "reports"

        /

        "rapport_IA.txt"

    )



    with st.expander(

        "📄 Lire le rapport IA",

        expanded=False

    ):


        if report_file.exists():


            report_text = report_file.read_text(

                encoding="utf-8"

            )


            st.text_area(

                "Rapport",

                report_text,

                height=600,

                label_visibility="collapsed"

            )


        else:


            st.info(

                "Aucun rapport IA enregistré."

            )





# ==========================================================
# MESSAGE
# ==========================================================


st.divider()



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

    "⬅ Retour"

):


    st.switch_page(

        "ui/pages/00_Config.py"

    )