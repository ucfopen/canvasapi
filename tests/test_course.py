import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.course import Course
from pycanvas.quiz import Quiz
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas import Canvas

INVALID_ID = 9001


class TestCourse(unittest.TestCase):
    """
    Tests core Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['create', 'get_by_id', 'get_quiz', 'list_quizzes', 'list_quizzes2'],
            'generic': ['not_found'],
            'quiz': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.quiz = self.course.get_quiz(1)

    #create_quiz()
    def test_create_quiz(self):
        title = 'Newer Title'
        new_quiz = self.course.create_quiz(self.course.id, quiz={'title': title})

        assert isinstance(new_quiz, Quiz)
        assert hasattr(new_quiz, 'title')
        assert new_quiz.title == title

    #get_quiz()
    def test_get_quiz(self):
        target_quiz = self.course.get_quiz(1)

        assert isinstance(target_quiz, Quiz)

    def test_get_quiz_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.course.get_quiz(INVALID_ID)

    #list_quizzes()
    def test_list_quizzes(self):
        quizzes = self.course.list_quizzes()
        quiz_list = [quiz for quiz in quizzes]

        assert len(quiz_list) == 4
        assert isinstance(quiz_list[0], Quiz)

    #list_enrollments()
    def test_list_enrollments(self):
        enrollments = self.user.list_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], enrollment)
