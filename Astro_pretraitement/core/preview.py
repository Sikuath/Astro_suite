import numpy as np
from astropy.io import fits
from PIL import Image


def fits_preview(path):

    with fits.open(path) as hdul:
        data = hdul[0].data


    if data is None:
        return None


    data = np.nan_to_num(data)


    # Stretch rapide pour visualisation
    low = np.percentile(data, 1)
    high = np.percentile(data, 99)


    if high == low:
        return None


    img = (data - low) / (high - low)

    img = np.clip(img, 0, 1)


    img = (img * 255).astype(np.uint8)


    image = Image.fromarray(img)


    # Réduction de 50 %
    new_size = (
        image.width // 2,
        image.height // 2
    )

    image = image.resize(
        new_size,
        Image.Resampling.LANCZOS
    )


    return image