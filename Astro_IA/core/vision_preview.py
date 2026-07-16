# ==========================================================
# Astro IA
# Génération preview vision LLaVA
# FITS linéaire -> PNG couleur étiré astro
# ==========================================================


from pathlib import Path

import numpy as np

from astropy.io import fits
from PIL import Image

from core.config import load_config



# ==========================================================
# STRETCH ASTRONOMIQUE
# ==========================================================


def stretch_channel(channel):

    """
    Stretch asinh astronomique.
    Destiné uniquement à la vision LLaVA.
    Aucun traitement scientifique.
    """

    channel = np.asarray(
        channel,
        dtype=np.float32
    )


    channel = np.nan_to_num(
        channel,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )


    # retrait fond de ciel
    background = np.percentile(
        channel,
        5
    )


    channel = channel - background


    channel[channel < 0] = 0



    # normalisation robuste

    high = np.percentile(
        channel,
        99.5
    )


    if high <= 0:

        raise ValueError(
            "Signal inexploitable."
        )


    channel = np.clip(
        channel,
        0,
        high
    )


    channel /= high



    # stretch asinh type astro

    strength = 15.0


    channel = (

        np.arcsinh(
            strength * channel
        )

        /

        np.arcsinh(
            strength
        )

    )


    return channel



# ==========================================================
# CREATION PREVIEW
# ==========================================================


def create_vision_preview(
    fits_path
):


    """
    Création PNG couleur pour LLaVA.

    Compatible :
    - FITS mono
    - FITS RGB ASI/Siril

    Aucun calcul scientifique.
    """



    fits_path = Path(
        fits_path
    ).resolve()



    if not fits_path.exists():

        raise FileNotFoundError(
            fits_path
        )



    # ======================================================
    # DOSSIER TEMP
    # ======================================================


    config = load_config()


    images_dir = (

        config
        .get(
            "paths",
            {}
        )
        .get(
            "images"
        )

    )


    if not images_dir:

        raise ValueError(
            "Chemin images absent config.json"
        )



    temp_dir = (

        Path(images_dir)
        /
        "x_temp"

    )


    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )



    output = (

        temp_dir
        /
        "vision_preview.png"

    )



    # ======================================================
    # LECTURE FITS
    # ======================================================


    with fits.open(
        fits_path
    ) as hdul:


        data = hdul[0].data

        header = hdul[0].header



    if data is None:

        raise ValueError(
            "Aucune donnée FITS"
        )



    print()
    print("==============================")
    print("DEBUG FITS VISION")
    print("==============================")
    print(
        "Shape :",
        data.shape
    )
    print(
        "dtype :",
        data.dtype
    )
    print(
        "NAXIS :",
        header.get(
            "NAXIS"
        )
    )
    print("==============================")
    print()



    data = np.asarray(
        data,
        dtype=np.float32
    )



    # ======================================================
    # RGB FITS
    # ======================================================


    if (

        data.ndim == 3

        and

        data.shape[0] == 3

    ):


        print(
            "FITS RGB détecté"
        )



        r = stretch_channel(
            data[0]
        )


        g = stretch_channel(
            data[1]
        )


        b = stretch_channel(
            data[2]
        )


        rgb = np.stack(

            (
                r,
                g,
                b

            ),

            axis=2

        )



    # ======================================================
    # MONO FITS
    # ======================================================


    elif data.ndim == 2:


        print(
            "FITS monochrome détecté"
        )


        mono = stretch_channel(
            data
        )


        rgb = np.stack(

            (
                mono,
                mono,
                mono

            ),

            axis=2

        )



    else:


        raise ValueError(

            f"Format FITS non supporté : {data.shape}"

        )



    # ======================================================
    # CONVERSION PNG
    # ======================================================


    rgb = (

        rgb * 255

    ).clip(
        0,
        255
    ).astype(
        np.uint8
    )



    img = Image.fromarray(
        rgb,
        mode="RGB"
    )



    img.thumbnail(
        (
            1536,
            1536
        )
    )



    img.save(
        output,
        "PNG",
        optimize=True
    )



    print(
        "Preview couleur créée :",
        output
    )


    return output



print(
    "vision_preview.py chargé OK"
)


print(
    "create_vision_preview disponible"
)