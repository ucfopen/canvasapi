import unittest
import settings

from util import register_uris
from pycanvas.course import Course
from pycanvas.quiz import Quiz

class TestCourses(unittest.TestCase):
    """
    Tests core Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['create']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    def test_create_quiz(self):
        title = 'New Title'
        new_quiz = self.course.create_quiz(self.course.id, quiz={'title': title})

        assert isinstance(new_quiz, Course)
        assert hasattr(new_quiz, 'title')
        assert new_quiz.title == title

    def test_get_quiz(self):
        pass

    def test_list_quizzes(self):
        pass
