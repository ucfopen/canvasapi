from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.calendar_event import CalendarEvent
from canvasapi.canvas_object import CanvasObject
from canvasapi.communication_channel import CommunicationChannel
from canvasapi.folder import Folder
from canvasapi.paginated_list import PaginatedList
from canvasapi.upload import Uploader
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class User(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def get_profile(self, **kwargs):
        """
        Retrieve this user's profile.

        :calls: `GET /api/v1/user/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.profile.settings>`_

        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/{}/profile'.format(self.id)
        )
        return response.json()

    def get_page_views(self, **kwargs):
        """
        Retrieve this user's page views.

        :calls: `GET /api/v1/users/:user_id/page_views \
        <https://canvas.instructure.com/doc/api/users.html#method.page_views.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.PageView`
        """
        from canvasapi.page_view import PageView

        return PaginatedList(
            PageView,
            self._requester,
            'GET',
            'users/{}/page_views'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_courses(self, **kwargs):
        """
        Retrieve all courses this user is enrolled in.

        :calls: `GET /api/v1/users/:user_id/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.user_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from canvasapi.course import Course

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'users/{}/courses'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_missing_submissions(self):
        """
        Retrieve all past-due assignments for which the student does not
        have a submission.

        :calls: `GET /api/v1/users/:user_id/missing_submissions \
        <https://canvas.instructure.com/doc/api/users.html#method.users.missing_submissions>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'users/{}/missing_submissions'.format(self.id)
        )

    def update_settings(self, **kwargs):
        """
        Update this user's settings.

        :calls: `PUT /api/v1/users/:id/settings \
        <https://canvas.instructure.com/doc/api/users.html#method.users.settings>`_

        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'users/{}/settings'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def get_color(self, asset_string):
        """
        Return the custom colors that have been saved by this user for a given context.

        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.

        :calls: `GET /api/v1/users/:id/colors/:asset_string \
        <https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_color>`_

        :param asset_string: The asset to retrieve the color from.
        :type asset_string: str
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/{}/colors/{}'.format(self.id, asset_string)
        )
        return response.json()

    def get_colors(self):
        """
        Return all custom colors that have been saved by this user.

        :calls: `GET /api/v1/users/:id/colors \
        <https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_colors>`_

        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/{}/colors'.format(self.id)
        )
        return response.json()

    def update_color(self, asset_string, hexcode):
        """
        Update a custom color for this user for a given context.

        This allows colors for the calendar and elsewhere to be customized on a user basis.

        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.
        The `hexcode` parameter need not include the '#'.

        :calls: `PUT /api/v1/users/:id/colors/:asset_string \
        <https://canvas.instructure.com/doc/api/users.html#method.users.set_custom_color>`_

        :param asset_string: The asset to modify the color for.
        :type asset_string: str
        :param hexcode: The hexcode of the color to use.
        :type hexcode: str
        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'users/{}/colors/{}'.format(self.id, asset_string),
            hexcode=hexcode
        )
        return response.json()

    def edit(self, **kwargs):
        """
        Modify this user's information.

        :calls: `PUT /api/v1/users/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.update>`_

        :rtype: :class:`canvasapi.user.User`
        """
        response = self._requester.request(
            'PUT',
            'users/{}'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        super(User, self).set_attributes(response.json())
        return self

    def merge_into(self, destination_user):
        """
        Merge this user into another user.

        :calls: `PUT /api/v1/users/:id/merge_into/:destination_user_id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.merge_into>`_

        :param destination_user: The object or ID of the user to merge into.
        :type destination_user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.user.User`
        """
        dest_user_id = obj_or_id(destination_user, 'destination_user', (User, ))

        response = self._requester.request(
            'PUT',
            'users/{}/merge_into/{}'.format(self.id, dest_user_id),
        )
        super(User, self).set_attributes(response.json())
        return self

    def get_avatars(self):
        """
        Retrieve the possible user avatar options that can be set with the user update endpoint.

        :calls: `GET /api/v1/users/:user_id/avatars \
        <https://canvas.instructure.com/doc/api/users.html#method.profile.profile_pics>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.avatar.Avatar`
        """
        from canvasapi.avatar import Avatar

        return PaginatedList(
            Avatar,
            self._requester,
            'GET',
            'users/{}/avatars'.format(self.id)
        )

    def get_assignments(self, course, **kwargs):
        """
        Return the list of assignments for this user if the current
        user (the API key owner) has rights to view. See List assignments for valid arguments.

        :calls: `GET /api/v1/users/:user_id/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.user_index>`_

        :param course: The object or ID of the course to retrieve.
        :type course: :class:`canvasapi.course.Course` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.course import Course

        course_id = obj_or_id(course, "course", (Course,))

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'users/{}/courses/{}/assignments'.format(self.id, course_id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments for this user.

        :calls: `GET /api/v1/users/:user_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'users/{}/enrollments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def upload(self, file, **kwargs):
        """
        Upload a file for a user.

        NOTE: You *must* have authenticated with this user's API key to
        upload on their behalf no matter what permissions the issuer of the
        request has.

        :calls: `POST /api/v1/users/:user_id/files \
        <https://canvas.instructure.com/doc/api/users.html#method.users.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        return Uploader(
            self._requester,
            'users/{}/files'.format(self.id),
            file,
            **kwargs
        ).start()

    def list_calendar_events_for_user(self, **kwargs):
        """
        List calendar events that the current user can view or manage.

        :calls: `GET /api/v1/users/:user_id/calendar_events \
        <https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.user_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.calendar_event.CalendarEvent`
        """
        return PaginatedList(
            CalendarEvent,
            self._requester,
            'GET',
            'users/{}/calendar_events'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_communication_channels(self, **kwargs):
        """
        List communication channels for the specified user, sorted by
        position.

        :calls: `GET /api/v1/users/:user_id/communication_channels \
        <https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.communication_channel.CommunicationChannel`
        """
        return PaginatedList(
            CommunicationChannel,
            self._requester,
            'GET',
            'users/{}/communication_channels'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_files(self, **kwargs):
        """
        Returns the paginated list of files for the user.

        :calls: `GET api/v1/courses/:user_id/files \
            <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            'GET',
            'users/{}/files'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_file(self, file, **kwargs):
        """
        Return the standard attachment json object for a file.

        :calls: `GET /api/v1/users/:group_id/files/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_

        :param file: The object or ID of the file to retrieve.
        :type file: :class:`canvasapi.file.File` or int

        :rtype: :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        file_id = obj_or_id(file, "file", (File,))

        response = self._requester.request(
            'GET',
            'users/{}/files/{}'.format(self.id, file_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return File(self._requester, response.json())

    def get_folder(self, folder):
        """
        Returns the details for a user's folder

        :calls: `GET /api/v1/users/:user_id/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi.folder.Folder` or int

        :rtype: :class:`canvasapi.folder.Folder`
        """
        from canvasapi.folder import Folder

        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self._requester.request(
            'GET',
            'users/{}/folders/{}'.format(self.id, folder_id)
        )
        return Folder(self._requester, response.json())

    def list_folders(self):
        """
        Returns the paginated list of all folders for the given user. This will be returned as a
        flat list containing all subfolders as well.

        :calls: `GET /api/v1/users/:user_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        return PaginatedList(
            Folder,
            self._requester,
            'GET',
            'users/{}/folders'.format(self.id)
        )

    def create_folder(self, name, **kwargs):
        """
        Creates a folder in this user.

        :calls: `POST /api/v1/users/:user_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

        :param name: The name of the folder.
        :type name: str
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'POST',
            'users/{}/folders'.format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def list_user_logins(self, **kwargs):
        """
        Given a user ID, return that user's logins for the given account.

        :calls: `GET /api/v1/users/:user_id/logins \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.login.Login`
        """
        from canvasapi.login import Login

        return PaginatedList(
            Login,
            self._requester,
            'GET',
            'users/{}/logins'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_observees(self, **kwargs):
        """
        List the users that the given user is observing

        :calls:  `GET /api/v1/users/:user_id/observees \
        <https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'users/{}/observees'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def add_observee_with_credentials(self, **kwargs):
        """
        Register the given user to observe another user, given the observee's credentials.

        :calls: `POST /api/v1/users/:user_id/observees \
        <https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.create>`_

        :rtype: :class:`canvasapi.user.User`
        """

        response = self._requester.request(
            'POST',
            'users/{}/observees'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return User(self._requester, response.json())

    def show_observee(self, observee_id):
        """
        Gets information about an observed user.

        :calls: `GET /api/v1/users/:user_id/observees/:observee_id \
        <https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.show>`_

        :param observee_id: The login id for the user to observe.
        :type observee_id: int
        :rtype: :class: `canvasapi.user.User`
        """

        response = self._requester.request(
            'GET',
            'users/{}/observees/{}'.format(self.id, observee_id)
        )
        return User(self._requester, response.json())

    def add_observee(self, observee_id):
        """
        Registers a user as being observed by the given user.

        :calls: `PUT /api/v1/users/:user_id/observees/:observee_id \
        <https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.update>`_

        :param observee_id: The login id for the user to observe.
        :type observee_id: int
        :rtype: :class: `canvasapi.user.User`
        """

        response = self._requester.request(
            'PUT',
            'users/{}/observees/{}'.format(self.id, observee_id)
        )
        return User(self._requester, response.json())

    def remove_observee(self, observee_id):
        """
        Unregisters a user as being observed by the given user.

        :calls: `DELETE /api/v1/users/:user_id/observees/:observee_id \
        <https://canvas.instructure.com/doc/api/user_observees.html#method.user_observees.destroy>`_

        :param observee_id: The login id for the user to observe.
        :type observee_id: int
        :rtype: :class: `canvasapi.user.User`
        """

        response = self._requester.request(
            'DELETE',
            'users/{}/observees/{}'.format(self.id, observee_id)
        )
        return User(self._requester, response.json())


@python_2_unicode_compatible
class UserDisplay(CanvasObject):

    def __str__(self):
        return "{}".format(self.display_name)
