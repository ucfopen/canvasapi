import requests

from canvasapi.exceptions import (
    BadRequest, CanvasException, InvalidAccessToken, ResourceDoesNotExist,
    Unauthorized
)


class Requester(object):
    """
    Responsible for handling HTTP requests.
    """

    def __init__(self, base_url, access_token):
        """
        :param base_url: The base URL of the Canvas instance's API.
        :type base_url: str
        :param access_token: The API key to authenticate requests with.
        :type access_token: str
        """
        self.base_url = base_url
        self.access_token = access_token
        self._session = requests.Session()

    def request(self, method, endpoint=None, headers=None, use_auth=True, _url=None, **kwargs):
        """
        Make a request to the Canvas API and return the response.

        :param method: The HTTP method for the request.
        :type method: str
        :param endpoint: The endpoint to call.
        :type endpoint: str
        :param headers: Optional HTTP headers to be sent with the request.
        :type headers: dict
        :param use_auth: Optional flag to remove the authentication header from the request.
        :type use_auth: bool
        :param _url: Optional argument to send a request to a URL outside of the Canvas API. \
                    If this is selected and an endpoint is provided, the endpoint will be \
                    ignored and only the _url argument will be used.
        :type _url: str
        :rtype: str
        """
        full_url = _url if _url else "%s%s" % (self.base_url, endpoint)

        if not headers:
            headers = {}

        if use_auth:
            auth_header = {'Authorization': 'Bearer %s' % (self.access_token)}
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

        if response.status_code == 400:
            raise BadRequest(response.json())
        elif response.status_code == 401:
            if 'WWW-Authenticate' in response.headers:
                raise InvalidAccessToken(response.json())
            else:
                raise Unauthorized(response.json())
        elif response.status_code == 404:
            raise ResourceDoesNotExist('Not Found')
        elif response.status_code == 500:
            raise CanvasException("API encountered an error processing your request")

        return response

    def _get_request(self, url, headers, params=None):
        """
        Issue a GET request to the specified endpoint with the data provided.

        :param url: str
        :pararm headers: dict
        :param params: dict
        """
        return self._session.get(url, headers=headers, params=params)

    def _post_request(self, url, headers, data=None):
        """
        Issue a POST request to the specified endpoint with the data provided.

        :param url: str
        :pararm headers: dict
        :param params: dict
        :param data: dict
        """
        if 'file' in data:
            file = {'file': data['file']}
            del data['file']
        else:
            file = None

        return self._session.post(url, headers=headers, data=data, files=file)

    def _delete_request(self, url, headers, data=None):
        """
        Issue a DELETE request to the specified endpoint with the data provided.

        :param url: str
        :pararm headers: dict
        :param params: dict
        :param data: dict
        """
        return self._session.delete(url, headers=headers, data=data)

    def _put_request(self, url, headers, data=None):
        """
        Issue a PUT request to the specified endpoint with the data provided.

        :param url: str
        :pararm headers: dict
        :param params: dict
        :param data: dict
        """
        return self._session.put(url, headers=headers, data=data)
