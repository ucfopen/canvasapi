import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.bookmark import Bookmark
from canvasapi.course import Course
from canvasapi.favorite import Favorite
from canvasapi.group import Group
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCurrentUser(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        with requests_mock.Mocker() as m:
            register_uris({"current_user": ["get_by_id"]}, m)
            self.user = self.canvas.get_current_user()

    # __str__()
    def test__str__(self, m):
        string = str(self.user)
        self.assertIsInstance(string, str)

    # get_groups()
    def test_get_groups(self, m):
        register_uris({"current_user": ["list_groups", "list_groups2"]}, m)

        groups = self.user.get_groups()
        group_list = [group for group in groups]

        self.assertEqual(len(group_list), 4)
        self.assertIsInstance(group_list[0], Group)

    # get_bookmarks()
    def test_get_bookmarks(self, m):
        register_uris({"bookmark": ["list_bookmarks"]}, m)

        bookmarks = self.user.get_bookmarks()
        bookmark_list = [bookmark for bookmark in bookmarks]
        self.assertEqual(len(bookmark_list), 2)
        self.assertIsInstance(bookmark_list[0], Bookmark)

    # get_bookmark()
    def test_get_bookmark(self, m):
        register_uris({"bookmark": ["get_bookmark"]}, m)

        bookmark_by_id = self.user.get_bookmark(45)
        self.assertIsInstance(bookmark_by_id, Bookmark)
        self.assertEqual(bookmark_by_id.name, "Test Bookmark 3")
        bookmark_by_obj = self.user.get_bookmark(bookmark_by_id)
        self.assertIsInstance(bookmark_by_obj, Bookmark)
        self.assertEqual(bookmark_by_obj.name, "Test Bookmark 3")

    # create_bookmark()
    def test_create_bookmark(self, m):
        register_uris({"bookmark": ["create_bookmark"]}, m)
        evnt = self.user.create_bookmark(
            name="Test Bookmark", url="https://www.google.com"
        )
        self.assertIsInstance(evnt, Bookmark)
        self.assertEqual(evnt.name, "Test Bookmark")
        self.assertEqual(evnt.url, "https://www.google.com")

    # get_favorite_courses()
    def test_get_favorite_courses(self, m):
        register_uris({"current_user": ["get_favorite_courses"]}, m)

        fav_courses = self.user.get_favorite_courses()
        fav_course_list = [course for course in fav_courses]
        self.assertIsInstance(fav_courses[0], Course)
        self.assertIsInstance(fav_courses[1], Course)
        self.assertEqual(len(fav_course_list), 2)
        self.assertEqual(fav_courses[0].name, "Fave Course 1")
        self.assertEqual(fav_courses[0].id, 1)
        self.assertEqual(fav_courses[0].course_code, "DND-4848")
        self.assertEqual(fav_courses[1].name, "Fave Course 2")

    # get_favorite_groups()
    def test_get_favorite_groups(self, m):
        register_uris({"current_user": ["get_favorite_groups"]}, m)

        fav_groups = self.user.get_favorite_groups()
        fav_groups_list = [group for group in fav_groups]
        self.assertEqual(len(fav_groups_list), 2)
        self.assertIsInstance(fav_groups[0], Group)
        self.assertIsInstance(fav_groups[1], Group)
        self.assertEqual(fav_groups[0].name, "Group 1")
        self.assertEqual(fav_groups[0].id, 1)

    # add_favorite_course()
    def test_add_favorite_course(self, m):
        register_uris(
            {"current_user": ["add_favorite_course"], "course": ["get_by_id"]}, m
        )

        fav_by_id = self.user.add_favorite_course(1)
        self.assertIsInstance(fav_by_id, Favorite)
        self.assertEqual(fav_by_id.context_type, "course")
        self.assertEqual(fav_by_id.context_id, 1)

        obj = self.canvas.get_course(1)
        fav_by_obj = self.user.add_favorite_course(obj)
        self.assertIsInstance(fav_by_obj, Favorite)
        self.assertEqual(fav_by_obj.context_type, "course")
        self.assertEqual(fav_by_obj.context_id, 1)

    def test_add_favorite_course_sis_id(self, m):
        register_uris({"current_user": ["add_favorite_course_by_sis_id"]}, m)

        fav_by_sis = self.user.add_favorite_course("test-sis-id", use_sis_id=True)

        self.assertIsInstance(fav_by_sis, Favorite)
        self.assertEqual(fav_by_sis.context_id, 1)
        self.assertEqual(fav_by_sis.context_type, "course")

    # add_favorite_group()
    def test_add_favorite_group(self, m):
        register_uris(
            {"current_user": ["add_favorite_group"], "group": ["get_by_id"]}, m
        )

        fav_by_id = self.user.add_favorite_group(1)
        self.assertIsInstance(fav_by_id, Favorite)
        self.assertEqual(fav_by_id.context_type, "group")
        self.assertEqual(fav_by_id.context_id, 1)

        obj = self.canvas.get_group(1)
        fav_by_obj = self.user.add_favorite_group(obj)
        self.assertIsInstance(fav_by_obj, Favorite)
        self.assertEqual(fav_by_obj.context_type, "group")
        self.assertEqual(fav_by_obj.context_id, 1)

    def test_add_favorite_group_sis_id(self, m):
        register_uris({"current_user": ["add_favorite_group_by_sis_id"]}, m)

        fav_by_sis = self.user.add_favorite_group("test-sis-id", use_sis_id=True)

        self.assertIsInstance(fav_by_sis, Favorite)
        self.assertEqual(fav_by_sis.context_id, 1)
        self.assertEqual(fav_by_sis.context_type, "group")

    # reset_favorite_courses()
    def test_reset_favorite_courses(self, m):
        register_uris({"current_user": ["reset_favorite_courses"]}, m)

        response = self.user.reset_favorite_courses()
        self.assertTrue(response)

    # reset_favorite_groups()
    def test_reset_favorite_groups(self, m):
        register_uris({"current_user": ["reset_favorite_groups"]}, m)

        response = self.user.reset_favorite_groups()
        self.assertTrue(response)
