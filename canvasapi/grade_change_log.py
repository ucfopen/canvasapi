from canvasapi.canvas_object import CanvasObject


class GradeChangeEvent(CanvasObject):
    def __str__(self):
        return "{} {} - {} ({})".format(
            self.event_type, self.grade_before, self.grade_after, self.id
        )
