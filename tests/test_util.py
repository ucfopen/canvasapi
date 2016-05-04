import unittest

from pycanvas.util import combine_kwargs, obj_or_id


class TestCourse(unittest.TestCase):
    """
    Tests utility methods
    """

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
    def test_obj_or_id(self):
        # TODO
        pass
