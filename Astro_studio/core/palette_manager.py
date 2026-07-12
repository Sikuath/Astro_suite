from pathlib import Path
import json
from datetime import datetime



CONFIG_FILE = Path(
    "config/palettes.json"
)



# =====================================================
# UTILITAIRE ECRITURE JSON
# =====================================================

def _write_palettes(palettes):

    CONFIG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "custom": palettes
            },
            f,
            indent=4,
            ensure_ascii=False
        )





# =====================================================
# CHARGEMENT
# =====================================================

def load_custom_palettes():

    """
    Retourne :

    {
        "Nom palette":
        {
            "coefficients": [...],
            "description": "",
            "objet": "",
            "date": ""
        }
    }
    """

    if not CONFIG_FILE.exists():

        return {}



    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)



    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}



    custom = data.get(
        "custom",
        {}
    )



    # sécurité structure JSON

    if not isinstance(
        custom,
        dict
    ):

        return {}



    return custom





# =====================================================
# SAUVEGARDE / CREATION / MODIFICATION
# =====================================================

def save_custom_palette(
    name,
    coefficients,
    description="",
    objet=""
):


    palettes = load_custom_palettes()



    palettes[name] = {


        "coefficients": [

            float(c)

            for c in coefficients

        ],


        "description": description,


        "objet": objet,


        "date": datetime.now().strftime(
            "%Y-%m-%d"
        )

    }



    _write_palettes(
        palettes
    )





# =====================================================
# SUPPRESSION
# =====================================================

def delete_custom_palette(
    name
):


    palettes = load_custom_palettes()



    if name in palettes:

        del palettes[name]



    _write_palettes(
        palettes
    )





# =====================================================
# RECUPERATION COEFFICIENTS
# =====================================================

def get_palette_coefficients(
    name
):


    palettes = load_custom_palettes()



    if name not in palettes:

        return None



    coeffs = palettes[name].get(
        "coefficients"
    )



    if not coeffs:

        return None



    return tuple(
        float(c)
        for c in coeffs
    )





# =====================================================
# RECUPERATION COMPLETE
# =====================================================

def get_palette(
    name
):

    """
    Retourne une palette complète.
    """

    palettes = load_custom_palettes()



    return palettes.get(
        name
    )





# =====================================================
# RENOMMAGE
# =====================================================

def rename_palette(
    old_name,
    new_name
):


    palettes = load_custom_palettes()



    if old_name not in palettes:

        return False



    if new_name in palettes:

        return False



    palettes[new_name] = palettes.pop(
        old_name
    )



    _write_palettes(
        palettes
    )



    return True





# =====================================================
# LISTE DES PALETTES
# =====================================================

def list_custom_palettes():

    """
    Retourne uniquement les noms.
    """

    return list(
        load_custom_palettes().keys()
    )