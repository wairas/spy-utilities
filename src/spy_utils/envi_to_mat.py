import argparse
import traceback
import numpy as np
import os
import scipy.io
import spectral.io.envi as envi

from spy_utils.core import Range, is_int


OUTPUT_TYPE_SIMPLE = "simple"
OUTPUT_TYPE_HAPPY = "happy"

OUTPUT_TYPES = [
    OUTPUT_TYPE_SIMPLE,
    OUTPUT_TYPE_HAPPY,
]


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


def output_simple(envi_input, img, mat_output, bands=None):
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


def output_happy(envi_input, img, mat_output, bands=None):
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

    envi_base = os.path.basename(os.path.dirname(envi_input))
    y_str = ""
    for i in range(len(envi_base)):
        if envi_base[i] == ".":
            y_str += "."
        elif is_int(envi_base[i]):
            y_str += envi_base[i]
        else:
            break
    y = float(y_str)

    data = {
        "FinalMask": [1.0],  # TODO
        "ceiling": 1.0,  # TODO
        "class": True,  # TODO
        "normcube": normcube,
        "lambda": wavelength_subset(img, bands),
        "y": y,
    }
    scipy.io.savemat(mat_output, mdict=data)


def output(envi_input, mat_output, bands=None, output_type=OUTPUT_TYPE_SIMPLE):
    """
    Converts the ENVI file to a Matlab file.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param mat_output: the Matlab output to generate
    :type mat_output: str
    :param bands: the range of 1-based band indices to output, uses all if None
    :type bands: str
    :param output_type: how to output the hyperspectral data
    :type output_type: str
    """
    img = envi.open(envi_input)
    if bands is None:
        bands = "first-last"
    bands = Range(bands, maximum=img.nbands).indices(zero_based=True)

    if output_type == OUTPUT_TYPE_SIMPLE:
        output_happy(envi_input, img, mat_output, bands)
    else:
        raise Exception("Unhandled output type: %s" % output_type)


def main(args=None):
    """
    The main method for parsing command-line arguments and labeling.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="Converts an ENVI file to a Matlab file. Requires .hdr and .dat files.",
        prog="spy-envi_to_mat",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="FILE", help="the ENVI file to convert", required=True)
    parser.add_argument("-o", "--output", metavar="FILE", help="the RGB file to generate (JPG or PNG).", required=True)
    parser.add_argument("-b", "--bands", metavar="BANDS", help="the range of 1-based band indices to output; uses all bands if not specified.", default="first-last")
    parser.add_argument("-t", "--output_type", choices=OUTPUT_TYPES, help="the type of Matlab file to generate.", default=OUTPUT_TYPE_SIMPLE)
    parsed = parser.parse_args(args=args)
    output(parsed.input, parsed.output, bands=parsed.bands)


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
