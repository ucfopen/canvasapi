import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.collaboration import Collaboration, Collaborator
from canvasapi.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris


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

    def test_get_collaborators(self, m):
        register_uris({"collaboration": ["get_collaborators"]}, m)

        collaborator_list = self.collaboration.get_collaborators()

        self.assertIsInstance(collaborator_list, PaginatedList)
        self.assertIsInstance(collaborator_list[0], Collaborator)
        self.assertEqual(collaborator_list[0].id, 12345)
        self.assertEqual(collaborator_list[0].name, "Don Draper")


@requests_mock.Mocker()
class TestCollaborator(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.collaborator = Collaborator(
            self.canvas._Canvas__requester,
            {"id": 12345, "type": "user", "name": "Don Draper"},
        )

    def test_str(self, m):
        test_str = str(self.collaborator)
        self.assertIsInstance(test_str, str)
