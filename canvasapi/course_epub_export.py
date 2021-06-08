from canvasapi.canvas_object import CanvasObject


class CourseEpubExport(CanvasObject):
    def __str__(self):
        return "{} course_id:({}) epub_id:({}) {} ".format(
            self.name,
            self.id,
            self.epub_export["id"],
            self.epub_export["workflow_state"],
        )
