from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.upload import FileOrPathLike, Uploader
from canvasapi.util import combine_kwargs, obj_or_id


class Folder(CanvasObject):
    def __str__(self):
        return "{}".format(self.full_name)

    def copy_file(self, source_file, **kwargs):
        """
        Copies a file into the current folder.

        :calls: `POST /api/v1/folders/:dest_folder_id/copy_file \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.copy_file>`_

        :param source_file: The object or id of the source file.
        :type source_file: int or :class:`canvasapi.file.File`

        :rtype: :class:`canvasapi.folder.Folder`
        """
        from canvasapi.file import File

        file_id = obj_or_id(source_file, "source_file", (File,))
        kwargs["source_file_id"] = file_id

        response = self._requester.request(
            "POST",
            "folders/{}/copy_file".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return File(self._requester, response.json())

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
            "POST",
            "folders/{}/folders".format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs),
        )
        return Folder(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Remove this folder. You can only delete empty folders unless you set the
          'force' flag.

        :calls: `DELETE /api/v1/folders/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.api_destroy>`_

        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            "DELETE", "folders/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def get_files(self, **kwargs):
        """
        Returns the paginated list of files for the folder.

        :calls: `GET /api/v1/folders/:id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            "GET",
            "folders/{}/files".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_folders(self, **kwargs):
        """
        Returns the paginated list of folders in the folder.

        :calls: `GET /api/v1/folders/:id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        return PaginatedList(
            Folder, self._requester, "GET", "folders/{}/folders".format(self.id)
        )

    def update(self, **kwargs):
        """
        Updates a folder.

        :calls: `PUT /api/v1/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.update>`_

        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            "PUT", "folders/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if "name" in response.json():
            super(Folder, self).set_attributes(response.json())

        return Folder(self._requester, response.json())

    def upload(self, file: FileOrPathLike, **kwargs):
        """
        Upload a file to this folder.

        :calls: `POST /api/v1/folders/:folder_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        my_path = "folders/{}/files".format(self.id)
        return Uploader(self._requester, my_path, file, **kwargs).start()
