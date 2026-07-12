from pathlib import Path


# =====================================================
# FICHIERS ATTENDUS
# =====================================================

SHO_FILES = [
    "HA.fit",
    "SII.fit",
    "OIII.fit"
]


LRGB_FILES = [
    "L.fit",
    "R.fit",
    "G.fit",
    "B.fit"
]


# =====================================================
# DETECTION DU PROJET
# =====================================================

def detect_project(workdir):
    """
    Détecte automatiquement le type de projet.

    Retour :

    {
        "type": "SHO" | "LRGB" | None,
        "valid": True / False,
        "missing": [...],
        "detected": [...]
    }
    """

    workdir = Path(workdir)

    if not workdir.exists():

        return {
            "type": None,
            "valid": False,
            "missing": [],
            "detected": []
        }

    filenames = [
        f.name
        for f in workdir.iterdir()
        if f.is_file()
    ]

    # -------------------------------------------------
    # SHO
    # -------------------------------------------------

    sho_missing = [
        f
        for f in SHO_FILES
        if f not in filenames
    ]

    sho_ok = len(sho_missing) == 0

    # -------------------------------------------------
    # LRGB
    # -------------------------------------------------

    lrgb_missing = [
        f
        for f in LRGB_FILES
        if f not in filenames
    ]

    lrgb_ok = len(lrgb_missing) == 0

    # -------------------------------------------------
    # Les deux détectés (erreur)
    # -------------------------------------------------

    if sho_ok and lrgb_ok:

        return {
            "type": "MIXED",
            "valid": False,
            "missing": [],
            "detected": filenames
        }

    # -------------------------------------------------
    # SHO
    # -------------------------------------------------

    if sho_ok:

        return {
            "type": "SHO",
            "valid": True,
            "missing": [],
            "detected": SHO_FILES
        }

    # -------------------------------------------------
    # LRGB
    # -------------------------------------------------

    if lrgb_ok:

        return {
            "type": "LRGB",
            "valid": True,
            "missing": [],
            "detected": LRGB_FILES
        }

    # -------------------------------------------------
    # SHO incomplet
    # -------------------------------------------------

    sho_present = sum(
        f in filenames
        for f in SHO_FILES
    )

    if sho_present > 0:

        return {
            "type": "SHO",
            "valid": False,
            "missing": sho_missing,
            "detected": [
                f
                for f in SHO_FILES
                if f in filenames
            ]
        }

    # -------------------------------------------------
    # LRGB incomplet
    # -------------------------------------------------

    lrgb_present = sum(
        f in filenames
        for f in LRGB_FILES
    )

    if lrgb_present > 0:

        return {
            "type": "LRGB",
            "valid": False,
            "missing": lrgb_missing,
            "detected": [
                f
                for f in LRGB_FILES
                if f in filenames
            ]
        }

    # -------------------------------------------------
    # Rien reconnu
    # -------------------------------------------------

    return {
        "type": None,
        "valid": False,
        "missing": [],
        "detected": []
    }