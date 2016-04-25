import json

import requests_mock


def register_uris(base_url, requirements, adapter):
    """
    Given a list of required fixtures and an adapter object, register each fixture
    as a uri with the adapter.

    :param base_url: str
    :param requirements: dict
    :param adapter: requests_mock.Adapter
    """
    for fixture, objects in requirements.iteritems():

        try:
            data = json.loads(open('tests/fixtures/%s.json' % (fixture)).read())
        except:
            raise ValueError('Fixture %s.json contains invalid JSON.' % (fixture))

        for obj in objects:
            obj = data.get(obj)

            method = requests_mock.ANY if obj['method'] == 'ANY' else obj['method']
            url = requests_mock.ANY if obj['endpoint'] == 'ANY' else base_url + obj['endpoint']

            try:
                adapter.register_uri(
                    method,
                    url,
                    json=obj.get('data'),
                    status_code=obj.get('status_code'),
                    headers=obj.get('headers', {})
                )
            except Exception as e:
                print e
