import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestDay(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id", "get_gradebook_history_dates"]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.gradebook_history_dates = self.course.get_gradebook_history_dates()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.gradebook_history_dates)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestGrader(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id", "get_gradebook_history_details"]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.gradebook_history_details = self.course.get_gradebook_history_details(
                "03-26-2019"
            )[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.gradebook_history_details)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestSubmissionHistory(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id", "get_submission_history"]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.submission_history = self.course.get_submission_history(
                "08-23-2019", 1, 1
            )[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.submission_history)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestSubmissionVersion(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id", "get_uncollated_submissions"]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.uncollated_submissions = self.course.get_uncollated_submissions()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.uncollated_submissions)
        self.assertIsInstance(string, str)
