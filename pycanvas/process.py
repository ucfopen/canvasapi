from pycanvas.canvas_object import CanvasObject


class Process(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "%s: %s, %s" % (self.id, self.tag, self.workflow_state)
