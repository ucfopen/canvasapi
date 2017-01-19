import unittest

import requests_mock

from pycanvas import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestDiscussionTopic(unittest.TestCase):

	@classmethod
	def setUp(self):
		self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

		with requests_mock.Mocker() as m:
			requires = {
				'course': ['get_by_id', 'get_discussion_topic']
			}
			register_uris(requires, m)

			self.course = self.canvas.get_course(1)
			self.discussion_topic = self.course.get_discussion_topic(1)

	def test__str__(self, m):
		string = str(self.discussion_topic)
		self.assertIsInstance(string, str)

	
		