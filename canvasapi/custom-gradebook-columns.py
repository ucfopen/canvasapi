from canvasapi.progress import Progress # why? - bulk data returns a Progress obj

"""
not complete, I am currently:
- writing out skeleton for functions
steps:
description ✓
calls ✓
params (required ones listed only?)
return type
delete all unneccessary comments 
"""

	class CustomGradebookColumns(CanvasObject):
		"""
		both get_custom_columns and create_custom_column should be in course.py!

		def get_custom_columns(self): # should be in canvas.py? or course.py?
		
		List of all the custom gradebook columns for a course.

		:calls: `GET /api/v1/courses/:course_id/custom_gradebook_columns \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.index>`_
		
		:rtype: :class:`canvasapi.paginated_list.PaginatedList` of
	    	:class:`canvasapi.custom_gradebook-columns.CustomGradebookColumns`
		"""

		"""
		def create_custom_column(self): # should be in canvas.py?
		
		Create a custom gradebook column.

		:calls: `POST /api/v1/courses/:course_id/custom_gradebook_columns \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.create>`_

	    :rtype: :class:`canvasapi.custom_gradebook-columns.CustomGradebookColumns`
		"""

		def update_custom_column(self):
		"""
		Return a CustomColumn object.

		:calls: `PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.update>`_

	    :rtype: :class:`canvasapi.custom_gradebook-columns.CustomGradebookColumns`
		"""

		def delete(self):
		"""
		Permanently delete a custom column.

		:calls: `DELETE /api/v1/courses/:course_id/custom_gradebook_columns/:id \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.destroy>`_
		"""

		def reorder_custom_columns(self):
		"""
		Put the given columns in a specific order based on given parameter.

		:calls: `POST /api/v1/courses/:course_id/custom_gradebook_columns/reorder \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.reorder>`_
		"""

	class CustomGradebookColumnData(CanvasObject):
		# where the requests for custom gradebook column data exist 

		def get_column_entries(self, **kwargs): 
		"""
		Returns a list of ColumnData objects.

		:calls: `GET /api/v1/courses/:course_id/custom_gradebook_columns/:id/data \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.index>`_ 
		"""

		def update_data(self):
		"""
		Sets the content of a custom column.

		:calls: `PUT /api/v1/courses/:course_id/custom_gradebook_columns/:id/data/:user_id \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.update>`_
		"""

		def bulk_update_data(self):
		"""
		Set the content of custom columns.

		:calls: `PUT /api/v1/courses/:course_id/custom_gradebook_column_data \
	    <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.bulk_update>`_

	    :rtype: :class:`canvasapi.progress.Progress`
		"""
