import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import RequiredFieldMissing
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestQuizGroup(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"course": ["get_by_id"], "quiz": ["get_by_id_5", "get_quiz_group"]}, m
            )

            self.course = self.canvas.get_course(1)
            self.quiz_group = self.course.get_quiz(5).get_quiz_group(10)

    # __str__()
    def test__str__(self, m):
        string = str(self.quiz_group)
        self.assertIsInstance(string, str)

    # update_question_group()
    def test_update(self, m):
        register_uris({"quiz_group": ["update"]}, m)

        quiz_group = [{"name": "Test Group", "pick_count": 1, "question_points": 2}]
        result = self.quiz_group.update(quiz_group)

        self.assertIsInstance(result, bool)
        self.assertTrue(result)

        self.assertEqual(self.quiz_group.id, 10)
        self.assertEqual(self.quiz_group.quiz_id, 5)
        self.assertEqual(self.quiz_group.name, quiz_group[0].get("name"))
        self.assertEqual(self.quiz_group.pick_count, quiz_group[0].get("pick_count"))
        self.assertEqual(
            self.quiz_group.question_points, quiz_group[0].get("question_points")
        )

    def test_update_empty_list(self, m):
        register_uris({"quiz_group": ["update"]}, m)

        quiz_group = []

        with self.assertRaises(ValueError):
            self.quiz_group.update(quiz_group)

    def test_update_incorrect_param(self, m):
        register_uris({"quiz_group": ["update"]}, m)

        quiz_group = [1]

        with self.assertRaises(ValueError):
            self.quiz_group.update(quiz_group)

    def test_update_incorrect_dict(self, m):
        register_uris({"quiz_group": ["update"]}, m)

        quiz_group = [{}]

        with self.assertRaises(RequiredFieldMissing):
            self.quiz_group.update(quiz_group)

    # delete_question_group()
    def test_delete(self, m):
        register_uris({"quiz_group": ["delete"]}, m)

        result = self.quiz_group.delete()

        self.assertTrue(result)

    # reorder_question_group()
    def test_reorder_question_group(self, m):
        register_uris({"quiz_group": ["reorder_question_group"]}, m)

        newOrdering = [{"id": 2}, {"id": 1, "type": "question"}]
        result = self.quiz_group.reorder_question_group(newOrdering)

        self.assertTrue(result)

    def test_reorderquestion_group_empty_list(self, m):
        register_uris({"quiz_group": ["reorder_question_group"]}, m)

        order = []

        with self.assertRaises(ValueError):
            self.quiz_group.reorder_question_group(order)

    def test_reorderquestion_group_incorrect_param(self, m):
        register_uris({"quiz_group": ["reorder_question_group"]}, m)

        order = [1]

        with self.assertRaises(ValueError):
            self.quiz_group.reorder_question_group(order)

    def test_reorderquestion_group_incorrect_dict(self, m):
        register_uris({"quiz_group": ["reorder_question_group"]}, m)

        order = [{"something": 2}]

        with self.assertRaises(ValueError):
            self.quiz_group.reorder_question_group(order)
