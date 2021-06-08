from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, is_multivalued


class CustomGradebookColumn(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def delete(self, **kwargs):
        """
        Permanently delete a custom column.

        :calls: `DELETE /api/v1/courses/:course_id/custom_gradebook_columns/:id \
            <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.destroy>`_
        :rtype: :class:`canvasapi.custom_gradebook_columns.CustomGradebookColumn`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/custom_gradebook_columns/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return CustomGradebookColumn(self._requester, response.json())

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
            self._requester,
            "GET",
            "courses/{}/custom_gradebook_columns/{}/data".format(
                self.course_id, self.id
            ),
            {"course_id": self.course_id, "gradebook_column_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def reorder_custom_columns(self, order, **kwargs):
        """
        Put the given columns in a specific order based on given parameter.

        :calls: `POST /api/v1/courses/:course_id/custom_gradebook_columns/reorder \
            <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.reorder>`_

        :param order: The order the columns are supposed to be in.
        :type order: list of int

        :returns: True if successful (status code of 200)
        :rtype: bool
        """
        # Convert iterable sequence to comma-separated string
        if is_multivalued(order):
            order = ",".join([str(topic_id) for topic_id in order])

        # Check if is a string with commas
        if not isinstance(order, str) or "," not in order:
            raise ValueError("Param `order` must be a list, tuple, or string.")

        response = self._requester.request(
            "POST",
            "courses/{}/custom_gradebook_columns/reorder".format(self.course_id),
            _kwargs=combine_kwargs(**kwargs),
            order=order,
        )

        return response.json().get("reorder")

    def update_custom_column(self, **kwargs):
        """
        Update a CustomColumn object.

        :calls: `PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id \
            <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.update>`_

        :rtype: :class:`canvasapi.custom_gradebook_columns.CustomGradebookColumn`
        """

        response = self._requester.request(
            "PUT",
            "courses/{}/custom_gradebook_columns/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if response.json().get("title"):
            super(CustomGradebookColumn, self).set_attributes(response.json())

        return self


class ColumnData(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.user_id, self.content)

    def update_column_data(self, column_data, **kwargs):
        """
        Sets the content of a custom column.

        :calls: `PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id/data/:user_id \
            <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.update>`_

        :param column_data: The content in the column.
        :type column_data: str

        :rtype: :class:`canvasapi.custom_gradebook_columns.ColumnData`
        """

        kwargs["column_data"] = column_data

        response = self._requester.request(
            "PUT",
            "courses/{}/custom_gradebook_columns/{}/data/{}".format(
                self.course_id, self.gradebook_column_id, self.user_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        if response.json().get("content"):
            super(ColumnData, self).set_attributes(response.json())

        return self
