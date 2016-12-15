import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.conversation import Conversation
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestConversation(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'conversation': ['get_by_id']}, m)

            self.conversation = self.canvas.get_conversation(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.conversation)
        assert isinstance(string, str)

    # edit()
    def test_edit(self, m):
        register_uris({'conversation': ['edit_conversation']}, m)

        new_subject = "conversations api example"
        success = self.conversation.edit(subject=new_subject)
        assert success

    def test_edit_fail(self, m):
        requires = {'conversation': ['get_by_id_2', 'edit_conversation_fail']}
        register_uris(requires, m)

        temp_convo = self.canvas.get_conversation(2)
        assert temp_convo.edit() is False

    # delete()
    def test_delete(self, m):
        register_uris({'conversation': ['delete_conversation']}, m)

        success = self.conversation.delete()
        assert success

    def test_delete_fail(self, m):
        requires = {'conversation': ['get_by_id_2', 'delete_conversation_fail']}
        register_uris(requires, m)

        temp_convo = self.canvas.get_conversation(2)
        assert temp_convo.delete() is False

    # add_recipients()
    def test_add_recipients(self, m):
        register_uris({'conversation': ['add_recipients']}, m)

        recipients = {'bob': 1, 'joe': 2}
        string_bob = "Bob was added to the conversation by Hank TA"
        string_joe = "Joe was added to the conversation by Hank TA"
        result = self.conversation.add_recipients([recipients['bob'], recipients['joe']])
        assert hasattr(result, 'messages')
        assert len(result.messages) == 2
        assert result.messages[0]["body"] == string_bob
        assert result.messages[1]["body"] == string_joe

    # add_message()
    def test_add_message(self, m):
        register_uris({'conversation': ['add_message']}, m)

        test_string = "add_message test body"
        result = self.conversation.add_message(test_string)
        assert isinstance(result, Conversation)
        assert len(result.messages) == 1
        assert result.messages[0]['id'] == 3

    # delete_message()
    def test_delete_message(self, m):
        register_uris({'conversation': ['delete_message']}, m)

        id_list = [1]
        result = self.conversation.delete_messages(id_list)
        assert 'subject' in result
        assert result['id'] == 1
