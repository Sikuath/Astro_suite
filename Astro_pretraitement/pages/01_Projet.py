import streamlit as st
from pathlib import Path

from core.config import load_config, save_config
from core.reject import clear_rejected_folder


st.title("📁 Projet")


config = load_config()


lights_current = config.get(
    "lights_folder",
    ""
)

rejected_current = config.get(
    "rejected_folder",
    ""
)


lights_folder = st.text_input(
    "📷 Dossier des Lights",
    value=lights_current
)


rejected_folder = st.text_input(
    "🗑️ Dossier des rejets",
    value=rejected_current
)



if st.button("💾 Enregistrer configuration"):

    lights_path = Path(lights_folder)
    rejected_path = Path(rejected_folder)


    if not lights_path.exists():

        st.error(
            "Le dossier Lights n'existe pas"
        )


    else:

        if not rejected_path.exists():

            rejected_path.mkdir(
                parents=True,
                exist_ok=True
            )


        config["lights_folder"] = lights_folder
        config["rejected_folder"] = rejected_folder


        save_config(config)


        st.session_state["lights_folder"] = lights_folder
        st.session_state["rejected_folder"] = rejected_folder


        st.success(
            "Configuration sauvegardée"
        )



st.divider()


st.subheader("🧹 Gestion des rejets")


if rejected_folder:

    rejected_path = Path(rejected_folder)


    if rejected_path.exists():


        if "confirm_clear_rejected" not in st.session_state:

            st.session_state.confirm_clear_rejected = False



        if st.button(
            "🗑️ Vider le dossier des rejets",
            use_container_width=True
        ):

            st.session_state.confirm_clear_rejected = True



        if st.session_state.confirm_clear_rejected:

            st.warning(
                "⚠️ Attention : cette action va supprimer définitivement "
                "tout le contenu du dossier des rejets.\n\n"
                "Êtes-vous certain de vouloir continuer ?"
            )


            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "✅ Oui, vider le dossier",
                    use_container_width=True
                ):

                    clear_rejected_folder(
                        rejected_folder
                    )


                    st.session_state.confirm_clear_rejected = False


                    st.success(
                        "Le dossier des rejets a été vidé"
                    )


                    st.rerun()



            with col2:

                if st.button(
                    "❌ Annuler",
                    use_container_width=True
                ):

                    st.session_state.confirm_clear_rejected = False

                    st.rerun()


    else:

        st.info(
            "Le dossier des rejets n'existe pas encore"
        )


else:

    st.info(
        "Choisissez un dossier de rejets"
    )