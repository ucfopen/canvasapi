from pycanvas.canvas_object import CanvasObject


class PageView(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.url, self.created_at)
