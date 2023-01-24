import argparse
import json
import numpy as np
import traceback
import spectral
import spectral.io.envi as envi

FORMAT_PLAINTEXT = "text"
FORMAT_JSON = "json"
FORMATS = [FORMAT_PLAINTEXT, FORMAT_JSON]


def interleave_to_str(interleave):
    """
    Turns the interleave type into a string.

    :param interleave: the interleave to turn into a string
    :type interleave: int
    :return: the interleave string
    :rtype: str
    """
    if interleave == spectral.BIL:
        return 'BIL'
    elif interleave == spectral.BIP:
        return 'BIP'
    elif interleave == spectral.BSQ:
        return 'BSQ'
    else:
        raise Exception("Unknown interleave type: %d" % interleave)


def generate(envi_input, format=None, info_output=None):
    """
    Generates information from an ENVI file.

    :param envi_input: the ENVI file to use
    :type envi_input: str
    :param info_output: the file to write the output to
    :type info_output: str
    :param format: the type of output to generate
    :type format: str
    """
    img = envi.open(envi_input)

    if format == FORMAT_PLAINTEXT:
        info = "Filename....: %s\n" % img.filename \
               + "# Rows......: %d\n" % img.nrows \
               + "# Cols......: %d\n" % img.ncols \
               + "# Bands.....: %d\n" % img.nbands \
               + "Interleave..: %s\n" % interleave_to_str(img.interleave) \
               + "Quantization: %d bits\n" % (img.sample_size * 8) \
               + "Data format.: %s\n" % np.dtype(img.dtype).name
    elif format == FORMAT_JSON:
        d = dict()
        d["filename"] = img.filename
        d["rows"] = img.nrows
        d["cols"] = img.ncols
        d["bands"] = img.nbands
        d["interleave"] = interleave_to_str(img.interleave)
        d["quantization_bits"] = img.sample_size * 8
        d["data_format"] = np.dtype(img.dtype).name
        info = json.dumps(d, indent=2)
    else:
        raise Exception("Unknown output format: %s" % format)

    if info_output is None:
        print(info)
    else:
        with open(info_output, "w") as fp:
            fp.write(info)
            fp.write("\n")


def main(args=None):
    """
    The main method for parsing command-line arguments and labeling.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="Outputs information on ENVI files in various formats, on stdout or to a file.",
        prog="spy-envi_info",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="FILE", help="the ENVI file to obtain information from", required=True)
    parser.add_argument("-o", "--output", metavar="FILE", help="the file to write the information to", required=False)
    parser.add_argument("-f", "--format", choices=FORMATS, default=FORMAT_PLAINTEXT, help="the format to use for the information.", required=False)
    parsed = parser.parse_args(args=args)
    generate(parsed.input, format=parsed.format, info_output=parsed.output)


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
