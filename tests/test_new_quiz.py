import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.new_quiz import NewQuiz
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestNewQuiz(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id"]}, m)
            register_uris(
                {"new_quiz": ["get_new_quiz"]},
                m,
                base_url=settings.BASE_URL_NEW_QUIZZES,
            )

            self.course = self.canvas.get_course(1)
            self.new_quiz = self.course.get_new_quiz(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.new_quiz)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete(self, m):
        register_uris(
            {"new_quiz": ["delete_new_quiz"]},
            m,
            base_url=settings.BASE_URL_NEW_QUIZZES,
        )

        deleted_quiz = self.new_quiz.delete()

        self.assertIsInstance(deleted_quiz, NewQuiz)
        self.assertTrue(hasattr(deleted_quiz, "title"))
        self.assertEqual(deleted_quiz.title, "New Quiz One")
        self.assertTrue(hasattr(deleted_quiz, "course_id"))
        self.assertEqual(deleted_quiz.course_id, self.course.id)

    # update()
    def test_update(self, m):
        register_uris(
            {"new_quiz": ["update_new_quiz"]},
            m,
            base_url=settings.BASE_URL_NEW_QUIZZES,
        )

        new_title = "New Quiz One - Updated!"
        new_instructions = "<p>This is the updated New Quiz. You got this!</p>"
        new_quiz = self.new_quiz.update(
            quiz={"title": new_title, "instructions": new_instructions}
        )

        self.assertIsInstance(new_quiz, NewQuiz)
        self.assertTrue(hasattr(new_quiz, "title"))
        self.assertEqual(new_quiz.title, new_title)
        self.assertTrue(hasattr(new_quiz, "instructions"))
        self.assertEqual(new_quiz.instructions, new_instructions)
        self.assertTrue(hasattr(new_quiz, "course_id"))
        self.assertEqual(new_quiz.course_id, self.course.id)
