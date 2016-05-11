import unittest

import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas
from pycanvas.course import CourseNickname
from pycanvas.user import User
from pycanvas.util import combine_kwargs, obj_or_id


class TestCourse(unittest.TestCase):
    """
    Tests utility methods
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found'],
            'user': ['get_by_id', 'course_nickname']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    # combine_kwargs()
    def test_combine_kwargs(self):
        key1_dict = {
            'subkey1-1': 'value1',
            'subkey1-2': 'value2',
            'subkey1-3': 'value3',
        }
        key2_dict = {
            'subkey2-1': 'value4',
            'subkey2-2': 'value5',
            'subkey2-3': 'value6',
        }
        result = combine_kwargs(key1=key1_dict, key2=key2_dict)

        assert isinstance(result, dict)
        expected_keys = [
            'key1[subkey1-1]',
            'key1[subkey1-2]',
            'key1[subkey1-3]',
            'key2[subkey2-1]',
            'key2[subkey2-2]',
            'key2[subkey2-3]'
        ]
        assert all(key in result for key in expected_keys)

    # obj_or_id()
    def test_obj_or_id_int(self):
        user_id = obj_or_id(1, 'user_id', (User,))

        assert isinstance(user_id, int)
        assert user_id == 1

    def test_obj_or_id_str_valid(self):
        user_id = obj_or_id("1", 'user_id', (User,))

        assert isinstance(user_id, int)
        assert user_id == 1

    def test_obj_or_id_str_invalid(self):
        with self.assertRaises(TypeError):
            obj_or_id("1a", 'user_id', (User,))

    def test_obj_or_id_obj(self):
        user = self.canvas.get_user(1)

        user_id = obj_or_id(user, 'user_id', (User,))

        assert isinstance(user_id, int)
        assert user_id == 1

    def test_obj_or_id_obj_no_id(self):
        nick = self.canvas.get_course_nickname(1)

        with self.assertRaises(TypeError):
            obj_or_id(nick, 'nickname_id', (CourseNickname,))
