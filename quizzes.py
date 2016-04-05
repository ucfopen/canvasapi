from canvas_object import CanvasObject
from paginated_list import PaginatedList

class Quizzes(CanvasObject):

    def __str__(self):
        return "id %s, title: %s" % (
            self.id,
            self.name
        )

    