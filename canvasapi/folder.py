from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


class Folder(CanvasObject):

    def __str__(self):
        return str(self.full_name)

    def list_files(self, **kwargs):
        """
        Returns the paginated list of files for the folder.

        :calls: `GET api/v1/folders/:id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            'GET',
            'folders/%s/files' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def delete(self, **kwargs):
        """
        Remove this folder. You can only delete empty folders unless you set the
          'force' flag.

        :calls: `DELETE /api/v1/folders/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.api_destroy>`_

        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'DELETE',
            'folders/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def list_folders(self):
        """
        Returns the paginated list of folders in the folder.

        :calls: `GET /api/v1/folders/:id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        return PaginatedList(
            Folder,
            self._requester,
            'GET',
            'folders/%s/folders' % (self.id)
        )

    def create_folder(self, name, **kwargs):
        """
        Creates a folder within this folder.

        :calls: `POST /api/v1/folders/:folder_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

        :param name: The name of the folder.
        :type name: str
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'POST',
            'folders/%s/folders' % self.id,
            name=name,
            **combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def update(self, **kwargs):
        """
        Updates a folder.

        :calls: `PUT /api/v1/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.update>`_

        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'PUT',
            'folders/%s' % self.id,
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Folder, self).set_attributes(response.json())

        return Folder(self._requester, response.json())
