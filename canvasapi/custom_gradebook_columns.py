# don't forget - delete unnecessary comments
from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import (
    PaginatedList,
)  # why? - get column entries returns paginated list

# from canvasapi.user import User  # why? - user_id is needed in ColumnData
from canvasapi.util import (
    combine_kwargs,
    is_multivalued,
)


class CustomGradebookColumn(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    # COMPLETE :) - review 
    def update_custom_column(self, column, **kwargs):
        """
        Return a CustomColumn object.

        :calls: `PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.update>`_
        param column[title]: The header text of the column.
        :type column[title]: str
        :rtype: :class:`canvasapi.custom_gradebook_columns.CustomGradebookColumn`
        """
        kwargs["column"] = column

        response = self._requester.request(
            "PUT",
            "courses/{}/custom_gradebook_columns/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return CustomGradebookColumn(self._requester, response.json())

    # COMPLETE :) - review
    def get_column_entries(self, **kwargs):
        """
        Returns a list of ColumnData objects.

        :calls: `GET /api/v1/courses/:course_id/custom_gradebook_columns/:id/data \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.index>`_
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.custom_gradebook_columns.ColumnData`
        """
        return PaginatedList(
            ColumnData,
            "GET",
            "courses/{}/custom_gradebook_columns/{}/data".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    # COMPLETE :) - review
    def delete(self):
        """
        Permanently delete a custom column.

        :calls: `DELETE /api/v1/courses/:course_id/custom_gradebook_columns/:id \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.destroy>`_
        :rtype: returns the column that it deleted
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/custom_gradebook_columns/{}".format(self.course_id, self.id),
            event="delete",
        )

        return response.json().get("delete")

    # ???
    def reorder_custom_columns(self, order):
        """
        Put the given columns in a specific order based on given parameter.

        :calls: `POST /api/v1/courses/:course_id/custom_gradebook_columns/reorder \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.reorder>`_
        :param order: The order the columns are supposed to be in.
        :type order: int
        :returns: True if successful (status code of 200)
        :rtype: bool
        """

        # note: doesn't have a description?
        # course.py: reorder_pinned_topics
        # Convert iterable sequence to comma-separated string
        if is_multivalued(order):
            order = ",".join([str(topic_id) for topic_id in order])

        # Check if is a string with commas
        if not isinstance(order, str) or "," not in order:
            raise ValueError("Param `order` must be a list, tuple, or string.")

        response = self._requester.request(
            "POST", "courses/{}/custom_gradebook_columns/reorder".format(self.course_id)
        )
        return response.status_code == 200


class ColumnData(CanvasObject):
    def __str__(self):
        return "Content: {} ({})".format(self.user_id, self.content)

    # ???
    def update_column_data(self, column_data):
        """
        Sets the content of a custom column.

        :calls: `PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id/data/:user_id \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.update>`_
        param column_data[content]: The content in the column.
        type column_data[content]: str
        :rtype: :class:`canvasapi.custom_gradebook_columns.ColumnData`
        """

        response = self._requester.request(
            "PUT",
            "courses/{}/custom_gradebook_columns/{}/data/{}".format(
                self.course_id, self.id, self.user_id
            ),
        )

        pass
        return response
