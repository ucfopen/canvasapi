import unittest
import uuid
from itertools import chain

import requests_mock

from canvasapi import Canvas
from canvasapi.course import CourseNickname
from canvasapi.user import User
from canvasapi.util import (
    clean_headers,
    combine_kwargs,
    file_or_path,
    get_institution_url,
    is_multivalued,
    normalize_bool,
    obj_or_id,
    obj_or_str,
)
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestUtil(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

    # is_multivalued()
    def test_is_multivalued_bool(self, m):
        self.assertFalse(is_multivalued(False))

    def test_is_multivalued_integer(self, m):
        self.assertFalse(is_multivalued(int(1)))

    def test_is_multivalued_str(self, m):
        self.assertFalse(is_multivalued("string"))

    def test_is_multivalued_unicode(self, m):
        self.assertFalse(is_multivalued("unicode"))

    def test_is_multivalued_bytes(self, m):
        self.assertFalse(is_multivalued(b"bytes"))

    def test_is_multivalued_list(self, m):
        self.assertTrue(is_multivalued(["item"]))

    def test_is_multivalued_list_iter(self, m):
        self.assertTrue(is_multivalued(iter(["item"])))

    def test_is_multivalued_tuple(self, m):
        self.assertTrue(is_multivalued(("item",)))

    def test_is_multivalued_tuple_iter(self, m):
        self.assertTrue(is_multivalued(iter(("item",))))

    def test_is_multivalued_set(self, m):
        self.assertTrue(is_multivalued({"element"}))

    def test_is_multivalued_set_iter(self, m):
        self.assertTrue(is_multivalued(iter({"element"})))

    def test_is_multivalued_dict(self, m):
        self.assertTrue(is_multivalued({"key": "value"}))

    def test_is_multivalued_dict_iter(self, m):
        self.assertTrue(is_multivalued(iter({"key": "value"})))

    def test_is_multivalued_dict_keys(self, m):
        self.assertTrue(is_multivalued({"key": "value"}.keys()))

    def test_is_multivalued_dict_values(self, m):
        self.assertTrue(is_multivalued({"key": "value"}.values()))

    def test_is_multivalued_dict_items(self, m):
        self.assertTrue(is_multivalued({"key": "value"}.items()))

    def test_is_multivalued_generator_expr(self, m):
        self.assertTrue(is_multivalued(item for item in ("item",)))

    def test_is_multivalued_generator_call(self, m):
        def yielder():
            yield "item"

        self.assertTrue(is_multivalued(yielder()))

    def test_is_multivalued_chain(self, m):
        self.assertTrue(is_multivalued(chain((1,), (2,))))

    def test_is_multivalued_zip(self, m):
        self.assertTrue(is_multivalued(zip((1,), (2,))))

    # combine_kwargs()
    def test_combine_kwargs_empty(self, m):
        result = combine_kwargs()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_combine_kwargs_single(self, m):
        result = combine_kwargs(var="test")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("var", "test"), result)

    def test_combine_kwargs_single_dict(self, m):
        result = combine_kwargs(var={"foo": "bar"})
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("var[foo]", "bar"), result)

    def test_combine_kwargs_single_list_empty(self, m):
        result = combine_kwargs(var=[])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_combine_kwargs_single_list_single_item(self, m):
        result = combine_kwargs(var=["test"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("var[]", "test"), result)

    def test_combine_kwargs_single_list_multiple_items(self, m):
        result = combine_kwargs(foo=["bar1", "bar2", "bar3", "bar4"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)

        self.assertIn(("foo[]", "bar1"), result)
        self.assertIn(("foo[]", "bar2"), result)
        self.assertIn(("foo[]", "bar3"), result)
        self.assertIn(("foo[]", "bar4"), result)

        # Ensure kwargs are in correct order
        self.assertTrue(
            result.index(("foo[]", "bar1"))
            < result.index(("foo[]", "bar2"))
            < result.index(("foo[]", "bar3"))
            < result.index(("foo[]", "bar4"))
        )

    def test_combine_kwargs_single_generator_empty(self, m):
        result = combine_kwargs(var=(value for value in ()))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_combine_kwargs_single_generator_single_item(self, m):
        result = combine_kwargs(var=(value for value in ("test",)))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("var[]", "test"), result)

    def test_combine_kwargs_single_generator_multiple_items(self, m):
        result = combine_kwargs(
            foo=(value for value in ("bar1", "bar2", "bar3", "bar4"))
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)

        self.assertIn(("foo[]", "bar1"), result)
        self.assertIn(("foo[]", "bar2"), result)
        self.assertIn(("foo[]", "bar3"), result)
        self.assertIn(("foo[]", "bar4"), result)

        # Ensure kwargs are in correct order
        self.assertTrue(
            result.index(("foo[]", "bar1"))
            < result.index(("foo[]", "bar2"))
            < result.index(("foo[]", "bar3"))
            < result.index(("foo[]", "bar4"))
        )

    def test_combine_kwargs_multiple_dicts(self, m):
        result = combine_kwargs(var1={"foo": "bar"}, var2={"fizz": "buzz"})
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        self.assertIn(("var1[foo]", "bar"), result)
        self.assertIn(("var2[fizz]", "buzz"), result)

    def test_combine_kwargs_multiple_mixed(self, m):
        result = combine_kwargs(
            var1=True,
            var2={"fizz": "buzz"},
            var3="foo",
            var4=42,
            var5=["test1", "test2", "test3"],
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 7)

        self.assertIn(("var1", True), result)
        self.assertIn(("var2[fizz]", "buzz"), result)
        self.assertIn(("var3", "foo"), result)
        self.assertIn(("var4", 42), result)
        self.assertIn(("var5[]", "test1"), result)
        self.assertIn(("var5[]", "test2"), result)
        self.assertIn(("var5[]", "test3"), result)

        # Ensure list kwargs are in correct order
        self.assertTrue(
            result.index(("var5[]", "test1"))
            < result.index(("var5[]", "test2"))
            < result.index(("var5[]", "test3"))
        )

    def test_combine_kwargs_nested_dict(self, m):
        result = combine_kwargs(dict={"key": {"subkey": "value"}})
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        self.assertIn(("dict[key][subkey]", "value"), result)

    def test_combine_kwargs_multiple_nested_dicts(self, m):
        result = combine_kwargs(
            dict1={
                "key1": {"subkey1-1": "value1-1", "subkey1-2": "value1-2"},
                "key2": {"subkey2-1": "value2-1", "subkey2-2": "value2-2"},
            },
            dict2={
                "key1": {"subkey1-1": "value1-1", "subkey1-2": "value1-2"},
                "key2": {"subkey2-1": "value2-1", "subkey2-2": "value2-2"},
            },
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 8)

        self.assertIn(("dict1[key1][subkey1-1]", "value1-1"), result)
        self.assertIn(("dict1[key1][subkey1-2]", "value1-2"), result)
        self.assertIn(("dict1[key2][subkey2-1]", "value2-1"), result)
        self.assertIn(("dict1[key2][subkey2-2]", "value2-2"), result)
        self.assertIn(("dict2[key1][subkey1-1]", "value1-1"), result)
        self.assertIn(("dict2[key1][subkey1-2]", "value1-2"), result)
        self.assertIn(("dict2[key2][subkey2-1]", "value2-1"), result)
        self.assertIn(("dict2[key2][subkey2-2]", "value2-2"), result)

    def test_combine_kwargs_super_nested_dict(self, m):
        result = combine_kwargs(
            big_dict={"a": {"b": {"c": {"d": {"e": "We need to go deeper"}}}}}
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("big_dict[a][b][c][d][e]", "We need to go deeper"), result)

    def test_combine_kwargs_dict_list_dict(self, m):
        result = combine_kwargs(
            dict_list_dict={
                "key1": [{"subkey1a": "value1a"}, {"subkey1b": "value1b"}],
                "key2": [{"subkey2a": ["value2a1", "value2a2"]}],
            }
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        self.assertIn(("dict_list_dict[key1][][subkey1a]", "value1a"), result)
        self.assertIn(("dict_list_dict[key1][][subkey1b]", "value1b"), result)
        self.assertIn(("dict_list_dict[key2][][subkey2a][]", "value2a1"), result)
        self.assertIn(("dict_list_dict[key2][][subkey2a][]", "value2a2"), result)

    def test_combine_kwargs_the_gauntlet(self, m):
        result = combine_kwargs(
            foo="bar",
            fb={3: "fizz", 5: "buzz", 15: "fizzbuzz"},
            true=False,
            life=42,
            basic_list=["foo", "bar"],
            days_of_xmas={
                "first": {1: "partridge in a pear tree"},
                "second": {1: "partridge in a pear tree", "2": "turtle doves"},
                "third": {
                    1: "partridge in a pear tree",
                    "2": "turtle doves",
                    3: "french hens",
                },
                "fourth": {
                    1: "partridge in a pear tree",
                    "2": "turtle doves",
                    3: "french hens",
                    "4": "mocking birds",
                },
                "fifth": {
                    1: "partridge in a pear tree",
                    "2": "turtle doves",
                    3: "french hens",
                    "4": "mocking birds",
                    "5": "GOLDEN RINGS",
                },
            },
            super_nest={"1": {"2": {"3": {"4": {"5": {"6": "tada"}}}}}},
            list_dicts=[
                {"l_d1a": "val1a", "l_d1b": "val1b"},
                {"l_d2a": "val2a", "l_d2b": "val2b"},
            ],
            nest_list=[["1a", "1b"], ["2a", "2b"], ["3a", "3b"]],
            generator=(v for v in ("g1", "g2", "g3")),
            dict_list={"key": ["item1", "item2"]},
            dict_list_dict={
                "key1": [{"subkey1a": "value1a"}, {"subkey1b": "value1b"}],
                "key2": [{"subkey2a": "value2a"}, {"subkey2b": "value2b"}],
            },
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 43)

        # Check that all keys were generated correctly
        self.assertIn(("foo", "bar"), result)
        self.assertIn(("fb[3]", "fizz"), result)
        self.assertIn(("fb[5]", "buzz"), result)
        self.assertIn(("fb[15]", "fizzbuzz"), result)
        self.assertIn(("true", False), result)
        self.assertIn(("life", 42), result)
        self.assertIn(("basic_list[]", "foo"), result)
        self.assertIn(("basic_list[]", "bar"), result)
        self.assertIn(("days_of_xmas[first][1]", "partridge in a pear tree"), result)
        self.assertIn(("days_of_xmas[second][1]", "partridge in a pear tree"), result)
        self.assertIn(("days_of_xmas[second][2]", "turtle doves"), result)
        self.assertIn(("days_of_xmas[third][1]", "partridge in a pear tree"), result)
        self.assertIn(("days_of_xmas[third][2]", "turtle doves"), result)
        self.assertIn(("days_of_xmas[third][3]", "french hens"), result)
        self.assertIn(("days_of_xmas[fourth][1]", "partridge in a pear tree"), result)
        self.assertIn(("days_of_xmas[fourth][2]", "turtle doves"), result)
        self.assertIn(("days_of_xmas[fourth][3]", "french hens"), result)
        self.assertIn(("days_of_xmas[fourth][4]", "mocking birds"), result)
        self.assertIn(("days_of_xmas[fifth][1]", "partridge in a pear tree"), result)
        self.assertIn(("days_of_xmas[fifth][2]", "turtle doves"), result)
        self.assertIn(("days_of_xmas[fifth][3]", "french hens"), result)
        self.assertIn(("days_of_xmas[fifth][4]", "mocking birds"), result)
        self.assertIn(("days_of_xmas[fifth][5]", "GOLDEN RINGS"), result)
        self.assertIn(("super_nest[1][2][3][4][5][6]", "tada"), result)
        self.assertIn(("list_dicts[][l_d1b]", "val1b"), result)
        self.assertIn(("list_dicts[][l_d1a]", "val1a"), result)
        self.assertIn(("list_dicts[][l_d2b]", "val2b"), result)
        self.assertIn(("list_dicts[][l_d2a]", "val2a"), result)
        self.assertIn(("nest_list[][]", "1a"), result)
        self.assertIn(("nest_list[][]", "1b"), result)
        self.assertIn(("nest_list[][]", "2a"), result)
        self.assertIn(("nest_list[][]", "2b"), result)
        self.assertIn(("nest_list[][]", "3a"), result)
        self.assertIn(("nest_list[][]", "3b"), result)
        self.assertIn(("generator[]", "g1"), result)
        self.assertIn(("generator[]", "g2"), result)
        self.assertIn(("generator[]", "g3"), result)
        self.assertIn(("dict_list[key][]", "item1"), result)
        self.assertIn(("dict_list[key][]", "item2"), result)
        self.assertIn(("dict_list_dict[key1][][subkey1a]", "value1a"), result)
        self.assertIn(("dict_list_dict[key1][][subkey1b]", "value1b"), result)
        self.assertIn(("dict_list_dict[key2][][subkey2a]", "value2a"), result)
        self.assertIn(("dict_list_dict[key2][][subkey2b]", "value2b"), result)

        # Ensure list kwargs are in correct order
        self.assertTrue(
            result.index(("basic_list[]", "foo"))
            < result.index(("basic_list[]", "bar"))
        )
        self.assertTrue(
            result.index(("list_dicts[][l_d1a]", "val1a"))
            < result.index(("list_dicts[][l_d2a]", "val2a"))
        )
        self.assertTrue(
            result.index(("list_dicts[][l_d1b]", "val1b"))
            < result.index(("list_dicts[][l_d2b]", "val2b"))
        )
        self.assertTrue(
            result.index(("nest_list[][]", "1a"))
            < result.index(("nest_list[][]", "1b"))
            < result.index(("nest_list[][]", "2a"))
            < result.index(("nest_list[][]", "2b"))
            < result.index(("nest_list[][]", "3a"))
            < result.index(("nest_list[][]", "3b"))
        )
        self.assertTrue(
            result.index(("generator[]", "g1"))
            < result.index(("generator[]", "g2"))
            < result.index(("generator[]", "g3"))
        )
        self.assertTrue(
            result.index(("dict_list[key][]", "item1"))
            < result.index(("dict_list[key][]", "item2"))
        )

    # obj_or_id()
    def test_obj_or_id_int(self, m):
        user_id = obj_or_id(1, "user_id", (User,))

        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, 1)

    def test_obj_or_id_str_valid(self, m):
        user_id = obj_or_id("1", "user_id", (User,))

        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, 1)

    def test_obj_or_id_str_invalid(self, m):
        with self.assertRaises(TypeError):
            obj_or_id("1a", "user_id", (User,))

    def test_obj_or_id_obj(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user = self.canvas.get_user(1)

        user_id = obj_or_id(user, "user_id", (User,))

        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, 1)

    def test_obj_or_id_obj_no_id(self, m):
        register_uris({"user": ["course_nickname"]}, m)

        nick = self.canvas.get_course_nickname(1)

        with self.assertRaises(TypeError):
            obj_or_id(nick, "nickname_id", (CourseNickname,))

    def test_obj_or_id_multiple_objs(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user = self.canvas.get_user(1)

        user_id = obj_or_id(user, "user_id", (CourseNickname, User))

        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, 1)

    def test_obj_or_id_user_self(self, m):
        user_id = obj_or_id("self", "user_id", (User,))

        self.assertIsInstance(user_id, str)
        self.assertEqual(user_id, "self")

    def test_obj_or_id_nonuser_self(self, m):
        with self.assertRaises(TypeError):
            obj_or_id("self", "user_id", (CourseNickname,))

    # obj_or_str()
    def test_obj_or_str_obj_attr(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user = self.canvas.get_user(1)

        user_name = obj_or_str(user, "name", (User,))

        self.assertIsInstance(user_name, str)
        self.assertEqual(user_name, "John Doe")

    def test_obj_or_str_obj_no_attr(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user = self.canvas.get_user(1)

        with self.assertRaises(AttributeError):
            obj_or_str(user, "display_name", (User,))

    def test_obj_or_str_mult_obj(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user = self.canvas.get_user(1)

        user_name = obj_or_str(user, "name", (CourseNickname, User))

        self.assertIsInstance(user_name, str)

    def test_obj_or_str_invalid_attr_parameter(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user = self.canvas.get_user(1)

        with self.assertRaises(TypeError):
            obj_or_str(user, user, (User,))

    def test_obj_or_str_invalid_obj_type(self, m):
        with self.assertRaises(TypeError):
            obj_or_str("user", "name", (User,))

    # get_institution_url()
    def test_get_institution_url(self, m):
        correct_url = "https://my.canvas.edu"

        # strip trailing slash
        self.assertEqual(get_institution_url("https://my.canvas.edu/"), correct_url)
        # strip trailing slash but keep path
        self.assertEqual(
            get_institution_url("https://my.canvas.edu/test/2/"),
            correct_url + "/test/2",
        )
        # strip whitespace
        self.assertEqual(get_institution_url(" https://my.canvas.edu "), correct_url)
        # strip whitespace and trailing slash
        self.assertEqual(get_institution_url(" https://my.canvas.edu/ "), correct_url)

    # file_or_path()
    def test_file_or_path_file(self, m):
        filename = "testfile_file_or_path_file_{}".format(uuid.uuid4().hex)

        try:
            # create file and pass it in directly
            with open(filename, "w+") as file:
                handler, is_path = file_or_path(file)

                self.assertFalse(is_path)
        finally:
            cleanup_file(filename)

    def test_file_or_path_valid_path(self, m):
        filename = "testfile_file_or_path_valid_path_{}".format(uuid.uuid4().hex)

        try:
            # create file and immediately close it
            open(filename, "w+").close()

            handler, is_path = file_or_path(filename)
            self.assertTrue(is_path)

            # close re-opened file
            handler.close()
        finally:
            cleanup_file(filename)

    def test_file_or_path_invalid_path(self, m):
        filename = "testfile_file_or_path_invalid_path_{}".format(uuid.uuid4().hex)

        # intentionally do not create file

        with self.assertRaises(IOError):
            handler, is_path = file_or_path(filename)

    # normalize_bool()
    def test_normalize_bool_boolean(self, m):
        self.assertTrue(normalize_bool(True, "value"))
        self.assertFalse(normalize_bool(False, "value"))

    def test_normalize_bool_str_lower(self, m):
        self.assertTrue(normalize_bool("true", "value"))
        self.assertFalse(normalize_bool("false", "value"))

    def test_normalize_bool_str_upper(self, m):
        self.assertTrue(normalize_bool("True", "value"))
        self.assertFalse(normalize_bool("False", "value"))

    def test_normalize_bool_str_invalid(self, m):
        with self.assertRaises(ValueError) as cm:
            normalize_bool("invalid", "value")

        self.assertIn("Parameter `value` must", cm.exception.args[0])

    # clean_headers()
    def test_clean_headers_no_authorization(self, m):
        headers = {"Content-Type": "application/json"}

        self.assertEqual(clean_headers(headers), headers)

    def test_clean_headers_authorization_stripped(self, m):
        headers = {
            "Authorization": "Bearer SOMETOKEN1234",
            "Content-Type": "application/json",
        }

        cleaned_headers = clean_headers(headers)
        cleaned_authorization_header = cleaned_headers["Authorization"]
        self.assertEqual(cleaned_authorization_header, "****1234")
        self.assertEqual(cleaned_headers["Content-Type"], "application/json")

    def test_clean_headers_does_not_mutate_original_dict(self, m):
        headers = {
            "Authorization": "Bearer SOMETOKEN1234",
            "Content-Type": "application/json",
        }

        cleaned_headers = clean_headers(headers)
        self.assertIsNot(cleaned_headers, headers)

    def test_clean_headers_strips_malformed_keys_correctly(self, m):
        headers = {"Authorization": "Bearer  123,45"}

        cleaned_headers = clean_headers(headers)
        self.assertEqual(cleaned_headers["Authorization"], "****3,45")
