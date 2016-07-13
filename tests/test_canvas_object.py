import unittest

from pycanvas.canvas_object import CanvasObject


class TestCanvasObject(unittest.TestCase):
    """
    Test CanvasObject functionality.
    """

    # to_json()
    def test_canvas_object_to_json(self):
        attributes = {'name': 'Test Object', 'id': 1}
        canvas_obj = CanvasObject(None, attributes)

        prev_json = canvas_obj.to_json()
        assert isinstance(prev_json, str)

        attributes.update({'name': 'Test Object 2'})
        canvas_obj.set_attributes(attributes)

        assert canvas_obj.to_json() != prev_json
