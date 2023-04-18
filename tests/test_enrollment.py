import unittest

import requests_mock

from canvasapi.canvas import Canvas
from canvasapi.enrollment import Enrollment
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestEnrollment(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"account": ["get_by_id"], "enrollment": ["get_by_id"]}
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.enrollment = self.account.get_enrollment(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.enrollment)
        self.assertIsInstance(string, str)

    # deactivate()
    def test_deactivate(self, m):
        register_uris({"enrollment": ["deactivate"]}, m)

        target_enrollment = self.enrollment.deactivate("conclude")

        self.assertIsInstance(target_enrollment, Enrollment)

    def test_deactivate_invalid_task(self, m):
        with self.assertRaises(ValueError):
            self.enrollment.deactivate("finish")

    # reactivate()
    def test_reactivate(self, m):
        register_uris({"enrollment": ["reactivate"]}, m)

        target_enrollment = self.enrollment.reactivate()

        self.assertIsInstance(target_enrollment, Enrollment)

    # accept()
    def test_accept(self, m):
        register_uris({"enrollment": ["accept"]}, m)

        enrollment_accepted = self.enrollment.accept()

        self.assertIsInstance(enrollment_accepted, bool)
        self.assertTrue(enrollment_accepted)

    # reject()
    def test_reject(self, m):
        register_uris({"enrollment": ["reject"]}, m)

        enrollment_rejected = self.enrollment.reject()

        self.assertIsInstance(enrollment_rejected, bool)
        self.assertTrue(enrollment_rejected)
