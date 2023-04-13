import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.favorite import Favorite
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFavorite(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "current_user": [
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()

    # __str__()
    def test_uncapitalized___str__(self, m):
        register_uris(
            {
                "current_user": [
                    "add_favorite_course",
                    "add_favorite_group",
                ]
            },
            m,
        )

        favorite_course = self.user.add_favorite_course(1)
        favorite_group = self.user.add_favorite_group(1)

        string = str(favorite_course)
        self.assertIsInstance(string, str)

        string = str(favorite_group)
        self.assertIsInstance(string, str)

    def test_capitalized___str__(self, m):
        register_uris(
            {
                "current_user": [
                    "add_favorite_course_cap_context_type",
                    "add_favorite_group_cap_context_type",
                ]
            },
            m,
        )

        favorite_course = self.user.add_favorite_course(1)
        favorite_group = self.user.add_favorite_group(1)

        string = str(favorite_course)
        self.assertIsInstance(string, str)

        string = str(favorite_group)
        self.assertIsInstance(string, str)

    # remove()
    def test_remove_uncapitalized_favorite_course(self, m):
        register_uris(
            {
                "current_user": [
                    "add_favorite_course",
                    "remove_favorite_course",
                ]
            },
            m,
        )

        favorite_course = self.user.add_favorite_course(1)

        evnt = favorite_course.remove()

        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "course")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_uncapitalized_favorite_group(self, m):
        register_uris(
            {
                "current_user": [
                    "add_favorite_group",
                    "remove_favorite_group",
                ]
            },
            m,
        )

        favorite_group = self.user.add_favorite_group(1)

        evnt = favorite_group.remove()

        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "group")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_capitalized_favorite_course(self, m):
        register_uris(
            {
                "current_user": [
                    "add_favorite_course_cap_context_type",
                    "remove_favorite_course_cap_context_type",
                ]
            },
            m,
        )

        favorite_course = self.user.add_favorite_course(1)

        evnt = favorite_course.remove()

        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "Course")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_capitalized_favorite_group(self, m):
        register_uris(
            {
                "current_user": [
                    "add_favorite_group_cap_context_type",
                    "remove_favorite_group_cap_context_type",
                ]
            },
            m,
        )

        favorite_group = self.user.add_favorite_group(1)

        evnt = favorite_group.remove()

        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "Group")
        self.assertEqual(evnt.context_id, 1)
