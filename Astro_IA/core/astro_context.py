# ==========================================================
# Astro Suite
# core/astro_context.py
#
# Construction contexte céleste complet
#
# FITS HEADER
#       |
#       +--> coordonnées équatoriales / galactiques
#       +--> éphémérides observation
#       +--> informations objet
#
# Injection dans session Astro IA
# ==========================================================


from pathlib import Path
import json


from core.astro_coordinates import (
    coordinates_from_header
)


from core.astro_ephemeris import (
    build_ephemeris
)


from core.astro_object import (
    build_object_context
)



# ==========================================================
# INJECTION DANS SESSION JSON
# ==========================================================

def inject_astro_context(
    context,
    session_folder
):
    """
    Injecte le contexte astronomique
    dans la session Astro IA la plus récente.

    Paramètres :
        context : dictionnaire astro_context
        session_folder : dossier data_sessions

    Retour :
        True si succès
        False sinon
    """



    folder = Path(
        session_folder
    )


    if not folder.exists():

        return False



    files = sorted(

        folder.glob(
            "astro_session_*.json"
        ),

        reverse=True

    )


    if not files:

        return False



    session_file = files[0]



    try:


        with open(

            session_file,

            "r",

            encoding="utf-8"

        ) as f:


            session = json.load(f)



        session["astro_context"] = context



        with open(

            session_file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                session,

                f,

                indent=4,

                ensure_ascii=False

            )



        return True



    except Exception as e:


        print(
            f"Erreur injection astro_context : {e}"
        )


        return False





# ==========================================================
# CONSTRUCTION CONTEXTE CELESTE
# ==========================================================

def build_astro_context(
    header
):
    """
    Construit toutes les données astronomiques
    utiles à Astro IA depuis un header FITS.

    Retour :
        dictionnaire JSON
    """



    if not header:

        return {}



    context = {}



    # ------------------------------------------------------
    # COORDONNEES
    # ------------------------------------------------------

    coordinates = coordinates_from_header(
        header
    )


    if coordinates:

        context["coordinates"] = coordinates




    # ------------------------------------------------------
    # EPHEMERIDES
    # ------------------------------------------------------

    ephemeris = build_ephemeris(
        header
    )

    print("DEBUG EPHEMERIS")
    print(ephemeris)
    if ephemeris:

        context["ephemeris"] = ephemeris




    # ------------------------------------------------------
    # OBJET
    # ------------------------------------------------------

    object_data = build_object_context(
        header
    )


    if object_data:

        context["object"] = object_data




    return context





# ==========================================================
# TEST LOCAL
# ==========================================================

if __name__ == "__main__":


    import json



    header_test = {


        "OBJECT":

        "NGC 6871",


        "RA":

        302.710263958162,


        "DEC":

        35.9201543476497,


        "SITELAT":

        43.1241,


        "SITELONG":

        1.61518,


        "DATE-OBS":

        "2026-07-08T23:15:00.839926"

    }



    result = build_astro_context(

        header_test

    )



    print(

        json.dumps(

            result,

            indent=4,

            ensure_ascii=False

        )

    )