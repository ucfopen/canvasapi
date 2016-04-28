import unittest
import settings


import requests_mock
from pycanvas import Canvas
from pycanvas.quiz import Quiz
from util import register_uris


class TestQuizzes(unittest.TestCase):
    """
    Tests Quiz functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id'],
            'generic': ['not_found'],
            'quiz': ['edit', 'get_by_id'],
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.quiz = self.course.get_quiz(1)

    def test_edit_quiz(self):
        title = 'New Title'
        edited_quiz = self.quiz.edit_quiz(self.course.id, quiz={'title': title})

        assert isinstance(edited_quiz, Quiz)
        assert hasattr(edited_quiz, 'title')
        assert edited_quiz.title == title


    def test_delete_quiz(self):
        pass
