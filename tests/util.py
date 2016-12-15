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
            data = json.loads(open('tests/fixtures/%s.json' % (fixture)).read())
        except:
            raise ValueError('Fixture %s.json contains invalid JSON.' % (fixture))

        for obj in objects:
            obj = data.get(obj)

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
