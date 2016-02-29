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

    def request(self, method, endpoint, headers={}, **kwargs):
        """
        Makes a request to the Canvas API.

        :param method: string
        :param endpoint: string
        :param headers: dict
        """
        full_url = self.base_url + endpoint

        auth_header = {'Authorization': 'Bearer ' + self.access_token}
        headers.update(auth_header)

        if method == 'GET':
            req_method = self._get_request
        elif method == 'POST':
            req_method = self._post_request
        elif method == 'DELETE':
            req_method = self._delete_request
        elif method == 'PUT':
            req_method = self._put_request

        response = req_method(full_url, headers, kwargs)
        return response

    def _get_request(self, url, headers, params={}):
        """
        Issue a GET request to the specified endpoint with the data provided.

        :param url: string
        :pararm headers: dict
        :param params: dict
        """
        return requests.get(url, headers=headers, params=params)

    def _post_request(self, url, headers, data={}):
        """
        Issue a POST request to the specified endpoint with the data provided.

        :param url: string
        :pararm headers: dict
        :param params: dict
        :param data: dict
        """
        return requests.post(url, headers=headers, data=data)

    def _delete_request(self, url, headers, data={}):
        """
        Issue a DELETE request to the specified endpoint with the data provided.

        :param url: string
        :pararm headers: dict
        :param params: dict
        :param data: dict
        """
        return requests.delete(url, headers=headers, data=data)

    def _put_request(self, url, headers, data={}):
        """
        Issue a PUT request to the specified endpoint with the data provided.

        :param url: string
        :pararm headers: dict
        :param params: dict
        :param data: dict
        """
        return requests.put(url, headers=headers, data=data)
