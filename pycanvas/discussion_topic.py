from pycanvas.canvas_object import CanvasObject

class DiscussionTopic(CanvasObject):
	def __str__(self):
		return "{} ({})".format(self.title, self.id) 
