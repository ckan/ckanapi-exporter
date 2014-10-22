[![PyPI version](https://badge.fury.io/py/ckanapi-exporter.svg)](http://badge.fury.io/py/ckanapi-exporter)


ckanapi-exporter
================

An API client (usable as a command-line script or as a Python library)
for exporting dataset metadata from CKAN sites to Excel-compatible
CSV files.

This is a thin wrapper around [losser](https://github.com/ckan/losser),
hooking it up to the CKAN API.

TODO: Document the preprocessing of dataset extras.


Requirements
------------

Python 2.7, or 2.6 with the argparse library.


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
2. Transform and filter the datasets according to the columns specified in columns.json
3. Write the result as UTF8-encoded, CSV-formatted text to output.csv

TODO: Document the columns.json file format.

Using as a Python library:

    import ckanapi_exporter.exporter as exporter
    csv_string = exporter.export('http://demo.ckan.org', 'columns.json')

Returns a UTF8-encoded string.

The second argument can be either the filename of the columns.json file as a
string, or a list of dictionaries (equivalent to the contents of columns.json
file after loading the JSON).
