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
    Création d'une luminance calculée.

    Modes Python :
    - Ha
    - SHO synthétique

    Les modes :
    - Aucune
    - L externe

    sont gérés par l'interface.
    """

    if mode == "Ha":

        L = H.copy()


    elif mode == "SHO synthétique":

        s, h, o = coeffs


        total = s + h + o

        if total != 0:

            s /= total
            h /= total
            o /= total


        L = (
            s * S
            +
            h * H
            +
            o * O
        )


    else:

        raise ValueError(
            f"Mode luminance Python inconnu : {mode}"
        )


    return normalize(L)




# ─────────────────────────────
# APPLICATION LUMINANCE
# ─────────────────────────────

def apply_luminance(
    R,
    G,
    B,
    L,
    strength=1.0
):
    """
    Injection d'une luminance dans RGB.
    """

    if L is None:

        return (
            R,
            G,
            B
        )


    current_L = (
        R
        +
        G
        +
        B
    ) / 3.0


    ratio = L / (
        current_L
        +
        1e-8
    )


    ratio = np.clip(
        ratio,
        0,
        10
    )


    R2 = R * (
        1 - strength
        +
        strength * ratio
    )


    G2 = G * (
        1 - strength
        +
        strength * ratio
    )


    B2 = B * (
        1 - strength
        +
        strength * ratio
    )


    return (
        R2,
        G2,
        B2
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