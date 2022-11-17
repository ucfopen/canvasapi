import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.rubric import Rubric, RubricAssessment, RubricAssociation
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestRubric(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "create_rubric"]}, m)

            self.course = self.canvas.get_course(1)
            self.rubric = self.course.create_rubric()["rubric"]

    # delete
    def test_delete(self, m):
        register_uris({"rubric": ["delete_rubric"]}, m)

        rubric = self.rubric.delete()

        self.assertIsInstance(rubric, Rubric)
        self.assertEqual(rubric.id, 1)
        self.assertEqual(rubric.title, "Course Rubric 1")
        self.assertEqual(rubric.context_id, 1)
        self.assertEqual(rubric.context_type, "Course")
        self.assertEqual(rubric.points_possible, 10.0)
        self.assertFalse(rubric.reusable)
        self.assertTrue(rubric.read_only)
        self.assertTrue(rubric.free_form_critereon_comments)
        self.assertTrue(rubric.hide_score_total)

    # __str__()
    def test__str__(self, m):
        string = str(self.rubric)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestGradingStandard(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "get_rubric_single"]}, m)

            self.course = self.canvas.get_course(1)
            self.rubric = self.course.get_rubric(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.rubric)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestRubricAssessment(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": [
                        "get_by_id",
                        "create_rubric_with_association",
                        "create_rubric_association",
                    ],
                    "rubric": ["create_rubric_assessment"],
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.rubric = self.course.create_rubric()
            self.association = self.course.create_rubric_association()
            self.assessment = self.association.create_rubric_assessment()

    def test__str__(self, m):
        string = str(self.assessment)
        self.assertIsInstance(string, str)

    def test_update(self, m):
        register_uris({"rubric": ["update_rubric_assessment"]}, m)

        self.assertEqual(self.assessment.provisional, "false")

        updated_assessment = self.assessment.update(provisional=True)

        self.assertEqual(updated_assessment.id, 1)
        self.assertEqual(updated_assessment.provisional, "true")

    def test_delete(self, m):
        register_uris({"rubric": ["delete_rubric_assessment"]}, m)

        deleted_assessment = self.assessment.delete()

        self.assertEqual(deleted_assessment.id, 1)
        self.assertIsInstance(deleted_assessment, RubricAssessment)


@requests_mock.Mocker()
class TestRubricAssociation(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": [
                        "get_by_id",
                        "create_rubric_with_association",
                        "create_rubric_association",
                    ]
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.rubric = self.course.create_rubric()
            self.association = self.course.create_rubric_association()

    # __str__()
    def test__str__(self, m):
        string = str(self.rubric["rubric_association"])
        self.assertIsInstance(string, str)

    # update
    def test_update(self, m):
        register_uris({"rubric": ["update_rubric_association"]}, m)

        self.assertEqual(self.association.id, 4)

        rubric_association = self.association.update()

        self.assertEqual(rubric_association, self.association)
        self.assertEqual(rubric_association.id, 5)
        self.assertIsInstance(rubric_association, RubricAssociation)
        self.assertEqual(rubric_association.association_type, "Assignment")

    # delete
    def test_delete(self, m):
        register_uris({"rubric": ["delete_rubric_association"]}, m)

        rubric_association = self.association.delete()

        self.assertIsInstance(rubric_association, RubricAssociation)
        self.assertEqual(rubric_association.id, 4)
        self.assertEqual(rubric_association.association_type, "Assignment")
