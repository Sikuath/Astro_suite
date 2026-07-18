# ==========================================================
# Astro Suite
# core/astro_coordinates.py
#
# Conversion coordonnées célestes
# FITS RA/DEC -> Galactique
# ==========================================================


from astropy.coordinates import (
    SkyCoord
)

import astropy.units as u



# ==========================================================
# CREATION COORDONNEES
# ==========================================================

def build_coordinates(
    ra,
    dec
):
    """
    Construit les coordonnées célestes.

    Entrées :
        ra  : degrés (float)
        dec : degrés (float)

    Retour :
        dictionnaire compatible JSON
    """


    if ra is None or dec is None:

        return {}



    try:


        ra = float(ra)

        dec = float(dec)



        coord = SkyCoord(

            ra=ra * u.deg,

            dec=dec * u.deg,

            frame="icrs"

        )



        galactic = coord.galactic



        return {


            "equatorial": {

                "ra_deg": ra,

                "dec_deg": dec

            },


            "galactic": {

                "longitude_deg": round(

                    galactic.l.deg,

                    6

                ),

                "latitude_deg": round(

                    galactic.b.deg,

                    6

                )

            }


        }



    except Exception as e:


        return {

            "error": str(e)

        }




# ==========================================================
# EXTRACTION HEADER FITS
# ==========================================================

def coordinates_from_header(
    header
):
    """
    Extraction directe depuis un header FITS.

    Priorité :
    RA / DEC numériques
    """



    if not header:

        return {}



    ra = header.get(
        "RA"
    )


    dec = header.get(
        "DEC"
    )



    if ra is None or dec is None:


        return {}



    return build_coordinates(

        ra,

        dec

    )



# ==========================================================
# TEST LOCAL
# ==========================================================

if __name__ == "__main__":


    test = build_coordinates(

        304.240809914361,

        41.9586459458434

    )


    import json


    print(

        json.dumps(

            test,

            indent=4

        )

    )