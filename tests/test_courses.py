import unittest
import settings

from util import register_uris
from pycanvas.course import Course


class TestCourses(unittest.TestCase):
    """
    Tests core Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {

        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    def test_create_quiz(self):
        pass

    def test_get_quiz(self):
        pass

    def test_list_quizzes(self):
        pass
