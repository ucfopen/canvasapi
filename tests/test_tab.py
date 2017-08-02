from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestTab(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'course': ['get_by_id', 'list_tabs']
            }, m)

            self.course = self.canvas.get_course(1)

            tabs = self.course.list_tabs()
            tab_list = [tab for tab in tabs]

            self.tab = tab_list[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.tab)
        self.assertIsInstance(string, str)
