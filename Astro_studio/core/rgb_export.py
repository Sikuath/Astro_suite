from pathlib import Path
import subprocess
import numpy as np

from core.fits_io import save_fits



# ─────────────────────────────────
# EXPORT DES COUCHES RGB
# ─────────────────────────────────

def save_rgb_channels(
    workdir,
    R,
    G,
    B,
    header=None
):
    """
    Sauvegarde les couches RGB linéaires.

    Création :
        R.fit
        G.fit
        B.fit
    """

    workdir = Path(workdir)

    workdir.mkdir(
        parents=True,
        exist_ok=True
    )


    save_fits(
        workdir / "R.fit",
        R,
        header
    )


    save_fits(
        workdir / "G.fit",
        G,
        header
    )


    save_fits(
        workdir / "B.fit",
        B,
        header
    )



# ─────────────────────────────────
# CREATION RGB FINAL
# ─────────────────────────────────

def save_rgb_final(
    R,
    G,
    B,
    workdir,
    header=None
):
    """
    Création du fichier RGB final.

    Format :
        RGB_final.fit

    Cube FITS :
        couche 0 = R
        couche 1 = G
        couche 2 = B
    """

    workdir = Path(workdir)

    workdir.mkdir(
        parents=True,
        exist_ok=True
    )


    rgb_cube = np.stack(
        [
            R,
            G,
            B
        ]
    )


    output = (
        workdir /
        "RGB_final.fit"
    )


    save_fits(
        output,
        rgb_cube,
        header
    )


    return output



# ─────────────────────────────────
# OUVERTURE DANS SIRIL GRAPHIQUE
# ─────────────────────────────────

def open_with_siril(
    image_path,
    siril_path
):
    """
    Ouvre une image finale dans Siril GUI.

    Utilise :
        siril.exe

    Ne pas utiliser pour :
        siril-cli.exe
        (réservé aux scripts)
    """

    image_path = Path(image_path)
    siril_path = Path(siril_path)



    print("========== DEBUG SIRIL ==========")

    print(
        "IMAGE :",
        image_path
    )

    print(
        "IMAGE EXISTE :",
        image_path.exists()
    )

    print(
        "SIRIL CONFIG :",
        siril_path
    )



    # Vérification image

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image introuvable : {image_path}"
        )



    # Gestion chemin dossier ou exe

    if siril_path.is_dir():

        siril_exe = (
            siril_path /
            "siril.exe"
        )

    else:

        siril_exe = siril_path



    print(
        "SIRIL EXE :",
        siril_exe
    )

    print(
        "SIRIL EXISTE :",
        siril_exe.exists()
    )



    if not siril_exe.exists():

        raise FileNotFoundError(
            f"Siril introuvable : {siril_exe}"
        )



    cmd = [
        str(siril_exe),
        str(image_path)
    ]



    print(
        "COMMANDE :",
        cmd
    )



    # UNE SEULE OUVERTURE

    subprocess.Popen(
        cmd,
        cwd=str(image_path.parent),
        shell=False
    )



    print(
        "SIRIL LANCE"
    )