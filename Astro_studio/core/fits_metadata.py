from pathlib import Path
from astropy.io import fits


def update_final_header(
        rgb_file,
        workdir
):

    rgb_file = Path(rgb_file)
    workdir = Path(workdir)


    if not rgb_file.exists():

        raise FileNotFoundError(
            rgb_file
        )


    # ==================================================
    # Détection des couches disponibles
    # ==================================================

    possible_layers = [

        [
            "HA_linear.fit",
            "OIII_linear.fit",
            "SII_linear.fit"
        ],

        [
            "L_linear.fit",
            "R_linear.fit",
            "G_linear.fit",
            "B_linear.fit"
        ]

    ]


    layers = []


    for candidate in possible_layers:

        if all(
            (workdir / f).exists()
            for f in candidate
        ):

            layers = candidate
            break



    if not layers:

        raise RuntimeError(
            "Aucune couche linear trouvée"
        )



    hdr_values = {}


    total_live = 0

    total_stack = 0



    # ==================================================
    # Lecture des headers couches
    # ==================================================

    for layer in layers:


        file = workdir / layer


        hdr = fits.getheader(file)



        total_live += float(

            hdr.get(
                "LIVETIME",
                hdr.get(
                    "EXPTIME",
                    0
                )
            )

        )



        total_stack += int(

            hdr.get(
                "STACKCNT",
                1
            )

        )



        # première couche comme référence

        if not hdr_values:


            for key in [

                "OBJECT",
                "DATE-OBS",

                "TELESCOP",
                "FOCALLEN",

                "INSTRUME",

                "GAIN",
                "OFFSET",

                "CCD-TEMP",

                "RA",
                "DEC",

                "OBJCTRA",
                "OBJCTDEC"

            ]:

                if key in hdr:

                    hdr_values[key] = hdr[key]



    # ==================================================
    # Injection dans RGB_final.fit
    # ==================================================

    with fits.open(

        rgb_file,

        mode="update"

    ) as hdul:


        header = hdul[0].header



        for key, value in hdr_values.items():

            header[key] = value



        header["STACKCNT"] = (

            total_stack,

            "Nombre poses combinees"

        )


        header["LIVETIME"] = (

            total_live,

            "Temps integration total secondes"

        )


        header["ASTMODE"] = (

            "SHO" if "HA_linear.fit" in layers else "LRGB",

            "Mode Astro Suite"

        )


        header["ASTROAPP"] = (

            "Astro Suite",

            "Logiciel traitement"

        )


        hdul.flush()