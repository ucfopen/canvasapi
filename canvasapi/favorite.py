from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Favorite(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.context_type, self.context_id)

    def remove(self, **kwargs):
        """
        Remove a course or group from the current user's favorites.

        :calls: :Course: `DELETE /api/v1/users/self/favorites/courses/:id \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.remove_favorite_course>`_
                :Group: `DELETE /api/v1/users/self/favorites/groups/:id \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.remove_favorite_groups>`_

        :rtype: :class:`canvasapi.favorite.Favorite`
        """
        if self.context_type.lower() == "course":
            id = self.context_id
            uri_str = "users/self/favorites/courses/{}"

        elif self.context_type.lower() == "group":
            id = self.context_id
            uri_str = "users/self/favorites/groups/{}"

        response = self._requester.request(
            "DELETE", uri_str.format(id), _kwargs=combine_kwargs(**kwargs)
        )
        return Favorite(self._requester, response.json())
