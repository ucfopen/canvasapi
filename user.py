from canvas_object import CanvasObject
from paginated_list import PaginatedList


class User(CanvasObject):

    def profile(self, **kwargs):
        """
        Get a user's profile.

        :calls: `GET /api/v1/user/:id <https://canvas.instructure.com/doc/api/users.html#method.profile.settings>`
        :rtype: :class:`pycanvas.user.User`
        """
        response = self._requester.request(
            'GET',
            'users/%s/profile' % (id)
        )
        return response.json()

    def get_page_views(self):
        """
        Get a user's pageviews.

        :calls: `GET /api/v1/users/:user_id/page_views <https://canvas.instructure.com/doc/api/users.html#method.page_views.index>`
        :rtype :class:`pycanvas.user.User`
        """
        from page_view import PageView

        return PaginatedList(
            PageView,
            self._requester,
            'GET',
            'users/%s/page_views' % (self.id)
        )

    def __str__(self):
        return "%s" % (self.name)
