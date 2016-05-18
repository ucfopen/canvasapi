
import unittest
import requests_mock
import settings

from pycanvas import Canvas
from pycanvas.role import Role
from pycanvas.account import Account
from util import register_uris


class TestRole(unittest.TestCase):
    """
    Tests Role methods.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': ['get_by_id','get_role'],
            'generic': ['not_found'],
            'user': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.account = self.canvas.get_account(1)
        self.role = self.account.get_role(2)

    # __str__()
    def test__str__(self):
        string = str(self.role)
        assert isinstance(string, str)
