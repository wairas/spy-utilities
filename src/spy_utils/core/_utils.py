import numpy as np


def is_int(s):
    """
    Checks whether the string represents an integer.

    :param s: the string to check
    :type s: str
    :return: True if an integer
    :rtype: bool
    """
    try:
        int(s)
        return True
    except:
        return False


def is_float(s):
    """
    Checks whether the string represents a float.

    :param s: the string to check
    :type s: str
    :return: True if a float
    :rtype: bool
    """
    try:
        float(s)
        return True
    except:
        return False


def is_bool(s):
    """
    Checks whether the string represents a bool.

    :param s: the string to check
    :type s: str
    :return: True if a bool
    :rtype: bool
    """
    try:
        bool(s)
        return True
    except:
        return False


def spectral_subset(img, bands=None):
    """
    Generates a subset of the hyper-spectal data if necessary.

    :param img: the spectral image to turn into numpy array
    :param bands: the bands to select (list of 0-based indices), uses all if None
    :type bands: list
    :return: the spectral data
    :rtype: np.ndarray
    """
    b = img.load()
    if bands is not None:
        b_new = np.ndarray((b.shape[0], b.shape[1], len(bands)), dtype=b.dtype)
        for i in range(len(bands)):
            b_new[:, :, i] = np.reshape(b[:, :, bands[i]], b_new[:, :, i].shape)
        b = b_new
    return b


def wavelength_subset(img, bands=None):
    """
    Returns the list of wavelengths.

    :param img: the ENVI image to get the wavelengths from
    :param bands: the bands to use (list of 0-based indices), uses all if None
    :type bands: list
    :return: the list of wave numbers (list of floats)
    :rtype: list
    """
    if bands is None:
        return [[float(x)] for x in img.metadata["wavelength"]]
    else:
        return [[float(img.metadata["wavelength"][b])] for b in bands]
