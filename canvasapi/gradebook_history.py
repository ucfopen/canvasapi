from canvasapi.canvas_object import CanvasObject


class Day(CanvasObject):
    def __str__(self):
        return "{}".format(self.date)


class Grader(CanvasObject):
    def __str__(self):
        return "{}".format(self.id)


class SubmissionHistory(CanvasObject):
    def __str__(self):
        return "{}".format(self.submission_id)


class SubmissionVersion(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.assignment_id, self.id)
