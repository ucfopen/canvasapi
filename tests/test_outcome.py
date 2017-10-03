from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.account import Account
from canvasapi.course import Course
from canvasapi.outcome import Outcome, OutcomeGroup, OutcomeLink
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestOutcome(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    'account': ['get_by_id'],
                    'course': ['get_by_id'],
                    'outcome': [
                        'account_root_outcome_group',
                        'canvas_root_outcome_group',
                        'course_root_outcome_group'
                    ]
                }, m
            )

            self.canvas_outcome_group = self.canvas.get_root_outcome_group()

            self.account = self.canvas.get_account(1)
            self.account_outcome_group = self.account.get_root_outcome_group()
            self.account_outcome_groups = self.account.get_outcome_groups_in_context()
            self.account_outcome_links = self.account.get_all_outcome_links_in_context()

            self.course = self.canvas.get_course(1)
            self.course_outcome_group = self.course.get_root_outcome_group()
            self.course_outcome_groups = self.course.get_outcome_groups_in_context()
            self.course_outcome_links = self.course.get_all_outcome_links_in_context()

            self.example_outcome = self.course_outcome_links[0].outcome

    # __str__()
    def test__str__(self, m):
        string = str(self.example_outcome)
        self.assertIsInstance(string, str)

    # show()
    def test_show(self, m):
        test_show = self.example_outcome.show()

        self.assertIsInstance(test_show, Outcome)
    '''
    # update()
    def test_update(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, Outcome)
    '''


@requests_mock.Mocker()
class TestOutcomeLink(unittest.TestCase):
    def setUp(self):
        return

    # __str__()
    # def test__str__(self, m):
    #     string = str(self.outcome)
    #     self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestOutcomeGroup(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    'account': ['get_by_id'],
                    'course': ['get_by_id'],
                    'outcome': [
                        'account_root_outcome_group',
                        'canvas_root_outcome_group',
                        'course_root_outcome_group'
                    ]
                }, m
            )

            self.canvas_outcome_group = self.canvas.get_root_outcome_group()
            self.account = self.canvas.get_account(1)
            self.account_outcome_group = self.account.get_root_outcome_group()
            self.course = self.canvas.get_course(1)
            self.course_outcome_group = self.course.get_root_outcome_group()

    # __str__()
    # def test__str__(self, m):
    #     string = str(self.canvas_outcome_group)
    #     self.assertIsInstance(string, str)

    '''
    # show()
    def test_show(self, m):
        test_show_outcome_group = self.show()
        self.assertIsInstance(test_show_outcome_group, OutcomeGroup)

    # update()
    def test_update(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeGroup)

    # delete()
    def test_delete(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeGroup)

    # list_linked_outcomes()
    def test_list_linked_outcomes(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ[0], OutcomeLink)

    # link_existing()
    def test_link_existing(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeLink)

    # link_new()
    def test_link_new(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeLink)

    # unlink_outcome()
    def test_unlink_outcome(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeLink)

    # list_subgroups()
    def test_list_subgroups(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ[0], OutcomeGroup)

    # create_subgroup()
    def test_create_subgroup(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeGroup)

    # import_outcome_group()
    def test_import_outcome_group(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeGroup)
    '''
