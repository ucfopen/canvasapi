from canvas_object import CanvasObject


class Enrollment(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.course_code, self.name)
