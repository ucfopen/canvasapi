import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.course import Course
from pycanvas.module import Module
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
            'course': [
                'create', 'get_by_id', 'get_quiz', 'list_quizzes', 'list_quizzes2',
                'list_modules', 'list_modules2', 'get_module_by_id', 'create_module'
            ],
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

    def test_list_modules(self):
        modules = self.course.list_modules()
        module_list = [module for module in modules]

        assert len(module_list) == 4
        assert isinstance(module_list[0], Module)

    def test_get_module(self):
        target_module = self.course.get_module(1)

        assert isinstance(target_module, Module)

    def test_create_module(self):
        name = 'Name'
        new_module = self.course.create_module(self.course.id, module={'name': name})

        assert isinstance(new_module, Module)
        assert hasattr(new_module, 'name')
