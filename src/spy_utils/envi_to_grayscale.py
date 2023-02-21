import argparse
import traceback
import spectral.io.envi as envi
from spectral import save_rgb
from simple_range import Range


PH_BAND_0 = "{BAND0}"
""" placeholder for the 0-based band. """

PH_BAND_1 = "{BAND1}"
""" placeholder for the 1-based band. """

PLACEHOLDERS = [PH_BAND_0, PH_BAND_1]


def convert(envi_input, grayscale_output, bands="1", verbose=False):
    """
    Converts the ENVI file to RGB.

    :param envi_input: the ENVI file to convert
    :type envi_input: str
    :param grayscale_output: the grayscale output to generate (can include PLACEHOLDERS)
    :type grayscale_output: str
    :param bands: the range of bands to extract (1-based indices, e.g., 'first-last', '1-6,7,9,23-29', first/second/third/last_2/last_1/last accepted as well)
    :type bands: str
    :param verbose: whether to be verbose in the output
    :type verbose: bool
    """
    if verbose:
        print("Loading %s..." % envi_input)
    img = envi.open(envi_input)
    brange = Range(bands, maximum=img.nbands)
    indices = brange.indices()
    if len(indices) == 0:
        raise Exception("No indices selected!")
    if verbose:
        print("Selected indices (0-based): %s" % str(indices))
    has_phs = False
    if len(indices) > 1:
        for ph in PLACEHOLDERS:
            if ph in grayscale_output:
                has_phs = True
                break
        if not has_phs:
            raise Exception("Multiple bands selected, but no placeholder in output name (placeholders: %s)!" % ",".join(PLACEHOLDERS))
    num_digits = len(str(max(indices) + 1))
    for i in indices:
        output_file = grayscale_output
        if has_phs:
            output_file = output_file.replace(PH_BAND_0, str(i).zfill(num_digits))
            output_file = output_file.replace(PH_BAND_1, str(i+1).zfill(num_digits))
        if verbose:
            print("%d/%d: Saving %s..." % ((i+1), len(indices), output_file))
        save_rgb(output_file, img, bands=(i, i, i))


def main(args=None):
    """
    The main method for parsing command-line arguments and labeling.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="Converts an ENVI file to grayscale file(s) based on the selected range of bands. Requires .hdr and .dat files.",
        prog="spy-envi_to_grayscale",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="FILE", help="the ENVI file to convert", required=True)
    parser.add_argument("-o", "--output", metavar="FILE", help="the grayscale RGB file to generate (JPG or PNG); use placeholders '%s' and '%s' for 0-based and 1-based band indices in the filename." % (PH_BAND_0, PH_BAND_1), required=True)
    parser.add_argument("-b", "--bands", metavar="RANGE", help="the range of bands to output (1-based indices), e.g., 'first-last', '7', '3-7,9,45'", default="1")
    parser.add_argument("-v", "--verbose", action="store_true", help="whether to output some progress information.")
    parsed = parser.parse_args(args=args)
    convert(parsed.input, parsed.output, bands=parsed.bands, verbose=parsed.verbose)


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
