from spectral import save_rgb


def envi_to_spy(img, rgb_output, bands=None):
    """
    Generates an RGB file using spectral-python's approach.

    :param img: the ENVI image to save as RGB
    :param rgb_output: the RGB output file
    :type rgb_output: str
    :param bands: the int list of bands to use for the R,G,B channels, auto if None
    :type bands: list
    """
    if bands is not None:
        bands = tuple(bands)
    save_rgb(rgb_output, img, bands=bands)
