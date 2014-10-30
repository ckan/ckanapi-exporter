[![Build Status](https://travis-ci.org/ckan/ckanapi-exporter.svg)](https://travis-ci.org/ckan/ckanapi-exporter)
[![Coverage Status](https://img.shields.io/coveralls/ckan/ckanapi-exporter.svg)](https://coveralls.io/r/ckan/ckanapi-exporter)
[![Latest Version](https://pypip.in/version/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Downloads](https://pypip.in/download/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Supported Python versions](https://pypip.in/py_versions/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Development Status](https://pypip.in/status/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![License](https://pypip.in/license/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)

ckanapi-exporter
================

An API client (usable as a command-line script or as a Python library)
for exporting dataset metadata from CKAN sites to Excel-compatible
CSV files.

This is a thin wrapper around [losser](https://github.com/ckan/losser),
hooking it up to the CKAN API.

Requirements
------------

Python 2.7, does not work with 2.6!


Installation
------------

To install run:

    pip install ckanapi-exporter

To install for development, create and activate a Python virtual environment
then do:

    git clone https://github.com/ckan/ckanapi-exporter.git
    cd ckanapi-exporter
    python setup.py develop


Usage
-----

From the command line:

    ckanapi-exporter --url 'http://demo.ckan.org' --columns columns.json > output.csv

This will:

1. Fetch metadata for all datasets from demo.ckan.org
   ([TODO](https://github.com/ckan/ckanapi-exporter/issues/1): optionally only export some datasets)
2. Transform and filter the datasets according to the columns specified in `columns.json`
3. Write the result as UTF8-encoded, CSV-formatted text to `output.csv`

You must supply the `columns.json` file specifying what columns should be in
the output CSV table and how the values for those columns should be retrieved
from the datasets. For example:

    {
      "Data Owner": {
          "pattern_path": "^author$",
          "unique": true,
          "case_sensitive": true
      },
      "Delivery Unit": {
          "pattern_path": ["^extras$", "^Delivery Unit$"],
          "unique": true
      },
      "Contributor": {
          "pattern_path": ["^extras$", "^Contributor.*"]
      },
      "Description": {
          "pattern_path": "^notes$",
          "unique": true,
          "case_sensitive": true,
          "max_length": 255
      },
      "Format": {
          "pattern_path": ["^resources$", "^format$"],
          "case_sensitive": true,
          "deduplicate": true
      }
    }

This specifies five column headings for the output CSV:

1. Data Owner
2. Delivery Unit
3. Contributor
4. Description
5. Format

The columns in the CSV file will be in the order that they appear in the
`columns.json` file.

The values for the Data Owner column are found by matching the regular
expression `"^author$"` against the top-level keys of each of the datasets.
This will export the "author" fields of the datasets.

The values for the Delivery Unit column are found by looking for a dataset
extra whose name matches the regular expression `"^Delivery Unit$"`. If more
than one extra has a matching name it will crash with a `UniqueError`.
This will export the "Delivery Unit" extras of the datasets.

The values for the Contributor column are found by looking for dataset
extras whose names match the regular expression `"^Contributor.*"`
case-insensitively. This will find extras named "contributor", "Contributor",
"Contributor 1", "Contributor 2", etc. When there are multiple matches they'll
be written as a quoted comma-separated list in the CSV file, for example:
`"Thom Yorke,Nigel Godrich,Jonny Greenwood"`.

The Description column finds the "notes" field of each dataset and truncates
the value to the first 255 characters.

The Format column finds the "format" field of each of the dataset's resources
and outputs them as a quoted comma-separated list, deduplicated. For example:
`"JSON, CSV, PDF"`.

See the [losser docs](https://github.com/ckan/losser) for further documentation
of the `columns.json` file format.

For a working example `columns.json` file that you can use against demo.ckan.org,
see [ckanapi_exporter/test_columns.json](test_columns.json).


### Using as a Python Library

You can also import ckanapi-exporter in Python and use it from your CKAN API
client or plugin:

    import ckanapi_exporter.exporter as exporter
    csv_string = exporter.export('http://demo.ckan.org', 'columns.json')

Returns a UTF8-encoded string.

The second argument can be either the filename of the columns.json file as a
string, or a list of dictionaries (equivalent to the contents of columns.json
file after loading the JSON).


Dataset Preprocessing
---------------------

ckanapi-exporter does some preprocessing of the datasets from CKAN before
passing them to losser. Normally CKAN's dataset extras are formatted as a list
of dictionaries:

    {
      ...
      "extras": [
        {
          "key": "extra 1",
          "value": "value 1"
        },
        {
          "key": "extra 2",
          "value": "value 2"
        },
        ...
      ],
      ...
    }

This is not very convenient for losser, which can only match patterns against
an object's keys not their values. So ckanapi-exporter transforms this into a
single dictionary:

    {
      ...
      "extras": {
        "extra 1": "value 1",
        "extra 2": "value 2",
        ...
      },
      ...
    }

This enables you to retrieve extras by name with pattern paths like this in
your `columns.json`: `["^extras$", "^extra 1$"]`.

Improvements to losser could make this preprocessing unnecessary.
