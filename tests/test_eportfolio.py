import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.eportfolio import EPortfolio, EPortfolioPage
from canvasapi.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestEPortfolio(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"eportfolio": ["get_eportfolio_by_id"]}, m)

            self.eportfolio = self.canvas.get_eportfolio(1)

    def test_str(self, m):
        eportfolio_string = str(self.eportfolio)
        self.assertEqual(eportfolio_string, "ePortfolio 1")

    def test_delete_eportfolio(self, m):
        register_uris({"eportfolio": ["delete_eportfolio"]}, m)

        deleted_eportfolio = self.eportfolio.delete()

        self.assertIsInstance(deleted_eportfolio, EPortfolio)
        self.assertEqual(deleted_eportfolio.deleted_at, "2022-07-05T21:00:00Z")
        self.assertEqual(deleted_eportfolio.workflow_state, "deleted")

    def test_get_eportfolio_pages(self, m):
        register_uris({"eportfolio": ["get_eportfolio_pages"]}, m)

        pages = self.eportfolio.get_eportfolio_pages()

        string_page = str(pages[0])

        self.assertIsInstance(pages, PaginatedList)
        self.assertIsInstance(pages[0], EPortfolioPage)
        self.assertIsInstance(pages[1], EPortfolioPage)
        self.assertEqual(pages[0].position, 1)
        self.assertEqual(pages[1].position, 2)
        self.assertEqual(string_page, "1. ePortfolio 1")

    def test_moderate_eportfolio_as_spam(self, m):
        register_uris({"eportfolio": ["moderate_eportfolio_as_spam"]}, m)

        spam_eportfolio = self.eportfolio.moderate_eportfolio(
            spam_status="marked_as_spam"
        )

        self.assertIsInstance(spam_eportfolio, EPortfolio)
        self.assertEqual(spam_eportfolio.spam_status, "marked_as_spam")

    def test_restore_deleted_eportfolio(self, m):
        register_uris(
            {"eportfolio": ["delete_eportfolio", "restore_deleted_eportfolio"]}, m
        )

        eportfolio = self.eportfolio.delete()

        self.assertIsInstance(eportfolio, EPortfolio)
        self.assertEqual(eportfolio.workflow_state, "deleted")
        self.assertEqual(eportfolio.deleted_at, "2022-07-05T21:00:00Z")

        restored = eportfolio.restore()

        self.assertEqual(restored.workflow_state, "active")
        self.assertEqual(restored.deleted_at, "null")
