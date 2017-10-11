import sys
import argparse

import ckanapi
import losser.losser
import losser.cli
import math


VERSION = '0.0.6'


# TODO: Make this more generic, accept search params as param.
def get_datasets_from_ckan(url, apikey):
    user_agent = ('ckanapi-exporter/{version} '
                  '(+https://github.com/ckan/ckanapi-exporter)').format(
                          version=VERSION)
    api = ckanapi.RemoteCKAN(url, apikey=apikey, user_agent=user_agent)

    #find out if there are more than the hard coded 1000 datasets and how many pages
    response = api.action.package_search()
    num_pages = int(math.ceil(response['count']/1000.0))

    #loop over to collect up all datasets from the CKAN instance
    datasets = []
    for page in range(0, num_pages):
        offset = page * 1000
        paged_response = api.action.package_search(rows=1000,start=offset)
        #merge these results into one library
        datasets.extend(paged_response["results"])

    #return the large libaray to go about it's business
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


def export(url, columns, apikey=None, pretty=False):
    datasets = get_datasets_from_ckan(url, apikey)
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
    try:
        parsed_args = losser.cli.parse(parser=parser)
    except losser.cli.CommandLineExit as err:
        sys.exit(err.code)
    except losser.cli.CommandLineError as err:
        if err.message:
            parser.error(err.message)
    csv_string = export(
        parsed_args.url, parsed_args.columns, parsed_args.apikey,
        pretty=parsed_args.pretty)
    sys.stdout.write(csv_string)


if __name__ == "__main__":
    main()
