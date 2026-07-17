import streamlit as st
from pathlib import Path



from core.config import load_config
from core.session import init_session



from ui.sidebar import show_sidebar





# ==========================================================
# CONFIG STREAMLIT
# ==========================================================


st.set_page_config(

    page_title="Astro IA",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)





# ==========================================================
# CHARGEMENT CSS
# ==========================================================


css_file = Path(

    "ui/style.css"

)



if css_file.exists():


    st.markdown(

        f"""

<style>

{css_file.read_text(

    encoding="utf-8"

)}

</style>

""",

        unsafe_allow_html=True

    )







# ==========================================================
# CONFIGURATION
# ==========================================================


config = load_config()







# ==========================================================
# SESSION
# ==========================================================


init_session(

    config

)







# ==========================================================
# SIDEBAR
# ==========================================================


show_sidebar(

    config

)







# ==========================================================
# NAVIGATION PAGES
# ==========================================================


pages = {


    "📂 Workflow": [


        st.Page(

            "ui/pages/00_Config.py",

            title="Configuration",

            icon="⚙️"

        ),



        st.Page(

            "ui/pages/01_FITS.py",

            title="FITS",

            icon="📷"

        ),



        st.Page(

            "ui/pages/02_Analyse.py",

            title="Analyse IA",

            icon="🤖"

        ),



        st.Page(

            "ui/pages/03_Rapport.py",

            title="Rapport",

            icon="📋"

        ),



        st.Page(

            "ui/pages/04_Workflow.py",

            title="Workflow",

            icon="🧭"

        )

    ]

}







# ==========================================================
# EXECUTION
# ==========================================================


pg = st.navigation(

    pages

)



pg.run()