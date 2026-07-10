from astropy.io import fits
import numpy as np

def load_fits(path):
    data = fits.getdata(path).astype(np.float32)

    try:
        header = fits.getheader(path)
    except:
        header = None

    return data, header


def save_fits(path, data, header=None):
    fits.PrimaryHDU(
        data.astype(np.float32),
        header=header
    ).writeto(path, overwrite=True)