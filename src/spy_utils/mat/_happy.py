import os
import scipy.io

from spy_utils.core import spectral_subset, wavelength_subset, is_int


def envi_to_happy(envi_input, img, mat_output, bands=None):
    """
    Outputs the hyper-spectral data in happy format: FinalMask, ceiling, class, lambda, normcube, y.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param img: the hyper spectral image to output
    :param mat_output: the Matlab output to generate
    :type mat_output: str
    :param bands: list of band indices to output, all if None
    :type bands: list
    """
    # TODO normalize?
    normcube = spectral_subset(img, bands)

    if "ceiling" in img.metadata:
        ceiling = img.metadata["ceiling"]
    else:
        ceiling = 1

    envi_base = os.path.basename(os.path.dirname(envi_input))
    y_str = ""
    label = ""
    for i in range(len(envi_base)):
        if envi_base[i] == ".":
            y_str += "."
        elif is_int(envi_base[i]):
            y_str += envi_base[i]
        else:
            label = envi_base[i]
            break
    y = float(y_str)

    data = {
        "FinalMask": [1.0],  # TODO
        "ceiling": ceiling,
        "class": label == "r",  # x is False
        "normcube": normcube,
        "lambda": wavelength_subset(img, bands),
        "y": y,
    }
    scipy.io.savemat(mat_output, mdict=data)
