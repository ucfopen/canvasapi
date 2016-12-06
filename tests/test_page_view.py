import unittest

import requests_mock

from pycanvas import Canvas
from tests import settings
from util import register_uris


class TestPageView(unittest.TestCase):
    """
    Tests PageView functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found'],
            'user': ['get_by_id', 'page_views', 'page_views_p2']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.user = self.canvas.get_user(1)
        pageviews = self.user.get_page_views()
        self.pageview = pageviews[0]

    # __str__()
    def test__str__(self):
        string = str(self.pageview)
        assert isinstance(string, str)
