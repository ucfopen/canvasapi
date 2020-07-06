from canvasapi.canvas_object import CanvasObject


class ContentExport(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.export_type, self.user_id, self.id)
