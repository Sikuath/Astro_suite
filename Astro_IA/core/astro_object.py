# ==========================================================
# Astro Suite
# core/astro_object.py
#
# Enrichissement objet astronomique
#
# FITS OBJECT / RA / DEC
# ->
# SIMBAD informations
# ==========================================================


from astroquery.simbad import Simbad

from astropy.coordinates import (
    SkyCoord
)

import astropy.units as u





# ==========================================================
# CONFIG SIMBAD
# ==========================================================

def configure_simbad():

    """
    Ajoute les champs utiles.
    """

    simbad = Simbad()


    try:

        simbad.add_votable_fields(

            "otype",

            "flux(V)",

            "flux(B)",

            "sptype"

        )


    except Exception:

        pass



    return simbad





# ==========================================================
# RECHERCHE PAR NOM
# ==========================================================

def query_by_name(
    name
):

    """
    Recherche SIMBAD par nom.
    """


    if not name:

        return {}



    try:


        simbad = configure_simbad()


        result = simbad.query_object(
            name
        )



        if result is None:

            return {}



        row = result[0]



        data = {}



        if "MAIN_ID" in row.colnames:

            data["main_id"] = str(

                row["MAIN_ID"]

            )



        if "OTYPE" in row.colnames:

            data["type"] = str(

                row["OTYPE"]

            )



        if "SP_TYPE" in row.colnames:

            data["spectral_type"] = str(

                row["SP_TYPE"]

            )



        if "FLUX_V" in row.colnames:

            try:

                data["magnitude_v"] = float(

                    row["FLUX_V"]

                )

            except:

                pass



        return data



    except Exception:


        return {}





# ==========================================================
# RECHERCHE PAR COORDONNEES
# ==========================================================

def query_by_coordinates(
    ra,
    dec
):

    """
    Recherche SIMBAD autour d'une position.
    """



    try:


        coord = SkyCoord(

            ra=float(ra) * u.deg,

            dec=float(dec) * u.deg,

            frame="icrs"

        )



        simbad = configure_simbad()



        result = simbad.query_region(

            coord,

            radius="5 arcmin"

        )



        if result is None:

            return {}



        row = result[0]



        return {


            "main_id": str(

                row["MAIN_ID"]

            ),


            "type": str(

                row["OTYPE"]

            )


        }



    except Exception:


        return {}





# ==========================================================
# CONSTELLATION
# ==========================================================

def get_constellation(
    ra,
    dec
):

    """
    Retourne constellation IAU.
    """



    try:


        from astropy.coordinates import (

            get_constellation

        )



        coord = SkyCoord(

            ra=float(ra)*u.deg,

            dec=float(dec)*u.deg,

            frame="icrs"

        )



        return get_constellation(

            coord,

            short_name=False

        )



    except:


        return None





# ==========================================================
# CONTEXTE OBJET COMPLET
# ==========================================================

def build_object_context(
    header
):

    """
    Construction bloc objet pour Astro IA.
    """



    if not header:

        return {}



    name = header.get(

        "OBJECT",

        ""

    )


    ra = header.get(

        "RA"

    )


    dec = header.get(

        "DEC"

    )



    result = {


        "input_name": name,


        "coordinates": {


            "ra": ra,

            "dec": dec


        }


    }





    # Recherche nom

    simbad = query_by_name(

        name

    )



    if not simbad and ra and dec:


        simbad = query_by_coordinates(

            ra,

            dec

        )



    if simbad:


        result["simbad"] = simbad



    constellation = get_constellation(

        ra,

        dec

    )


    if constellation:


        result["constellation"] = constellation



    return result






# ==========================================================
# TEST LOCAL
# ==========================================================

if __name__ == "__main__":


    header_test = {


        "OBJECT":

        "NGC 6871",


        "RA":

        302.710263958162,


        "DEC":

        35.9201543476497


    }



    import json



    data = build_object_context(

        header_test

    )



    print(

        json.dumps(

            data,

            indent=4,

            ensure_ascii=False

        )

    )