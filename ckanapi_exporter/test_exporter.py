import inspect
import json
import os.path

import httpretty

import ckanapi_exporter.exporter as exporter


def _absolute_path(relative_path):
    """Return an absolute path given a path relative to this Python file."""
    return os.path.join(os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe()))), relative_path)


def _mock_package_search(url, body):
    """Mock the package_search API of the given CKAN site.

    Make it return the given body dict as JSON.

    """
    if not url.endswith("/"):
        url = url + "/"
    # This is a bit brittle, we're relying on the fact that ckanapi will end
    # up posting to this URL.
    url = url + "api/action/package_search"
    body = json.dumps(body)
    httpretty.register_uri(httpretty.POST, url, body=body,
                           content_type="application/json")


@httpretty.activate
def test_export():

    # The CKAN site whose API we're going to mock.
    url = "http://demo.ckan.org"

    # The mock package_search result from CKAN.
    body = {
        "help": "blah blah blah",
        "success": True,
        "result": {
            "count": 3,
            "sort":"score desc, metadata_modified desc",
            "facets": {},
            "results": [
                {
                    "author": "Guybrush Threepwood",
                    "notes": "test notes 1",
                    "resources": [
                        {"format": "CSV"},
                        {"format": "JSON"},
                    ],
                    "extras": [
                        {"key": "Update Frequency",
                         "value": "yearly",
                        },
                    ],
                },
                {
                    "author": "Elaine Marley",
                    "notes": "test notes 2",
                    "resources": [
                        {"format": "PDF"},
                        {"format": "TXT"},
                    ],
                    "extras": [
                        {"key": "update",
                         "value": "monthly",
                        },
                    ],
                },
                {
                    "author": "Mancomb Seepgood",
                    "notes": "test notes 3",
                    "resources": [
                        {"format": "XLS"},
                        {"format": "JPEG"},
                    ],
                    "extras": [
                        {"key": "Updated",
                         "value": "weekly",
                        },
                    ],
                },
            ]
        }
    }
    _mock_package_search(url, body)

    csv_string = exporter.export(url, _absolute_path("test_columns.json"))

    assert csv_string == (
        "Data Owner,Description,Formats,Update Frequency\r\n"
        'Guybrush Threepwood,test notes 1,"CSV, JSON",yearly\r\n'
        'Elaine Marley,test notes 2,"PDF, TXT",monthly\r\n'
        'Mancomb Seepgood,test notes 3,"XLS, JPEG",weekly\r\n'
    )
