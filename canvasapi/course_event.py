from canvasapi.canvas_object import CanvasObject


class CourseEvent(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.name, self.start_at, self.conclude_at)
