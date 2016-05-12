import unittest
import settings

import requests_mock
from pycanvas import Canvas
from pycanvas.module import Module, ModuleItem
from util import register_uris


class TestModule(unittest.TestCase):
    """
    Tests Module functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id', 'get_module_by_id'],
            'module': [
                'edit', 'delete', 'relock', 'list_module_items',
                'list_module_items2', 'get_module_item_by_id', 'create_module_item',
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.module = self.course.get_module(1)

    # edit()
    def test_edit_module(self):
        name = 'New Name'
        edited_module = self.module.edit(self.course.id, module={'name': name})

        assert isinstance(edited_module, Module)
        assert hasattr(edited_module, 'name')
        assert edited_module.name == name

    # delete()
    def test_delete_module(self):
        deleted_module = self.module.delete(self.course.id)

        assert isinstance(deleted_module, Module)

    #relock()
    def test_relock(self):
        relocked_module = self.module.relock(self.course.id)

        assert isinstance(relocked_module, Module)

    #list_module_items()
    def test_list_module_items(self):
        module_items = self.module.list_module_items(self.course.id)
        module_item_list = [module_item for module_item in module_items]

        assert isinstance(module_item_list[0], ModuleItem)
        assert len(module_item_list) == 4

    #get_module_item()
    def test_get_module_item(self):
        module_item = self.module.get_module_item(1, 1)

        assert isinstance(module_item, ModuleItem)

    #create_module_item()
    def test_create_module_item(self):
        title = 'Module Item Name'
        module_item = self.module.create_module_item(self.course.id, module_item={'title': title})

        assert isinstance(module_item, ModuleItem)

    #__str__
    def test__str__(self):
        string = str(self.module)
        assert isinstance(string, str)


class TestModuleItem(unittest.TestCase):
    """
    Tests Module Item functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id', 'get_module_by_id'],
            'module': [
                'get_module_item_by_id', 'edit_module_item',
                'delete_module_item', 'complete_module_item',
                'uncomplete_module_item'
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.module = self.course.get_module(1)
        self.module_item = self.module.get_module_item(1, 1)

    #edit()
    def test_edit_module_item(self):
        title = 'New Title'
        edited_module_item = self.module_item.edit(self.module_item.id, module_item={'title': title})

        assert isinstance(edited_module_item, ModuleItem)
        assert hasattr(edited_module_item, 'title')
        assert edited_module_item.title == title

    #delete()
    def test_delete(self):
        deleted_module_item = self.module_item.delete(self.course.id)

        assert isinstance(deleted_module_item, ModuleItem)

    #complete(course_id, True)
    def test_complete(self):
        completed_module_item = self.module_item.completed(self.course.id, True)

        assert isinstance(completed_module_item, ModuleItem)
        assert hasattr(completed_module_item, 'completion_requirement')

    #complete(course_id, False)
    def test_uncomplete(self):
        completed_module_item = self.module_item.completed(self.course.id, False)

        assert isinstance(completed_module_item, ModuleItem)
        assert hasattr(completed_module_item, 'completion_requirement')

    def test__str__(self):
        string = str(self.module_item)
        assert isinstance(string, str)
