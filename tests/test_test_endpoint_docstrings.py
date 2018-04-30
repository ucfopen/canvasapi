import unittest
import requests_mock
from canvasapi.canvas_object import CanvasObject

from tests.test_endpoint_docstrings import test_methods

class TestTestEndpointDocstrings(unittest.TestCase):
    @requests_mock.Mocker()
    def test_test_methods(self, m):
        assert not test_methods(ExampleMethods.example_method_should_fail_online_documentation)
        assert not test_methods(ExampleMethods.example_method_should_fail_implementation_verb)
        assert not test_methods(ExampleMethods.example_method_should_fail_implementation_URL)
        assert test_methods(ExampleMethods.example_method_should_pass_no_api_call)
        assert test_methods(ExampleMethods.example_method_should_pass_all_correct)

class ExampleMethods(CanvasObject):
    def example_method_should_fail_online_documentation(self):
        """
        :calls: `DELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.wrong>`_

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
