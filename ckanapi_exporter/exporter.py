import sys
import argparse

import ckanapi
import losser.losser as losser


VERSION = '0.0.1'


# TODO: Make this more generic, accept search params as param.
def get_datasets_from_ckan(api):
    response = api.action.package_search(rows=1000000)
    return response["results"]


def extras_to_dicts(datasets):
    for dataset in datasets:
        extras_dict = {}
        for extra in dataset.get("extras"):
            key = extra["key"]
            value = extra["value"]
            assert key not in extras_dict
            extras_dict[key] = value
        dataset["extras"] = extras_dict


def export(url, columns, apikey=None):
    user_agent = ('ckanapi-exporter/{version} '
                  '(+https://github.com/ckan/ckanapi-exporter)').format(
                          version=VERSION)
    api = ckanapi.RemoteCKAN(url, apikey=apikey, user_agent=user_agent)
    datasets = get_datasets_from_ckan(api)
    extras_to_dicts(datasets)
    csv_string = losser.table(datasets, columns, csv=True)
    return csv_string


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Export datasets from a CKAN site to JSON or CSV.",
    )
    parser.add_argument(
        "--url",
        help="the root URL of the CKAN site to export datasets from, "
             "for example: 'http://demo.ckan.org'",
        required=True,
    )
    parser.add_argument(
        "--columns",
        help="the path to the JSON file specifying the columns to output, "
             "for example: columns.json",
        required=True,
    )
    parser.add_argument(
        "--apikey",
        help="the API key to use when fetching datasets from the CKAN site, "
             "use this option if you want to export private datasets as well "
             "as public ones",
        )
    parsed_args = parser.parse_args(args)

    csv_string = export(parsed_args.url, parsed_args.columns,
                        parsed_args.apikey)
    sys.stdout.write(csv_string)


if __name__ == "__main__":
    main()
