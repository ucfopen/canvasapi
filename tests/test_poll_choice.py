import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.poll_choice import PollChoice
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPollChoice(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"poll_choice": ["get_choice"], "poll": ["get_poll"]}
            register_uris(requires, m)
            self.poll = self.canvas.get_poll(1)
            self.poll.poll_choice = self.poll.get_choice(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.poll.poll_choice)
        self.assertIsInstance(string, str)

    # get_choices()
    def test_get_choices(self, m):
        register_uris({"poll_choice": ["get_choices"]}, m)

        choices_list = self.poll.get_choices()

        self.assertIsInstance(choices_list[0], PollChoice)
        self.assertIsInstance(choices_list[1], PollChoice)

    # get_choice()
    def test_get_choice(self, m):
        register_uris({"poll_choice": ["get_choice"]}, m)

        choice_by_id = self.poll.get_choice(1)
        self.assertIsInstance(choice_by_id, PollChoice)
        self.assertTrue(choice_by_id.is_correct)
        self.assertEqual(choice_by_id.text, "Example choice")
        self.assertEqual(choice_by_id.position, 1)

        choice_by_obj = self.poll.get_choice(choice_by_id)
        self.assertIsInstance(choice_by_obj, PollChoice)
        self.assertTrue(choice_by_obj.is_correct)
        self.assertEqual(choice_by_obj.text, "Example choice")
        self.assertEqual(choice_by_obj.position, 1)

    # create_choice()
    def test_create_choice(self, m):
        register_uris({"poll_choice": ["create_choice"]}, m)

        new_choice_t = self.poll.create_choice([{"text": "Example choice"}])
        self.assertIsInstance(new_choice_t, PollChoice)
        self.assertTrue(hasattr(new_choice_t, "text"))

        new_choice_t_ic = self.poll.create_choice(
            [{"text": "Example choice"}, {"is_correct": True}]
        )
        self.assertIsInstance(new_choice_t_ic, PollChoice)
        self.assertTrue(hasattr(new_choice_t_ic, "text"))
        self.assertTrue(hasattr(new_choice_t_ic, "is_correct"))

        new_choice_t_p = self.poll.create_choice(
            [{"text": "Example choice"}, {"position": 1}]
        )
        self.assertIsInstance(new_choice_t_p, PollChoice)
        self.assertTrue(hasattr(new_choice_t_p, "text"))
        self.assertTrue(hasattr(new_choice_t_p, "position"))

        new_choice_t_ic_p = self.poll.create_choice(
            [{"text": "Example choice"}, {"is_correct": True}, {"position": 1}]
        )
        self.assertIsInstance(new_choice_t_ic_p, PollChoice)
        self.assertTrue(hasattr(new_choice_t_ic_p, "text"))
        self.assertTrue(hasattr(new_choice_t_ic_p, "is_correct"))
        self.assertTrue(hasattr(new_choice_t_ic_p, "position"))

    # create_choice()
    def test_create_choice_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.poll.create_choice(poll_choice={})

    # update()
    def test_update(self, m):
        register_uris({"poll_choice": ["update"]}, m)

        updated_choice_t = self.poll.poll_choice.update([{"text": "Changed example"}])
        self.assertIsInstance(updated_choice_t, PollChoice)
        self.assertEqual(updated_choice_t.text, "Changed example")

        updated_choice_t_ic = self.poll.poll_choice.update(
            [{"text": "Changed example"}, {"is_correct": False}]
        )
        self.assertIsInstance(updated_choice_t_ic, PollChoice)
        self.assertEqual(updated_choice_t_ic.text, "Changed example")
        self.assertFalse(updated_choice_t_ic.is_correct)

        updated_choice_t_p = self.poll.poll_choice.update(
            [{"text": "Changed example"}, {"position": 2}]
        )
        self.assertIsInstance(updated_choice_t_p, PollChoice)
        self.assertEqual(updated_choice_t_p.text, "Changed example")
        self.assertEqual(updated_choice_t_p.position, 2)

        updated_choice_t_ic_p = self.poll.poll_choice.update(
            [{"text": "Changed example"}, {"is_correct": False}, {"position": 2}]
        )
        self.assertIsInstance(updated_choice_t_ic_p, PollChoice)
        self.assertEqual(updated_choice_t_ic_p.text, "Changed example")
        self.assertFalse(updated_choice_t_ic.is_correct)
        self.assertEqual(updated_choice_t_p.position, 2)

    # update_choice()
    def test_update_choice_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.poll.poll_choice.update(poll_choice={})

    # delete()
    def test_delete(self, m):
        register_uris({"poll_choice": ["delete"]}, m)

        result = self.poll.poll_choice.delete()
        self.assertTrue(result)
