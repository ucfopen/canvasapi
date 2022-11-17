from canvasapi.canvas_object import CanvasObject


class CourseEvent(CanvasObject):
    def __str__(self):
        return self.name
