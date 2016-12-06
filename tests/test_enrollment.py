import unittest

import requests_mock

from pycanvas.canvas import Canvas
from pycanvas.enrollment import Enrollment
from tests import settings
from tests.util import register_uris


class TestEnrollment(unittest.TestCase):
    """
    Test Enrollment methods
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': ['get_by_id'],
            'generic': ['not_found'],
            'enrollment': ['deactivate', 'get_by_id', 'reactivate']
        }
        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.account = self.canvas.get_account(1)
        self.enrollment = self.account.get_enrollment(1)

    # __str__()
    def test__str__(self):
        string = str(self.enrollment)
        self.assertIsInstance(string, str)

    # deactivate()
    def test_deactivate(self):
        target_enrollment = self.enrollment.deactivate('conclude')

        self.assertIsInstance(target_enrollment, Enrollment)

    def test_deactivate_invalid_task(self):
        with self.assertRaises(ValueError):
            self.enrollment.deactivate('finish')

    # reactivate()
    def test_reactivate(self):
        target_enrollment = self.enrollment.reactivate()

        self.assertIsInstance(target_enrollment, Enrollment)
