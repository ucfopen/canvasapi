import unittest
import uuid
import os

import requests_mock

from pycanvas.canvas import Canvas
from pycanvas.upload import Uploader
import settings
from util import register_uris


class TestUploader(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        requires = {
            'uploader': [
                'upload_response', 'upload_response_upload_url',
                'upload_response_no_upload_url', 'upload_response_no_upload_params',
                'upload_response_fail', 'upload_fail'
            ]
        }

        adapter = requests_mock.Adapter()
        register_uris(settings.BASE_URL, requires, adapter)

        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        self.requester = self.canvas._Canvas__requester

    def setUp(self):
        self.filename = 'testfile_%s' % uuid.uuid4().hex
        self.file = open(self.filename, 'w+')

    def tearDown(self):
        # http://stackoverflow.com/a/10840586
        # Not as stupid as it looks.
        try:
            os.remove(self.filename)
        except OSError:
            pass

    # start()
    def test_start(self):
        uploader = Uploader(self.requester, 'upload_response', self.file)
        result = uploader.start()

        assert result[0] is True
        assert isinstance(result[1], dict)
        assert 'url' in result[1]

    # start()
    def test_start_path(self):
        uploader = Uploader(self.requester, 'upload_response', self.filename)
        result = uploader.start()

        assert result[0] is True
        assert isinstance(result[1], dict)
        assert 'url' in result[1]

    # start()
    def test_start_file_does_not_exist(self):
        with self.assertRaises(IOError):
            Uploader(self.requester, 'upload_response', 'test_file_not_real.xyz')

    # upload()
    def test_upload_no_upload_url(self):
        with self.assertRaises(Exception):
            Uploader(self.requester, 'upload_response_no_upload_url', self.filename).start()

    # upload()
    def test_upload_no_upload_params(self):
        with self.assertRaises(Exception):
            Uploader(self.requester, 'upload_response_no_upload_params', self.filename).start()

    # upload()
    def test_upload_fail(self):
        uploader = Uploader(self.requester, 'upload_response_fail', self.file)
        result = uploader.start()

        assert result[0] is False
        assert isinstance(result[1], dict)
        assert 'url' not in result[1]
