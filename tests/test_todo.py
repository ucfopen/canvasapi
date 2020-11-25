import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.todo import Todo
from tests import settings


@requests_mock.Mocker()
class TestTodo(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.todo = Todo(
            self.canvas._Canvas__requester,
            {
                "type": "grading",
                "assignment": {},
                "ignore": ".. url ..",
                "ignore_permanently": ".. url ..",
                "html_url": ".. url ..",
                "needs_grading_count": 3,
                "context_type": "course",
                "course_id": 1,
                "group_id": None,
            },
        )

    def test_str(self, m):
        test_str = str(self.todo)
        self.assertIsInstance(test_str, str)
        self.assertEqual(test_str, "Todo Item (grading)")
