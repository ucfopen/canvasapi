from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.upload import Uploader
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class Submission(CanvasObject):

    def __str__(self):
        return '{}-{}'.format(self.assignment_id, self.user_id)

    def edit(self, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

        :rtype: :class:`canvasapi.submission.Submission`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/assignments/{}/submissions/{}'.format(
                self.course_id,
                self.assignment_id,
                self.user_id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)

        super(Submission, self).set_attributes(response_json)
        return self

    def mark_read(self, **kwargs):
        """
        Mark submission as read. No request fields are necessary.

        :calls: `PUT
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

        :returns: True if successfully marked as read.
        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/assignments/{}/submissions/{}/read'.format(
                self.course_id,
                self.assignment_id,
                self.user_id
            )
        )
        return response.status_code == 204

    def mark_unread(self, **kwargs):
        """
        Mark submission as unread. No request fields are necessary.

        :calls: `DELETE
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

        :returns: True if successfully marked as unread.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/assignments/{}/submissions/{}/read'.format(
                self.course_id,
                self.assignment_id,
                self.user_id
            )
        )
        return response.status_code == 204

    def upload_comment(self, file, **kwargs):
        """
        Upload a file to attach to this submission as a comment.

        :calls: `POST \
        /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/files \
        <https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
            and the JSON response from the API.
        :rtype: tuple
        """
        response = Uploader(
            self._requester,
            'courses/{}/assignments/{}/submissions/{}/comments/files'.format(
                self.course_id,
                self.assignment_id,
                self.user_id
            ),
            file,
            **kwargs
        ).start()

        if response[0]:
            self.edit(
                comment={
                    'file_ids': [response[1]['id']]
                }
            )

        return response
