import streamlit as st
from pathlib import Path
import base64


from core.workflow_manager import (
    get_workflow,
    workflow_summary
)



# ==========================================================
# BACKGROUND GLOBAL
# ==========================================================


def load_background():


    img = (

        Path(__file__)
        .parent
        /
        "background.jpg"

    )


    if not img.exists():

        return



    image64 = base64.b64encode(

        img.read_bytes()

    ).decode()



    css = f"""

<style>


/* ==================================================
   APPLICATION BACKGROUND
================================================== */


.stApp {{

    background:

        linear-gradient(

            rgba(5,10,20,0.40),

            rgba(5,10,20,0.40)

        ),

        url(
        "data:image/jpeg;base64,{image64}"
        );


    background-size:

        cover;


    background-position:

        center;


    background-attachment:

        fixed;

}}



/* ==================================================
   MAIN CONTAINER GLASS
================================================== */


div.block-container {{

    background:

        rgba(15,18,30,0.30);


    backdrop-filter:

        blur(8px);


    border-radius:

        20px;


    padding:

        2rem;


    margin-top:

        1rem;

}}



/* ==================================================
   SIDEBAR GLASS
================================================== */


section[data-testid="stSidebar"] {{

    background:

        rgba(10,15,30,0.55);


    backdrop-filter:

        blur(12px);

}}



section[data-testid="stSidebar"] > div {{

    background:

        transparent;

}}



/* ==================================================
   TEXTES
================================================== */


h1,h2,h3,h4,h5,h6 {{

    color:

        white;

}}



p,label {{

    color:

        #ECECEC;

}}



/* ==================================================
   BUTTONS
================================================== */


.stButton > button {{

    background:

        rgba(80,120,255,0.25);


    color:

        white;


    border-radius:

        10px;


    border:

        1px solid rgba(255,255,255,0.25);

}}



.stButton > button:hover {{

    background:

        rgba(80,120,255,0.45);

}}



/* ==================================================
   CODE / TERMINAL IA
================================================== */


.stCode {{

    background:

        rgba(0,0,0,0.85);


    border-radius:

        12px;

}}



.stCode code {{

    color:

        #00ff88;


    font-family:

        Consolas,
        Courier New,
        monospace;

}}



/* ==================================================
   COMPACT UI
================================================== */


.block-container {{

    padding-top:

        1rem;


    padding-bottom:

        1rem;

}}



</style>

"""


    st.markdown(

        css,

        unsafe_allow_html=True

    )





# ==========================================================
# SIDEBAR
# ==========================================================


def show_sidebar(config):


    # Chargement fond global

    load_background()



    with st.sidebar:



        # ==========================================
        # TITRE
        # ==========================================


        st.title(

            "🤖 Astro IA"

        )


        st.caption(

            "Assistant astrophotographique local"

        )


        st.divider()



        # ==========================================
        # WORKFLOW PROJET
        # ==========================================

        st.subheader("📂 Workflow")

        project_path = st.session_state.get("project_path")

        if project_path:

            try:

                summary = workflow_summary(project_path)

                st.metric(
                    "Progression",
                    f"{summary['done']} / {summary['total']}"
                )

            except Exception:

                st.info("Workflow indisponible")

        else:

            st.info("Aucun projet actif")

        st.divider()
        
        # ==========================================
        # IA
        # ==========================================


        st.subheader(

            "🖥 IA"

        )



        ollama = config.get(

            "ollama",

            {}

        )



        st.write(

            f"**Assistant :** "
            f"{ollama.get(
                'default_model',
                'Non défini'
            )}"

        )


        st.write(

            f"**Vision :** "
            f"{ollama.get(
                'vision_model',
                'Non défini'
            )}"

        )



        st.divider()



        # ==========================================
        # SESSION
        # ==========================================


        st.subheader(

            "🔭 Session"

        )



        instrument = st.session_state.get(

            "instrument",

            "Aucun"

        )


        objet = st.session_state.get(

            "object_name",

            "Aucun"

        )


        image = st.session_state.get(

            "image_name",

            "Aucune"

        )



        st.write(

            f"**Instrument :** {instrument}"

        )


        st.write(

            f"**Objet :** {objet}"

        )


        st.write(

            f"**Image :** {image}"

        )



        st.divider()



        # ==========================================
        # PROJET ACTIF
        # ==========================================


        st.subheader(

            "📁 Projet"

        )



        if project_path:


            st.write(

                f"**Dossier :**"

            )


            st.caption(

                str(project_path)

            )


        else:


            st.info(

                "Aucun projet chargé."

            )



        # ==========================================
        # FOOTER
        # ==========================================


        st.markdown(

            """

<style>

.astro-sidebar-footer {


    margin-top:

        40px;


    padding-top:

        15px;


    border-top:

        1px solid rgba(255,255,255,0.15);


    text-align:

        center;


    font-size:

        0.55em;


    color:

        #999;


    line-height:

        1.5;

}


</style>



<div class="astro-sidebar-footer">


© 2026 <b>Sikuath</b> — Astro Suite<br>

Logiciel distribué sous licence MIT.<br>

Images, captures d'écran et contenus graphiques<br>

sous licence <b>CC BY-NC-ND 4.4</b>,<br>

sauf mention contraire.


</div>

""",

            unsafe_allow_html=True

        )