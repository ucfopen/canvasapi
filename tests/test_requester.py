import unittest
from datetime import datetime
from urllib.parse import quote

import requests
import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import (
    BadRequest,
    CanvasException,
    Conflict,
    Forbidden,
    InvalidAccessToken,
    RateLimitExceeded,
    ResourceDoesNotExist,
    Unauthorized,
    UnprocessableEntity,
)
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestRequester(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        self.requester = self.canvas._Canvas__requester

    # request()
    def test_request_get(self, m):
        register_uris({"requests": ["get"]}, m)

        response = self.requester.request("GET", "fake_get_request")
        self.assertEqual(response.status_code, 200)

    def test_request_get_binary(self, m):
        m.register_uri(
            "GET",
            settings.BASE_URL_WITH_VERSION + "get_binary_data",
            content=b"\xff\xff\xff",
            status_code=200,
            headers={},
        )

        response = self.requester.request("GET", "get_binary_data")
        self.assertEqual(response.content, b"\xff\xff\xff")

    def test_request_get_datetime(self, m):
        date = datetime.today()

        def custom_matcher(request):
            match_query = "date={}".format(quote(date.isoformat()).lower())
            if request.query == match_query:
                resp = requests.Response()
                resp.status_code = 200
                return resp

        m.add_matcher(custom_matcher)

        response = self.requester.request("GET", "test", date=date)
        self.assertEqual(response.status_code, 200)

    def test_request_post(self, m):
        register_uris({"requests": ["post"]}, m)

        response = self.requester.request("POST", "fake_post_request")
        self.assertEqual(response.status_code, 200)

    def test_request_post_datetime(self, m):
        date = datetime.today()

        def custom_matcher(request):
            match_text = "date={}".format(quote(date.isoformat()))
            if request.text == match_text:
                resp = requests.Response()
                resp.status_code = 200
                return resp

        m.add_matcher(custom_matcher)

        response = self.requester.request("POST", "test", date=date)
        self.assertEqual(response.status_code, 200)

    def test_request_delete(self, m):
        register_uris({"requests": ["delete"]}, m)

        response = self.requester.request("DELETE", "fake_delete_request")
        self.assertEqual(response.status_code, 200)

    def test_request_patch(self, m):
        register_uris({"requests": ["patch"]}, m)

        response = self.requester.request("PATCH", "fake_patch_request")
        self.assertEqual(response.status_code, 200)

    def test_request_put(self, m):
        register_uris({"requests": ["put"]}, m)

        response = self.requester.request("PUT", "fake_put_request")
        self.assertEqual(response.status_code, 200)

    def test_request_cache(self, m):
        register_uris({"requests": ["get"]}, m)

        response = self.requester.request("GET", "fake_get_request")
        self.assertEqual(response, self.requester._cache[0])

    def test_request_cache_clear_after_5(self, m):
        register_uris({"requests": ["get", "post"]}, m)

        for i in range(5):
            self.requester.request("GET", "fake_get_request")

        response = self.requester.request("POST", "fake_post_request")

        self.assertLessEqual(len(self.requester._cache), 5)
        self.assertEqual(response, self.requester._cache[0])

    def test_request_lowercase_boolean(self, m):
        def custom_matcher(request):
            if "test=true" in request.text and "test2=false" in request.text:
                resp = requests.Response()
                resp.status_code = 200
                return resp

        m.add_matcher(custom_matcher)

        response = self.requester.request("POST", "test", test=True, test2=False)
        self.assertEqual(response.status_code, 200)

    def test_request_400(self, m):
        register_uris({"requests": ["400"]}, m)

        with self.assertRaises(BadRequest):
            self.requester.request("GET", "400")

    def test_request_401_InvalidAccessToken(self, m):
        register_uris({"requests": ["401_invalid_access_token"]}, m)

        with self.assertRaises(InvalidAccessToken):
            self.requester.request("GET", "401_invalid_access_token")

    def test_request_401_Unauthorized(self, m):
        register_uris({"requests": ["401_unauthorized"]}, m)

        with self.assertRaises(Unauthorized):
            self.requester.request("GET", "401_unauthorized")

    def test_request_403(self, m):
        register_uris({"requests": ["403"]}, m)

        with self.assertRaises(Forbidden):
            self.requester.request("GET", "403")

    def test_request_403_RateLimitExeeded(self, m):
        register_uris({"requests": ["403_rate_limit"]}, m)

        with self.assertRaises(RateLimitExceeded) as exc:
            self.requester.request("GET", "403_rate_limit")

        self.assertEqual(
            exc.exception.message,
            "Rate Limit Exceeded. X-Rate-Limit-Remaining: 3.14159265359",
        )

    def test_request_403_RateLimitExeeded_no_remaining_header(self, m):
        register_uris({"requests": ["403_rate_limit_no_remaining_header"]}, m)

        with self.assertRaises(RateLimitExceeded) as exc:
            self.requester.request("GET", "403_rate_limit_no_remaining_header")

        self.assertEqual(
            exc.exception.message,
            "Rate Limit Exceeded. X-Rate-Limit-Remaining: Unknown",
        )

    def test_request_404(self, m):
        register_uris({"requests": ["404"]}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.requester.request("GET", "404")

    def test_request_409(self, m):
        register_uris({"requests": ["409"]}, m)

        with self.assertRaises(Conflict):
            self.requester.request("GET", "409")

    def test_request_422(self, m):
        register_uris({"requests": ["422"]}, m)

        with self.assertRaises(UnprocessableEntity):
            self.requester.request("GET", "422")

    def test_request_500(self, m):
        register_uris({"requests": ["500"]}, m)

        with self.assertRaises(CanvasException):
            self.requester.request("GET", "500")

    def test_request_generic(self, m):
        register_uris({"requests": ["502", "503", "absurd"]}, m)

        with self.assertRaises(CanvasException):
            self.requester.request("GET", "502")

        with self.assertRaises(CanvasException):
            self.requester.request("GET", "503")

        with self.assertRaises(CanvasException):
            self.requester.request("GET", "absurd")
