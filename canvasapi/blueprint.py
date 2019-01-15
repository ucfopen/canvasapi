from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class BlueprintTemplate(CanvasObject):

    def __str__(self):
        return "{}".format(self.id)

    def get_associated_courses(self, **kwargs):
        """
        Return a list of courses associated with the given blueprint.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id/
        associated_courses \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.associated_courses>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from canvasapi.course import Course

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'courses/{}/blueprint_templates/{}/associated_courses'.format(
                self.course_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

    def update_associated_courses(self, **kwargs):
        """
        Add or remove new associations for the blueprint template.

        :calls: `PUT /api/v1/courses/:course_id/blueprint_templates/:template_id/update_associations \ <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.update_associations>`_

        :returns: True if the course was added or removed, False otherwise.
        :rtype bool
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/blueprint_templates/{}/update_associations'.format(
                self.course_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json().get("success", False)

    def associated_course_migration(self, **kwargs):
        """
        Start a migration to update content in all associated courses.

        :calls: `POST /api/v1/courses/:course_id/blueprint_templates/:template_id/migrations \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.queue_migration>`_

        :rtype: :class:`canvasapi.blueprint.BlueprintMigration`
        """
        response = self._requester.request(
            'POST',
            'courses/{}/blueprint_templates/{}/migrations'.format(
                self.course_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return BlueprintTemplate(self._requester, response.json())

# must use content_type, content_id, and restricted param for the function call to work
# there must be an instance of the content_type in the course
    def change_blueprint_restrictions(self, **kwargs):
        """
        Set or remove restrictions on a blueprint course object.

        :calls: `PUT /api/v1/courses/:course_id/blueprint_templates/:template_id/restrict_item \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.restrict_item>`_

        :returns: True if the restriction was succesfully applied.
        :rtype bool
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/blueprint_templates/{}/restrict_item'.format(
                self.course_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json().get("success", False)
