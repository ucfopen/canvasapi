from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import warnings

from canvasapi.canvas_object import CanvasObject


class TestCanvasObject(unittest.TestCase):

    # to_json()
    def test_canvas_object_to_json(self):
        warnings.simplefilter("always", DeprecationWarning)

        with warnings.catch_warnings(record=True) as warning_list:
            attributes = {"name": "Test Object", "id": 1}
            canvas_obj = CanvasObject(None, attributes)

            prev_json = canvas_obj.to_json()
            self.assertIsInstance(prev_json, str)

            attributes.update({"name": "Test Object 2"})
            canvas_obj.set_attributes(attributes)

            self.assertNotEqual(canvas_obj.to_json(), prev_json)

        self.assertEqual(len(warning_list), 4)
        self.assertEqual(warning_list[0].category, DeprecationWarning)
        self.assertEqual(warning_list[1].category, DeprecationWarning)
        self.assertEqual(warning_list[2].category, DeprecationWarning)
        self.assertEqual(warning_list[3].category, DeprecationWarning)
