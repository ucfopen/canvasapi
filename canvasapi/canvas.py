import warnings

from canvasapi.account import Account
from canvasapi.comm_message import CommMessage
from canvasapi.course import Course
from canvasapi.course_epub_export import CourseEpubExport
from canvasapi.current_user import CurrentUser
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.file import File
from canvasapi.folder import Folder
from canvasapi.group import Group, GroupCategory
from canvasapi.paginated_list import PaginatedList
from canvasapi.requester import Requester
from canvasapi.section import Section
from canvasapi.todo import Todo
from canvasapi.user import User
from canvasapi.util import combine_kwargs, get_institution_url, obj_or_id


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
        if "api/v1" in base_url:
            raise ValueError(
                "`base_url` should not specify an API version. Remove trailing /api/v1/"
            )

        if "http://" in base_url:
            warnings.warn(
                "Canvas may respond unexpectedly when making requests to HTTP "
                "URLs. If possible, please use HTTPS.",
                UserWarning,
            )

        if not base_url.strip():
            warnings.warn(
                "Canvas needs a valid URL, please provide a non-blank `base_url`.",
                UserWarning,
            )

        if "://" not in base_url:
            warnings.warn(
                "An invalid `base_url` for the Canvas API Instance was used. "
                "Please provide a valid HTTP or HTTPS URL if possible.",
                UserWarning,
            )

        # Ensure that the user-supplied access token and base_url contain no leading or
        # trailing spaces that might cause issues when communicating with the API.
        access_token = access_token.strip()
        base_url = get_institution_url(base_url)

        self.__requester = Requester(base_url, access_token)

    def clear_course_nicknames(self, **kwargs):
        """
        Remove all stored course nicknames.

        :calls: `DELETE /api/v1/users/self/course_nicknames \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.clear>`_

        :returns: True if the nicknames were cleared, False otherwise.

        :rtype: bool
        """

        response = self.__requester.request(
            "DELETE",
            "users/self/course_nicknames",
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json().get("message") == "OK"

    def conversations_batch_update(self, conversation_ids, event, **kwargs):
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
            "mark_as_read",
            "mark_as_unread",
            "star",
            "unstar",
            "archive",
            "destroy",
        ]

        if event not in ALLOWED_EVENTS:
            raise ValueError(
                "{} is not a valid action. Please use one of the following: {}".format(
                    event, ",".join(ALLOWED_EVENTS)
                )
            )

        if len(conversation_ids) > 500:
            raise ValueError(
                "You have requested {} updates, which exceeds the limit of 500".format(
                    len(conversation_ids)
                )
            )

        kwargs["conversation_ids"] = conversation_ids
        kwargs["event"] = event

        response = self.__requester.request(
            "PUT",
            "conversations",
            _kwargs=combine_kwargs(**kwargs),
        )
        return_progress = Progress(self.__requester, response.json())
        return return_progress

    def conversations_get_running_batches(self, **kwargs):
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
            "GET", "conversations/batches", _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def conversations_mark_all_as_read(self, **kwargs):
        """
        Mark all conversations as read.

        :calls: `POST /api/v1/conversations/mark_all_as_read \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.mark_all_as_read>`_

        :rtype: `bool`
        """
        response = self.__requester.request(
            "POST", "conversations/mark_all_as_read", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json() == {}

    def conversations_unread_count(self, **kwargs):
        """
        Get the number of unread conversations for the current user

        :calls: `GET /api/v1/conversations/unread_count \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.unread_count>`_

        :returns: simple object with unread_count, example: {'unread_count': '7'}
        :rtype: `dict`
        """
        response = self.__requester.request(
            "GET", "conversations/unread_count", _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def create_account(self, **kwargs):
        """
        Create a new root account.

        :calls: `POST /api/v1/accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`_

        :rtype: :class:`canvasapi.account.Account`
        """
        response = self.__requester.request(
            "POST", "accounts", _kwargs=combine_kwargs(**kwargs)
        )
        return Account(self.__requester, response.json())

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
            isinstance(appointment_group, dict)
            and "context_codes" in appointment_group
            and "title" in appointment_group
        ):
            kwargs["appointment_group"] = appointment_group

        elif (
            isinstance(appointment_group, dict)
            and "context_codes" not in appointment_group
        ):
            raise RequiredFieldMissing(
                "Dictionary with key 'context_codes' is missing."
            )

        elif isinstance(appointment_group, dict) and "title" not in appointment_group:
            raise RequiredFieldMissing("Dictionary with key 'title' is missing.")

        response = self.__requester.request(
            "POST", "appointment_groups", _kwargs=combine_kwargs(**kwargs)
        )

        return AppointmentGroup(self.__requester, response.json())

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

        if isinstance(calendar_event, dict) and "context_code" in calendar_event:
            kwargs["calendar_event"] = calendar_event
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'context_codes' is required."
            )

        response = self.__requester.request(
            "POST", "calendar_events", _kwargs=combine_kwargs(**kwargs)
        )

        return CalendarEvent(self.__requester, response.json())

    def create_conversation(self, recipients, body, **kwargs):
        """
        Create a new Conversation.

        :calls: `POST /api/v1/conversations \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.create>`_

        :param recipients: An array of recipient ids.
            These may be user ids or course/group ids prefixed
            with 'course\\_' or 'group\\_' respectively,
            e.g. recipients=['1', '2', 'course_3']
        :type recipients: `list` of `str`
        :param body: The body of the message being added.
        :type body: `str`
        :rtype: list of :class:`canvasapi.conversation.Conversation`
        """
        from canvasapi.conversation import Conversation

        kwargs["recipients"] = recipients
        kwargs["body"] = body

        response = self.__requester.request(
            "POST", "conversations", _kwargs=combine_kwargs(**kwargs)
        )
        return [Conversation(self.__requester, convo) for convo in response.json()]

    def create_group(self, **kwargs):
        """
        Create a group

        :calls: `POST /api/v1/groups/ \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.create>`_

        :rtype: :class:`canvasapi.group.Group`
        """
        response = self.__requester.request(
            "POST", "groups", _kwargs=combine_kwargs(**kwargs)
        )
        return Group(self.__requester, response.json())

    def create_planner_note(self, **kwargs):
        """
        Create a planner note for the current user

        :calls: `POST /api/v1/planner_notes \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.create>`_

        :rtype: :class:`canvasapi.planner.PlannerNote`
        """
        from canvasapi.planner import PlannerNote

        response = self.__requester.request(
            "POST", "planner_notes", _kwargs=combine_kwargs(**kwargs)
        )
        return PlannerNote(self.__requester, response.json())

    def create_planner_override(self, plannable_type, plannable_id, **kwargs):
        """
        Create a planner override for the current user

        :calls: `POST /api/v1/planner/overrides \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.create>`_

        :param plannable_type: Type of the item that you are overriding in the planner
        :type plannable_type: str

        :param plannable_id: ID of the item that you are overriding in the planner
        :type plannable_id: int or :class:`canvasapi.planner.PlannerOverride`

        :rtype: :class:`canvasapi.planner.PlannerOverride`
        """
        from canvasapi.planner import PlannerOverride

        if isinstance(plannable_type, str):
            kwargs["plannable_type"] = plannable_type
        else:
            raise RequiredFieldMissing("plannable_type is required as a str.")
        if isinstance(plannable_id, int):
            kwargs["plannable_id"] = plannable_id
        else:
            raise RequiredFieldMissing("plannable_id is required as an int.")

        response = self.__requester.request(
            "POST", "planner/overrides", _kwargs=combine_kwargs(**kwargs)
        )
        return PlannerOverride(self.__requester, response.json())

    def create_poll(self, polls, **kwargs):
        """
        Create a new poll for the current user.

        :calls: `POST /api/v1/polls \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.create>`_

        :param polls: List of polls to create. `'question'` key is required.
        :type polls: list of dict
        :rtype: :class:`canvasapi.poll.Poll`
        """
        from canvasapi.poll import Poll

        if (
            isinstance(polls, list)
            and isinstance(polls[0], dict)
            and "question" in polls[0]
        ):
            kwargs["polls"] = polls
        else:
            raise RequiredFieldMissing(
                "List of dictionaries each with key 'question' is required."
            )

        response = self.__requester.request(
            "POST", "polls", _kwargs=combine_kwargs(**kwargs)
        )
        return Poll(self.__requester, response.json()["polls"][0])

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
            uri_str = "accounts/sis_account_id:{}"
        else:
            account_id = obj_or_id(account, "account", (Account,))
            uri_str = "accounts/{}"

        response = self.__requester.request(
            "GET", uri_str.format(account_id), _kwargs=combine_kwargs(**kwargs)
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
            "GET",
            "accounts",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_activity_stream_summary(self, **kwargs):
        """
        Return a summary of the current user's global activity stream.

        :calls: `GET /api/v1/users/self/activity_stream/summary \
        <https://canvas.instructure.com/doc/api/users.html#method.users.activity_stream_summary>`_

        :rtype: dict
        """
        response = self.__requester.request(
            "GET",
            "users/self/activity_stream/summary",
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_announcements(self, context_codes, **kwargs):
        """
        List announcements.

        :calls: `GET /api/v1/announcements \
        <https://canvas.instructure.com/doc/api/announcements.html#method.announcements_api.index>`_

        :param context_codes: Course ID(s) or <Course> objects to request announcements from.
        :type context_codes: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
                :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        from canvasapi.discussion_topic import DiscussionTopic

        if type(context_codes) is not list or len(context_codes) == 0:
            raise RequiredFieldMissing("context_codes need to be passed as a list")

        if isinstance(context_codes[0], str) and "course_" in context_codes[0]:
            # Legacy support for context codes passed as list of `course_123`-style strings
            kwargs["context_codes"] = context_codes
        else:
            # The type of object in `context_codes` is taken care of by obj_or_id, extracting
            # the course ID from a <Course> object or by returning plain strings.
            course_ids = [
                obj_or_id(course_id, "context_codes", (Course,))
                for course_id in context_codes
            ]

            # Set the **kwargs object vaue so it can be combined with others passed by the user.
            kwargs["context_codes"] = [
                f"course_{course_id}" for course_id in course_ids
            ]

        return PaginatedList(
            DiscussionTopic,
            self.__requester,
            "GET",
            "announcements",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_appointment_group(self, appointment_group, **kwargs):
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
            "GET",
            "appointment_groups/{}".format(appointment_group_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return AppointmentGroup(self.__requester, response.json())

    def get_appointment_groups(self, **kwargs):
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
            "GET",
            "appointment_groups",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_brand_variables(self, **kwargs):
        """
        Get account brand variables

        :calls: `GET /api/v1/brand_variables \
        <https://canvas.instructure.com/doc/api/brand_configs.html>`_

        :returns: JSON with brand variables for the account.
        :rtype: dict
        """
        response = self.__requester.request(
            "GET", "brand_variables", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def get_calendar_event(self, calendar_event, **kwargs):
        """
        Return single Calendar Event by id

        :calls: `GET /api/v1/calendar_events/:id \
        <https://canvas.instructure.com/doc/api/calendar_events.html#method.calendar_events_api.show>`_

        :param calendar_event: The object or ID of the calendar event.
        :type calendar_event: :class:`canvasapi.calendar_event.CalendarEvent` or int

        :rtype: :class:`canvasapi.calendar_event.CalendarEvent`
        """
        from canvasapi.calendar_event import CalendarEvent

        calendar_event_id = obj_or_id(
            calendar_event, "calendar_event", (CalendarEvent,)
        )

        response = self.__requester.request(
            "GET",
            "calendar_events/{}".format(calendar_event_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return CalendarEvent(self.__requester, response.json())

    def get_calendar_events(self, **kwargs):
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
            "GET",
            "calendar_events",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_comm_messages(self, user, **kwargs):
        """
        Retrieve a paginated list of messages sent to a user.

        :calls: `GET /api/v1/comm_messages \
        <https://canvas.instructure.com/doc/api/comm_messages.html#method.comm_messages_api.index>`_

        :param user: The object or ID of the user.
        :type user: :class:`canvasapi.user.User` or int

        :returns: Paginated list containing messages sent to user
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.comm_message.CommMessage`

        """

        kwargs["user_id"] = obj_or_id(user, "user", (User,))

        return PaginatedList(
            CommMessage,
            self.__requester,
            "GET",
            "comm_messages",
            _kwargs=combine_kwargs(**kwargs),
        )

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
            "GET",
            "conversations/{}".format(conversation_id),
            _kwargs=combine_kwargs(**kwargs),
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
            "GET",
            "conversations",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_course(self, course, use_sis_id=False, **kwargs):
        """
        Retrieve a course by its ID.

        :calls: `GET /api/v1/courses/:id \
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
            uri_str = "courses/sis_course_id:{}"
        else:
            course_id = obj_or_id(course, "course", (Course,))
            uri_str = "courses/{}"

        response = self.__requester.request(
            "GET", uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Course(self.__requester, response.json())

    def get_course_accounts(self, **kwargs):
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
            "GET",
            "course_accounts",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_course_nickname(self, course, **kwargs):
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
            "GET",
            "users/self/course_nicknames/{}".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return CourseNickname(self.__requester, response.json())

    def get_course_nicknames(self, **kwargs):
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
            "GET",
            "users/self/course_nicknames",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_courses(self, **kwargs):
        """
        Return a list of active courses for the current user.

        :calls: `GET /api/v1/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        return PaginatedList(
            Course, self.__requester, "GET", "courses", _kwargs=combine_kwargs(**kwargs)
        )

    def get_current_user(self):
        """
        Return a details of the current user.

        :calls: `GET /api/v1/users/:user_id \
        <https://canvas.instructure.com/doc/api/users.html#method.current_user.show>`_

        :rtype: :class:`canvasapi.current_user.CurrentUser`
        """
        return CurrentUser(self.__requester)

    def get_epub_exports(self, **kwargs):
        """
        Return a list of epub exports for the associated course.

        :calls: `GET /api/v1/epub_exports\
        <https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course_epub_export.CourseEpubExport`
        """

        return PaginatedList(
            CourseEpubExport,
            self.__requester,
            "GET",
            "epub_exports",
            _root="courses",
            kwargs=combine_kwargs(**kwargs),
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
            "GET", "files/{}".format(file_id), _kwargs=combine_kwargs(**kwargs)
        )
        return File(self.__requester, response.json())

    def get_folder(self, folder, **kwargs):
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
            "GET", "folders/{}".format(folder_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Folder(self.__requester, response.json())

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
            uri_str = "groups/sis_group_id:{}"
        else:
            group_id = obj_or_id(group, "group", (Group,))
            uri_str = "groups/{}"

        response = self.__requester.request(
            "GET", uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Group(self.__requester, response.json())

    def get_group_category(self, category, **kwargs):
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
            "GET",
            "group_categories/{}".format(category_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return GroupCategory(self.__requester, response.json())

    def get_group_participants(self, appointment_group, **kwargs):
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
            "GET",
            "appointment_groups/{}/groups".format(appointment_group_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_outcome(self, outcome, **kwargs):
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
            "GET", "outcomes/{}".format(outcome_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Outcome(self.__requester, response.json())

    def get_outcome_group(self, group, **kwargs):
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
            "GET",
            "global/outcome_groups/{}".format(outcome_group_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return OutcomeGroup(self.__requester, response.json())

    def get_planner_note(self, planner_note, **kwargs):
        """
        Retrieve a planner note for the current user

        :calls: `GET /api/v1/planner_notes/:id \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.show>`_

        :param planner_note: The ID of the planner note to retrieve.
        :type planner_note: int or :class:`canvasapi.planner.PlannerNote`

        :rtype: :class:`canvasapi.planner.PlannerNote`
        """
        from canvasapi.planner import PlannerNote

        if isinstance(planner_note, int) or isinstance(planner_note, PlannerNote):
            planner_note_id = obj_or_id(planner_note, "planner_note", (PlannerNote,))
        else:
            raise RequiredFieldMissing(
                "planner_note is required as an object or as an int."
            )

        response = self.__requester.request(
            "GET",
            "planner_notes/{}".format(planner_note_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return PlannerNote(self.__requester, response.json())

    def get_planner_notes(self, **kwargs):
        """
        Retrieve the paginated list of planner notes

        :calls: `GET /api/v1/planner_notes \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.planner.PlannerNote`
        """
        from canvasapi.planner import PlannerNote

        return PaginatedList(
            PlannerNote,
            self.__requester,
            "GET",
            "planner_notes",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_planner_override(self, planner_override, **kwargs):
        """
        Retrieve a planner override for the current user

        :calls: `GET /api/v1/planner/overrides/:id \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.show>`_

        :param planner_override: The override or the ID of the planner override to retrieve.
        :type planner_override: int or :class:`canvasapi.planner.PlannerOverride`

        :rtype: :class:`canvasapi.planner.PlannerOverride`
        """
        from canvasapi.planner import PlannerOverride

        if isinstance(planner_override, int) or isinstance(
            planner_override, PlannerOverride
        ):
            planner_override_id = obj_or_id(
                planner_override, "planner_override", (PlannerOverride,)
            )
        else:
            raise RequiredFieldMissing(
                "planner_override is required as an object or as an int."
            )

        response = self.__requester.request(
            "GET",
            "planner/overrides/{}".format(planner_override_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return PlannerOverride(self.__requester, response.json())

    def get_planner_overrides(self, **kwargs):
        """
        Retrieve a planner override for the current user

        :calls: `GET /api/v1/planner/overrides \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.planner.PlannerOverride`
        """
        from canvasapi.planner import PlannerOverride

        return PaginatedList(
            PlannerOverride,
            self.__requester,
            "GET",
            "planner/overrides",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_poll(self, poll, **kwargs):
        """
        Get a single poll, based on the poll id.

        :calls: `GET /api/v1/polls/:id \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.show>`_

        :param poll: The ID of the poll or the poll to change.
        :type poll: int
        :rtype: :class:`canvasapi.poll.Poll`
        """
        from canvasapi.poll import Poll

        poll_id = obj_or_id(poll, "poll", (Poll,))

        response = self.__requester.request(
            "GET", "polls/{}".format(poll_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Poll(self.__requester, response.json()["polls"][0])

    def get_polls(self, **kwargs):
        """
        Returns a paginated list of polls for the current user

        :calls: `GET /api/1/polls \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.poll.Poll`
        """
        from canvasapi.poll import Poll

        return PaginatedList(
            Poll,
            self.__requester,
            "GET",
            "polls",
            _root="polls",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_progress(self, progress, **kwargs):
        """
        Get a specific progress.

        :calls: `GET /api/v1/progress/:id
            <https://canvas.instructure.com/doc/api/progress.html#method.progress.show>`_

        :param progress: The object or ID of the progress to retrieve.
        :type progress: int, str or :class:`canvasapi.progress.Progress`

        :rtype: :class:`canvasapi.progress.Progress`
        """

        from canvasapi.progress import Progress

        progress_id = obj_or_id(progress, "progress", (Progress,))

        response = self.__requester.request(
            "GET", "progress/{}".format(progress_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Progress(self.__requester, response.json())

    def get_root_outcome_group(self, **kwargs):
        """
        Redirect to root outcome group for context

        :calls: `GET /api/v1/global/root_outcome_group \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect>`_

        :returns: The OutcomeGroup of the context.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        response = self.__requester.request(
            "GET", "global/root_outcome_group", _kwargs=combine_kwargs(**kwargs)
        )
        return OutcomeGroup(self.__requester, response.json())

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
            uri_str = "sections/sis_section_id:{}"
        else:
            section_id = obj_or_id(section, "section", (Section,))
            uri_str = "sections/{}"

        response = self.__requester.request(
            "GET", uri_str.format(section_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Section(self.__requester, response.json())

    def get_todo_items(self, **kwargs):
        """
        Return the current user's list of todo items, as seen on the user dashboard.

        :calls: `GET /api/v1/users/self/todo \
        <https://canvas.instructure.com/doc/api/users.html#method.users.todo_items>`_

        :rtype: dict
        """
        return PaginatedList(
            Todo,
            self.__requester,
            "GET",
            "users/self/todo",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_upcoming_events(self, **kwargs):
        """
        Return the current user's upcoming events, i.e. the same things shown
        in the dashboard 'Coming Up' sidebar.

        :calls: `GET /api/v1/users/self/upcoming_events \
        <https://canvas.instructure.com/doc/api/users.html#method.users.upcoming_events>`_

        :rtype: dict
        """
        response = self.__requester.request(
            "GET", "users/self/upcoming_events", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def get_user(self, user, id_type=None, **kwargs):
        """
        Retrieve a user by their ID. `id_type` denotes which endpoint to try as there are
        several different IDs that can pull the same user record from Canvas.

        Refer to API documentation's
        `User <https://canvas.instructure.com/doc/api/users.html#User>`_
        example to see the ID types a user can be retrieved with.

        :calls: `GET /api/v1/users/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>`_

        :param user: The user's object or ID.
        :type user: :class:`canvasapi.user.User` or int
        :param id_type: The ID type.
        :type id_type: str

        :rtype: :class:`canvasapi.user.User`
        """
        if id_type:
            uri = "users/{}:{}".format(id_type, user)
        elif user == "self":
            uri = "users/self"
        else:
            user_id = obj_or_id(user, "user", (User,))
            uri = "users/{}".format(user_id)

        response = self.__requester.request(
            "GET", uri, _kwargs=combine_kwargs(**kwargs)
        )
        return User(self.__requester, response.json())

    def get_user_participants(self, appointment_group, **kwargs):
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
            "GET",
            "appointment_groups/{}/users".format(appointment_group_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def graphql(self, query, variables=None, **kwargs):
        """
        Makes a GraphQL formatted request to Canvas

        :calls: `POST /api/graphql \
        <https://canvas.instructure.com/doc/api/file.graphql.html>`_

        :param query: The GraphQL query to execute as a String
        :type query: str
        :param variables: The variable values as required by the supplied query
        :type variables: dict

        :rtype: dict
        """
        response = self.__requester.request(
            "POST",
            "graphql",
            headers={"Content-Type": "application/json"},
            _kwargs=combine_kwargs(**kwargs)
            + [("query", query), ("variables", variables)],
            # Needs to call special endpoint without api/v1
            _url=self.__requester.original_url + "/api/graphql",
            json=True,
        )

        return response.json()

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

        calendar_event_id = obj_or_id(
            calendar_event, "calendar_event", (CalendarEvent,)
        )

        if participant_id:
            uri = "calendar_events/{}/reservations/{}".format(
                calendar_event_id, participant_id
            )
        else:
            uri = "calendar_events/{}/reservations".format(calendar_event_id)

        response = self.__requester.request(
            "POST", uri, _kwargs=combine_kwargs(**kwargs)
        )
        return CalendarEvent(self.__requester, response.json())

    def search_accounts(self, **kwargs):
        """
        Return a list of up to 5 matching account domains. Partial matches on
        name and domain are supported.

        :calls: `GET /api/v1/accounts/search \
        <https://canvas.instructure.com/doc/api/account_domain_lookups.html#method.account_domain_lookups.search>`_

        :rtype: dict
        """
        response = self.__requester.request(
            "GET", "accounts/search", _kwargs=combine_kwargs(**kwargs)
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
            "GET", "search/all_courses", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def search_recipients(self, **kwargs):
        """
        Find valid recipients (users, courses and groups) that the current user
        can send messages to.
        Returns a list of mixed data types.

        :calls: `GET /api/v1/search/recipients  \
        <https://canvas.instructure.com/doc/api/search.html#method.search.recipients>`_

        :rtype: `list`
        """
        if "search" not in kwargs:
            kwargs["search"] = " "

        response = self.__requester.request(
            "GET", "search/recipients", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()

    def set_course_nickname(self, course, nickname, **kwargs):
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

        kwargs["nickname"] = nickname

        response = self.__requester.request(
            "PUT",
            "users/self/course_nicknames/{}".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return CourseNickname(self.__requester, response.json())
