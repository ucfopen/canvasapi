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

    # __str__()
    def test_uncapitalized___str__(self, m):

        with requests_mock.Mocker() as m:
            requires = {
                "current_user": [
                    "add_favorite_course",
                    "add_favorite_group",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_course = self.user.add_favorite_course(1)
            self.favorite_group = self.user.add_favorite_group(1)

        string = str(self.favorite_course)
        self.assertIsInstance(string, str)

        string = str(self.favorite_group)
        self.assertIsInstance(string, str)

    def test_capitalized___str__(self, m):

        with requests_mock.Mocker() as m:
            requires = {
                "current_user_capitalized_context_types": [
                    "add_favorite_course",
                    "add_favorite_group",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_course = self.user.add_favorite_course(1)
            self.favorite_group = self.user.add_favorite_group(1)


        string = str(self.favorite_course)
        self.assertIsInstance(string, str)

        string = str(self.favorite_group)
        self.assertIsInstance(string, str)

    # remove()
    def test_remove_uncapitalized_favorite_course(self, m):

        with requests_mock.Mocker() as m:
            requires = {
                "current_user": [
                    "add_favorite_course",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_course = self.user.add_favorite_course(1)

            register_uris({"current_user": ["remove_favorite_course"]}, m)

            evnt = self.favorite_course.remove()

        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "course")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_uncapitalized_favorite_group(self, m):

        with requests_mock.Mocker() as m:
            requires = {
                "current_user": [
                    "add_favorite_group",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_group = self.user.add_favorite_group(1)

            register_uris({"current_user": ["remove_favorite_group"]}, m)

            evnt = self.favorite_group.remove()

        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "group")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_capitalized_favorite_course(self, m):

        with requests_mock.Mocker() as m:
            requires = {
                "current_user_capitalized_context_types": [
                    "add_favorite_course",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_course = self.user.add_favorite_course(1)

            register_uris({"current_user_capitalized_context_types": ["remove_favorite_course"]}, m)

            evnt = self.favorite_course.remove()
        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "Course")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_capitalized_favorite_group(self, m):

        with requests_mock.Mocker() as m:
            requires = {
                "current_user_capitalized_context_types": [
                    "add_favorite_group",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_group = self.user.add_favorite_group(1)

            register_uris({"current_user_capitalized_context_types": ["remove_favorite_group"]}, m)

            evnt = self.favorite_group.remove()
        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "Group")
        self.assertEqual(evnt.context_id, 1)
