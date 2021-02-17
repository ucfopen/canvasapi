from canvasapi.util import combine_kwargs
from canvasapi.canvas_object import CanvasObject
import json
class ProvisionalGrades(CanvasObject):
    def __init__(self, requester, attributes):
        super(ProvisionalGrades, self).__init__(requester, attributes)
    """
    :calls: PUT /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/bulk_select \
    <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.bulk_select>
    :param course_id: The ID of a course
    :type course_id: int
    :param assignment_id: the ID of the assignment
    :type assignment_id: int
    :rtype: list[dicts]
    """
    def provisional_grades_bulk_select(self, course_id, assignment_id, **kwargs):
        response = self._requester.request(
                "PUT", "courses/'{}'/assignment/'{}'/provisional_grades/bulk_select".format(
                self.course_id, self.assignment_id), 
                _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        return response_json

    """
    :calls: GET /api/v1/courses:course_id/provisional_grades/status/?student_id= \
    <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.status>
    :param course_id: ID of course
    :type course_id: int
    :rtype: JSON
    """
    def get_provisional_grades_status(self, course_id, assignment_id):
        from canvasapi.user import User
        user_id = obj_or_id(user, "user", (User,))
        kwargs["user_id"] = user_id
        request = self._requester.request(
                "GET",
                "courses/{}/assignments/{}/provisional_grades/status/?student_id={}".format(
                    self.course_id, self.assignment_id, self.id
                    ),
                    _kwargs=combine_kwargs(**kwargs)
                )

        response_json = response.json()
        return response_json
    

    """
    :calls: PUT /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/:provisonal_grade_id/select \
    <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.select>

    Choose which provisional grade the student should receive for a submission. 
    The caller must be the final grader for the assignment or an admin with :select_final_grade rights.

    :param course_id: ID of course
    :type course_id: int
    :param assignment_id: ID of assignment
    :type assignment_id: int
    :param provisional_grade_id: ID of the provisional grade
    :type provisional_grade_id: int
    :rtype: JSON
    """
    def selected_provisional_grade(self, course_id, assignment_id, provisional_grade_id, **kwargs):
        uri_str = "courses/{}/assignment/{}/provisional_grades/{}/select"
        response = self._requester.request(
                "PUT", "courses/{}/assignment/{}/provisional_grades/{}/select".format(
                    self.course_id, self.assignment_id, self.provisional_grade_id
                    ),
                    _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        return response_json()

    """
    :calls: POST /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/publish \
    <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.publish>
    :param course_id: ID of specified course
    :type course_id: int
    :param assignment_id: ID of specified assignment
    :type assignment_id: int
    """
    def publish_provisional_grades(self, course_id, assignment_id, **kwargs):
        response = self._requester.request(
                "POST", 
                "courses/{}/assignment/{}/provisional_grades/publish".format(
                    self.course_id, self.assignment_id
                    ),
                    _kwargs=combine_kwargs(**kwargs)
            )
        
    """
    :call: GET /api/v1/courses/:course_id/assignments/:assignment_id/anonymous_provisional_grades/status \
    <https://canvas.instructure.com/doc/api/all_resources.html#method.anonymous_provisional_grades.status>
    :rtype: dict
    """
    def show_provisonal_grades_for_student(self, course_id, assignment_id, **kwargs):
        response = self._requester.request(
                "GET", "courses/{}/assignment/{}anonymous_provisional_grades/status?anonymous_id={}".format(
                    self.course_id, self.assignment_id, self.anonymous_id
                    ),
                    _kwargs=combine_kwargs(**kwargs)
            )

        response_json = response.json()
        return response_json