from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from canvasapi.canvas_object import CanvasObject


class TestCanvasObject(unittest.TestCase):

    # to_json()
    def test_canvas_object_to_json(self):
        attributes = {"name": "Test Object", "id": 1}
        canvas_obj = CanvasObject(None, attributes)

        prev_json = canvas_obj.to_json()
        self.assertIsInstance(prev_json, str)

        attributes.update({"name": "Test Object 2"})
        canvas_obj.set_attributes(attributes)

        self.assertNotEqual(canvas_obj.to_json(), prev_json)
