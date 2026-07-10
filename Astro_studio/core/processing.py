import numpy as np



# ─────────────────────────────
# MELANGE SHO
# ─────────────────────────────

def mix_sho(
    S,
    H,
    O,
    r_s,
    r_h,
    g_h,
    g_o,
    b_o
):
    """
    Création des couches RGB
    à partir des couches SHO.

    Données conservées linéaires.
    """

    R = (
        r_s * S
        +
        r_h * H
    )


    G = (
        g_h * H
        +
        g_o * O
    )


    B = (
        b_o * O
    )


    # sécurité FITS

    R = np.clip(
        R,
        0,
        None
    )

    G = np.clip(
        G,
        0,
        None
    )

    B = np.clip(
        B,
        0,
        None
    )


    return R, G, B



# ─────────────────────────────
# PALETTES
# ─────────────────────────────

def apply_palette(
    palette
):

    palettes = {


        # SII -> Rouge
        # Ha  -> Vert
        # OIII -> Bleu

        "Hubble SHO":
        (
            0.8,
            0.2,
            0.7,
            0.3,
            1.0
        ),



        # HOO renforcé
        # Ajout léger de Ha dans R
        # pour éviter un canal rouge vide
        # dans les FITS linéaires

        "HOO Boost":
        (
            0.0,
            0.15,
            0.3,
            0.7,
            1.0
        ),



        "HOO Natural":
        (
            0.0,
            0.10,
            0.6,
            0.4,
            1.0
        ),



        "Hα Rich":
        (
            0.2,
            0.8,
            0.8,
            0.2,
            0.8
        ),



        # OIII dominant
        # Petit apport Ha pour garder
        # un RGB exploitable dans Siril

        "OIII Rich":
        (
            0.0,
            0.10,
            0.0,
            1.0,
            1.0
        ),



        "Foraxx Pro":
        (
            0.6,
            0.4,
            0.4,
            0.6,
            1.0
        ),



        "Gold & Blue":
        (
            1.0,
            0.0,
            0.5,
            0.5,
            1.0
        ),



        "Teal & Orange":
        (
            0.9,
            0.1,
            0.3,
            0.7,
            1.0
        )

    }


    return palettes.get(
        palette,
        palettes["Hubble SHO"]
    )