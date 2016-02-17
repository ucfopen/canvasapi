from pycanvas import CanvasObject

class Course(CanvasObject):

	def __init__(self, id, name, course_code):
		"""
		:param id: int
		:param name: string
		:param course_code: string
		"""
		self.id = id
		self.name = name
		self.course_code = course_code
