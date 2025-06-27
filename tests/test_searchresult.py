import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.searchresult import SearchResult
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSearchResult(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": [
                        "get_by_id",
                        "smartsearch_basic",
                        "smartsearch_with_filter",
                        "get_page",
                        "get_assignment",
                        "get_discussion_topic",
                        "get_announcement",
                        "get_disc_topic",
                    ]
                },
                m,
            )
            self.course = self.canvas.get_course(1)
            self.basic_result = list(self.course.smartsearch("Copernicus"))[0]
            self.assignment_result = list(
                self.course.smartsearch("derivatives", filter=["assignments"])
            )[0]

    def test_str_representation(self, m):
        register_uris({"course": ["smartsearch_basic"]}, m)
        self.assertEqual(
            str(self.basic_result), "<SearchResult: Assignment - Chain Rule Practice>"
        )

    def test_str_fallback(self, m):
        register_uris({"course": ["smartsearch_basic"]}, m)
        result = list(self.course.smartsearch("Copernicus"))[0]
        delattr(result, "title")
        self.assertIn("Untitled", str(result))

    def test_missing_fields_raises(self, m):
        with self.assertRaises(ValueError):
            SearchResult(self.basic_result._requester, {"content_type": "WikiPage"})

    def test_resolve_page(self, m):
        register_uris({"course": ["get_assignment"]}, m)
        resolved = self.basic_result.resolve(self.course)
        self.assertEqual(resolved.title, "Derivatives HW")

    def test_resolve_assignment(self, m):
        register_uris({"course": ["get_assignment"]}, m)
        resolved = self.assignment_result.resolve(self.course)
        self.assertEqual(resolved.title, "Derivatives HW")

    def test_resolve_discussion(self, m):
        register_uris({"course": ["get_disc_topic"]}, m)
        result = SearchResult(
            self.basic_result._requester,
            {
                "content_id": 6,
                "content_type": "DiscussionTopic",
                "title": "Intro Discussion",
                "html_url": "https://canvas.example.com/discussion",
            },
        )
        resolved = result.resolve(self.course)
        self.assertEqual(resolved.title, "Class Cancelled")

    def test_resolve_announcement(self, m):
        register_uris({"course": ["get_discussion_topic", "get_announcement"]}, m)
        result = SearchResult(
            self.basic_result._requester,
            {
                "content_id": 7,
                "content_type": "Announcement",
                "title": "Class Cancelled",
                "html_url": "https://canvas.example.com/announcements",
            },
        )
        resolved = result.resolve(self.course)
        self.assertEqual(resolved.title, "Class Cancelled")

    def test_resolve_unknown_type_raises(self, m):
        result = SearchResult(
            self.basic_result._requester,
            {
                "content_id": 999,
                "content_type": "MysteryThing",
                "title": "Mystery",
                "html_url": "https://canvas.example.com/unknown",
            },
        )
        with self.assertRaises(ValueError):
            result.resolve(self.course)

    def test_resolve_missing_attrs_raises(self, m):
        with self.assertRaises(ValueError):
            result = SearchResult(self.basic_result._requester, {"title": "Incomplete"})
            result.resolve(self.course)

    def test_resolve_raises_if_missing_attrs(self, m):
        result = SearchResult(
            self.course._requester,
            {
                "content_id": 42,
                "content_type": "Assignment",
                "title": "Partial Result",
                "html_url": "https://canvas.example.com",
            },
        )
        delattr(result, "content_id")
        with self.assertRaises(ValueError) as ctx:
            result.resolve(self.course)
        self.assertIn("content_type", str(ctx.exception))
