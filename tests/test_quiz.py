import unittest
import settings


import requests_mock
from pycanvas import Canvas
from pycanvas.quiz import Quiz
from util import register_uris


class TestQuiz(unittest.TestCase):
    """
    Tests Quiz functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id'],
            'generic': ['not_found'],
            'quiz': ['delete', 'edit', 'get_by_id'],
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.quiz = self.course.get_quiz(1)

    def test_edit(self):
        title = 'New Title'
        edited_quiz = self.quiz.edit(self.course.id, quiz={'title': title})

        assert isinstance(edited_quiz, Quiz)
        assert hasattr(edited_quiz, 'title')
        assert edited_quiz.title == title

    def test_delete(self):
        title = "Great Title"
        deleted_quiz = self.quiz.delete(self.course.id, quiz={'title': title})

        assert isinstance(deleted_quiz, Quiz)
        assert hasattr(deleted_quiz, 'title')
        assert deleted_quiz.title == title
