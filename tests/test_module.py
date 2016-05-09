import unittest
import settings

import requests_mock
from pycanvas import Canvas
from pycanvas.module import Module
from util import register_uris


class TestModule(unittest.TestCase):
    """
    Tests Module functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id', 'get_module_by_id'],
            'module': ['edit', 'delete', 'relock']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.module = self.course.get_module(1)

    # edit()
    def test_edit(self):
        name = 'New Name'
        edited_module = self.module.edit(self.course.id, module={'name': name})

        assert isinstance(edited_module, Module)
        assert hasattr(edited_module, 'name')
        assert edited_module.name == name

    # delete()
    def test_delete(self):
        deleted_module = self.module.delete(self.course.id)

        assert isinstance(deleted_module, Module)

    #relock()
    def test_relock(self):
        relocked_module = self.module.relock(self.course.id)

        assert isinstance(relocked_module, Module)
