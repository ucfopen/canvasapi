from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.grading_standard import GradingStandard
from canvasapi.exceptions import CanvasException, RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.rubric import Rubric
from canvasapi.util import combine_kwargs, obj_or_id

@python_2_unicode_compatible
class ContentMigration(CanvasObject):
	def __str__(self):
		return "{} {}".format(self.migration_type_title, self.id)

@python_2_unicode_compatible
class MigrationIssue(CanvasObject):
	def __str__(self):
		return "{}: {}".format(self.id,self.description)

@python_2_unicode_compatible
class Migrator(CanvasObject):
	def __str__(self):
		return "{}".format(self.type)
