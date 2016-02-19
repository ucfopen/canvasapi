import requests


class Requester(object):
    """
    Responsible for handling HTTP requests.
    """

    def __init__(self, base_url, access_token):
        """
        :param base_url: string
        :param access_token: string
        """
        self.base_url = base_url
        self.access_token = access_token

        # Try to establish an initial connection to Canvas
        response = self.request('GET', 'accounts')

        if response.status_code != 200:
            raise Exception('Invalid base URL or access token.')

    def request(self, method, endpoint, **kwargs):
        """Makes a request to the Canvas API.

        :param method: string
        :param endpoint: string
        """

        if method == 'GET':
            response = self._get_request(self.base_url + endpoint, kwargs)

        if method == 'POST':
            response = self._post_request(self.base_url + endpoint, kwargs)

        return response

    def _get_request(self, url, data):
        """Issue a GET request to the specified endpoint with the data provided.

        :param url: string
        :param data: dict
        """
        return requests.get(url + '?access_token=%s' % (self.access_token))

    def _post_request(self, url, data):
        """Issue a POST request to the specified endpoint with the data provided.

        :param url: string
        :param data: dict
        """
        pass
