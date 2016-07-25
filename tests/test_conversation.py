import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.conversation import Conversation
from tests import settings
from tests.util import register_uris


class TestConversation(unittest.TestCase):
    """
    Tests PageView functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'conversation': [
                'get_by_id',
                "get_by_id_2",
                'edit_conversation',
                'edit_conversation_fail',
                'delete_conversation',
                'delete_conversation_fail',
                'add_recipients',
                'add_message',
                'delete_message',
                'mark_all_as_read',
                'unread_count',
                'get_running_batches',
                'batch_update'
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
        result = self.conversation.add_recipients([recipients['bob'],recipients['joe']])
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
        result = self.conversation.delete_message(id_list)
        assert 'subject' in result
        assert result['id'] == 1

    # mark_all_as_read()
    def test_mark_all_as_read(self):
        result = self.conversation.mark_all_as_read()
        assert result is True

    # unread_count()
    def test_unread_count(self):
        result = self.conversation.unread_count()
        assert result['unread_count'] == "7"

    # get_running_batches()
    def test_get_running_batches(self):
        result = self.conversation.get_running_batches()
        assert len(result) == 2
        assert 'body' in result[0]['message']
        assert result[1]['message']['author_id'] == 1

    # batch_update()
    def test_batch_update(self):
        from pycanvas.process import Process
        conversation_ids= [1, 2]
        this_event = "mark_as_read"
        result = self.conversation.batch_update(event=this_event, conversation_ids=conversation_ids)
        assert isinstance(result, Process)

    def test_batch_updated_fail_on_event(self):
        conversation_ids= [1, 2]
        this_event = "this doesn't work"
        result = self.conversation.batch_update(event=this_event, conversation_ids=conversation_ids)
        assert isinstance(result, ValueError)

    def test_batch_updated_fail_on_ids(self):
        conversation_ids = [None] * 501
        this_event = "mark_as_read"
        result = self.conversation.batch_update(event=this_event, conversation_ids=conversation_ids)
        assert isinstance(result, ValueError)
