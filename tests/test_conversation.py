import unittest

import requests_mock

import settings
from pycanvas import Canvas
from util import register_uris


class TestConversation(unittest.TestCase):
    """
    Tests PageView functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'conversation': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, {'generic': ['not_found']}, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.conversation = self.canvas.get_conversation(1)

    # __str__()
    def test__str__(self):
        string = str(self.conversation)
        assert isinstance(string, str)
