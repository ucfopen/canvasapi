import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.course import Course
from pycanvas.quiz import Quiz
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas import Canvas


class TestAccount(unittest.TestCase):
    """
    Tests core Account functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {

        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)
