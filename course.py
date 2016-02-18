from pycanvas import CanvasObject

class Course(CanvasObject):

	@property
	def id(self):
	    return self.attributes['id']

	@property
	def name(self):
	    return self.attributes['name']
	
	@property
	def sis_course_id(self):
	    return self.attributes['sis_course_id']