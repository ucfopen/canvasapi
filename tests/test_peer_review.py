import unittest

import requests_mock

from canvasapi.canvas import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPeerReview(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_assignment_by_id"],
                "assignment": ["list_peer_reviews"],
            }

            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)
            self.peer_reviews = [
                peer_review for peer_review in self.assignment.get_peer_reviews()
            ]

    # __str__()
    def test__str__(self, m):
        string = str(self.peer_reviews[0])
        self.assertIsInstance(string, str)
