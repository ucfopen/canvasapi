import unittest
import warnings
from datetime import datetime

import pytz
import requests_mock

from canvasapi.canvas_object import CanvasObject
from canvasapi.requester import Requester
from tests import settings


@requests_mock.Mocker()
class TestCanvasObject(unittest.TestCase):
    def setUp(self):
        self.canvas_object = CanvasObject(
            Requester(settings.BASE_URL, settings.API_KEY), {}
        )

    # set_attributes
    def test_set_attributes_valid_date(self, m):
        attributes = {
            "start_at": "2012-05-05T00:00:00Z",
            "end_at": "2012-08-05",
            "offset_time": "2018-05-21T10:22:25+01:00",
            "half_offset": "2018-05-21T13:52:25+04:30",
            "big_offset_time": "2018-05-21T23:22:25+14:00",
            "big_offset_neg": "2018-05-20T23:22:25-10:00",
        }

        start_date = datetime.strptime(
            attributes["start_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=pytz.utc)
        end_date = datetime.strptime(attributes["end_at"], "%Y-%m-%d").replace(
            tzinfo=pytz.utc
        )
        offset_time = datetime.strptime(
            "2018-05-21T09:22:25Z", "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=pytz.utc)

        self.canvas_object.set_attributes(attributes)

        self.assertTrue(hasattr(self.canvas_object, "start_at_date"))
        self.assertEqual(self.canvas_object.start_at_date, start_date)
        self.assertTrue(hasattr(self.canvas_object, "end_at_date"))
        self.assertEqual(self.canvas_object.end_at_date, end_date)
        self.assertTrue(hasattr(self.canvas_object, "offset_time_date"))
        self.assertEqual(self.canvas_object.offset_time_date, offset_time)
        self.assertTrue(hasattr(self.canvas_object, "big_offset_time_date"))
        self.assertEqual(self.canvas_object.big_offset_time_date, offset_time)
        self.assertTrue(hasattr(self.canvas_object, "big_offset_neg_date"))
        self.assertEqual(self.canvas_object.big_offset_neg_date, offset_time)

        self.assertTrue(hasattr(self.canvas_object, "half_offset_date"))
        self.assertEqual(self.canvas_object.half_offset_date, offset_time)

    def test_set_attributes_invalid_date(self, m):
        attributes = {"start_at": "2017-01-01T00:00+00:00:00", "end_at": "2012-08-0"}

        self.canvas_object.set_attributes(attributes)

        self.assertFalse(hasattr(self.canvas_object, "start_at_date"))
        self.assertFalse(hasattr(self.canvas_object, "end_at_date"))
        self.assertTrue(hasattr(self.canvas_object, "start_at"))
        self.assertTrue(hasattr(self.canvas_object, "end_at"))

    # set_attributes 'content-type'
    def test_set_attributes_with_content_type(self, m):
        attributes = {
            "content-type": "application/json",
            "content_type": "another_application/json",
            "filename": "example.json",
        }

        self.canvas_object.set_attributes(attributes)

        self.assertTrue(hasattr(self.canvas_object, "content-type"))
        self.assertEqual(
            getattr(self.canvas_object, "content-type"), "application/json"
        )
        self.assertTrue(hasattr(self.canvas_object, "content_type"))
        self.assertEqual(self.canvas_object.content_type, "another_application/json")
        self.assertTrue(hasattr(self.canvas_object, "filename"))
        self.assertEqual(self.canvas_object.filename, "example.json")

    def test_set_attributes_with_content_type_reversed(self, m):
        # Reversed the order of the attributes to test overwrite behavior
        attributes = {
            "content_type": "another_application/json",
            "content-type": "application/json",
            "filename": "example.json",
        }

        self.canvas_object.set_attributes(attributes)

        self.assertTrue(hasattr(self.canvas_object, "content-type"))
        self.assertEqual(
            getattr(self.canvas_object, "content-type"), "application/json"
        )
        self.assertTrue(hasattr(self.canvas_object, "content_type"))
        self.assertEqual(self.canvas_object.content_type, "another_application/json")
        self.assertTrue(hasattr(self.canvas_object, "filename"))
        self.assertEqual(self.canvas_object.filename, "example.json")

    def test__getattribute__content_type_warns(self, m):
        attributes = {"content-type": "application/json"}
        self.canvas_object.set_attributes(attributes)

        warnings.simplefilter("always", DeprecationWarning)

        with warnings.catch_warnings(record=True) as warning_list:
            self.canvas_object.__getattribute__("content-type")

        self.assertEqual(len(warning_list), 1)
        self.assertEqual(warning_list[0].category, DeprecationWarning)
