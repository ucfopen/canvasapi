import json

import requests_mock

from tests import settings


def register_uris(requirements, requests_mocker):
    """
    Given a list of required fixtures and an requests_mocker object,
    register each fixture as a uri with the mocker.

    :param base_url: str
    :param requirements: dict
    :param requests_mocker: requests_mock.mocker.Mocker
    """
    for fixture, objects in requirements.iteritems():

        try:
            data = json.loads(open('tests/fixtures/{}.json'.format(fixture)).read())
        except:
            raise ValueError('Fixture {}.json contains invalid JSON.'.format(fixture))

        if not isinstance(objects, list):
            raise TypeError('{} is not a list.'.format(objects))

        for obj_name in objects:
            obj = data.get(obj_name)

            if obj is None:
                raise ValueError('{} does not exist in {}.json'.format(
                    obj_name.__repr__(),
                    fixture
                ))

            method = requests_mock.ANY if obj['method'] == 'ANY' else obj['method']
            url = requests_mock.ANY if obj['endpoint'] == 'ANY' else settings.BASE_URL + obj['endpoint']

            try:
                requests_mocker.register_uri(
                    method,
                    url,
                    json=obj.get('data'),
                    status_code=obj.get('status_code', 200),
                    headers=obj.get('headers', {})
                )
            except Exception as e:
                print e
