from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from canvasapi.account import Account
from canvasapi.course import Course
from canvasapi.current_user import CurrentUser
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.file import File
from canvasapi.folder import Folder
from canvasapi.group import Group, GroupCategory
from canvasapi.paginated_list import PaginatedList
from canvasapi.requester import Requester
from canvasapi.section import Section
from canvasapi.user import User
from canvasapi.util import combine_kwargs, get_institution_url, obj_or_id


warnings.simplefilter('always', DeprecationWarning)


class Canvas(object):
    """
    The main class to be instantiated to provide access to Canvas's API.
    """

    def __init__(self, base_url, access_token):
        """
        :param base_url: The base URL of the Canvas instance's API.
        :type base_url: str
        :param access_token: The API key to authenticate requests with.
        :type access_token: str
        """
        new_url = get_institution_url(base_url)

        if 'api/v1' in base_url:
            warnings.warn(
                "`base_url` no longer requires an API version be specified. "
                "Rewriting `base_url` to {}".format(new_url),
                DeprecationWarning
            )
        base_url = new_url + '/api/v1/'

        self.__requester = Requester(base_url, access_token)

    def create_account(self, **kwargs):
        """
        Create a new root account.

        :calls: `POST /api/v1/accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`_

        :rtype: :class:`canvasapi.account.Account`
        """
        response = self.__requester.request(
            'POST',
            'accounts',
            _kwargs=combine_kwargs(**kwargs)
        )
        return Account(self.__requester, response.json())

    def get_account(self, account, use_sis_id=False, **kwargs):
        """
        Retrieve information on an individual account.

        :calls: `GET /api/v1/accounts/:id \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show>`_

        :param account: The object or ID of the account to retrieve.
        :type account: int, str or :class:`canvasapi.account.Account`
        :param use_sis_id: Whether or not account_id is an sis ID.
            Defaults to `False`.
        :type use_sis_id: bool

        :rtype: :class:`canvasapi.account.Account`
        """
        if use_sis_id:
            account_id = account
            uri_str = 'accounts/sis_account_id:{}'
        else:
            account_id = obj_or_id(account, "account", (Account,))
            uri_str = 'accounts/{}'

        response = self.__requester.request(
            'GET',
            uri_str.format(account_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Account(self.__requester, response.json())

    def get_accounts(self, **kwargs):
        """
        List accounts that the current user can view or manage.

        Typically, students and teachers will get an empty list in
        response. Only account admins can view the accounts that they
        are in.

        :calls: `GET /api/v1/accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.Account`
        """
        return PaginatedList(
            Account,
            self.__requester,
            'GET',
            'accounts',
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_course_accounts(self):
        """
        List accounts that the current user can view through their
        admin course enrollments (Teacher, TA or designer enrollments).

        Only returns `id`, `name`, `workflow_state`, `root_account_id`
        and `parent_account_id`.

        :calls: `GET /api/v1/course_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.course_accounts>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.Account`
        """
        return PaginatedList(
            Account,
            self.__requester,
            'GET',
            'course_accounts',
        )

    def get_course(self, course, use_sis_id=False, **kwargs):
        """
        Retrieve a course by its ID.

        :calls: `GET /courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`_

        :param course: The object or ID of the course to retrieve.
        :type course: int, str or :class:`canvasapi.course.Course`
        :param use_sis_id: Whether or not course_id is an sis ID.
            Defaults to `False`.
        :type use_sis_id: bool

        :rtype: :class:`canvasapi.course.Course`
        """
        if use_sis_id:
            course_id = course
            uri_str = 'courses/sis_course_id:{}'
        else:
            course_id = obj_or_id(course, "course", (Course,))
            uri_str = 'courses/{}'

        response = self.__requester.request(
            'GET',
            uri_str.format(course_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Course(self.__requester, response.json())

    def get_user(self, user, id_type=None):
        """
        Retrieve a user by their ID. `id_type` denotes which endpoint to try as there are
        several different IDs that can pull the same user record from Canvas.

        Refer to API documentation's
        `User <https://canvas.instructure.com/doc/api/users.html#User>`_
        example to see the ID types a user can be retrieved with.

        :calls: `GET /users/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>`_

        :param user: The user's object or ID.
        :type user: :class:`canvasapi.user.User` or int
        :param id_type: The ID type.
        :type id_type: str

        :rtype: :class:`canvasapi.user.User`
        """
        if id_type:
            uri = 'users/{}:{}'.format(id_type, user)
        elif user == 'self':
            uri = 'users/self'
        else:
            user_id = obj_or_id(user, "user", (User,))
            uri = 'users/{}'.format(user_id)

        response = self.__requester.request(
            'GET',
            uri
        )
        return User(self.__requester, response.json())

    def get_current_user(self):
        return CurrentUser(self.__requester)

    def get_courses(self, **kwargs):
        """
        Return a list of active courses for the current user.

        :calls: `GET /api/v1/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        return PaginatedList(
            Course,
            self.__requester,
            'GET',
            'courses',
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_activity_stream_summary(self):
        """
        Return a summary of the current user's global activity stream.

        :calls: `GET /api/v1/users/self/activity_stream/summary \
        <https://canvas.instructure.com/doc/api/users.html#method.users.activity_stream_summary>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/activity_stream/summary'
        )
        return response.json()

    def get_todo_items(self):
        """
        Return the current user's list of todo items, as seen on the user dashboard.

        :calls: `GET /api/v1/users/self/todo \
        <https://canvas.instructure.com/doc/api/users.html#method.users.todo_items>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/todo'
        )
        return response.json()

    def get_upcoming_events(self):
        """
        Return the current user's upcoming events, i.e. the same things shown
        in the dashboard 'Coming Up' sidebar.

        :calls: `GET /api/v1/users/self/upcoming_events \
        <https://canvas.instructure.com/doc/api/users.html#method.users.upcoming_events>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/upcoming_events'
        )
        return response.json()

    def get_course_nicknames(self):
        """
        Return all course nicknames set by the current account.

        :calls: `GET /api/v1/users/self/course_nicknames \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.CourseNickname`
        """
        from canvasapi.course import CourseNickname

        return PaginatedList(
            CourseNickname,
            self.__requester,
            'GET',
            'users/self/course_nicknames'
        )

    def get_course_nickname(self, course):
        """
        Return the nickname for the given course.

        :calls: `GET /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.show>`_

        :param course: The object or ID of the course.
        :type course: :class:`canvasapi.course.Course` or int

        :rtype: :class:`canvasapi.course.CourseNickname`
        """
        from canvasapi.course import CourseNickname

        course_id = obj_or_id(course, "course", (Course,))

        response = self.__requester.request(
            'GET',
            'users/self/course_nicknames/{}'.format(course_id)
        )
        return CourseNickname(self.__requester, response.json())

    def get_section(self, section, use_sis_id=False, **kwargs):
        """
        Get details about a specific section.

        :calls: `GET /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.show>`_

        :param section: The object or ID of the section to get.
        :type section: :class:`canvasapi.section.Section` or int
        :param use_sis_id: Whether or not section_id is an sis ID.
            Defaults to `False`.
        :type use_sis_id: bool

        :rtype: :class:`canvasapi.section.Section`
        """
        if use_sis_id:
            section_id = section
            uri_str = 'sections/sis_section_id:{}'
        else:
            section_id = obj_or_id(section, "section", (Section,))
            uri_str = 'sections/{}'

        response = self.__requester.request(
            'GET',
            uri_str.format(section_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Section(self.__requester, response.json())

    def set_course_nickname(self, course, nickname):
        """
        Set a nickname for the given course. This will replace the
        course's name in the output of subsequent API calls, as
        well as in selected places in the Canvas web user interface.

        :calls: `PUT /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.update>`_

        :param course: The ID of the course.
        :type course: :class:`canvasapi.course.Course` or int
        :param nickname: The nickname for the course.
        :type nickname: str

        :rtype: :class:`canvasapi.course.CourseNickname`
        """
        from canvasapi.course import CourseNickname

        course_id = obj_or_id(course, "course", (Course,))

        response = self.__requester.request(
            'PUT',
            'users/self/course_nicknames/{}'.format(course_id),
            nickname=nickname
        )
        return CourseNickname(self.__requester, response.json())

    def clear_course_nicknames(self):
        """
        Remove all stored course nicknames.

        :calls: `DELETE /api/v1/users/self/course_nicknames \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

        :returns: True if the nicknames were cleared, False otherwise.
        :rtype: bool
        """
        response = self.__requester.request(
            'DELETE',
            'users/self/course_nicknames'
        )
        return response.json().get('message') == 'OK'

    def search_accounts(self, **kwargs):
        """
        Return a list of up to 5 matching account domains. Partial matches on
        name and domain are supported.

        :calls: `GET /api/v1/accounts/search \
        <https://canvas.instructure.com/doc/api/account_domain_lookups.html#method.account_domain_lookups.search>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'accounts/search',
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def create_group(self, **kwargs):
        """
        Create a group

        :calls: `POST /api/v1/groups/ \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.create>`_

        :rtype: :class:`canvasapi.group.Group`
        """
        response = self.__requester.request(
            'POST',
            'groups',
            _kwargs=combine_kwargs(**kwargs)
        )
        return Group(self.__requester, response.json())

    def get_group(self, group, use_sis_id=False, **kwargs):
        """
        Return the data for a single group. If the caller does not
        have permission to view the group a 401 will be returned.

        :calls: `GET /api/v1/groups/:group_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.show>`_

        :param group: The object or ID of the group to get.
        :type group: :class:`canvasapi.group.Group` or int

        :param use_sis_id: Whether or not group_id is an sis ID.
            Defaults to `False`.
        :type use_sis_id: bool

        :rtype: :class:`canvasapi.group.Group`
        """

        if use_sis_id:
            group_id = group
            uri_str = 'groups/sis_group_id:{}'
        else:
            group_id = obj_or_id(group, "group", (Group,))
            uri_str = 'groups/{}'

        response = self.__requester.request(
            'GET',
            uri_str.format(group_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Group(self.__requester, response.json())

    def get_group_category(self, category):
        """
        Get a single group category.

        :calls: `GET /api/v1/group_categories/:group_category_id \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.show>`_

        :param category: The object or ID of the category.
        :type category: :class:`canvasapi.group.GroupCategory` or int

        :rtype: :class:`canvasapi.group.GroupCategory`
        """
        category_id = obj_or_id(category, "category", (GroupCategory,))

        response = self.__requester.request(
            'GET',
            'group_categories/{}'.format(category_id)
        )
        return GroupCategory(self.__requester, response.json())

    def create_conversation(self, recipients, body, **kwargs):
        """
        Create a new Conversation.

        :calls: `POST /api/v1/conversations \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.create>`_

        :param recipients: An array of recipient ids.
            These may be user ids or course/group ids prefixed
            with 'course\_' or 'group\_' respectively,
            e.g. recipients=['1', '2', 'course_3']
        :type recipients: `list` of `str`
        :param body: The body of the message being added.
        :type body: `str`
        :rtype: list of :class:`canvasapi.conversation.Conversation`
        """
        from canvasapi.conversation import Conversation

        kwargs['recipients'] = recipients
        kwargs['body'] = body

        response = self.__requester.request(
            'POST',
            'conversations',
            _kwargs=combine_kwargs(**kwargs)
        )
        return [Conversation(self.__requester, convo) for convo in response.json()]

    def get_conversation(self, conversation, **kwargs):
        """
        Return single Conversation

        :calls: `GET /api/v1/conversations/:id \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.show>`_

        :param conversation: The object or ID of the conversation.
        :type conversation: :class:`canvasapi.conversation.Conversation` or int

        :rtype: :class:`canvasapi.conversation.Conversation`
        """
        from canvasapi.conversation import Conversation

        conversation_id = obj_or_id(conversation, "conversation", (Conversation,))

        response = self.__requester.request(
            'GET',
            'conversations/{}'.format(conversation_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Conversation(self.__requester, response.json())

    def get_conversations(self, **kwargs):
        """
        Return list of conversations for the current user, most resent ones first.

        :calls: `GET /api/v1/conversations \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of \
        :class:`canvasapi.conversation.Conversation`
        """
        from canvasapi.conversation import Conversation

        return PaginatedList(
            Conversation,
            self.__requester,
            'GET',
            'conversations',
            _kwargs=combine_kwargs(**kwargs)
        )

    def conversations_mark_all_as_read(self):
        """
        Mark all conversations as read.

        :calls: `POST /api/v1/conversations/mark_all_as_read \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.mark_all_as_read>`_

        :rtype: `bool`
        """
        response = self.__requester.request(
            'POST',
            'conversations/mark_all_as_read'
        )
        return response.json() == {}

    def conversations_unread_count(self):
        """
        Get the number of unread conversations for the current user

        :calls: `GET /api/v1/conversations/unread_count \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.unread_count>`_

        :returns: simple object with unread_count, example: {'unread_count': '7'}
        :rtype: `dict`
        """
        response = self.__requester.request(
            'GET',
            'conversations/unread_count'
        )

        return response.json()

    def conversations_get_running_batches(self):
        """
        Returns any currently running conversation batches for the current user.
        Conversation batches are created when a bulk private message is sent
        asynchronously.

        :calls: `GET /api/v1/conversations/batches \
            <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batches>`_

        :returns: dict with list of batch objects - not currently a Class
        :rtype: `dict`
        """

        response = self.__requester.request(
            'GET',
            'conversations/batches'
        )

        return response.json()

    def conversations_batch_update(self, conversation_ids, event):
        """

        :calls: `PUT /api/v1/conversations \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batch_update>`_

        :param conversation_ids: List of conversations to update. Limited to 500 conversations.
        :type conversation_ids: `list` of `str`
        :param event: The action to take on each conversation.
        :type event: `str`
        :rtype: :class:`canvasapi.progress.Progress`
        """

        from canvasapi.progress import Progress

        ALLOWED_EVENTS = [
            'mark_as_read',
            'mark_as_unread',
            'star',
            'unstar',
            'archive',
            'destroy'
        ]

        try:
            if event not in ALLOWED_EVENTS:
                raise ValueError(
                    '{} is not a valid action. Please use one of the following: {}'.format(
                        event,
                        ','.join(ALLOWED_EVENTS)
                    )
                )

            if len(conversation_ids) > 500:
                raise ValueError(
                    'You have requested {} updates, which exceeds the limit of 500'.format(
                        len(conversation_ids)
                    )
                )

            response = self.__requester.request(
                'PUT',
                'conversations',
                event=event,
                **{"conversation_ids[]": conversation_ids}
            )
            return_progress = Progress(self.__requester, response.json())
            return return_progress

        except ValueError as e:
            return e

    def create_calendar_event(self, calendar_event, **kwargs):
        """
        Create a new Calendar Event.

        :calls: `POST /api/v1/calendar_events \
        <https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.create>`_

        :param calendar_event: The attributes of the calendar event.
        :type calendar_event: `dict`
        :rtype: :class:`canvasapi.calendar_event.CalendarEvent`
        """
        from canvasapi.calendar_event import CalendarEvent

        if isinstance(calendar_event, dict) and 'context_code' in calendar_event:
            kwargs['calendar_event'] = calendar_event
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'context_codes' is required."
            )

        response = self.__requester.request(
            'POST',
            'calendar_events',
            _kwargs=combine_kwargs(**kwargs)
        )

        return CalendarEvent(self.__requester, response.json())

    def list_calendar_events(self, **kwargs):
        """
        List calendar events.

        :calls: `GET /api/v1/calendar_events \
        <https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.calendar_event.CalendarEvent`
        """
        from canvasapi.calendar_event import CalendarEvent

        return PaginatedList(
            CalendarEvent,
            self.__requester,
            'GET',
            'calendar_events',
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_calendar_event(self, calendar_event):
        """
        Return single Calendar Event by id

        :calls: `GET /api/v1/calendar_events/:id \
        <https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.show>`_

        :param calendar_event: The object or ID of the calendar event.
        :type calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int

        :rtype: :class:`canvasapi.calendar_event.CalendarEvent`
        """
        from canvasapi.calendar_event import CalendarEvent

        calendar_event_id = obj_or_id(calendar_event, "calendar_event", (CalendarEvent,))

        response = self.__requester.request(
            'GET',
            'calendar_events/{}'.format(calendar_event_id)
        )
        return CalendarEvent(self.__requester, response.json())

    def reserve_time_slot(self, calendar_event, participant_id=None, **kwargs):
        """
        Return single Calendar Event by id

        :calls: `POST /api/v1/calendar_events/:id/reservations \
        <https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.reserve>`_

        :param calendar_event: The object or ID of the calendar event.
        :type calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int

        :param participant_id: The ID of the participant, if given.
        :type participant_id: str

        :rtype: :class:`canvasapi.calendar_event.CalendarEvent`
        """
        from canvasapi.calendar_event import CalendarEvent

        calendar_event_id = obj_or_id(calendar_event, "calendar_event", (CalendarEvent,))

        if participant_id:
            uri = 'calendar_events/{}/reservations/{}'.format(
                calendar_event_id, participant_id
            )
        else:
            uri = 'calendar_events/{}/reservations'.format(calendar_event_id)

        response = self.__requester.request(
            'POST',
            uri,
            _kwargs=combine_kwargs(**kwargs)
        )
        return CalendarEvent(self.__requester, response.json())

    def list_appointment_groups(self, **kwargs):
        """
        List appointment groups.

        :calls: `GET /api/v1/appointment_groups \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.appointment_group.AppointmentGroup`
        """
        from canvasapi.appointment_group import AppointmentGroup

        return PaginatedList(
            AppointmentGroup,
            self.__requester,
            'GET',
            'appointment_groups',
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_appointment_group(self, appointment_group):
        """
        Return single Appointment Group by id

        :calls: `GET /api/v1/appointment_groups/:id \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.show>`_

        :param appointment_group: The ID of the appointment group.
        :type appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int

        :rtype: :class:`canvasapi.appointment_group.AppointmentGroup`
        """
        from canvasapi.appointment_group import AppointmentGroup

        appointment_group_id = obj_or_id(
            appointment_group, "appointment_group", (AppointmentGroup,)
        )

        response = self.__requester.request(
            'GET',
            'appointment_groups/{}'.format(appointment_group_id)
        )
        return AppointmentGroup(self.__requester, response.json())

    def create_appointment_group(self, appointment_group, **kwargs):
        """
        Create a new Appointment Group.

        :calls: `POST /api/v1/appointment_groups \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.create>`_

        :param appointment_group: The attributes of the appointment group.
        :type appointment_group: `dict`
        :param title: The title of the appointment group.
        :type title: `str`
        :rtype: :class:`canvasapi.appointment_group.AppointmentGroup`
        """
        from canvasapi.appointment_group import AppointmentGroup

        if (
                isinstance(appointment_group, dict) and
                'context_codes' in appointment_group and
                'title' in appointment_group
        ):
            kwargs['appointment_group'] = appointment_group

        elif (
            isinstance(appointment_group, dict) and
            'context_codes' not in appointment_group
        ):
            raise RequiredFieldMissing(
                "Dictionary with key 'context_codes' is missing."
            )

        elif isinstance(appointment_group, dict) and 'title' not in appointment_group:
            raise RequiredFieldMissing("Dictionary with key 'title' is missing.")

        response = self.__requester.request(
            'POST',
            'appointment_groups',
            _kwargs=combine_kwargs(**kwargs)
        )

        return AppointmentGroup(self.__requester, response.json())

    def list_user_participants(self, appointment_group, **kwargs):
        """
        List user participants in this appointment group.

        :calls: `GET /api/v1/appointment_groups/:id/users \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.users>`_

        :param appointment_group: The object or ID of the appointment group.
        :type appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.user.User`
        """
        from canvasapi.appointment_group import AppointmentGroup
        from canvasapi.user import User

        appointment_group_id = obj_or_id(
            appointment_group, "appointment_group", (AppointmentGroup,)
        )

        return PaginatedList(
            User,
            self.__requester,
            'GET',
            'appointment_groups/{}/users'.format(appointment_group_id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_group_participants(self, appointment_group, **kwargs):
        """
        List student group participants in this appointment group.

        :calls: `GET /api/v1/appointment_groups/:id/groups \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.groups>`_

        :param appointment_group: The object or ID of the appointment group.
        :type appointment_group: :class:`canvasapi.appointment_group.AppointmentGroup` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.group.Group`
        """
        from canvasapi.appointment_group import AppointmentGroup
        from canvasapi.group import Group

        appointment_group_id = obj_or_id(
            appointment_group, "appointment_group", (AppointmentGroup,)
        )

        return PaginatedList(
            Group,
            self.__requester,
            'GET',
            'appointment_groups/{}/groups'.format(appointment_group_id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_file(self, file, **kwargs):
        """
        Return the standard attachment json object for a file.

        :calls: `GET /api/v1/files/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_

        :param file: The object or ID of the file to retrieve.
        :type file: :class:`canvasapi.file.File` or int

        :rtype: :class:`canvasapi.file.File`
        """
        file_id = obj_or_id(file, "file", (File,))

        response = self.__requester.request(
            'GET',
            'files/{}'.format(file_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return File(self.__requester, response.json())

    def get_folder(self, folder):
        """
        Return the details for a folder

        :calls: `GET /api/v1/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi.folder.Folder` or int

        :rtype: :class:`canvasapi.folder.Folder`
        """
        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self.__requester.request(
            'GET',
            'folders/{}'.format(folder_id)
        )
        return Folder(self.__requester, response.json())

    def search_recipients(self, **kwargs):
        """
        Find valid recipients (users, courses and groups) that the current user
        can send messages to.
        Returns a list of mixed data types.

        :calls: `GET /api/v1/search/recipients  \
        <https://canvas.instructure.com/doc/api/search.html#method.search.recipients>`_

        :rtype: `list`
        """
        if 'search' not in kwargs:
            kwargs['search'] = ' '

        response = self.__requester.request(
            'GET',
            'search/recipients',
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def search_all_courses(self, **kwargs):
        """
        List all the courses visible in the public index.
        Returns a list of dicts, each containing a single course.

        :calls: `GET /api/v1/search/all_courses \
        <https://canvas.instructure.com/doc/api/search.html#method.search.all_courses>`_

        :rtype: `list`
        """
        response = self.__requester.request(
            'GET',
            'search/all_courses',
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def get_outcome(self, outcome):
        """
        Returns the details of the outcome with the given id.

        :calls: `GET /api/v1/outcomes/:id \
        <https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show>`_

        :param outcome: The outcome object or ID to return.
        :type outcome: :class:`canvasapi.outcome.Outcome` or int

        :returns: An Outcome object.
        :rtype: :class:`canvasapi.outcome.Outcome`
        """
        from canvasapi.outcome import Outcome

        outcome_id = obj_or_id(outcome, "outcome", (Outcome,))
        response = self.__requester.request(
            'GET',
            'outcomes/{}'.format(outcome_id)
        )
        return Outcome(self.__requester, response.json())

    def get_root_outcome_group(self):
        """
        Redirect to root outcome group for context

        :calls: `GET /api/v1/global/root_outcome_group \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect>`_

        :returns: The OutcomeGroup of the context.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        response = self.__requester.request(
            'GET',
            'global/root_outcome_group'
        )
        return OutcomeGroup(self.__requester, response.json())

    def get_outcome_group(self, group):
        """
        Returns the details of the Outcome Group with the given id.

        :calls: `GET /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :param group: The outcome group object or ID to return.
        :type group: :class:`canvasapi.outcome.OutcomeGroup` or int

        :returns: An outcome group object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        outcome_group_id = obj_or_id(group, "group", (OutcomeGroup,))

        response = self.__requester.request(
            'GET',
            'global/outcome_groups/{}'.format(outcome_group_id)
        )

        return OutcomeGroup(self.__requester, response.json())
