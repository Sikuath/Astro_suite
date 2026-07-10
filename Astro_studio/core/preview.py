import numpy as np



def preview_scale(img):

    img = img.astype(np.float32)

    lo = np.nanpercentile(
        img,
        0.5
    )

    hi = np.nanpercentile(
        img,
        99.5
    )

    if hi - lo == 0:

        return np.zeros_like(img)


    return np.clip(
        (img - lo) / (hi - lo),
        0,
        1
    )



def asinh(img, k):

    return np.arcsinh(
        img * k
    ) / np.arcsinh(k)



def make_preview(
    R,
    G,
    B,
    stretch=3.0
):

    # --------------------------------
    # NORMALISATION COMMUNE RGB
    # --------------------------------

    rgb = np.dstack(
        [
            R,
            G,
            B
        ]
    ).astype(
        np.float32
    )


    lo = np.nanpercentile(
        rgb,
        0.5
    )


    hi = np.nanpercentile(
        rgb,
        99.5
    )


    if hi - lo == 0:

        return np.zeros_like(rgb)



    rgb = np.clip(
        (rgb - lo) / (hi - lo),
        0,
        1
    )



    # séparation après normalisation

    Rv = asinh(
        rgb[:,:,0],
        stretch
    )

    Gv = asinh(
        rgb[:,:,1],
        stretch
    )

    Bv = asinh(
        rgb[:,:,2],
        stretch
    )


    RGB = np.dstack(
        [
            Rv,
            Gv,
            Bv
        ]
    )


    return np.clip(
        RGB,
        0,
        1
    )