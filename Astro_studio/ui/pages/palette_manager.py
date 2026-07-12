import streamlit as st

from core.palette_manager import (
    load_custom_palettes,
    save_custom_palette,
    delete_custom_palette
)



# =====================================================
# PALETTE -> TEXTE
# =====================================================

def palette_to_text(name, data):

    coeff = data.get(
        "coefficients",
        [0,0,0,0,0]
    )


    return f"""Name = {name}

Object = {data.get("objet","")}


R_SII = {coeff[0]:.2f}
R_HA = {coeff[1]:.2f}

G_HA = {coeff[2]:.2f}
G_OIII = {coeff[3]:.2f}

B_OIII = {coeff[4]:.2f}


Notes = 
{data.get("description","")}

""".strip()




# =====================================================
# TEXTE -> PALETTE
# =====================================================

def text_to_palette(text):

    try:

        values = {}
        notes = []

        reading_notes = False


        for line in text.splitlines():

            line = line.strip()


            if not line:
                continue


            if line.startswith("Notes"):

                reading_notes = True
                continue



            if reading_notes:

                notes.append(line)
                continue



            if "=" in line:

                key, value = line.split(
                    "=",
                    1
                )

                values[key.strip()] = value.strip()



        coefficients = (

            float(
                values.get(
                    "R_SII",
                    0
                )
            ),

            float(
                values.get(
                    "R_HA",
                    0
                )
            ),

            float(
                values.get(
                    "G_HA",
                    0
                )
            ),

            float(
                values.get(
                    "G_OIII",
                    0
                )
            ),

            float(
                values.get(
                    "B_OIII",
                    0
                )
            )

        )



        return {

            "name":
                values.get(
                    "Name",
                    "Sans_nom"
                ),


            "objet":
                values.get(
                    "Object",
                    ""
                ),


            "coefficients":
                coefficients,


            "description":
                "\n".join(notes)

        }



    except Exception:

        return None




# =====================================================
# PAGE
# =====================================================

def show_palette_manager():


    st.markdown(
        """
        <style>


        /* terminal */

        div[data-testid="stTextArea"] textarea {

            font-family:
            "JetBrains Mono",
            "Courier New",
            monospace;

            font-size:0.85rem;

        }



        /* boutons */

        div.stButton > button {

            height:32px;

            padding:
            0.1rem 0.6rem;

            font-size:0.80rem;

        }



        /* selectbox */

        div[data-baseweb="select"] {

            font-size:0.85rem;

        }


        </style>
        """,
        unsafe_allow_html=True
    )



    st.title(
        "🎨 Palette SHO"
    )



    palettes = load_custom_palettes()



    if not palettes:

        st.info(
            "Aucune palette personnelle."
        )

        return




    names = sorted(
        palettes.keys()
    )



    # =================================================
    # LAYOUT
    # =================================================


    col_left, col_right = st.columns(
        [0.25,0.75],
        gap="medium"
    )



    # =================================================
    # SELECTEUR
    # =================================================


    with col_left:


        st.caption(
            "🎨 Palette"
        )


        selected = st.selectbox(

            "",

            names,

            label_visibility="collapsed"

        )



        st.write("")



        if st.button(
            "🗑 Supprimer",
            use_container_width=True
        ):


            delete_custom_palette(
                selected
            )


            st.success(
                "Palette supprimée"
            )

            st.rerun()




    data = palettes[selected]




    # =================================================
    # INITIALISATION EDITEUR
    # =================================================


    if (

        "palette_editor"
        not in st.session_state

        or

        st.session_state.get(
            "palette_editor_name"
        )
        != selected

    ):


        st.session_state.palette_editor = (
            palette_to_text(
                selected,
                data
            )
        )


        st.session_state.palette_editor_name = selected




    # =================================================
    # TERMINAL
    # =================================================


    with col_right:


        st.caption(
            "💻 Éditeur recette"
        )


        edited = st.text_area(

            "",

            key="palette_editor",

            height=430,

            label_visibility="collapsed"

        )



        col_save, col_space = st.columns(
            [0.20,0.80]
        )


        with col_save:


            save = st.button(
                "💾 Sauver",
                use_container_width=True
            )



        if save:


            result = text_to_palette(
                edited
            )


            if result:


                save_custom_palette(

                    result["name"],

                    result["coefficients"],

                    description=result["description"],

                    objet=result["objet"]

                )


                st.success(
                    "Palette sauvegardée ✔️"
                )


                st.rerun()


            else:


                st.error(
                    "Erreur format palette"
                )