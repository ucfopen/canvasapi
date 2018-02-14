from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.upload import Uploader


@python_2_unicode_compatible
class Submission(CanvasObject):

    def __str__(self):
        return "{}".format(self.id)

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
        from canvasapi.course import Course

        if not hasattr(self, 'course_id'):
            raise ValueError('Must use a course to upload file comments.')

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
            # 1337 h@x: remove once lazy loading is completed
            course = Course(self._requester, {'id': self.course_id})

            course.update_submission(
                self.assignment_id,
                self.user_id,
                comment={
                    'file_ids': [response[1]['id']]
                }
            )

        return response
