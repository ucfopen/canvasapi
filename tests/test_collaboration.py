from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.collaboration import Collaboration
from tests import settings


@requests_mock.Mocker()
class TestCollaboration(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.collaboration = Collaboration(
            self.canvas._Canvas__requester,
            {
                "id": 1,
                "collaboration_type": "Microsoft Office",
                "document_id": "oinwoenfe8w8ef_onweufe89fef",
                "user_id": 92,
                "context_id": 77,
                "context_type": "Course",
                "url": "null",
                "created_at": "2012-06-01T00:00:00-06:00",
                "updated_at": "2012-06-01T00:00:00-06:00",
                "description": "null",
                "title": "null",
                "type": "ExternalToolCollaboration",
                "update_url": "null",
                "user_name": "John Danger",
            },
        )

    def test_str(self, m):
        test_str = str(self.collaboration)
        self.assertIsInstance(test_str, str)
