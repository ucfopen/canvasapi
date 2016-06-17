from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList
# from exceptions import RequiredFieldMissing


class ExternalTool(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.description)

    @property
    def parent_id(self):
        """
        Return the id of the course or account that spawned this tool.

        :rtype: int
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'account_id'):
            return self.account_id
        else:
            raise ValueError("ExternalTool does not have a course_id or account_id")

    @property
    def parent_type(self):
        """
        Return whether the tool was spawned from a course or account.

        :rtype: str
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'account_id'):
            return 'account'
        else:
            raise ValueError("ExternalTool does not have a course_id or account_id")

    def get_parent(self):
        """
        Return the object that spawned this tool.

        :rtype: :class:`pycanvas.account.Account` or :class:`pycanvas.account.Course`
        """
        from account import Account
        from course import Course

        response = self._requester.request(
            'GET',
            '%ss/%s' % (self.parent_type, self.parent_id)
        )

        if self.parent_type == 'account':
            return Account(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())
