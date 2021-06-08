from canvasapi.canvas_object import CanvasObject


class PollSubmission(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.poll_choice_id, self.id)
