[![Build Status](https://travis-ci.org/ckan/ckanapi-exporter.svg)](https://travis-ci.org/ckan/ckanapi-exporter)
[![Coverage Status](https://img.shields.io/coveralls/ckan/ckanapi-exporter.svg)](https://coveralls.io/r/ckan/ckanapi-exporter)
[![Latest Version](https://img.shields.io/pypi/v/ckanapi-exporter.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/ckanapi-exporter.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![Development Status](https://img.shields.io/pypi/status/ckanapi-exporter.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)
[![License](https://img.shields.io/pypi/l/ckanapi-exporter.svg)](https://pypi.python.org/pypi/ckanapi-exporter/)

ckanapi-exporter
================

An API client (usable as a command-line script or as a Python library) for
exporting dataset metadata from CKAN sites to Excel-compatible CSV files.


Installation
------------

To install run:

    pip install ckanapi-exporter


Usage
-----

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --column "Title" --pattern '^title$' > output.csv
```

This searches each dataset on demo.ckan.org for fields matching the
[regular expression](https://docs.python.org/2/howto/regex.html#regex-howto)
`^title$` (the `--pattern` argument) and puts the values into a
column called "Title" in the CSV file (the `--column` argument).  It'll create
an `output.csv` file something like this:

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
    <td>UK Cat Burglaries</td>
  </tr>
  <tr>
    <td>...</td>
  </tr>
</table>

You can add as many columns as you want: just add a `--column` and a
`--pattern` argument for each column. The title of the column in the CSV file
can be anything you want - it doesn't have to match the name of the field in
CKAN. Let's add a second column titled "Rights" that contains the
`license_title` fields from the datasets:

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column "Rights" --pattern '^license_title$' > output.csv
```

<table>
  <tr>
    <th>Title</th>
    <th>Rights</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
    <td>Creative Commons Attribution</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
    <td>Creative Commons CCZero</td>
  </tr>
  <tr>
    <td>UK Cat Burglaries</td>
    <td>UK Open Government Licence (OGL)</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

### API Parameters
The ckanapi-exporter calls the [`package_search`](http://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.get.package_search)
API action and you can pass in related query parameters by using the `--params`
argument and passing in a string formated as a dictionary. Each key: value pair
represents a query passed to the API call.

For example if you wanted to only export datasets between a date range you can
pass in the `fq` (filtered query) parameter and use `metadata_created` to filter
the results.

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --params "{'fq':'metadata_created:[2017-01-01T00:00:00Z TO 2017-01-31T23:59:99.999Z]'}" \
    --column "Title" --pattern '^title$' \
    --column "Rights" --pattern '^license_title$' > output.csv
```


### Transformations

You can apply certain transformations to the values from the datasets.
For example, let's add a third column with the first 50 characters of each
dataset's description (the `notes` field in the CKAN API):

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column "Rights" --pattern '^license_title$' \
    --column "Description" --pattern '^notes$' --max-length 50 > output.csv
```

<table>
  <tr>
    <th>Title</th>
    <th>Rights</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
    <td>Creative Commons Attribution</td>
    <td>Demo information about senior salaries from 11/04/</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
    <td>Creative Commons CCZero</td>
    <td>Data on spending over £500 generated for Open Data</td>
  </tr>
  <tr>
    <td>UK Cat Burglaries</td>
    <td>UK Open Government Licence (OGL)</td>
    <td>A record of cat burgalries, listing the cat names,</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>


### Exporting Resource Fields

Let's add a column containing the formats of each datasets' resources:

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column "Rights" --pattern '^license_title$' \
    --column "Description" --pattern '^notes$' --max-length 50 \
    --column Formats --pattern '^resources$' '^format$' > output.csv
```

This time the pattern has two arguments: `--pattern '^resources$' '^format$'`.
This means find the "resources" field of each dataset and then find the
"format" field of each resource. When a dataset has more than one resource
the formats will be combined into a quoted, comma-separated list in a single
table cell. It'll create a CSV file something like this:

<table>
  <tr>
    <th>Title</th>
    <th>Rights</th>
    <th>Description</th>
    <th>Formats</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
    <td>Creative Commons Attribution</td>
    <td>Demo information about senior salaries from 11/04/</td>
    <td>XLSX, CSV</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
    <td>Creative Commons CCZero</td>
    <td>Data on spending over £500 generated for Open Data</td>
    <td>CSV, CSV, CSV, CSV</td>
  </tr>
  <tr>
    <td>UK Cat Burglaries</td>
    <td>UK Open Government Licence (OGL)</td>
    <td>A record of cat burgalries, listing the cat names,</td>
    <td>JPEG, CSV, CSV</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

CSV is repeated a lot because lots of the datasets have multiple CSV resources.
You can add the `--deduplicate` option to the column to remove the duplication:

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column "Rights" --pattern '^license_title$' \
    --column "Description" --pattern '^notes$' --max-length 50 \
    --column Formats --pattern '^resources$' '^format$' --deduplicate \
    > output.csv
```

<table>
  <tr>
    <th>Title</th>
    <th>Rights</th>
    <th>Description</th>
    <th>Formats</th>
  </tr>
  <tr>
    <td>Senior Salaries Information</td>
    <td>Creative Commons Attribution</td>
    <td>Demo information about senior salaries from 11/04/</td>
    <td>XLSX, CSV</td>
  </tr>
  <tr>
    <td>Demo Data for Open Data in 1 Day - Spending Over £500</td>
    <td>Creative Commons CCZero</td>
    <td>Data on spending over £500 generated for Open Data</td>
    <td>CSV</td>
  </tr>
  <tr>
    <td>UK Cat Burglaries</td>
    <td>UK Open Government Licence (OGL)</td>
    <td>A record of cat burgalries, listing the cat names,</td>
    <td>JPEG, CSV</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
    <td>...</td>
    <td>...</td>
  </tr>
</table>


### Exporting Dataset Extras

Let's add a column with the values of the "Next Update" extra from each
dataset. Dataset publishers have been inconsistent with naming this column,
it's sometimes "Next Update" and sometimes "next update", "Next update day",
"Next Update Time" etc. We'll use a regular expression that matches all of
these possible names and combine them into a single "Next Update" column:

```bash
ckanapi-exporter --url 'https://demo.ckan.org' \
    --column "Title" --pattern '^title$' \
    --column "Rights" --pattern '^license_title$' \
    --column "Description" --pattern '^notes$' --max-length 50 \
    --column Formats --pattern '^resources$' '^format$' --deduplicate \
    --column "Next Update" --pattern '^extras$' '^next update.*' --unique \
    > output.csv
```

The two-part pattern `'^extras$' '^next update.*'` means to look in the
"extras" field of each dataset for extras whose name matches
`^next update.*`. We're expecting each dataset to have only one matching
extra so we add the `--unique` argument which will crash if a dataset has more
than one extra matching the pattern.

By default patterns are matched case-insensitively and whitespace is stripped
from field names before matching. To match case-sensitively and without
stripping whitespace add `--case-sensitive --strip false` to the column.

We can also find multiple extras and combine them into a single column.
For example, let's say our datasets have a "contributor" extra
(sometimes spelled "contributor", sometimes "Contributor"). Some datasets have
multiple extras named "Contributor 1", "Contributor 2" etc. We can find all of
these contributor extras and combine them into a single quoted, comma-separated
list with a pattern like this:

    --column Contributors --pattern '^extras$' '^contributor.*'


### Using a columns.json File

You can specify your columns in a `columns.json` file instead of on the command
line. Here's an example of the format:

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
ckanapi-exporter --url 'https://demo.ckan.org' --columns columns.json > output.csv
```

For a working example `columns.json` file that you can use against demo.ckan.org,
see [test_columns.json](ckanapi_exporter/test_columns.json).

ckanapi-exporter is a thin wrapper around
[losser](https://github.com/ckan/losser), hooking it up to the CKAN API.
For more documentation of the filtering and transforming options run
`ckanapi-exporter --help` or read losser's docs.


Using as a Python Library
-------------------------

You can also import ckanapi-exporter in Python and use it from your CKAN API
client or plugin:

```python
import ckanapi_exporter.exporter as exporter
csv_string = exporter.export('https://demo.ckan.org', 'columns.json')
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
