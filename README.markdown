[![Build Status](https://travis-ci.org/ckan/ckanapi-exporter.svg)](https://travis-ci.org/ckan/ckanapi-exporter)
[![Coverage Status](https://img.shields.io/coveralls/ckan/ckanapi-exporter.svg)](https://coveralls.io/r/ckan/ckanapi-exporter)
[![Latest Version](https://pypip.in/version/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Downloads](https://pypip.in/download/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Supported Python versions](https://pypip.in/py_versions/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Development Status](https://pypip.in/status/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![License](https://pypip.in/license/ckanapi-exporter/badge.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)

ckanapi-exporter
================

An API client (usable as a command-line script or as a Python library) for
exporting dataset metadata from CKAN sites to Excel-compatible CSV files.


Requirements
------------

Python 2.7, does not work with 2.6!


Installation
------------

To install run:

    pip install ckanapi-exporter


Usage
-----

For example, to create a one-column CSV file containing the titles of all the
datasets from demo.ckan.org:

```bash
ckanapi-exporter --url 'http://demo.ckan.org' \
    --column "Title" --pattern '^title$' > output.csv
```

This searches for the field matching the regular expression '^title$' in each
dataset (the `--pattern` argument) and puts the values into a column called
"Title" in the CSV file (the `--column` argument). It'll create an `output.csv`
file something like this:

<table>
  <tr>
    <th>Title</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
  </tr>
  <tr>
    <td>UK at Burglaries</td>
  </tr>
  <tr>
    <td>...</td>
  </tr>
</table>

To add a second column containing quoted, comma-separated lists of each of the
datasets' resource formats just add another pair of `--column` and
`--pattern` options:

```bash
ckanapi-exporter --url 'http://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column Formats --pattern '^resources$' '^format$' > output.csv
```

This time the pattern has two arguments: `--pattern '^resources$' '^format$'`.
This means find the "resources" field of each dataset and then find the
"format" field of each resource. It'll create a CSV file something like this:

<table>
  <tr>
    <th>Title</th>
    <th>Formats</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
    <td>XLSX, CSV</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
    <td>CSV, CSV, CSV, CSV</td>
  </tr>
  <tr>
    <td>UK at Burglaries</td>
    <td>JPEG, CSV, CSV</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

CSV is repeated a lot because lots of the datasets have multiple CSV resources.
You can add the `--deduplicate` option to the column to remove the duplication:

```bash
ckanapi-exporter --url 'http://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column Formats --pattern '^resources$' '^format$' --deduplicate \
    > output.csv
```

<table>
  <tr>
    <th>Title</th>
    <th>Formats</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
    <td>XLSX, CSV</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
    <td>CSV</td>
  </tr>
  <tr>
    <td>UK at Burglaries</td>
    <td>JPEG, CSV</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

You can also specify your columns in a `columns.json` file like this:

```json
{
  "Data Owner": {
      "pattern": "^author$",
      "unique": true,
      "case_sensitive": true
  },
  "Delivery Unit": {
      "pattern": ["^extras$", "^Delivery Unit$"],
      "unique": true
  },
  "Contributor": {
      "pattern": ["^extras$", "^Contributor.*"]
  },
  "Description": {
      "pattern": "^notes$",
      "unique": true,
      "case_sensitive": true,
      "max_length": 255
  },
  "Format": {
      "pattern": ["^resources$", "^format$"],
      "case_sensitive": true,
      "deduplicate": true
  }
}
```

Then tell ckanapi-exporter to read the column options from this file instead of
giving them on the command line:

```bash
ckanapi-exporter --url 'http://demo.ckan.org' --columns columns.json > output.csv
```

For a working example `columns.json` file that you can use against demo.ckan.org,
see [test_columns.json](ckanapi_exporter/test_columns.json).

ckanapi-exporter is a thin wrapper around
[losser](https://github.com/ckan/losser), hooking it up to the CKAN API.
For more documentation of the filtering and transforming options run
`ckanapi-exporter --help` or read losser's docs.


Exporting Dataset Extras
------------------------

This column in a `columns.json` file will find a dataset extra whose name (key)
matches the regular expression `"^Delivery Unit$" in each dataset, and will
crash if any dataset has more than one matching extra:

```json
"Delivery Unit": {
    "pattern_path": ["^extras$", "^Delivery Unit$"],
    "unique": true
},
```

This column will find dataset extras whose names match the regular expression
`"^Contributor.*"` case-insensitively. This will find extras named
"contributor", "Contributor", "Contributor 1", "Contributor 2", etc. When there
are multiple matches they'll be written as a quoted comma-separated list in the
CSV file, for example: `"Thom Yorke,Nigel Godrich,Jonny Greenwood"`.

```json
"Contributor": {
    "pattern_path": ["^extras$", "^Contributor.*"]
},
```


Using as a Python Library
-------------------------

You can also import ckanapi-exporter in Python and use it from your CKAN API
client or plugin:

```python
import ckanapi_exporter.exporter as exporter
csv_string = exporter.export('http://demo.ckan.org', 'columns.json')
```

Returns a UTF8-encoded string.

The second argument can be either the filename of the columns.json file as a
string, or a list of dictionaries (equivalent to the contents of columns.json
file after loading the JSON).


Development
-----------

To install for development, create and activate a Python virtual environment
then do:

```bash
git clone https://github.com/ckan/ckanapi-exporter.git
cd ckanapi-exporter
python setup.py develop
pip install -r dev-requirements.txt
```

To run the tests do:

    nosetests
