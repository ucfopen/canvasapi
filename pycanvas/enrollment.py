from canvas_object import CanvasObject


class Enrollment(CanvasObject):

    def __str__(self):
        return "id: %s, course_id: %s, user_id: %s, type: %s, " % (
            self.id,
            self.course_id,
            self.user_id,
            self.type
        )
