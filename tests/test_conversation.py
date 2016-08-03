import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.conversation import Conversation
from tests import settings
from tests.util import register_uris


class TestConversation(unittest.TestCase):
    """
    Tests Conversation functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'conversation': [
                'add_message', 'add_recipients', 'delete_conversation',
                'delete_conversation_fail', 'delete_message', 'edit_conversation',
                'edit_conversation_fail', 'get_by_id', 'get_by_id_2'
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, {'generic': ['not_found']}, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.conversation = self.canvas.get_conversation(1)

    # __str__()
    def test__str__(self):
        string = str(self.conversation)
        assert isinstance(string, str)

    # edit()
    def test_edit(self):
        new_subject = "conversations api example"
        success = self.conversation.edit(subject=new_subject)
        assert success

    def test_edit_fail(self):
        temp_convo = self.canvas.get_conversation(2)
        assert temp_convo.edit() is False

    # delete()
    def test_delete(self):
        success = self.conversation.delete()
        assert success

    def test_delete_fail(self):
        temp_convo = self.canvas.get_conversation(2)
        assert temp_convo.delete() is False

    # add_recipients()
    def test_add_recipients(self):
        recipients = {'bob': 1, 'joe': 2}
        string_bob = "Bob was added to the conversation by Hank TA"
        string_joe = "Joe was added to the conversation by Hank TA"
        result = self.conversation.add_recipients([recipients['bob'], recipients['joe']])
        assert hasattr(result, 'messages')
        assert len(result.messages) == 2
        assert result.messages[0]["body"] == string_bob
        assert result.messages[1]["body"] == string_joe

    # add_message()
    def test_add_message(self):
        test_string = "add_message test body"
        result = self.conversation.add_message(test_string)
        assert isinstance(result, Conversation)
        assert len(result.messages) == 1
        assert result.messages[0]['id'] == 3

    # delete_message()
    def test_delete_message(self):
        id_list = [1]
        result = self.conversation.delete_messages(id_list)
        assert 'subject' in result
        assert result['id'] == 1
