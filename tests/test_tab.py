import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.tab import Tab
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestTab(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": ["get_by_id", "list_tabs"],
                    "group": ["get_by_id", "list_tabs"],
                },
                m,
            )

            self.course = self.canvas.get_course(1)

            tabs = self.course.get_tabs()
            self.tab = tabs[1]

            self.group = self.canvas.get_group(1)
            group_tabs = self.group.get_tabs()
            self.tab_group = group_tabs[1]

    # __str__()
    def test__str__(self, m):
        string = str(self.tab)
        self.assertIsInstance(string, str)

    # update()
    def test_update_course(self, m):
        register_uris({"course": ["update_tab"]}, m)

        new_position = 3
        self.tab.update(position=new_position)

        self.assertIsInstance(self.tab, Tab)
        self.assertEqual(self.tab.position, 3)

    def test_update_group(self, m):
        with self.assertRaises(ValueError):
            self.tab_group.update(position=1)
