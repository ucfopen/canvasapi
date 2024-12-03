import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.lti_resource_link import LTIResourceLink
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestLTIResourceLink(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"extended_course": ["get_by_id"]}, m)
            self.extended_course = self.canvas.get_course(1)

    # create_lti_resource_link()
    def test_create_lti_resource_link(self, m):
        register_uris({"lti_resource_link": ["create_lti_resource_link"]}, m)
        evnt = self.user.create_lti_resource_link(
            name="Test LTI Resource Link", url="https://www.google.com"
        )
        self.assertIsInstance(evnt, LTIResourceLink)
        self.assertEqual(evnt.name, "Test LTI Resource Link")
        self.assertEqual(evnt.url, "https://www.google.com")
 
    # get_lti_resource_links()
    def test_get_lti_resource_links(self, m):
        register_uris({"lti_resource_link": ["list_lti_resource_links"]}, m)

        lti_resource_links = self.extended_course.get_lti_resource_links()
        lti_resource_link_list = [link for link in lti_resource_links]
        self.assertEqual(len(lti_resource_link_list), 2)
        self.assertIsInstance(lti_resource_link_list[0], LTIResourceLink)

    # get_lti_resource_link()
    def test_get_lti_resource_link(self, m):
        register_uris({"lti_resource_link": ["get_lti_resource_link"]}, m)

        lti_resource_link_by_id = self.extended_course.get_lti_resource_link(45)
        self.assertIsInstance(lti_resource_link_by_id, LTIResourceLink)
        self.assertEqual(lti_resource_link_by_id.name, "Test LTI Resource Link 3")
        lti_resource_link_by_obj = self.extended_course.get_lti_resource_link(lti_resource_link_by_id)
        self.assertIsInstance(lti_resource_link_by_obj, LTIResourceLink)
        self.assertEqual(lti_resource_link_by_obj.name, "Test LTI Resource Link 3")
