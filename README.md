# spy-utilities
Command-line utilities for the Spectral Python (SPy) library.

## Tools

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
