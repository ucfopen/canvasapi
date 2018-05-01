import unittest
import requests_mock
from canvasapi.canvas_object import CanvasObject

from tests.test_endpoint_docstrings import test_method, test_methods

class TestTestEndpointDocstrings(unittest.TestCase):
    def test_test_method(self):
        assert not test_method(ExampleMethods.example_method_should_fail_online_documentation, True)
        #assert not test_method(ExampleMethods.example_method_should_fail_implementation_verb, True)
        #assert not test_method(ExampleMethods.example_method_should_fail_implementation_URL, True)
        assert test_method(ExampleMethods.example_method_should_pass_no_api_call, True)
        assert test_method(ExampleMethods.example_method_should_pass_all_correct, True)
        test_methods()

class ExampleMethods(CanvasObject):
    def example_method_should_fail_online_documentation(self):
        """
        :calls: `PUT /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def example_method_should_fail_implementation_verb(self):
        """
        Delete this file.

        :calls: `DELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'POST',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def example_method_should_fail_implementation_URL(self):
        """
        Delete this file.

        :calls: `DELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'fils/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def example_method_should_pass_no_api_call(self):
        """
        Empty docstring.
        """
        return False

    def example_method_should_pass_all_correct(self):
        """
        Delete this file.

        :calls: `DELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())
