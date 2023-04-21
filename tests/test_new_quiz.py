import unittest

import requests_mock

from canvasapi import Canvas
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
