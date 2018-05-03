import unittest
from canvasapi.canvas_object import CanvasObject
from canvasapi.folder import Folder
from canvasapi.util import combine_kwargs, obj_or_id
from tests.test_endpoint_docstrings import test_method
# from tests.test_endpoint_docstrings import test_methods


# test_endpoint_docstrings
class TestTestEndpointDocstrings(unittest.TestCase):
    def test_test_method(self):
        assert not test_method(ExampleMethods.fails_wrong_docstring_verb, True)
        assert not test_method(ExampleMethods.fails_invalid_docstring_verb, True)
        assert test_method(ExampleMethods.passes_no_api_call, True)
        assert test_method(ExampleMethods.passes_good_docstring, True)
        assert test_method(ExampleMethods.passes_multiple_endpoints, True)
        assert test_method(ExampleMethods.passes_multiline_URL, True)
        assert test_method(ExampleMethods.passes_calls_but_not_api, True)
        # test_methods()


class ExampleMethods(CanvasObject):
    def fails_wrong_docstring_verb(self):
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

    def passes_no_api_call(self):
        """
        Empty docstring.
        """
        return False

    def passes_good_docstring(self):
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

    def passes_multiple_endpoints(self, folder):
        """
        Return the details for a folder

        :calls: `GET /api/v1/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi.folder.Folder` or int

        :rtype: :class:`canvasapi.folder.Folder`
        """
        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self.__requester.request(
            'GET',
            'folders/{}'.format(folder_id)
        )
        return Folder(self.__requester, response.json())

    def fails_invalid_docstring_verb(self):
        """
        Delete this file.

        :calls: `BELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def passes_multiline_URL(self, **kwargs):
        """
        Fetch all preferences for the given communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/:communication_channel_id/ \
                notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            'GET',
            'users/{}/communication_channels/{}/notification_preferences'.format(
                self.user_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()['notification_preferences']

    def passes_calls_but_not_api():
        """
        Kick off uploading process. Handles open/closing file if a path
        is passed.

        :calls: request_upload_token
        :returns: True if the file uploaded successfully, False \
            otherwise, and the JSON response from the API.
        :rtype: tuple
        """
        pass
