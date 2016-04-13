import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.user import User
from pycanvas.exceptions import ResourceDoesNotExist
import settings
from util import register_uris


class TestCanvas(unittest.TestCase):
    """
    Tests core Canvas functionality.
    """
    def setUp(self):
        requires = {
            'generic': ['not_found'],
            'user': ['get_by_id', 'get_by_id_type'],
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    def test_get_user(self):
        user = self.canvas.get_user(1)

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    def test_get_user_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_user(2)

    def test_get_user_by_id_type(self):
        user = self.canvas.get_user('jdoe', 'sis_user_id')

        assert isinstance(user, User)
        assert hasattr(user, 'name')
