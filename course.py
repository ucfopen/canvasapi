from pycanvas import CanvasObject
from pycanvas.util import combine_kwargs


class Course(CanvasObject):

    def conclude(self):
        """
        Marks the course as concluded.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="conclude"
        )
        response_json = response.json()
        return response_json.get('conclude', False)

    def delete(self):
        """
        Permanently deletes the course.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="delete"
        )
        response_json = response.json()
        return response_json.get('delete', False)

    def users(self, search_term=None, **kwargs):
        """
        Lists all users in a course.
        If a `search_term` is provided, only returns matching users
        """
        # TODO: Return user objects instead of just json
        response = self._requester.request(
            'GET',
            'courses/%s/search_users' % (self.id),
            search_term=search_term,
            **combine_kwargs(**kwargs)
        )
        return response.json()
