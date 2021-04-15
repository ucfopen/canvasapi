import unittest

import requests_mock
import pytz
from datetime import datetime
from canvasapi.canvas_object import CanvasObject
from canvasapi.requester import Requester
from tests import settings

from dateutil import parser


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

        time_1 = parser.isoparse(attributes["offset_time"])
        time_2 = parser.isoparse("2018-05-21T09:22:25Z")

        print(time_1.utcoffset())
        print(time_2)

        self.canvas_object.set_attributes(attributes)

        self.assertTrue(hasattr(self.canvas_object, "start_at_date"))
        self.assertEqual(self.canvas_object.start_at_date, start_date)
        self.assertTrue(hasattr(self.canvas_object, "end_at_date"))
        self.assertEqual(self.canvas_object.end_at_date, end_date)
        self.assertTrue(hasattr(self.canvas_object, "offset_time"))
        self.assertEqual(self.canvas_object.offset_time_date, offset_time)

    def test_set_attributes_invalid_date(self, m):
        attributes = {"start_at": "2017-01-01T00:00+00:00:00", "end_at": "2012-08-0"}

        self.canvas_object.set_attributes(attributes)

        self.assertFalse(hasattr(self.canvas_object, "start_at_date"))
        self.assertFalse(hasattr(self.canvas_object, "end_at_date"))
        self.assertTrue(hasattr(self.canvas_object, "start_at"))
        self.assertTrue(hasattr(self.canvas_object, "end_at"))
