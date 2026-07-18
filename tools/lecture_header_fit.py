#!/usr/bin/env python3

from pathlib import Path
import sys

from astropy.io import fits


# ==========================================================
# FORMATAGE
# ==========================================================

def format_value(value, decimals=2):

    if value is None:
        return "?"

    try:
        return f"{float(value):.{decimals}f}".replace(".", ",")

    except Exception:
        return str(value)



# ==========================================================
# TEST FITS
# ==========================================================

def test_fits(filename):

    path = Path(filename)

    print("=" * 60)
    print("🔭 TEST HEADER FITS")
    print("=" * 60)

    print(f"Fichier : {path}")
    print()


    if not path.exists():

        print("❌ Fichier introuvable")
        return


    try:

        with fits.open(path) as hdul:

            header = hdul[0].header


            print("✅ FITS valide")
            print()


            print("=" * 60)
            print("📷 INFORMATIONS PRINCIPALES")
            print("=" * 60)


            keys = [

                ("OBJECT", "Objet"),
                ("TELESCOP", "Télescope"),
                ("INSTRUME", "Caméra"),
                ("FOCALLEN", "Focale"),
                ("EXPTIME", "Temps pose"),
                ("FILTER", "Filtre"),
                ("GAIN", "Gain"),
                ("OFFSET", "Offset"),
                ("CCD-TEMP", "Température CCD"),
                ("XPIXSZ", "Pixel X"),
                ("YPIXSZ", "Pixel Y"),
                ("RA", "RA"),
                ("DEC", "DEC"),
                ("DATE-OBS", "Date"),

                # éventuels mots-clés Astro_suite
                ("ASTROEXP", "Temps intégration Astro_suite"),
                ("ASTROIMG", "Nombre images"),
                ("ASTROTYPE", "Type traitement"),

            ]


            for key, label in keys:

                if key in header:

                    print(
                        f"{label:<30}: {header[key]}"
                    )


            print()


            print("=" * 60)
            print("📋 HEADER COMPLET")
            print("=" * 60)


            for card in header.cards:

                print(
                    f"{card.keyword:<15} = {card.value}"
                )


    except Exception as e:

        print()
        print("❌ Erreur lecture FITS")
        print(e)



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage : python test_fits_header.py fichier.fit"
        )

    else:

        test_fits(
            sys.argv[1]
        )