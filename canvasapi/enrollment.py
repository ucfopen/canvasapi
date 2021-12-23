from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Enrollment(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.type, self.id)

    def deactivate(self, task, **kwargs):
        """
        Delete, conclude, or deactivate an enrollment.

        The following tasks can be performed on an enrollment: conclude, delete, \
        inactivate, deactivate.

        :calls: `DELETE /api/v1/courses/:course_id/enrollments/:id \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.destroy>`_

        :param task: The task to perform on the enrollment.
        :type task: str
        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        ALLOWED_TASKS = ["conclude", "delete", "inactivate", "deactivate"]

        if task not in ALLOWED_TASKS:
            raise ValueError(
                "{} is not a valid task. Please use one of the following: {}".format(
                    task, ",".join(ALLOWED_TASKS)
                )
            )

        kwargs["task"] = task

        response = self._requester.request(
            "DELETE",
            "courses/{}/enrollments/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Enrollment(self._requester, response.json())

    def reactivate(self, **kwargs):
        """
        Activate an inactive enrollment.

        :calls: `PUT /api/v1/courses/:course_id/enrollments/:id/reactivate \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.reactivate>`_

        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/enrollments/{}/reactivate".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Enrollment(self._requester, response.json())
