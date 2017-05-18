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
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`

        :rtype :class:`canvasapi.paginated_list.PaginatedList` of
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
