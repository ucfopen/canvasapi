from pycanvas import CanvasObject


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
        return response

    def delete(self):
        """
        Permanently deletes the course.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="delete"
        )
        return response
