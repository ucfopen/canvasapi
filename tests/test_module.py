import unittest
import settings

import requests_mock
from pycanvas import Canvas
from pycanvas.exceptions import RequiredFieldMissing
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
        edited_module = self.module.edit(module={'name': name})

        assert isinstance(edited_module, Module)
        assert hasattr(edited_module, 'name')
        assert edited_module.name == name
        assert hasattr(edited_module, 'course_id')
        assert edited_module.course_id == self.course.id

    # delete()
    def test_delete_module(self):
        deleted_module = self.module.delete()

        assert isinstance(deleted_module, Module)
        assert hasattr(deleted_module, 'course_id')
        assert deleted_module.course_id == self.course.id

    #relock()
    def test_relock(self):
        relocked_module = self.module.relock()

        assert isinstance(relocked_module, Module)
        assert hasattr(relocked_module, 'course_id')
        assert relocked_module.course_id == self.course.id

    #list_module_items()
    def test_list_module_items(self):
        module_items = self.module.list_module_items()
        module_item_list = [module_item for module_item in module_items]

        assert len(module_item_list) == 4
        assert isinstance(module_item_list[0], ModuleItem)
        assert hasattr(module_item_list[0], 'course_id')
        assert module_item_list[0].course_id == self.course.id

    #get_module_item()
    def test_get_module_item(self):
        module_item = self.module.get_module_item(1)

        assert isinstance(module_item, ModuleItem)
        assert hasattr(module_item, 'course_id')
        assert module_item.course_id == self.course.id

    #create_module_item()
    def test_create_module_item(self):
        module_item = self.module.create_module_item(
            module_item={
                'type': 'Page',
                'content_id': 1
            }
        )
        assert isinstance(module_item, ModuleItem)
        assert hasattr(module_item, 'course_id')
        assert module_item.course_id == self.course.id

    def test_create_module_item_fail1(self):
        with self.assertRaises(RequiredFieldMissing):
            self.module.create_module_item(
                module_item={'content_id': 1}
            )

    def test_create_module_item_fail2(self):
        with self.assertRaises(RequiredFieldMissing):
            self.module.create_module_item(
                module_item={'type': 'Page'}
            )

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
        self.module_item = self.module.get_module_item(1)

    #edit()
    def test_edit_module_item(self):
        title = 'New Title'
        edited_module_item = self.module_item.edit(
            module_item={'title': title}
        )

        assert isinstance(edited_module_item, ModuleItem)
        assert hasattr(edited_module_item, 'title')
        assert edited_module_item.title == title
        assert hasattr(edited_module_item, 'course_id')
        assert edited_module_item.course_id == self.course.id

    #delete()
    def test_delete(self):
        deleted_module_item = self.module_item.delete()

        assert isinstance(deleted_module_item, ModuleItem)
        assert hasattr(deleted_module_item, 'course_id')
        assert deleted_module_item.course_id == self.course.id

    #complete(course_id, True)
    def test_complete(self):
        completed_module_item = self.module_item.complete()

        assert isinstance(completed_module_item, ModuleItem)
        assert hasattr(completed_module_item, 'completion_requirement')
        assert hasattr(completed_module_item, 'course_id')
        assert completed_module_item.course_id == self.course.id

    #complete(course_id, False)
    def test_uncomplete(self):
        completed_module_item = self.module_item.uncomplete()

        assert isinstance(completed_module_item, ModuleItem)
        assert hasattr(completed_module_item, 'completion_requirement')
        assert hasattr(completed_module_item, 'course_id')
        assert completed_module_item.course_id == self.course.id

    def test__str__(self):
        string = str(self.module_item)
        assert isinstance(string, str)
