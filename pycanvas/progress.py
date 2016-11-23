from pycanvas.canvas_object import CanvasObject


class Progress(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "{} - {} ({})".format(self.tag, self.workflow_state, self.id)
