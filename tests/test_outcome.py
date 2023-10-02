import unittest

import requests_mock

from canvasapi import Canvas
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
                    "course": ["get_by_id"],
                    "outcome": [
                        "account_root_outcome_group",
                        "canvas_root_outcome_group",
                        "course_root_outcome_group",
                        "course_outcome_links_in_context",
                        "outcome_example",
                    ],
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.course_outcome_links = self.course.get_all_outcome_links_in_context()
            self.example_outcome = self.course_outcome_links[0].get_outcome()

    # __str__()
    def test__str__(self, m):
        string = str(self.example_outcome)
        self.assertIsInstance(string, str)

    # update()
    def test_update(self, m):
        register_uris({"outcome": ["outcome_update"]}, m)
        self.assertEqual(self.example_outcome.title, "Outcome Show Example")
        result = self.example_outcome.update(title="new_title")
        self.assertTrue(result)
        self.assertIsInstance(self.example_outcome, Outcome)
        self.assertEqual(self.example_outcome.title, "new_title")


@requests_mock.Mocker()
class TestOutcomeLink(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "account": ["get_by_id"],
                    "course": ["get_by_id"],
                    "outcome": [
                        "account_outcome_links_in_context",
                        "course_outcome_links_in_context",
                    ],
                },
                m,
            )

            self.account = self.canvas.get_account(1)
            self.account_outcome_links = self.account.get_all_outcome_links_in_context()
            self.course = self.canvas.get_course(1)
            self.course_outcome_links = self.course.get_all_outcome_links_in_context()

    # __str__()
    def test__str__(self, m):
        register_uris({"outcome": ["course_outcome_links_in_context"]}, m)
        string = str(self.course_outcome_links[0])
        self.assertIsInstance(string, str)

    # get_outcome()
    def test_get_outcome(self, m):
        register_uris(
            {"outcome": ["outcome_example", "course_outcome_links_in_context"]}, m
        )
        result = self.course_outcome_links[0].get_outcome()
        self.assertIsInstance(result, Outcome)

    # get_outcome_group()
    def test_get_outcome_group(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_example_account",
                    "account_outcome_links_in_context",
                    "outcome_group_example_course",
                    "course_outcome_links_in_context",
                ]
            },
            m,
        )
        result = self.course_outcome_links[0].get_outcome_group()
        self.assertIsInstance(result, OutcomeGroup)
        result = self.account_outcome_links[0].get_outcome_group()
        self.assertIsInstance(result, OutcomeGroup)


@requests_mock.Mocker()
class TestOutcomeGroup(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "account": ["get_by_id"],
                    "course": ["get_by_id"],
                    "outcome": [
                        "account_root_outcome_group",
                        "canvas_root_outcome_group",
                        "course_root_outcome_group",
                        "course_outcome_links_in_context",
                        "outcome_example",
                    ],
                },
                m,
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

            self.example_outcome = self.course_outcome_links[0].get_outcome()

    # __str__()
    def test__str__(self, m):
        string = str(self.canvas_outcome_group)
        self.assertIsInstance(string, str)

    # update()
    def test_update(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_update_global",
                    "outcome_group_update_account",
                    "outcome_group_update_course",
                ]
            },
            m,
        )

        new_title = "New Outcome Group Title"

        self.assertEqual(self.account_outcome_group.title, "ROOT")
        result = self.account_outcome_group.update(title=new_title)
        self.assertTrue(result)
        self.assertIsInstance(self.account_outcome_group, OutcomeGroup)
        self.assertEqual(self.account_outcome_group.title, new_title)

        self.assertEqual(self.canvas_outcome_group.title, "ROOT")
        result = self.canvas_outcome_group.update(title=new_title)
        self.assertTrue(result)
        self.assertIsInstance(self.canvas_outcome_group, OutcomeGroup)
        self.assertEqual(self.canvas_outcome_group.title, new_title)

        self.assertEqual(self.course_outcome_group.title, "ROOT")
        result = self.course_outcome_group.update(title=new_title)
        self.assertTrue(result)
        self.assertIsInstance(self.course_outcome_group, OutcomeGroup)
        self.assertEqual(self.course_outcome_group.title, new_title)

    # delete()
    def test_delete(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_delete_global",
                    "outcome_group_delete_account",
                    "outcome_group_delete_course",
                ]
            },
            m,
        )

        self.assertEqual(self.account_outcome_group.title, "ROOT")
        result = self.account_outcome_group.delete()
        self.assertTrue(result)

        self.assertEqual(self.canvas_outcome_group.title, "ROOT")
        result = self.canvas_outcome_group.delete()
        self.assertTrue(result)

        self.assertEqual(self.course_outcome_group.title, "ROOT")
        result = self.course_outcome_group.delete()
        self.assertTrue(result)

    # get_linked_outcomes()
    def test_get_linked_outcomes(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_list_linked_outcomes_account",
                    "outcome_group_list_linked_outcomes_global",
                    "outcome_group_list_linked_outcomes_courses",
                ]
            },
            m,
        )

        result = self.account_outcome_group.get_linked_outcomes()
        self.assertIsInstance(result[0], OutcomeLink)
        self.assertEqual(result[0].outcome_group["id"], 2)
        self.assertEqual(result[0].outcome_group["title"], "Account Test Outcome Group")

        result = self.canvas_outcome_group.get_linked_outcomes()
        self.assertIsInstance(result[0], OutcomeLink)
        self.assertEqual(result[0].outcome_group["id"], 2)
        self.assertEqual(result[0].outcome_group["title"], "Global Test Outcome Group")

        result = self.course_outcome_group.get_linked_outcomes()
        self.assertIsInstance(result[0], OutcomeLink)
        self.assertEqual(result[0].outcome_group["id"], 2)
        self.assertEqual(result[0].outcome_group["title"], "Course Test Outcome Group")

    # link_existing()
    def test_link_existing(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_example",
                    "outcome_group_link_existing_global",
                    "outcome_group_link_existing_account",
                    "outcome_group_link_existing_course",
                ]
            },
            m,
        )

        result = self.canvas_outcome_group.link_existing(self.example_outcome)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 2)

        result = self.account_outcome_group.link_existing(self.example_outcome)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 2)

        result = self.course_outcome_group.link_existing(self.example_outcome)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 2)

        result = self.canvas_outcome_group.link_existing(3)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 2)

        result = self.account_outcome_group.link_existing(3)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 2)

        result = self.course_outcome_group.link_existing(3)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 2)

    # link_new()
    def test_link_new(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_link_new_global",
                    "outcome_group_link_new_account",
                    "outcome_group_link_new_course",
                ]
            },
            m,
        )

        new_title = "New Outcome"

        result = self.canvas_outcome_group.link_new(title=new_title)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 1)
        self.assertEqual(result.outcome["id"], 2)
        self.assertEqual(result.outcome["context_type"], None)

        result = self.account_outcome_group.link_new(title=new_title)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 1)
        self.assertEqual(result.outcome["id"], 2)
        self.assertEqual(result.outcome["context_type"], "Account")

        result = self.course_outcome_group.link_new(title=new_title)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group["id"], 1)
        self.assertEqual(result.outcome["id"], 2)
        self.assertEqual(result.outcome["context_type"], "Course")

    # unlink_outcome()
    def test_unlink_outcome(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_example",
                    "outcome_group_unlink_outcome_global",
                    "outcome_group_unlink_outcome_account",
                    "outcome_group_unlink_outcome_course",
                ]
            },
            m,
        )

        result = self.canvas_outcome_group.unlink_outcome(self.example_outcome)
        self.assertTrue(result)

        result = self.account_outcome_group.unlink_outcome(self.example_outcome)
        self.assertTrue(result)

        result = self.course_outcome_group.unlink_outcome(self.example_outcome)
        self.assertTrue(result)

        result = self.canvas_outcome_group.unlink_outcome(3)
        self.assertTrue(result)

        result = self.account_outcome_group.unlink_outcome(3)
        self.assertTrue(result)

        result = self.course_outcome_group.unlink_outcome(3)
        self.assertTrue(result)

    # get_subgroups()
    def test_get_subgroups(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_list_subgroups_global",
                    "outcome_group_list_subgroups_account",
                    "outcome_group_list_subgroups_course",
                ]
            },
            m,
        )

        result = self.canvas_outcome_group.get_subgroups()
        self.assertIsInstance(result[0], OutcomeGroup)
        self.assertEqual(result[0].id, 2)
        self.assertEqual(result[0].title, "Global Listed Subgroup Title 1")
        self.assertTrue(hasattr(result[0], "context_type"))
        self.assertEqual(result[0].context_type, None)
        self.assertTrue(hasattr(result[0], "context_id"))
        self.assertEqual(result[0].context_id, None)
        self.assertIsInstance(result[1], OutcomeGroup)
        self.assertEqual(result[1].id, 3)
        self.assertEqual(result[1].title, "Global Listed Subgroup Title 2")
        self.assertTrue(hasattr(result[0], "context_type"))
        self.assertEqual(result[0].context_type, None)
        self.assertTrue(hasattr(result[0], "context_id"))
        self.assertEqual(result[0].context_id, None)

        result = self.account_outcome_group.get_subgroups()
        self.assertIsInstance(result[0], OutcomeGroup)
        self.assertEqual(result[0].id, 2)
        self.assertEqual(result[0].title, "Account Listed Subgroup Title 1")
        self.assertTrue(hasattr(result[0], "context_type"))
        self.assertEqual(result[0].context_type, "Account")
        self.assertTrue(hasattr(result[0], "context_id"))
        self.assertEqual(result[0].context_id, self.account.id)
        self.assertIsInstance(result[1], OutcomeGroup)
        self.assertEqual(result[1].id, 3)
        self.assertEqual(result[1].title, "Account Listed Subgroup Title 2")
        self.assertTrue(hasattr(result[0], "context_type"))
        self.assertEqual(result[0].context_type, "Account")
        self.assertTrue(hasattr(result[0], "context_id"))
        self.assertEqual(result[0].context_id, self.account.id)

        result = self.course_outcome_group.get_subgroups()
        self.assertIsInstance(result[0], OutcomeGroup)
        self.assertEqual(result[0].id, 2)
        self.assertEqual(result[0].title, "Course Listed Subgroup Title 1")
        self.assertTrue(hasattr(result[0], "context_type"))
        self.assertEqual(result[0].context_type, "Course")
        self.assertTrue(hasattr(result[0], "context_id"))
        self.assertEqual(result[0].context_id, self.course.id)
        self.assertIsInstance(result[1], OutcomeGroup)
        self.assertEqual(result[1].id, 3)
        self.assertEqual(result[1].title, "Course Listed Subgroup Title 2")
        self.assertTrue(hasattr(result[0], "context_type"))
        self.assertEqual(result[0].context_type, "Course")
        self.assertTrue(hasattr(result[0], "context_id"))
        self.assertEqual(result[0].context_id, self.course.id)

    # create_subgroup()
    def test_create_subgroup(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_create_subgroup_global",
                    "outcome_group_create_subgroup_account",
                    "outcome_group_create_subgroup_course",
                ]
            },
            m,
        )

        new_title = "New Subgroup Title"

        result = self.canvas_outcome_group.create_subgroup(new_title)
        self.assertEqual(
            self.canvas_outcome_group.id, result.parent_outcome_group["id"]
        )
        self.assertEqual(result.parent_outcome_group["title"], "Parent of Subgroup")
        self.assertEqual(result.title, "New Subgroup Title")

        result = self.account_outcome_group.create_subgroup(new_title)
        self.assertEqual(
            self.canvas_outcome_group.id, result.parent_outcome_group["id"]
        )
        self.assertEqual(result.parent_outcome_group["title"], "Parent of Subgroup")
        self.assertEqual(result.title, "New Subgroup Title")

        result = self.course_outcome_group.create_subgroup(new_title)
        self.assertEqual(
            self.canvas_outcome_group.id, result.parent_outcome_group["id"]
        )
        self.assertEqual(result.parent_outcome_group["title"], "Parent of Subgroup")
        self.assertEqual(result.title, "New Subgroup Title")

    # import_outcome_group()
    def test_import_outcome_group(self, m):
        register_uris(
            {
                "outcome": [
                    "outcome_group_import_outcome_group_global",
                    "outcome_group_import_outcome_group_account",
                    "outcome_group_import_outcome_group_course",
                ]
            },
            m,
        )

        result = self.canvas_outcome_group.import_outcome_group(3)
        self.assertEqual(result.id, 4)
        self.assertEqual(result.title, "Global Imported Subgroup Title")
        self.assertEqual(
            result.parent_outcome_group["id"], self.canvas_outcome_group.id
        )
        self.assertEqual(
            result.parent_outcome_group["title"], self.canvas_outcome_group.title
        )

        result = self.account_outcome_group.import_outcome_group(3)
        self.assertEqual(result.id, 4)
        self.assertEqual(result.title, "Account Imported Subgroup Title")
        self.assertEqual(
            result.parent_outcome_group["id"], self.account_outcome_group.id
        )
        self.assertEqual(
            result.parent_outcome_group["title"], self.account_outcome_group.title
        )

        result = self.course_outcome_group.import_outcome_group(3)
        self.assertEqual(result.id, 4)
        self.assertEqual(result.title, "Course Imported Subgroup Title")
        self.assertEqual(
            result.parent_outcome_group["id"], self.course_outcome_group.id
        )
        self.assertEqual(
            result.parent_outcome_group["title"], self.course_outcome_group.title
        )

        result_by_obj = self.course_outcome_group.import_outcome_group(result)
        self.assertEqual(result_by_obj.id, 4)
        self.assertEqual(result_by_obj.title, "Course Imported Subgroup Title")
        self.assertEqual(
            result_by_obj.parent_outcome_group["id"], self.course_outcome_group.id
        )
        self.assertEqual(
            result_by_obj.parent_outcome_group["title"], self.course_outcome_group.title
        )


@requests_mock.Mocker()
class TestOutcomeResult(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": ["get_by_id"],
                    "outcome": ["outcome_example", "outcome_result_example"],
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.course_outcome_results = self.course.get_outcome_results()
            self.outcome_result_example = self.course_outcome_results[0]
            # self.example_outcome = self.course_outcome_links[0].get_outcome()

    # __str__()
    def test__str__(self, m):
        string = str(self.outcome_result_example)
        self.assertIsInstance(string, str)
