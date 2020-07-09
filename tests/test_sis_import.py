import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.progress import Progress
from canvasapi.sis_import import SisImport
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSisImportGroup(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "account": ["get_by_id", "get_role"],
                "sis_import": ["get_by_id"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.sis_import = self.account.get_sis_import(2)

    # abort()
    def test_abort_sis_import(self, m):
        register_uris({"sis_import": ["abort_sis_import"]}, m)

        aborted_sis_import = self.sis_import.abort()

        self.assertIsInstance(aborted_sis_import, SisImport)

        self.assertTrue(
            aborted_sis_import.workflow_state == "aborted"
            if aborted_sis_import.progress < 100
            else True
        )

    # restore_states()
    def test_restore_states(self, m):
        register_uris({"sis_import": ["restore_sis_import_states"]}, m)

        restore_state_progress = self.sis_import.restore_states()

        self.assertIsInstance(restore_state_progress, Progress)
        self.assertEqual(restore_state_progress.context_id, self.sis_import.id)
        self.assertEqual(restore_state_progress.context_type, "SisBatch")
        self.assertEqual(restore_state_progress.tag, "sis_batch_state_restore")
