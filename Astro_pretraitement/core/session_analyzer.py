from pathlib import Path
import re

from core.fits_metadata import get_fits_metadata


# =====================================================
# Analyse automatique d'une session astro
# =====================================================

FILTER_PATTERNS = {

    "L": [
        r"_L_",
        r"_LUM_",
        r"_LUMINANCE_"
    ],

    "R": [
        r"_R_",
        r"_RED_"
    ],

    "G": [
        r"_G_",
        r"_GREEN_"
    ],

    "B": [
        r"_B_",
        r"_BLUE_"
    ],

    "H": [
        r"_H_",
        r"_HA_",
        r"_HALPHA_"
    ],

    "O": [
        r"_O_",
        r"_OIII_",
        r"_O3_"
    ],

    "S": [
        r"_S_",
        r"_SII_",
        r"_S2_"
    ]

}


# =====================================================
# Détection filtre
# =====================================================

def detect_filter(filename):

    name = filename.upper()

    for filt, patterns in FILTER_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                name
            ):

                return filt

    return None


# =====================================================
# Extraction objet depuis nom fichier
# =====================================================

def extract_target(filename):

    """
    Exemple :

    Light_NGC7000_300s_H_gain100.fit

    retourne :

    NGC7000
    """

    name = Path(
        filename
    ).stem

    match = re.search(
        r"Light[_-](.*?)[_-](?:\d+s)",
        name,
        re.IGNORECASE
    )

    if match:

        return match.group(1)

    return "Objet inconnu"


# =====================================================
# Extraction caméra depuis nom fichier
# =====================================================

def extract_camera(filename):

    cameras = [

        r"ASI\d+[A-Z]*",

        r"2600MM",

        r"533MM",

        r"294MM"

    ]

    for pattern in cameras:

        match = re.search(
            pattern,
            filename.upper()
        )

        if match:

            return match.group(0)

    return "Caméra inconnue"


# =====================================================
# Analyse complète session
# =====================================================

def analyze_session(folder):

    folder = Path(
        folder
    )

    result = {

        "target": "Objet inconnu",

        "camera": "Caméra inconnue",

        "filters": {},

        "type": "Inconnu",

        "files": 0

    }

    fits_files = list(
        folder.glob(
            "*.fit"
        )
    )

    if not fits_files:

        return result

    result["files"] = len(
        fits_files
    )

    # =================================================
    # Lecture FITS du premier fichier
    # =================================================

    first_file = fits_files[0]

    try:

        metadata = get_fits_metadata(
            first_file
        )

        if metadata.get("Objet"):

            result["target"] = metadata["Objet"]

        if metadata.get("Caméra"):

            result["camera"] = metadata["Caméra"]

    except Exception:

        pass

    # =================================================
    # Analyse des noms fichiers
    # =================================================

    for file in fits_files:

        # -----------------------------
        # Fallback objet
        # -----------------------------

        if result["target"] == "Objet inconnu":

            result["target"] = extract_target(
                file.name
            )

        # -----------------------------
        # Fallback caméra
        # -----------------------------

        if result["camera"] == "Caméra inconnue":

            result["camera"] = extract_camera(
                file.name
            )

        # -----------------------------
        # Filtre
        # -----------------------------

        filt = detect_filter(
            file.name
        )

        if filt:

            result["filters"][filt] = (

                result["filters"].get(
                    filt,
                    0
                )

                +

                1

            )

    # =================================================
    # Détection traitement
    # =================================================

    result["type"] = detect_session_type(
        result["filters"]
    )

    return result


# =====================================================
# Détermination type traitement
# =====================================================

def detect_session_type(filters):

    keys = set(
        filters.keys()
    )

    # =================================================
    # LSHO (à tester AVANT SHO)
    # =================================================

    if {
        "L",
        "S",
        "H",
        "O"
    }.issubset(keys):

        return "LSHO"

    # =================================================
    # SHO
    # =================================================

    if {
        "S",
        "H",
        "O"
    }.issubset(keys):

        return "SHO"

    # =================================================
    # LRGB
    # =================================================

    if {
        "L",
        "R",
        "G",
        "B"
    }.issubset(keys):

        return "LRGB"

    return "Inconnu"