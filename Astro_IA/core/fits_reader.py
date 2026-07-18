from pathlib import Path
from astropy.io import fits


def read_fits_header(filepath):

    """
    Lecture du header FITS

    Retourne un dictionnaire exploitable par Astro IA
    """

    filepath = Path(filepath)

    if not filepath.exists():

        return {
            "error": "Fichier introuvable"
        }


    try:

        with fits.open(filepath) as hdul:

            header = hdul[0].header


            data = {


                # ==================================================
                # OBJET
                # ==================================================

                "OBJECT":
                    header.get(
                        "OBJECT",
                        "Inconnu"
                    ),



                # ==================================================
                # DATE
                # ==================================================

                "DATE-OBS":
                    header.get(
                        "DATE-OBS",
                        "Inconnue"
                    ),



                # ==================================================
                # INSTRUMENT
                # ==================================================

                "TELESCOP":
                    header.get(
                        "TELESCOP",
                        "Inconnu"
                    ),


                "INSTRUME":
                    header.get(
                        "INSTRUME",
                        "Inconnu"
                    ),



                # ==================================================
                # OPTIQUE
                # ==================================================

                "FOCALLEN":
                    header.get(
                        "FOCALLEN",
                        "Inconnue"
                    ),



                # ==================================================
                # CAMERA
                # ==================================================

                "XPIXSZ":
                    header.get(
                        "XPIXSZ",
                        "Inconnue"
                    ),


                "YPIXSZ":
                    header.get(
                        "YPIXSZ",
                        "Inconnue"
                    ),



                # ==================================================
                # ACQUISITION
                # ==================================================

                "EXPTIME":
                    header.get(
                        "EXPTIME",
                        header.get(
                            "EXPOSURE",
                            "Inconnue"
                        )
                    ),


                "GAIN":
                    header.get(
                        "GAIN",
                        "Inconnu"
                    ),


                "OFFSET":
                    header.get(
                        "OFFSET",
                        "Inconnu"
                    ),


                "FILTER":
                    header.get(
                        "FILTER",
                        "Inconnu"
                    ),



                # ==================================================
                # TEMPERATURE
                # ==================================================

                "CCD-TEMP":
                    header.get(
                        "CCD-TEMP",
                        header.get(
                            "CCD_TEMP",
                            "Inconnue"
                        )
                    ),



                # ==================================================
                # COORDONNEES CELESTES
                # ==================================================

                "RA":
                    header.get(
                        "RA",
                        "Inconnue"
                    ),


                "DEC":
                    header.get(
                        "DEC",
                        "Inconnue"
                    ),


                # Coordonnées sexagésimales utiles
                "OBJCTRA":
                    header.get(
                        "OBJCTRA",
                        ""
                    ),


                "OBJCTDEC":
                    header.get(
                        "OBJCTDEC",
                        ""
                    ),



                # ==================================================
                # SITE OBSERVATION
                # ==================================================

                "SITELAT":
                    header.get(
                        "SITELAT",
                        None
                    ),


                "SITELONG":
                    header.get(
                        "SITELONG",
                        None
                    ),


                "SITEELEV":
                    header.get(
                        "SITEELEV",
                        0
                    ),



                # ==================================================
                # STACK / SESSION
                # ==================================================

                "STACKCNT":
                    header.get(
                        "STACKCNT",
                        0
                    ),


                "LIVETIME":
                    header.get(
                        "LIVETIME",
                        0
                    ),


                "ASTMODE":
                    header.get(
                        "ASTMODE",
                        ""
                    )


            }


            return data



    except Exception as e:


        return {
            "error": str(e)
        }