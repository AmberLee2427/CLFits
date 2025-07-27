# CLFits: FITS Header Editor

A command-line tool for viewing and editing the headers of FITS files.

[![PyPI Version](https://img.shields.io/pypi/v/clfits.svg)](https://pypi.org/project/clfits)
[![Test Coverage](https://codecov.io/gh/AmberLee2427/CLFits/branch/main/graph/badge.svg)](https://codecov.io/gh/AmberLee2427/CLFits)
[![CI Status](https://github.com/AmberLee2427/CLFits/actions/workflows/ci.yml/badge.svg)](https://github.com/AmberLee2427/CLFits/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install clfits
```

## Quick Start

### View a Header

To view the primary header of a FITS file:
```bash
clfits view my_image.fits
```

To view the header of a specific extension (e.g., the second HDU, index 1):
```bash
clfits view my_image.fits --hdu 1
```

Or view an extension by name:
```bash
clfits view my_image.fits --hdu "OBSERVATIONS"
```

### Get, Set, and Delete Keywords

```bash
# Get the value of a keyword
clfits get my_image.fits OBJECT

# Set a new value for a keyword
clfits set my_image.fits OBJECT "NGC 42"

# Set a keyword with a comment
clfits set my_image.fits OBSERVER "Webb" --comment "James Webb Space Telescope"

# Delete a keyword from the first extension's header
clfits del my_image.fits --hdu 1 TFORM1
```

### Search and Filter Keywords

Find all keywords starting with "NAXIS":
```bash
clfits search my_image.fits --key "NAXIS*"
```

Find all keywords in the "EVENTS" extension where the value is a specific string:
```bash
clfits search my_image.fits --hdu "EVENTS" --value "GTI"
```

### Export Headers

Export the primary header to a JSON file:
```bash
clfits export my_image.fits --output header.json
```

Export the header of the second HDU to YAML, printing to the console:
```bash
clfits export my_image.fits --hdu 1 --format yaml
```

## Documentation

Full documentation is available at [clfits.readthedocs.io](https://clfits.readthedocs.io). 
