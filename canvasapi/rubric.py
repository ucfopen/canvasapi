from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Rubric(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)


class RubricAssociation(CanvasObject):
    def __str__(self):
        return "{}, {}".format(self.id, self.association_type)

    def delete(self, **kwargs):
        """
        Delete a RubricAssociation.

        :calls: `DELETE /api/v1/courses/:course_id/rubric_associations/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.destroy>`_

        :rtype: :class:`canvasapi.rubric.RubricAssociation`
        """
        from canvasapi.rubric import RubricAssociation

        response = self._requester.request(
            "DELETE",
            "courses/{}/rubric_associations/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return RubricAssociation(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update a RubricAssociation.

        :calls: `PUT /api/v1/courses/:course_id/rubric_associations/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.update>`_

        :returns: Returns a RubricAssociation.
        :rtype: :class:`canvasapi.rubric.RubricAssociation`
        """
        from canvasapi.rubric import RubricAssociation

        response = self._requester.request(
            "PUT",
            "courses/{}/rubric_associations/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})
        if "association_type" in response_json:
            super(RubricAssociation, self).set_attributes(response_json)

        return self
