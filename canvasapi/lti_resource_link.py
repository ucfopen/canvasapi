from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id
from canvasapi.course import Course
from canvasapi.exceptions import RequiredFieldMissing

class LTIResourceLink(CanvasObject):
    def __init__(self, requester, attributes):
        # Initialize an LTIResourceLink object.
        super(LTIResourceLink, self).__init__(requester, attributes)

class ExtendedCourse(Course):
    def get_lti_resource_links(self, **kwargs):
        """
        Returns all LTI resource links for this course as a PaginatedList.

        :calls: `GET /api/v1/courses/:course_id/lti_resource_links \
        <https://canvas.instructure.com/doc/api/lti_resource_links.html#method.lti/resource_links.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList`
        """
        
        return PaginatedList(
            LTIResourceLink,
            self._requester,
            "GET",
            f"courses/{self.id}/lti_resource_links",
            kwargs=combine_kwargs(**kwargs)
        )

    def get_lti_resource_link(self, lti_resource_link, **kwargs):
        """
        Return details about the specified resource link.

        :calls: `GET /api/v1/courses/:course_id/lti_resource_links/:id \
        <https://canvas.instructure.com/doc/api/lti_resource_links.html#method.lti/resource_links.show>`_

        :param lti_resource_link: The object or ID of the LTI resource link.
        :type lti_resource_link: :class:`canvasapi.lti_resource_link.LTIResourceLink` or int

        :rtype: :class:`canvasapi.lti_resource_link.LTIResourceLink`
        """
        lti_resource_link_id = obj_or_id(lti_resource_link, "lti_resource_link", (LTIResourceLink,))

        response = self._requester.request(
            "GET",
            f"courses/{self.id}/lti_resource_links/{lti_resource_link_id}",
            _kwargs=combine_kwargs(**kwargs)
        )
        return LTIResourceLink(self._requester, response.json())

    def create_lti_resource_link(self, url, title=None, custom=None, **kwargs):
        """
        Create a new LTI resource link.

        :calls: `POST /api/v1/courses/:course_id/lti_resource_links \
        <https://canvas.instructure.com/doc/api/lti_resource_links.html#method.lti/resource_links.create>`_

        :param course_id: The ID of the course.
        :type course_id: `int`
        :param url: The launch URL for the resource link.
        :type url: `str`
        :param title: The title of the resource link.
        :type title: `str`, optional
        :param custom: Custom parameters to send to the tool.
        :type custom: `dict`, optional

        :rtype: :class:`canvasapi.lti_resource_link.LTIResourceLink`
        """

        if not url:
            raise RequiredFieldMissing("The 'url' paramter is required.")
        
        kwargs["url"] = url
        if title:
            kwargs["title"] = title
        if custom:
            kwargs["custom"] = custom

        response = self._requester.request(
            "POST",
            f"courses/{self.id}/lti_resource_links",
            _kwargs=combine_kwargs(**kwargs)
        )
        return LTIResourceLink(self._requester, response.json())
