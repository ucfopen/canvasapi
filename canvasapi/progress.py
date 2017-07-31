from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class Progress(CanvasObject):

    def __str__(self):
        return "{} - {} ({})".format(self.tag, self.workflow_state, self.id)

    def query(self):
        """
        Return completion and status information about an asynchronous job.

        :calls: `GET /api/v1/progress/:id \
        <https://canvas.instructure.com/doc/api/progress.html#method.progress.show>`_

        :rtype: :class:`canvasapi.progress.Progress`
        """
        response = self._requester.request(
            'GET',
            'progress/%s' % (self.id)
        )
        response_json = response.json()

        super(Progress, self).set_attributes(response_json)

        return Progress(self._requester, response_json)
