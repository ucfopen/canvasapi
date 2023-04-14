from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Rubric(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def delete(self, **kwargs):
        """
        Delete a Rubric.

        :calls: `DELETE /api/v1/courses/:course_id/rubrics/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.destroy>`_

        :rtype: :class:`canvasapi.rubric.Rubric`
        """
        from canvasapi.rubric import Rubric

        response = self._requester.request(
            "DELETE",
            "courses/{}/rubrics/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Rubric(self._requester, response.json())


class RubricAssessment(CanvasObject):
    def __str__(self):
        return "{}, {}".format(self.id, self.artifact_type)

    def delete(self, **kwargs):
        """
        Delete a single RubricAssessment.

        :calls: `DELETE /api/v1/courses/:course_id/rubric_associations\
        /:rubric_association_id/rubric_assessments/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.destroy>`_

        :rtype: :class:`canvasapi.rubric.RubricAssessment`
        """
        from canvasapi.rubric import RubricAssessment

        response = self._requester.request(
            "DELETE",
            "courses/{}/rubric_associations/{}/rubric_assessments/{}".format(
                self.course_id, self.rubric_association_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return RubricAssessment(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update a single RubricAssessment.

        :calls: `PUT /api/v1/courses/:course_id/rubric_associations\
        /:rubric_association_id/rubric_assessments/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.update>`_

        :rtype: :class:`canvasapi.rubric.RubricAssessment`
        """
        from canvasapi.rubric import RubricAssessment

        response = self._requester.request(
            "PUT",
            "courses/{}/rubric_associations/{}/rubric_assessments/{}".format(
                self.course_id, self.rubric_association_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return RubricAssessment(self._requester, response.json())


class RubricAssociation(CanvasObject):
    def __str__(self):
        return "{}, {}".format(self.id, self.association_type)

    def create_rubric_assessment(self, **kwargs):
        """
        Create a single RubricAssessment.

        :calls: `POST /api/v1/courses/:course_id/rubric_associations\
        /:rubric_association_id/rubric_assessments \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.create>`_

        :rtype: :class:`canvasapi.rubric.RubricAssessment`
        """
        from canvasapi.rubric import RubricAssessment

        response = self._requester.request(
            "POST",
            "courses/{}/rubric_associations/{}/rubric_assessments".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        assessment_json = response.json()
        assessment_json.update({"course_id": self.id})

        return RubricAssessment(self._requester, assessment_json)

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
