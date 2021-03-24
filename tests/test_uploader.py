import unittest
import uuid
from pathlib import Path

import requests_mock

from canvasapi.canvas import Canvas
from canvasapi.upload import Uploader
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestUploader(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        self.requester = self.canvas._Canvas__requester

        self.filename = "testfile_uploader_{}".format(uuid.uuid4().hex)
        self.file = open(self.filename, "w+")

    def tearDown(self):
        self.file.close()
        cleanup_file(self.filename)

    # start()
    def test_start(self, m):
        requires = {"uploader": ["upload_response", "upload_response_upload_url"]}
        register_uris(requires, m)

        uploader = Uploader(self.requester, "upload_response", self.file)
        result = uploader.start()

        self.assertTrue(result[0])
        self.assertIsInstance(result[1], dict)
        self.assertIn("url", result[1])

    def test_start_pathlib(self, m):
        requires = {"uploader": ["upload_response", "upload_response_upload_url"]}
        register_uris(requires, m)

        uploader = Uploader(self.requester, "upload_response", Path(self.filename))
        result = uploader.start()

        self.assertTrue(result[0])
        self.assertIsInstance(result[1], dict)
        self.assertIn("url", result[1])

    def test_start_path(self, m):
        requires = {"uploader": ["upload_response", "upload_response_upload_url"]}
        register_uris(requires, m)

        uploader = Uploader(self.requester, "upload_response", self.filename)
        result = uploader.start()

        self.assertTrue(result[0])
        self.assertIsInstance(result[1], dict)
        self.assertIn("url", result[1])

    def test_start_file_does_not_exist(self, m):
        with self.assertRaises(IOError):
            Uploader(self.requester, "upload_response", "test_file_not_real.xyz")

    # upload()
    def test_upload_no_upload_url(self, m):
        register_uris({"uploader": ["upload_response_no_upload_url"]}, m)

        with self.assertRaises(ValueError):
            Uploader(
                self.requester, "upload_response_no_upload_url", self.filename
            ).start()

    def test_upload_no_upload_params(self, m):
        register_uris({"uploader": ["upload_response_no_upload_params"]}, m)

        with self.assertRaises(ValueError):
            Uploader(
                self.requester, "upload_response_no_upload_params", self.filename
            ).start()

    def test_upload_fail(self, m):
        requires = {"uploader": ["upload_fail", "upload_response_fail"]}
        register_uris(requires, m)

        uploader = Uploader(self.requester, "upload_response_fail", self.file)
        result = uploader.start()

        self.assertFalse(result[0])
        self.assertIsInstance(result[1], dict)
        self.assertNotIn("url", result[1])
