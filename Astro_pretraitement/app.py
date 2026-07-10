import streamlit as st


st.set_page_config(
    page_title="Astro Prétraitement",
    page_icon="📷",
    layout="wide"
)


st.title("📷 Astro Prétraitement")

st.markdown(
    """
    ## Assistant de tri des acquisitions astronomiques

    Cette application permet :

    - visualisation rapide des lights FITS
    - suppression des mauvaises acquisitions
    - lancement du prétraitement Siril

    ---
    
    Commencez par choisir un projet dans le menu de gauche.
    """
)