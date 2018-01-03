from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.quiz import Quiz
from tests import settings
from tests.util import register_uris
from canvasapi.quiz_group import QuizGroup
from canvasapi.exceptions import RequiredFieldMissing


@requests_mock.Mocker()
class TestQuiz(unittest.TestCase):

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

    # get_quiz_group()
    def test_get_quiz_group(self, m):
        register_uris({'quiz': ['get_quiz_group']}, m)

        result = self.quiz.get_quiz_group(1)
        self.assertIsInstance(result, QuizGroup)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.quiz_id, 1)

    # create_question_group()
    def test_create_question_group(self, m):
        register_uris({'quiz': ['create_question_group']}, m)

        quiz_group = [{'name': 'Test Group', 'pick_count': 1,
                      'question_points': 2, 'assessment_question_bank_id': 3}]
        result = self.quiz.create_question_group(quiz_group)

        self.assertIsInstance(result, QuizGroup)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.quiz_id, 1)
        self.assertEqual(result.name, quiz_group[0].get('name'))
        self.assertEqual(result.pick_count, quiz_group[0].get('pick_count'))
        self.assertEqual(result.question_points, quiz_group[0].get('question_points'))
        self.assertEqual(result.assessment_question_bank_id,
                         quiz_group[0].get('assessment_question_bank_id'))

    def test_create_question_group_empty_list(self, m):
        register_uris({'quiz': ['create_question_group']}, m)

        quiz_group = []

        with self.assertRaises(ValueError):
            self.quiz.create_question_group(quiz_group)

    def test_create_question_group_incorrect_param(self, m):
        register_uris({'quiz': ['create_question_group']}, m)

        quiz_group = [1]

        with self.assertRaises(ValueError):
            self.quiz.create_question_group(quiz_group)

    def test_create_question_group_incorrect_dict(self, m):
        register_uris({'quiz': ['create_question_group']}, m)

        quiz_group = [{}]

        with self.assertRaises(RequiredFieldMissing):
            self.quiz.create_question_group(quiz_group)
