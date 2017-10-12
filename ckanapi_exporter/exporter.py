import sys
import argparse
import ast

import ckanapi
import losser.losser
import losser.cli
import math


VERSION = '0.1.0'

def get_datasets_from_ckan(url, apikey, params=None):
    """Gets the datasets from CKAN API and passed in parameters

    Parameters
    ----------
    url: str
        The url of the CKAN instance.
    apikey: str, optional
        The CKAN api key to access private datasets.
    params: str, optional
        A literal string representing a dictionary of parameters to pass to CKAN.

    Returns
    -------
    array:
        All the datasets requested in an array.

    """
    user_agent = ('ckanapi-exporter/{version} '
                  '(+https://github.com/ckan/ckanapi-exporter)').format(
                          version=VERSION)
    api = ckanapi.RemoteCKAN(url, apikey=apikey, user_agent=user_agent)

    #find out if there are more than the hard coded 1000 datasets and how many pages
    arguments = {'rows': 1000, 'start': 0}
    if params is not None:
        params_dict = ast.literal_eval(params)
        arguments.update(params_dict)

    response = api.call_action('package_search', arguments)
    num_pages = int(math.ceil(response['count']/1000.0))

    #loop over to collect up all datasets from the CKAN instance
    datasets = []
    for page in range(0, num_pages):
        arguments['start'] = page * 1000
        paged_response = api.call_action('package_search', arguments)
        #merge these results into one dictionary
        datasets.extend(paged_response["results"])

    #return the large array to go about it's business
    return datasets


def extras_to_dicts(datasets):
    for dataset in datasets:
        extras_dict = {}
        for extra in dataset.get("extras", []):
            key = extra["key"]
            value = extra["value"]
            assert key not in extras_dict
            extras_dict[key] = value
        dataset["extras"] = extras_dict


def export(url, columns, apikey=None, params=None, pretty=False):
    datasets = get_datasets_from_ckan(url, apikey, params)
    extras_to_dicts(datasets)
    csv_string = losser.losser.table(datasets, columns, csv=True,
                                     pretty=pretty)
    return csv_string


def main(args=None):
    parent_parser = losser.cli.make_parser(
        add_help=False, exclude_args=["-i"])
    parser = argparse.ArgumentParser(
        description="Export datasets from a CKAN site to JSON or CSV.",
        parents=[parent_parser],
    )
    parser.add_argument(
        "--url",
        help="the root URL of the CKAN site to export datasets from, "
             "for example: 'http://demo.ckan.org'",
        required=True,
    )
    parser.add_argument(
        "--apikey",
        help="the API key to use when fetching datasets from the CKAN site, "
             "use this option if you want to export private datasets as well "
             "as public ones",
        )
    parser.add_argument(
        "--params",
        help="a dictionary of CKAN API parameters passed into the export query",
        )
    try:
        parsed_args = losser.cli.parse(parser=parser)
    except losser.cli.CommandLineExit as err:
        sys.exit(err.code)
    except losser.cli.CommandLineError as err:
        if err.message:
            parser.error(err.message)
    csv_string = export(
        parsed_args.url, parsed_args.columns, parsed_args.apikey,
        parsed_args.params, pretty=parsed_args.pretty)
    sys.stdout.write(csv_string)


if __name__ == "__main__":
    main()
