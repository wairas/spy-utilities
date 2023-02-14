import argparse
import numpy as np
import traceback
import spectral.io.envi as envi

from PIL import Image
from spectral import save_rgb


CONVERSION_SPY = "spy"
CONVERSION_HAPPY = "happy"

CONVERSIONS = [
    CONVERSION_SPY,
    CONVERSION_HAPPY,
]


def to_happy(img, rgb_output, bands=None):
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


def to_spy(img, rgb_output, bands=None):
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


def convert(envi_input, rgb_output, bands=None, conversion=CONVERSION_SPY):
    """
    Converts the ENVI file to RGB.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param rgb_output: the RGB output to generate
    :type rgb_output: str
    :param bands: the comma-separated list of three bands to use as R,G,B channels in output
    :type bands: str
    :param conversion: how to generate the RGB output
    :type conversion: str
    """
    img = envi.open(envi_input)
    if bands is not None:
        bands = list(int(x) for x in bands.replace(" ", "").split(","))
        if len(bands) != 3:
            raise Exception("Expected three bands, but got %d instead: %s" % (len(bands), str(bands)))

    if conversion == CONVERSION_SPY:
        to_spy(img, rgb_output, bands=bands)
    elif conversion == CONVERSION_HAPPY:
        to_happy(img, rgb_output, bands=bands)
    else:
        raise Exception("Unhandled conversion: %s" % conversion)


def main(args=None):
    """
    The main method for parsing command-line arguments and labeling.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="Converts an ENVI file to an RGB. Requires .hdr and .dat files.",
        prog="spy-envi_to_rgb",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="FILE", help="the ENVI file to convert", required=True)
    parser.add_argument("-o", "--output", metavar="FILE", help="the RGB file to generate (JPG or PNG).", required=True)
    parser.add_argument("-b", "--bands", metavar="BANDS", help="the comma-separated list of the three bands to act as R,G,B channels (band indices are 0-based); combines all bands if not specified.")
    parser.add_argument("-c", "--conversion", choices=CONVERSIONS, help="how to generate the RGB file.", default=CONVERSION_SPY)
    parsed = parser.parse_args(args=args)
    convert(parsed.input, parsed.output, bands=parsed.bands, conversion=parsed.conversion)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    main()
