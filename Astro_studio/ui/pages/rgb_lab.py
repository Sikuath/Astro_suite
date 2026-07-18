import streamlit as st
from pathlib import Path

from core.rgb_export import (
    save_rgb_final,
    open_with_siril
)

from core.preview import make_preview
from core.fits_metadata import update_final_header


def show_rgb_lab():

    st.title("✨ RGB Lab")


    required = [
        "R",
        "G",
        "B",
        "workdir"
    ]


    if not all(
        key in st.session_state
        for key in required
    ):

        st.warning(
            "Aucune composition LRGB disponible."
        )

        return



    R = st.session_state.R
    G = st.session_state.G
    B = st.session_state.B


    workdir = Path(
        st.session_state.workdir
    )



    left, right = st.columns(
        [1,2],
        gap="large"
    )



    with left:


        st.subheader(
            "✨ Traitement RGB"
        )


        stretch = st.slider(
            "Stretch preview",
            0.5,
            10.0,
            3.0
        )


        st.divider()



        if st.button(
            "💾 Générer RGB_final.fit et ouvrir Siril"
        ):


            image_finale = save_rgb_final(
                R,
                G,
                B,
                workdir
            )
            update_final_header(
            image_finale,
            workdir
            )

            st.success(
                f"RGB_final créé : {image_finale}"
            )



            try:

                siril_gui = st.session_state.get(
                    "siril_gui"
                )


                if not siril_gui:

                    raise Exception(
                        "siril_gui absent"
                    )


                open_with_siril(
                    image_finale,
                    siril_gui
                )


                st.success(
                    "Siril ouvert avec RGB_final.fit ✔"
                )


            except Exception as e:

                st.error(
                    f"Erreur ouverture Siril : {e}"
                )



    with right:


        st.subheader(
            "👁 Résultat"
        )


        RGB = make_preview(
            R,
            G,
            B,
            stretch
        )


        st.image(
            RGB,
            use_container_width=True
        )