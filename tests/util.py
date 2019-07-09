from __future__ import absolute_import, division, print_function, unicode_literals
import json
import os

import requests_mock

from canvasapi.util import get_institution_url
from tests import settings


def register_uris(requirements, requests_mocker):
    """
    Given a list of required fixtures and an requests_mocker object,
    register each fixture as a uri with the mocker.

    :param base_url: str
    :param requirements: dict
    :param requests_mocker: requests_mock.mocker.Mocker
    """
    for fixture, objects in requirements.items():
        try:
            with open("tests/fixtures/{}.json".format(fixture)) as file:
                data = json.loads(file.read())
        except IOError:
            raise ValueError("Fixture {}.json contains invalid JSON.".format(fixture))

        if not isinstance(objects, list):
            raise TypeError("{} is not a list.".format(objects))

        for obj_name in objects:
            obj = data.get(obj_name)

            if obj is None:
                raise ValueError(
                    "{} does not exist in {}.json".format(obj_name.__repr__(), fixture)
                )

            method = requests_mock.ANY if obj["method"] == "ANY" else obj["method"]
            if obj["endpoint"] == "ANY":
                url = requests_mock.ANY
            else:
                url = (
                    get_institution_url(settings.BASE_URL)
                    + "/api/v1/"
                    + obj["endpoint"]
                )

            try:
                requests_mocker.register_uri(
                    method,
                    url,
                    json=obj.get("data"),
                    status_code=obj.get("status_code", 200),
                    headers=obj.get("headers", {}),
                )
            except Exception as e:
                print(e)


def cleanup_file(filename):
    """
    Remove a test file from the system. If the file doesn't exist, ignore.

    `Not as stupid as it looks. <http://stackoverflow.com/a/10840586>_`
    """
    try:
        os.remove(filename)
    except OSError:
        pass
