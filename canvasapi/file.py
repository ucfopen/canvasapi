from canvasapi.canvas_object import CanvasObject


class File(CanvasObject):

    def __str__(self):
        return str(self.display_name)

    def delete(self):
        """
        Delete this file.

        :calls: `DELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/%s' % (self.id)
        )
        return File(self._requester, response.json())
