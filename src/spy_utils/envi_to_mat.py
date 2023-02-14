import argparse
import traceback
import spectral.io.envi as envi

from spy_utils.core import Range
from spy_utils.mat import envi_to_simple, envi_to_happy


CONVERSION_SIMPLE = "simple"
CONVERSION_HAPPY = "happy"

CONVERSIONS = [
    CONVERSION_SIMPLE,
    CONVERSION_HAPPY,
]


def convert(envi_input, mat_output, bands=None, conversion=CONVERSION_SIMPLE):
    """
    Converts the ENVI file to a Matlab file.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param mat_output: the Matlab output to generate
    :type mat_output: str
    :param bands: the range of 1-based band indices to output, uses all if None
    :type bands: str
    :param conversion: how to convert the hyper-spectral data
    :type conversion: str
    """
    img = envi.open(envi_input)
    if bands is None:
        bands = "first-last"
    bands = Range(bands, maximum=img.nbands).indices(zero_based=True)

    if conversion == CONVERSION_SIMPLE:
        envi_to_simple(envi_input, img, mat_output, bands)
    elif conversion == CONVERSION_HAPPY:
        envi_to_happy(envi_input, img, mat_output, bands)
    else:
        raise Exception("Unhandled conversion: %s" % conversion)


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
    parser.add_argument("-c", "--conversion", choices=CONVERSIONS, help="the conversion type to apply.", default=CONVERSION_SIMPLE)
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
