import unittest
import settings

import requests_mock

from pycanvas import Canvas
from pycanvas.quiz import Quiz
from tests.util import register_uris


@requests_mock.Mocker()
class TestQuiz(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'course': ['get_by_id'], 'quiz': ['get_by_id']}, m)

            self.course = self.canvas.get_course(1)
            self.quiz = self.course.get_quiz(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.quiz)
        assert isinstance(string, str)

    # edit()
    def test_edit(self, m):
        register_uris({'quiz': ['edit']}, m)

        title = 'New Title'
        edited_quiz = self.quiz.edit(quiz={'title': title})

        assert isinstance(edited_quiz, Quiz)
        assert hasattr(edited_quiz, 'title')
        assert edited_quiz.title == title
        assert hasattr(edited_quiz, 'course_id')
        assert edited_quiz.course_id == self.course.id

    # delete()
    def test_delete(self, m):
        register_uris({'quiz': ['delete']}, m)

        title = "Great Title"
        deleted_quiz = self.quiz.delete(quiz={'title': title})

        assert isinstance(deleted_quiz, Quiz)
        assert hasattr(deleted_quiz, 'title')
        assert deleted_quiz.title == title
        assert hasattr(deleted_quiz, 'course_id')
        assert deleted_quiz.course_id == self.course.id
