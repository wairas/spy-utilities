# spy-utilities
Command-line utilities for the Spectral Python (SPy) library.

## Tools

### spy-envi_info

```
usage: spy-envi_info [-h] -i FILE [-o FILE] [-f {text,json}] [-p]

Outputs information on ENVI files in various formats, on stdout or to a file.

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        the ENVI file to obtain information from (default:
                        None)
  -o FILE, --output FILE
                        the file to write the information to (default: None)
  -f {text,json}, --format {text,json}
                        the format to use for the information. (default: text)
  -p, --full_path       whether to use the full path of the input file in the
                        output or just the base name (default) (default:
                        False)
```

### spy-envi_to_grayscale

```
usage: spy-envi_to_grayscale [-h] -i FILE -o FILE [-b RANGE] [-v]

Converts an ENVI file to grayscale file(s) based on the selected range of
bands. Requires .hdr and .dat files.

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        the ENVI file to convert (default: None)
  -o FILE, --output FILE
                        the grayscale RGB file to generate (JPG or PNG); use
                        placeholders '{BAND0}' and '{BAND1}' for 0-based and
                        1-based band indices in the filename. (default: None)
  -b RANGE, --bands RANGE
                        the range of bands to output (1-based indices), e.g.,
                        'first-last', '7', '3-7,9,45' (default: 1)
  -v, --verbose         whether to output some progress information. (default:
                        False)
```


### spy-envi_to_rgb

```
usage: spy-envi_to_rgb [-h] -i FILE -o FILE [-b BANDS]

Converts an ENVI file to an RGB. Requires .hdr and .dat files.

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        the ENVI file to convert (default: None)
  -o FILE, --output FILE
                        the RGB file to generate (JPG or PNG). (default: None)
  -b BANDS, --bands BANDS
                        the comma-separated list of the three bands to act as
                        R,G,B channels (band indices are 0-based); combines
                        all bands if not specified. (default: None)
```
