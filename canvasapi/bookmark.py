from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Bookmark(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self, **kwargs):
        """
        Delete this bookmark.

        :calls: `DELETE /api/v1/users/self/bookmarks/:id \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.destroy>`_

        :rtype: :class:`canvasapi.bookmark.Bookmark`
        """
        response = self._requester.request(
            "DELETE",
            "users/self/bookmarks/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Bookmark(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify this bookmark.

        :calls: `PUT /api/v1/users/self/bookmarks/:id \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.update>`_

        :rtype: :class:`canvasapi.bookmark.Bookmark`
        """
        response = self._requester.request(
            "PUT",
            "users/self/bookmarks/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if "name" in response.json() and "url" in response.json():
            super(Bookmark, self).set_attributes(response.json())

        return Bookmark(self._requester, response.json())
