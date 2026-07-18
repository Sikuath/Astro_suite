# ==========================================================
# SIMBAD CLIENT
# Astro IA
# ==========================================================


from astroquery.simbad import Simbad

from astropy.coordinates import SkyCoord

from astropy import units as u
from astroquery.simbad import Simbad
import warnings
from astroquery.exceptions import NoResultsWarning


warnings.filterwarnings(
    "ignore",
    category=NoResultsWarning
)



# ==========================================================
# VOCABULAIRE ASTRONOMIQUE
# ==========================================================


def get_astro_vocabulary(simbad_type):

    if not simbad_type:

        return []


    t = str(simbad_type).lower()


    vocabulary = []



    if "open cluster" in t or "cluster" in t:

        vocabulary = [

            "amas ouvert",

            "population stellaire",

            "champ riche en étoiles",

            "structure stellaire"

        ]



    elif "globular" in t:

        vocabulary = [

            "amas globulaire",

            "population stellaire ancienne",

            "concentration stellaire dense"

        ]



    elif (
        "nebula" in t
        or "hii" in t
        or "region" in t
    ):

        vocabulary = [

            "nébuleuse",

            "région d'émission",

            "gaz interstellaire",

            "structure diffuse"

        ]



    elif "galaxy" in t:

        vocabulary = [

            "galaxie",

            "structure extragalactique",

            "bras spiraux possibles",

            "halo galactique"

        ]



    elif "planetary" in t:

        vocabulary = [

            "nébuleuse planétaire",

            "enveloppe gazeuse",

            "étoile centrale"

        ]



    elif "star" in t:

        vocabulary = [

            "étoile",

            "source stellaire",

            "champ d'étoiles"

        ]



    return vocabulary







# ==========================================================
# CONFIGURATION SIMBAD
# ==========================================================


custom = Simbad()



custom.add_votable_fields(

    "otype",

    "ra(d)",

    "dec(d)"

)







# ==========================================================
# OUTIL LECTURE COLONNE ROBUSTE
# ==========================================================


def get_column(row, names):

    """
    Recherche une colonne avec plusieurs noms possibles.
    """

    for name in names:


        if name in row.colnames:

            return row[name]



    return None







# ==========================================================
# RECHERCHE OBJET
# ==========================================================


def query_object(object_name):

    """
    Recherche un objet SIMBAD par son nom.
    Retourne un dictionnaire exploitable par Astro IA.
    """



    if not object_name:

        return None



    try:


        result = custom.query_object(

            object_name

        )



        if result is None or len(result) == 0:

            return None



        row = result[0]



        name = get_column(

            row,

            [

                "main_id",

                "MAIN_ID"

            ]

        )



        obj_type = get_column(

            row,

            [

                "otype",

                "OTYPE"

            ]

        )



        ra = get_column(

            row,

            [

                "ra_d",

                "RA_d"

            ]

        )


        dec = get_column(

            row,

            [

                "dec_d",

                "DEC_d"

            ]

        )





        return {


            "name":

                str(name)
                .strip()
                if name is not None
                else object_name,



            "type":

                str(obj_type)
                .strip()
                if obj_type is not None
                else "Unknown",



            "ra":

                float(ra)
                if ra is not None
                else None,



            "dec":

                float(dec)
                if dec is not None
                else None,



            "vocabulary":

                get_astro_vocabulary(

                    obj_type

                )

        }





    except Exception as e:


        print(

            "Erreur SIMBAD objet :",

            e

        )


        return None







# ==========================================================
# DISTANCE ANGULAIRE
# ==========================================================


def angular_distance(

    ra1,

    dec1,

    ra2,

    dec2

):

    """
    Distance angulaire en degrés.
    """



    c1 = SkyCoord(

        ra1,

        dec1,

        unit="deg"

    )



    c2 = SkyCoord(

        ra2,

        dec2,

        unit="deg"

    )



    return (

        c1.separation(c2)

        .degree

    )







# ==========================================================
# RECHERCHE OBJETS DU CHAMP
# ==========================================================


def query_field(

    ra,

    dec,

    radius_arcmin

):

    """
    Recherche SIMBAD dans le champ.
    """



    objects = []



    try:


        coord = SkyCoord(

            ra,

            dec,

            unit="deg"

        )



        result = custom.query_region(

            coord,

            radius=

                radius_arcmin

                *

                u.arcmin

        )



        if result is None:

            return []





        for row in result:



            try:



                name = get_column(

                    row,

                    [

                        "main_id",

                        "MAIN_ID"

                    ]

                )



                obj_type = get_column(

                    row,

                    [

                        "otype",

                        "OTYPE"

                    ]

                )



                objects.append(


                    {


                    "name":

                        str(name)
                        .strip(),



                    "type":

                        str(obj_type),



                    "vocabulary":

                        get_astro_vocabulary(

                            obj_type

                        )

                    }

                )



            except Exception:


                continue





    except Exception as e:


        print(

            "Erreur SIMBAD champ :",

            e

        )



    return objects







# ==========================================================
# IDENTIFICATION COMPLETE
# ==========================================================


def identify_target(

    object_name,

    ra,

    dec,

    radius_arcmin

):


    result = {


        "confirmed":

            False,


        "object_name":

            object_name,


        "main_object":

            None,


        "distance_from_center_deg":

            None,


        "field_objects":

            []

    }






    simbad_object = query_object(

        object_name

    )



    if simbad_object:



        result["main_object"] = simbad_object



        if (

            ra is not None

            and

            dec is not None

            and

            simbad_object["ra"] is not None

        ):



            distance = angular_distance(

                ra,

                dec,

                simbad_object["ra"],

                simbad_object["dec"]

            )



            result["distance_from_center_deg"] = round(

                distance,

                4

            )



            if distance <= radius_arcmin / 60:


                result["confirmed"] = True



        else:


            result["confirmed"] = True







    if ra is not None and dec is not None:


        result["field_objects"] = query_field(

            ra,

            dec,

            radius_arcmin

        )



    return result