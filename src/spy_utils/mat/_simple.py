import scipy.io

from spy_utils.core import spectral_subset, wavelength_subset


def envi_to_simple(envi_input, img, mat_output, bands=None):
    """
    Outputs the hyper-spectral data in a simple format: filename, bands, wave_length.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param img: the hyper spectral image to output
    :param mat_output: the Matlab output to generate
    :type mat_output: str
    :param bands: list of band indices to output, all if None
    :type bands: list
    """
    data = {
        "filename": envi_input,
        "bands": spectral_subset(img, bands),
        "wavelength": wavelength_subset(img, bands),
    }
    scipy.io.savemat(mat_output, mdict=data)
