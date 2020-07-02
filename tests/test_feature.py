import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.feature import Feature, FeatureFlag
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFeature(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "account": ["get_by_id", "get_features"],
                "course": ["get_by_id", "get_features"],
                "user": ["get_by_id", "get_features"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.course = self.canvas.get_course(1)
            self.user = self.canvas.get_user(1)
            self.feature_account = self.account.get_features()[0]
            self.feature_course = self.course.get_features()[0]
            self.feature_user = self.user.get_features()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.feature_course)
        self.assertIsInstance(string, str)

    # _parent_id()
    def test_parent_id_account(self, m):
        self.assertEqual(self.feature_account._parent_id, 1)

    def test_parent_id_course(self, m):
        self.assertEqual(self.feature_course._parent_id, 1)

    def test_parent_id_user(self, m):
        self.assertEqual(self.feature_user._parent_id, 1)

    def test_parent_id_no_id(self, m):
        feature = Feature(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            feature._parent_id

    # _parent_type()
    def test_parent_type_account(self, m):
        self.assertEqual(self.feature_account._parent_type, "account")

    def test_parent_type_course(self, m):
        self.assertEqual(self.feature_course._parent_type, "course")

    def test_parent_type_user(self, m):
        self.assertEqual(self.feature_user._parent_type, "user")

    def test_parent_type_no_id(self, m):
        feature = Feature(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            feature._parent_type


@requests_mock.Mocker()
class TestFeatureFlag(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "account": ["get_by_id", "get_features", "get_feature_flag"],
                "course": ["get_by_id", "get_features", "get_feature_flag"],
                "user": ["get_by_id", "get_features", "get_feature_flag"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.course = self.canvas.get_course(1)
            self.user = self.canvas.get_user(1)
            self.feature_account = self.account.get_features()[0]
            self.feature_course = self.course.get_features()[0]
            self.feature_user = self.user.get_features()[0]
            self.feature_flag_account = self.account.get_feature_flag(
                self.feature_account
            )
            self.feature_flag_course = self.course.get_feature_flag(self.feature_course)
            self.feature_flag_user = self.user.get_feature_flag(self.feature_user)

    # __str__()
    def test__str__(self, m):
        string = str(self.feature_flag_course)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete_account(self, m):
        register_uris({"account": ["delete_feature_flag"]}, m)
        delete_flag = self.feature_flag_account.delete(self.feature_account)

        self.assertIsInstance(delete_flag, FeatureFlag)

    def test_delete_course(self, m):
        register_uris({"course": ["delete_feature_flag"]}, m)
        delete_flag = self.feature_flag_course.delete(self.feature_course)

        self.assertIsInstance(delete_flag, FeatureFlag)

    def test_delete_user(self, m):
        register_uris({"user": ["delete_feature_flag"]}, m)
        delete_flag = self.feature_flag_user.delete(self.feature_user)

        self.assertIsInstance(delete_flag, FeatureFlag)

    # set_feature_flag()
    def test_set_feature_flag_account(self, m):
        register_uris({"account": ["set_feature_flag"]}, m)
        update_flag = self.feature_flag_account.set_feature_flag(self.feature_account)

        self.assertIsInstance(update_flag, FeatureFlag)

    def test_set_feature_flag_course(self, m):
        register_uris({"course": ["set_feature_flag"]}, m)
        update_flag = self.feature_flag_course.set_feature_flag(self.feature_course)

        self.assertIsInstance(update_flag, FeatureFlag)

    def test_set_feature_flag_user(self, m):
        register_uris({"user": ["set_feature_flag"]}, m)
        update_flag = self.feature_flag_user.set_feature_flag(self.feature_user)

        self.assertIsInstance(update_flag, FeatureFlag)
