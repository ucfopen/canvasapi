import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCourseEvent(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "account": ["get_by_id", "query_audit_by_account"],
                "course": ["query_audit_by_course"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)

            # isolate one of the CourseEvent objects
            self.query_audit_by_account = self.account.query_audit_by_account()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.query_audit_by_account)
        self.assertIsInstance(string, str)
