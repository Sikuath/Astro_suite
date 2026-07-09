import numpy as np


# ─────────────────────────────
# CREATION LUMINANCE
# ─────────────────────────────

def make_luminance(
    S,
    H,
    O,
    mode="Ha",
    coeffs=(0.25, 0.60, 0.15)
):
    """
    Création de la luminance.

    Cette luminance sera envoyée directement
    à Siril pour la vraie recomposition RGB.
    """

    if mode == "Ha":

        L = H.copy()


    elif mode == "SHO synthétique":

        s, h, o = coeffs

        total = s + h + o

        if total > 0:

            s /= total
            h /= total
            o /= total


        L = (
            s * S +
            h * H +
            o * O
        )


    else:

        raise ValueError(
            f"Mode inconnu : {mode}"
        )


    return normalize(L)



# ─────────────────────────────
# PREVIEW LRGB
# ─────────────────────────────

def apply_luminance(
    R,
    G,
    B,
    L,
    strength=1.0
):
    """
    Aperçu de la fusion LRGB.

    Cette fonction sert uniquement
    à simuler visuellement le résultat Siril.

    """



    if L is None:

        return (
            R.copy(),
            G.copy(),
            B.copy()
        )



    # -------------------------
    # LUMINANCE RGB DE REFERENCE
    # -------------------------

    current = (
        0.2126 * R
        +
        0.7152 * G
        +
        0.0722 * B
    )



    # -------------------------
    # RAPPORT L / RGB
    # -------------------------

    ratio = (
        L /
        (
            current
            +
            1e-8
        )
    )



    ratio = np.clip(
        ratio,
        0.25,
        4.0
    )



    # réglage utilisateur

    ratio = (
        1
        +
        (ratio - 1)
        *
        strength
    )



    # -------------------------
    # APPLICATION LUMINANCE
    # -------------------------

    R_preview = R * ratio
    G_preview = G * ratio
    B_preview = B * ratio



    # -------------------------
    # PAS DE NORMALISATION ICI
    #
    # Siril conserve les rapports
    # entre les couleurs.
    # -------------------------

    R_preview = np.clip(
        R_preview,
        0,
        None
    )

    G_preview = np.clip(
        G_preview,
        0,
        None
    )

    B_preview = np.clip(
        B_preview,
        0,
        None
    )



    return (
        R_preview,
        G_preview,
        B_preview
    )



# ─────────────────────────────
# NORMALISATION
# ─────────────────────────────

def normalize(img):

    img = img.astype(
        np.float32
    )


    mini = np.nanmin(img)

    maxi = np.nanmax(img)



    if maxi - mini == 0:

        return img



    return (
        img - mini
    ) / (
        maxi - mini
    )