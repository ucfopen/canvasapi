import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.course import CourseNickname
from pycanvas.user import User
from pycanvas.util import combine_kwargs, obj_or_id
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestUtil(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

    # combine_kwargs()
    def test_combine_kwargs_empty(self, m):

        result = combine_kwargs()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_combine_kwargs_single(self, m):
        result = combine_kwargs(var='test')
        self.assertIsInstance(result, dict)
        self.assertTrue('var' in result)
        self.assertEqual(result['var'], 'test')

    def test_combine_kwargs_single_dict(self, m):
        result = combine_kwargs(var={'foo': 'bar'})
        self.assertIsInstance(result, dict)
        self.assertTrue('var[foo]' in result)
        self.assertEqual(result['var[foo]'], 'bar')

    def test_combine_kwargs_multiple_dicts(self, m):
        result = combine_kwargs(
            var1={'foo': 'bar'},
            var2={'fizz': 'buzz'}
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)

        self.assertIn('var1[foo]', result)
        self.assertEqual(result['var1[foo]'], 'bar')

        self.assertIn('var2[fizz]', result)
        self.assertEqual(result['var2[fizz]'], 'buzz')

    def test_combine_kwargs_multiple_mixed(self, m):
        result = combine_kwargs(
            var1=True,
            var2={'fizz': 'buzz'},
            var3='foo',
            var4=42,
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 4)

        expected_keys = ['var1', 'var2[fizz]', 'var3', 'var4']
        self.assertTrue(all(key in result for key in expected_keys))

        self.assertEqual(result['var1'], True)
        self.assertEqual(result['var2[fizz]'], 'buzz')
        self.assertEqual(result['var3'], 'foo')
        self.assertEqual(result['var4'], 42)

    def test_combine_kwargs_nested_dict(self, m):
        result = combine_kwargs(dict={
            'key': {'subkey': 'value'}
        })
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)

        self.assertIn('dict[key][subkey]', result)
        self.assertEqual(result['dict[key][subkey]'], 'value')

    def test_combine_kwargs_multiple_nested_dicts(self, m):
        result = combine_kwargs(
            dict1={
                'key1': {
                    'subkey1-1': 'value1-1',
                    'subkey1-2': 'value1-2'
                },
                'key2': {
                    'subkey2-1': 'value2-1',
                    'subkey2-2': 'value2-2'
                }
            },
            dict2={
                'key1': {
                    'subkey1-1': 'value1-1',
                    'subkey1-2': 'value1-2'
                },
                'key2': {
                    'subkey2-1': 'value2-1',
                    'subkey2-2': 'value2-2'
                }
            }
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 8)

        expected_keys = [
            'dict1[key1][subkey1-1]',
            'dict1[key1][subkey1-2]',
            'dict1[key2][subkey2-1]',
            'dict1[key2][subkey2-2]',
            'dict2[key1][subkey1-1]',
            'dict2[key1][subkey1-2]',
            'dict2[key2][subkey2-1]',
            'dict2[key2][subkey2-2]',
        ]
        self.assertTrue(all(key in result for key in expected_keys))

        self.assertEqual(result['dict1[key1][subkey1-1]'], 'value1-1')
        self.assertEqual(result['dict1[key1][subkey1-2]'], 'value1-2')
        self.assertEqual(result['dict1[key2][subkey2-1]'], 'value2-1')
        self.assertEqual(result['dict1[key2][subkey2-2]'], 'value2-2')
        self.assertEqual(result['dict2[key1][subkey1-1]'], 'value1-1')
        self.assertEqual(result['dict2[key1][subkey1-2]'], 'value1-2')
        self.assertEqual(result['dict2[key2][subkey2-1]'], 'value2-1')
        self.assertEqual(result['dict2[key2][subkey2-2]'], 'value2-2')

    def test_combine_kwargs_super_nested_dict(self, m):
        result = combine_kwargs(
            big_dict={'a': {'b': {'c': {'d': {'e': 'We need to go deeper'}}}}}
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)
        self.assertIn('big_dict[a][b][c][d][e]', result)
        self.assertEqual(result['big_dict[a][b][c][d][e]'], 'We need to go deeper')

    def test_combine_kwargs_the_gauntlet(self, m):
        result = combine_kwargs(
            foo='bar',
            fb={
                3: 'fizz',
                5: 'buzz',
                15: 'fizzbuzz'
            },
            true=False,
            life=42,
            days_of_xmas={
                'first': {
                    1: 'partridge in a pear tree'
                },
                'second': {
                    1: 'partridge in a pear tree',
                    '2': 'turtle doves',
                },
                'third': {
                    1: 'partridge in a pear tree',
                    '2': 'turtle doves',
                    3: 'french hens'
                },
                'fourth': {
                    1: 'partridge in a pear tree',
                    '2': 'turtle doves',
                    3: 'french hens',
                    '4': 'mocking birds',
                },
                'fifth': {
                    1: 'partridge in a pear tree',
                    '2': 'turtle doves',
                    3: 'french hens',
                    '4': 'mocking birds',
                    '5': 'GOLDEN RINGS'
                }
            },
            super_nest={'1': {'2': {'3': {'4': {'5': {'6': 'tada'}}}}}}
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 22)

        expected_keys = [
            'foo',
            'fb[3]',
            'fb[5]',
            'fb[15]',
            'true',
            'life',
            'days_of_xmas[first][1]',
            'days_of_xmas[second][1]',
            'days_of_xmas[second][2]',
            'days_of_xmas[third][1]',
            'days_of_xmas[third][2]',
            'days_of_xmas[third][3]',
            'days_of_xmas[fourth][1]',
            'days_of_xmas[fourth][2]',
            'days_of_xmas[fourth][3]',
            'days_of_xmas[fourth][4]',
            'days_of_xmas[fifth][1]',
            'days_of_xmas[fifth][2]',
            'days_of_xmas[fifth][3]',
            'days_of_xmas[fifth][4]',
            'days_of_xmas[fifth][5]',
            'super_nest[1][2][3][4][5][6]'
        ]

        self.assertTrue(all(key in result for key in expected_keys))

    # obj_or_id()
    def test_obj_or_id_int(self, m):
        user_id = obj_or_id(1, 'user_id', (User,))

        assert isinstance(user_id, int)
        assert user_id == 1

    def test_obj_or_id_str_valid(self, m):
        user_id = obj_or_id("1", 'user_id', (User,))

        assert isinstance(user_id, int)
        assert user_id == 1

    def test_obj_or_id_str_invalid(self, m):
        with self.assertRaises(TypeError):
            obj_or_id("1a", 'user_id', (User,))

    def test_obj_or_id_obj(self, m):
        register_uris({'user': ['get_by_id']}, m)

        user = self.canvas.get_user(1)

        user_id = obj_or_id(user, 'user_id', (User,))

        assert isinstance(user_id, int)
        assert user_id == 1

    def test_obj_or_id_obj_no_id(self, m):
        register_uris({'user': ['course_nickname']}, m)

        nick = self.canvas.get_course_nickname(1)

        with self.assertRaises(TypeError):
            obj_or_id(nick, 'nickname_id', (CourseNickname,))
