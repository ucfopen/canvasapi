import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.enrollment import Enrollment
from pycanvas import Canvas


class TestAccount(unittest.TestCase):
    """
    Tests core Account functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': ['create', 'enroll_by_id', 'get_by_id'],
            'generic': ['not_found']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.account = self.canvas.get_account(1)

    def test_enroll_by_id(self):
        target_enrollment = self.account.enroll_by_id(1, 1)

        assert isinstance(target_enrollment, Enrollment)
