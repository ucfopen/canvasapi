import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas import Canvas
from pycanvas.role import Role


class TestAccount(unittest.TestCase):
    """
    Tests core Account functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': ['get_by_id', 'get_role', 'list_roles', 'list_roles_2'],
            'generic': ['not_found']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.account = self.canvas.get_account(1)

    def test_list_roles(self):
        roles = self.account.list_roles()
        role_list = [role for role in roles]

        assert len(role_list) == 4
        assert isinstance(role_list[0], Role)

    def test_get_role(self):
        target_role = self.account.get_role(1, 2)

        assert isinstance(target_role, Role)
