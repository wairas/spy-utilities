import numpy as np

from PIL import Image


def envi_to_happy(img, rgb_output, bands=None):
    """
    Generates an RGB file using happy's approach.

    :param img: the ENVI image to save as RGB
    :param rgb_output: the RGB output file
    :type rgb_output: str
    :param bands: the int list of bands to use for the R,G,B channels, auto if None
    :type bands: list
    """
    if bands is None:
        bands = [0, img.nbands / 2, img.nbands - 1]
    data = img.load()
    mins = [np.amin(data[:, :, b]) for b in bands]
    maxs = [np.amax(data[:, :, b]) for b in bands]
    tmeans = [np.mean(data[:, :, b]) for b in bands]
    means = [tmeans[i] / max(tmeans) for i in range(len(tmeans))]
    channels = [data[:, :, i].reshape((img.nrows, img.ncols)) for i in bands]
    channels = [(channels[i] - mins[i]) / (maxs[i] - mins[i]) * means[i] for i in range(len(channels))]
    channels = [x * 255.0 for x in channels]
    arr = np.ndarray((img.nrows, img.ncols, 3))
    for i in range(3):
        arr[:, :, i] = channels[i]
    img = Image.fromarray(arr.astype('uint8'), 'RGB')
    with open(rgb_output, "wb") as fp:
        img.save(fp)
