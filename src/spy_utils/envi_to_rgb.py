import argparse
import traceback
import spectral.io.envi as envi
from spectral import save_rgb


def convert(envi_input, rgb_output, bands=None):
    """
    Converts the ENVI file to RGB.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param rgb_output: the RGB output to generate
    :type rgb_output: str
    :param bands: the comma-separated of bands in R,G,B to output
    :type bands: str
    """
    img = envi.open(envi_input)
    if bands is not None:
        bands = tuple(int(x) for x in bands.replace(" ", "").split(","))
    save_rgb(rgb_output, img, bands=bands)


def main(args=None):
    """
    The main method for parsing command-line arguments and labeling.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="Converts an ENVI file to an RGB. Requires .hdr and .dat files.",
        prog="spu-envi_to_rgb",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="FILE", help="the ENVI file to convert", required=True)
    parser.add_argument("-o", "--output", metavar="FILE", help="the RGB file to generate.", required=True)
    parser.add_argument("-b", "--bands", metavar="BANDS", help="the comma-separated list of R,G,B 3-tuple to extract.")
    parsed = parser.parse_args(args=args)
    convert(parsed.input, parsed.output, bands=parsed.bands)


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
