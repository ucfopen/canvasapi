import unittest

import requests_mock

import settings
from pycanvas import Canvas
from pycanvas.exceptions import BadRequest, CanvasException, PermissionError, ResourceDoesNotExist
from util import register_uris


class TestRequester(unittest.TestCase):
    """
    Tests Requester functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'requests': [
                '400', '401', '404', '500',
                'delete', 'get', 'post', 'put'
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        self.requester = self.canvas._Canvas__requester
        register_uris(settings.BASE_URL, requires, adapter)

    # request()
    def test_request_get(self):
        response = self.requester.request('GET', 'fake_get_request')
        assert response.status_code == 200

    def test_request_post(self):
        response = self.requester.request('POST', 'fake_post_request')
        assert response.status_code == 200

    def test_request_delete(self):
        response = self.requester.request('DELETE', 'fake_delete_request')
        assert response.status_code == 200

    def test_request_put(self):
        response = self.requester.request('PUT', 'fake_put_request')
        assert response.status_code == 200

    def test_request_400(self):
        with self.assertRaises(BadRequest):
            self.requester.request('GET', '400')

    def test_request_401(self):
        with self.assertRaises(PermissionError):
            self.requester.request('GET', '401')

    def test_request_404(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.requester.request('GET', '404')

    def test_request_500(self):
        with self.assertRaises(CanvasException):
            self.requester.request('GET', '500')
