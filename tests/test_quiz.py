import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.quiz import Quiz
from tests import settings
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
        self.assertIsInstance(string, str)

    # edit()
    def test_edit(self, m):
        register_uris({'quiz': ['edit']}, m)

        title = 'New Title'
        edited_quiz = self.quiz.edit(quiz={'title': title})

        self.assertIsInstance(edited_quiz, Quiz)
        self.assertTrue(hasattr(edited_quiz, 'title'))
        self.assertEqual(edited_quiz.title, title)
        self.assertTrue(hasattr(edited_quiz, 'course_id'))
        self.assertEqual(edited_quiz.course_id, self.course.id)

    # delete()
    def test_delete(self, m):
        register_uris({'quiz': ['delete']}, m)

        title = "Great Title"
        deleted_quiz = self.quiz.delete(quiz={'title': title})

        self.assertIsInstance(deleted_quiz, Quiz)
        self.assertTrue(hasattr(deleted_quiz, 'title'))
        self.assertEqual(deleted_quiz.title, title)
        self.assertTrue(hasattr(deleted_quiz, 'course_id'))
        self.assertEqual(deleted_quiz.course_id, self.course.id)
