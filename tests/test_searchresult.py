import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.page import Page
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
        self.assertEqual(
            str(self.basic_result), "<SearchResult: WikiPage - Nicolaus Copernicus>"
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
        register_uris({"course": ["get_page_smartsearch_variant"]}, m)
        resolved = self.basic_result.resolve()
        self.assertEqual(resolved.title, "Nicolaus Copernicus")

    def test_resolve_assignment(self, m):
        register_uris({"course": ["get_assignment_smartsearch_variant"]}, m)
        resolved = self.assignment_result.resolve()
        self.assertIsInstance(resolved, Assignment)
        self.assertEqual(resolved.name, "Derivatives HW")

    def test_resolve_discussion(self, m):
        register_uris({"course": ["get_disc_topic_smartsearch_variant"]}, m)
        result = SearchResult(
            self.basic_result._requester,
            {
                "content_id": 6,
                "content_type": "DiscussionTopic",
                "title": "Intro Discussion",
                "html_url": "https://canvas.example.com/discussion",
                "course_id": 1,
            },
        )
        resolved = result.resolve()
        self.assertEqual(resolved.title, "Please Discuss")

    def test_resolve_announcement(self, m):
        register_uris(
            {
                "course": [
                    "get_disc_topic_smartsearch_variant",
                    "get_announcement_smartsearch_variant",
                ]
            },
            m,
        )
        result = SearchResult(
            self.basic_result._requester,
            {
                "content_id": 7,
                "content_type": "Announcement",
                "title": "Class Cancelled",
                "html_url": "https://canvas.example.com/announcements",
                "course_id": 1,
            },
        )
        resolved = result.resolve()
        self.assertEqual(resolved.title, "Class Cancelled")

    def test_resolve_unknown_type_raises(self, m):
        result = SearchResult(
            self.basic_result._requester,
            {
                "content_id": 999,
                "content_type": "MysteryThing",
                "title": "Mystery",
                "html_url": "https://canvas.example.com/unknown",
                "course_id": 1,
            },
        )
        with self.assertRaises(ValueError):
            result.resolve()

    def test_resolve_missing_attrs_raises(self, m):
        with self.assertRaises(ValueError):
            result = SearchResult(self.basic_result._requester, {"title": "Incomplete"})
            result.resolve()

    def test_resolve_raises_if_missing_attrs(self, m):
        result = SearchResult(
            self.course._requester,
            {
                "content_id": 42,
                "content_type": "Assignment",
                "title": "Partial Result",
                "html_url": "https://canvas.example.com",
                "course_id": 1,
            },
        )
        delattr(result, "content_id")
        with self.assertRaises(ValueError) as ctx:
            result.resolve()
        self.assertIn("content_type", str(ctx.exception))

    def test_resolve_multiple_types(self, m):
        register_uris(
            {
                "course": [
                    "smartssearch_multiple_results",
                    "get_page_smartsearch_variant",
                    "get_assignment_smartsearch_variant",
                    "get_disc_topic_smartsearch_variant",
                    "get_announcement_smartsearch_variant",
                ]
            },
            m,
        )
        results = list(self.course.smartsearch("multiple"))
        self.assertEqual(len(results), 4)

        # WikiPage
        self.assertIsInstance(results[0].resolve(), Page)

        # Assignment
        self.assertIsInstance(results[1].resolve(), Assignment)

        # DiscussionTopic
        self.assertIsInstance(results[2].resolve(), DiscussionTopic)

        # Announcement (uses DiscussionTopic)
        self.assertIsInstance(results[3].resolve(), DiscussionTopic)
