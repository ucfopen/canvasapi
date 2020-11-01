from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import CanvasException, RequiredFieldMissing
from canvasapi.feature import Feature, FeatureFlag
from canvasapi.grading_period import GradingPeriod
from canvasapi.grading_standard import GradingStandard
from canvasapi.outcome_import import OutcomeImport
from canvasapi.paginated_list import PaginatedList
from canvasapi.rubric import Rubric
from canvasapi.sis_import import SisImport
from canvasapi.util import combine_kwargs, file_or_path, obj_or_id, obj_or_str


class Account(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def abort_sis_imports_pending(self, **kwargs):
        """
        Aborts all pending (created, but not processed or processing)
        SIS imports for the current account.

        :calls: `PUT /api/v1/accounts/:account_id/sis_imports/abort_all_pending \
        <https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort_all_pending>`_

        :returns: True if the API responds with aborted=True, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            "PUT",
            "accounts/{}/sis_imports/abort_all_pending".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json().get("aborted", False)

    def activate_role(self, role, **kwargs):
        """
        Reactivate an inactive role.

        :calls: `POST /api/v1/accounts/:account_id/roles/:id/activate \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.activate_role>`_

        :param role: The object or ID of the role.
        :type role: :class:`canvasapi.account.Role` or int
        :rtype: :class:`canvasapi.account.Role`
        """
        role_id = obj_or_id(role, "role", (Role,))

        response = self._requester.request(
            "POST",
            "accounts/{}/roles/{}/activate".format(self.id, role_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Role(self._requester, response.json())

    def add_authentication_providers(self, **kwargs):
        """
        Add external authentication providers for the account

        :calls: `POST /api/v1/accounts/:account_id/authentication_providers \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.create>`_

        :rtype: :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        from canvasapi.authentication_provider import AuthenticationProvider

        response = self._requester.request(
            "POST",
            "accounts/{}/authentication_providers".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        authentication_providers_json = response.json()
        authentication_providers_json.update({"account_id": self.id})

        return AuthenticationProvider(self._requester, authentication_providers_json)

    def add_grading_standards(self, title, grading_scheme_entry, **kwargs):
        """
        Create a new grading standard for the account.

        :calls: `POST /api/v1/accounts/:account_id/grading_standards \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create>`_

        :param title: The title for the Grading Standard
        :type title: str
        :param grading_scheme: A list of dictionaries containing keys for "name" and "value"
        :type grading_scheme: list[dict]
        :rtype: :class:`canvasapi.grading_standards.GradingStandard`
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError("Param `grading_scheme_entry` must be a non-empty list.")

        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError("grading_scheme_entry must consist of dictionaries.")
            if "name" not in entry or "value" not in entry:
                raise ValueError(
                    "Dictionaries with keys 'name' and 'value' are required."
                )
        kwargs["grading_scheme_entry"] = grading_scheme_entry

        response = self._requester.request(
            "POST",
            "accounts/%s/grading_standards" % (self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs),
        )

        return GradingStandard(self._requester, response.json())

    def close_notification_for_user(self, user, notification, **kwargs):
        """
        If the user no long wants to see a notification, it can be
        excused with this call.

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id/account_notifications/:id \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_close_notification>`_

        :param user: The user object or ID to close the notificaton for.
        :type user: :class:`canvasapi.user.User` or int
        :param notification: The notification object or ID to close.
        :type notification: :class:`canvasapi.account.AccountNotification` or int

        :rtype: :class:`canvasapi.account.AccountNotification`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))
        notif_id = obj_or_id(notification, "notification", (AccountNotification,))

        response = self._requester.request(
            "DELETE",
            "accounts/{}/users/{}/account_notifications/{}".format(
                self.id, user_id, notif_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return AccountNotification(self._requester, response.json())

    def create_account(self, **kwargs):
        """
        Create a new root account.

        :calls: `POST /api/v1/accounts/:account_id/root_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`_

        :rtype: :class:`canvasapi.account.Account`
        """
        response = self._requester.request(
            "POST",
            "accounts/{}/root_accounts".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Account(self._requester, response.json())

    def create_admin(self, user, **kwargs):
        """
        Flag an existing user as an admin of the current account.

        :calls: `POST /api/v1/accounts/:account_id/admins \
        <https://canvas.instructure.com/doc/api/admins.html#method.admins.create>`_

        :param user: The user object or ID to promote to admin.
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.account.Admin`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))
        kwargs["user_id"] = user_id

        response = self._requester.request(
            "POST",
            "accounts/{}/admins".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Admin(self._requester, response.json())

    def create_content_migration(self, migration_type, **kwargs):
        """
        Create a content migration.

        :calls: `POST /api/v1/accounts/:account_id/content_migrations \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create>`_

        :param migration_type: The migrator type to use in this migration
        :type migration_type: str or :class:`canvasapi.content_migration.Migrator`

        :rtype: :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration, Migrator

        if isinstance(migration_type, Migrator):
            kwargs["migration_type"] = migration_type.type
        elif isinstance(migration_type, str):
            kwargs["migration_type"] = migration_type
        else:
            raise TypeError("Parameter migration_type must be of type Migrator or str")

        response = self._requester.request(
            "POST",
            "accounts/{}/content_migrations".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return ContentMigration(self._requester, response_json)

    def create_course(self, **kwargs):
        """
        Create a course.

        :calls: `POST /api/v1/accounts/:account_id/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        from canvasapi.course import Course

        response = self._requester.request(
            "POST",
            "accounts/{}/courses".format(self.id),
            account_id=self.id,
            _kwargs=combine_kwargs(**kwargs),
        )
        return Course(self._requester, response.json())

    def create_enrollment_term(self, **kwargs):
        """
        Create an enrollment term.

        :calls: `POST /api/v1/accounts/:account_id/terms \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.create>`_

        :rtype: :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        from canvasapi.enrollment_term import EnrollmentTerm

        response = self._requester.request(
            "POST",
            "accounts/{}/terms".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        enrollment_term_json = response.json()
        enrollment_term_json.update({"account_id": self.id})

        return EnrollmentTerm(self._requester, enrollment_term_json)

    def create_external_tool(
        self, name, privacy_level, consumer_key, shared_secret, **kwargs
    ):
        """
        Create an external tool in the current account.

        :calls: `POST /api/v1/accounts/:account_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create>`_

        :param name: The name of the tool
        :type name: str
        :param privacy_level: What information to send to the external
            tool. Options are "anonymous", "name_only", "public"
        :type privacy_level: str
        :param consumer_key: The consumer key for the external tool
        :type consumer_key: str
        :param shared_secret: The shared secret with the external tool
        :type shared_secret: str
        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        response = self._requester.request(
            "POST",
            "accounts/{}/external_tools".format(self.id),
            name=name,
            privacy_level=privacy_level,
            consumer_key=consumer_key,
            shared_secret=shared_secret,
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"account_id": self.id})

        return ExternalTool(self._requester, response_json)

    def create_group_category(self, name, **kwargs):
        """
        Create a Group Category

        :calls: `POST /api/v1/accounts/:account_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create>`_

        :param name: Name of group category.
        :type name: str
        :rtype: :class:`canvasapi.group.GroupCategory`
        """
        from canvasapi.group import GroupCategory

        response = self._requester.request(
            "POST",
            "accounts/{}/group_categories".format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs),
        )
        return GroupCategory(self._requester, response.json())

    def create_notification(self, account_notification, **kwargs):
        """
        Create and return a new global notification for an account.

        :calls: `POST /api/v1/accounts/:account_id/account_notifications \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.create>`_

        :param account_notification: The notification to create.
        :type account_notification: dict
        :rtype: :class:`canvasapi.account.AccountNotification`
        """
        required_key_list = ["subject", "message", "start_at", "end_at"]
        required_keys_present = all(
            (x in account_notification for x in required_key_list)
        )

        if isinstance(account_notification, dict) and required_keys_present:
            kwargs["account_notification"] = account_notification
        else:
            raise RequiredFieldMissing(
                (
                    "account_notification must be a dictionary with keys "
                    "'subject', 'message', 'start_at', and 'end_at'."
                )
            )

        response = self._requester.request(
            "POST",
            "accounts/{}/account_notifications".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return AccountNotification(self._requester, response_json)

    def create_report(self, report_type, **kwargs):
        """
        Generates a report of a specific type for the account.

        :calls: `POST /api/v1/accounts/:account_id/reports/:report \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.create>`_

        :param report_type: The type of report.
        :type report_type: str

        :rtype: :class:`canvasapi.account.AccountReport`
        """

        response = self._requester.request(
            "POST",
            "accounts/{}/reports/{}".format(self.id, report_type),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return AccountReport(self._requester, response_json)

    def create_role(self, label, **kwargs):
        """
        Create a new course-level or account-level role.

        :calls: `POST /api/v1/accounts/:account_id/roles \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.add_role>`_

        :param label: The label for the role.
        :type label: str
        :rtype: :class:`canvasapi.account.Role`
        """
        response = self._requester.request(
            "POST",
            "accounts/{}/roles".format(self.id),
            label=label,
            _kwargs=combine_kwargs(**kwargs),
        )
        return Role(self._requester, response.json())

    def create_sis_import(self, attachment, **kwargs):
        """
        Create a new SIS import for the current account.

        :calls: `POST /api/v1/accounts/:account_id/sis_imports \
        <https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create>`_

        :param attachment: A file handler or path of the file to import.
        :type attachment: file or str

        :rtype: :class:`canvasapi.sis_import.SisImport`
        """

        attachment, is_path = file_or_path(attachment)

        try:
            response = self._requester.request(
                "POST",
                "accounts/{}/sis_imports".format(self.id),
                file={"attachment": attachment},
                _kwargs=combine_kwargs(**kwargs),
            )

            response_json = response.json()
            response_json.update({"account_id": self.id})

            return SisImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    def create_subaccount(self, account, **kwargs):
        """
        Add a new sub-account to a given account.

        :calls: `POST /api/v1/accounts/:account_id/sub_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.sub_accounts.create>`_

        :param account: The name of the account
        :type account: str

        :rtype: :class:`canvasapi.account.Account`
        """
        if isinstance(account, dict) and "name" in account:
            kwargs["account"] = account
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            "POST",
            "accounts/{}/sub_accounts".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Account(self._requester, response.json())

    def create_user(self, pseudonym, **kwargs):
        """
        Create and return a new user and pseudonym for an account.

        :calls: `POST /api/v1/accounts/:account_id/users \
        <https://canvas.instructure.com/doc/api/users.html#method.users.create>`_

        :param pseudonym: The pseudonym of the account.
        :type pseudonym: dict
        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        if isinstance(pseudonym, dict) and "unique_id" in pseudonym:
            kwargs["pseudonym"] = pseudonym
        else:
            raise RequiredFieldMissing("Dictionary with key 'unique_id' is required.")

        response = self._requester.request(
            "POST",
            "accounts/{}/users".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return User(self._requester, response.json())

    def create_user_login(self, user, login, **kwargs):
        """
        Create a new login for an existing user in the given account

        :calls: `POST /api/v1/accounts/:account_id/logins \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.create>`_

        :param user: The attributes of the user to create a login for
        :type user: `dict`
        :param login: The attributes of the login to create
        :type login: `dict`
        :rtype: :class:`canvasapi.login.Login`
        """
        from canvasapi.login import Login

        if isinstance(user, dict) and "id" in user:
            kwargs["user"] = user
        else:
            raise RequiredFieldMissing(("user must be a dictionary with keys " "'id'."))

        if isinstance(login, dict) and "unique_id" in login:
            kwargs["login"] = login
        else:
            raise RequiredFieldMissing(
                ("login must be a dictionary with keys " "'unique_id'.")
            )

        response = self._requester.request(
            "POST",
            "accounts/{}/logins".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Login(self._requester, response.json())

    def deactivate_role(self, role, **kwargs):
        """
        Deactivate a custom role.

        :calls: `DELETE /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.remove_role>`_

        :param role: The object or ID of the role.
        :type role: :class:`canvasapi.account.Role` or int

        :rtype: :class:`canvasapi.account.Role`
        """
        role_id = obj_or_id(role, "role", (Role,))

        response = self._requester.request(
            "DELETE",
            "accounts/{}/roles/{}".format(self.id, role_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Role(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete the current account

        Note: Cannot delete an account with active courses or active
        sub accounts. Cannot delete a root account.

        :calls: `DELETE /api/v1/accounts/:account_id/sub_accounts/:id \
        <https://canvas.beta.instructure.com/doc/api/accounts.html#method.sub_accounts.destroy>`_

        :returns: True if successfully deleted; False otherwise.
        :rtype: bool
        """
        if not hasattr(self, "parent_account_id") or not self.parent_account_id:
            raise CanvasException("Cannot delete a root account.")

        response = self._requester.request(
            "DELETE",
            "accounts/{}/sub_accounts/{}".format(self.parent_account_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json().get("workflow_state") == "deleted"

    def delete_grading_period(self, grading_period, **kwargs):
        """
        Delete a grading period for an account.

        :calls: `DELETE /api/v1/accounts/:account_id/grading_periods/:id \
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.destroy>`_

        :param grading_period: The GradingPeriod object or ID to delete.
        :type grading_period: :class:`canvasapi.grading_period.GradingPeriod` or int

        :returns: True if the grading period was deleted, False otherwise.
        :rtype: bool
        """

        grading_period_id = obj_or_id(
            grading_period, "grading_period", (GradingPeriod,)
        )

        response = self._requester.request(
            "DELETE",
            "accounts/{}/grading_periods/{}".format(self.id, grading_period_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json().get("delete")

    def delete_user(self, user, **kwargs):
        """
        Delete a user record from a Canvas root account.

        If a user is associated with multiple root accounts (in a
        multi-tenant instance of Canvas), this action will NOT remove
        them from the other accounts.

        WARNING: This API will allow a user to remove themselves from
        the account. If they do this, they won't be able to make API
        calls or log into Canvas at that account.

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.remove_user>`_

        :param user: The user object or ID to delete.
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "DELETE",
            "accounts/{}/users/{}".format(self.id, user_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return User(self._requester, response.json())

    def get_admins(self, **kwargs):
        """
        Get the paginated list of admins for the current account.

        :calls: `GET /api/v1/accounts/:account_id/admins \
        <https://canvas.instructure.com/doc/api/admins.html#method.admins.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.account.Admin`
        """

        return PaginatedList(
            Admin,
            self._requester,
            "GET",
            "accounts/{}/admins".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_all_outcome_links_in_context(self, **kwargs):
        """
        Get all outcome links for context - BETA

        :calls: `GET /api/v1/accounts/:account_id/outcome_group_links \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index>`_

        :returns: Paginated List of OutcomesLinks in the context.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeLink`
        """
        from canvasapi.outcome import OutcomeLink

        return PaginatedList(
            OutcomeLink,
            self._requester,
            "GET",
            "accounts/{}/outcome_group_links".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_authentication_events(self, **kwargs):
        """
        List authentication events for a given account.

        :calls: `GET /api/v1/audit/authentication/accounts/:account_id \
        <https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_account>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
                :class:`canvasapi.authentication_event.AuthenticationEvent`
        """
        from canvasapi.authentication_event import AuthenticationEvent

        return PaginatedList(
            AuthenticationEvent,
            self._requester,
            "GET",
            "audit/authentication/accounts/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_authentication_provider(self, authentication_provider, **kwargs):
        """
        Get the specified authentication provider

        :calls: `GET /api/v1/accounts/:account_id/authentication_providers/:id \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show>`_

        :param authentication_provider: The object or ID of the authentication provider
        :type authentication_provider:
            :class:`canvasapi.authentication_provider.AuthenticationProvider` or int

        :rtype: :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        from canvasapi.authentication_provider import AuthenticationProvider

        authentication_providers_id = obj_or_id(
            authentication_provider,
            "authentication provider",
            (AuthenticationProvider,),
        )

        response = self._requester.request(
            "GET",
            "accounts/{}/authentication_providers/{}".format(
                self.id, authentication_providers_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return AuthenticationProvider(self._requester, response.json())

    def get_authentication_providers(self, **kwargs):
        """
        Return the list of authentication providers

        :calls: `GET /api/v1/accounts/:account_id/authentication_providers \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        from canvasapi.authentication_provider import AuthenticationProvider

        return PaginatedList(
            AuthenticationProvider,
            self._requester,
            "GET",
            "accounts/{}/authentication_providers".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_content_migration(self, content_migration, **kwargs):
        """
        Retrive a content migration by its ID

        :calls: `GET /api/v1/accounts/:account_id/content_migrations/:id \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show>`_

        :param content_migration: The object or ID of the content migration to retrieve.
        :type contnet_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`

        :rtype: :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration

        migration_id = obj_or_id(
            content_migration, "content_migration", (ContentMigration,)
        )

        response = self._requester.request(
            "GET",
            "accounts/{}/content_migrations/{}".format(self.id, migration_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs):
        """
        List content migrations that the current account can view or manage.

        :calls: `GET /api/v1/accounts/:account_id/content_migrations/ \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration

        return PaginatedList(
            ContentMigration,
            self._requester,
            "GET",
            "accounts/{}/content_migrations".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_courses(self, **kwargs):
        """
        Retrieve the list of courses in this account.

        :calls: `GET /api/v1/accounts/:account_id/courses \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from canvasapi.course import Course

        return PaginatedList(
            Course,
            self._requester,
            "GET",
            "accounts/{}/courses".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_department_level_grade_data_completed(self, **kwargs):
        """
        Return the distribution of all concluded grades in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/completed/grades \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/completed/grades".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_grade_data_current(self, **kwargs):
        """
        Return the distribution of all available grades in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/grades \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/current/grades".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_grade_data_with_given_term(self, term_id, **kwargs):
        """
        Return the distribution of all available or concluded grades with the given term

        :calls: `GET /api/v1/accounts/:account_id/analytics/terms/:term_id/grades \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades>`_

        :param term_id: The ID of the term, or the strings "current" or "completed"
        :type term_id: int or str

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/terms/{}/grades".format(self.id, term_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_participation_data_completed(self, **kwargs):
        """
        Return page view hits all concluded courses in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/completed/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/completed/activity".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_participation_data_current(self, **kwargs):
        """
        Return page view hits all available courses in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/current/activity".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_participation_data_with_given_term(
        self, term_id, **kwargs
    ):
        """
        Return page view hits all available or concluded courses in the given term

        :calls: `GET /api/v1/accounts/:account_id/analytics/terms/:term_id/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation>`_

        :param term_id: The ID of the term, or the strings "current" or "completed"
        :type term_id: int or str

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/terms/{}/activity".format(self.id, term_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_statistics_completed(self, **kwargs):
        """
        Return all available numeric statistics about the department in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/statistics \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/completed/statistics".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_statistics_current(self, **kwargs):
        """
        Return all available numeric statistics about the department in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/statistics \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/current/statistics".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_department_level_statistics_with_given_term(self, term_id, **kwargs):
        """
        Return numeric statistics about the department with the given term

        :calls: `GET /api/v1/accounts/:account_id/analytics/terms/:term_id/statistics \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics>`_

        :param term_id: The ID of the term, or the strings "current" or "completed"
        :type term_id: int or str

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/analytics/terms/{}/statistics".format(self.id, term_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_enabled_features(self, **kwargs):
        """
        Lists all enabled features in an account.

        :calls: `GET /api/v1/accounts/:account_id/features/enabled \
        <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.feature.Feature`
        """
        return PaginatedList(
            Feature,
            self._requester,
            "GET",
            "accounts/{}/features/enabled".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_enrollment(self, enrollment, **kwargs):
        """
        Get an enrollment object by ID.

        :calls: `GET /api/v1/accounts/:account_id/enrollments/:id \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.show>`_

        :param enrollment: The object or ID of the enrollment to retrieve.
        :type enrollment: :class:`canvasapi.enrollment.Enrollment` or int

        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        enrollment_id = obj_or_id(enrollment, "enrollment", (Enrollment,))

        response = self._requester.request(
            "GET",
            "accounts/{}/enrollments/{}".format(self.id, enrollment_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Enrollment(self._requester, response.json())

    def get_enrollment_term(self, term, **kwargs):
        """
        Retrieve the details for an enrollment term in the account. Includes overrides by default.

        :calls: `GET /api/v1/accounts/:account_id/terms/:id \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.show>`_

        :param term: The object or ID of the enrollment term to retrieve.
        :type term: :class:`canvasapi.enrollment_term.EnrollmentTerm` or int

        :rtype: :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        from canvasapi.enrollment_term import EnrollmentTerm

        term_id = obj_or_id(term, "term", (EnrollmentTerm,))

        response = self._requester.request(
            "GET", "accounts/{}/terms/{}".format(self.id, term_id)
        )
        return EnrollmentTerm(self._requester, response.json())

    def get_enrollment_terms(self, **kwargs):
        """
        List enrollment terms for a context.

        :calls: `GET /api/v1/accounts/:account_id/terms \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        from canvasapi.enrollment_term import EnrollmentTerm

        return PaginatedList(
            EnrollmentTerm,
            self._requester,
            "GET",
            "accounts/{}/terms".format(self.id),
            {"account_id": self.id},
            _root="enrollment_terms",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_external_tool(self, tool, **kwargs):
        """
        :calls: `GET /api/v1/accounts/:account_id/external_tools/:external_tool_id \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show>`_

        :param tool: The object or ID of the tool
        :type tool: :class:`canvasapi.external_tool.ExternalTool` or int

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        tool_id = obj_or_id(tool, "tool", (ExternalTool,))

        response = self._requester.request(
            "GET",
            "accounts/{}/external_tools/{}".format(self.id, tool_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        tool_json = response.json()
        tool_json.update({"account_id": self.id})

        return ExternalTool(self._requester, tool_json)

    def get_external_tools(self, **kwargs):
        """
        :calls: `GET /api/v1/accounts/:account_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        return PaginatedList(
            ExternalTool,
            self._requester,
            "GET",
            "accounts/{}/external_tools".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_feature_flag(self, feature, **kwargs):
        """
        Returns the feature flag that applies to the given account.

        :calls: `GET /api/v1/accounts/:account_id/features/flags/:feature \
        <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show>`_

        :param feature: The feature object or name of the feature to retrieve.
        :type feature: :class:`canvasapi.feature.Feature` or str

        :rtype: :class:`canvasapi.feature.FeatureFlag`
        """
        feature_name = obj_or_str(feature, "name", (Feature,))

        response = self._requester.request(
            "GET",
            "accounts/{}/features/flags/{}".format(self.id, feature_name),
            _kwargs=combine_kwargs(**kwargs),
        )
        return FeatureFlag(self._requester, response.json())

    def get_features(self, **kwargs):
        """
        Lists all of the features of an account.

        :calls: `GET /api/v1/accounts/:account_id/features \
        <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.feature.Feature`
        """
        return PaginatedList(
            Feature,
            self._requester,
            "GET",
            "accounts/{}/features".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_global_notification(self, notification_id, **kwargs):
        """
        Returns a global notification for the current user.

        :calls: `GET /api/v1/accounts/:account_id/account_notifications/:id \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.show>`_

        :param notification_id: The notification ID of the desired notification.
        :type notification_id: `int`

        :rtype: :class:`canvasapi.account.AccountNotification`
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/account_notifications/{}".format(self.id, notification_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return AccountNotification(self._requester, response_json)

    def get_grading_periods(self, **kwargs):
        """
        Return a list of grading periods for the associated account.

        :calls: `GET /api/v1/accounts/:account_id/grading_periods \
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.grading_period.GradingPeriod`
        """

        return PaginatedList(
            GradingPeriod,
            self._requester,
            "GET",
            "accounts/{}/grading_periods".format(self.id),
            {"account_id": self.id},
            _root="grading_periods",
            kwargs=combine_kwargs(**kwargs),
        )

    def get_grading_standards(self, **kwargs):
        """
        Get a PaginatedList of the grading standards available for the account.

        :calls: `GET /api/v1/accounts/:account_id/grading_standards \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.grading_standards.GradingStandard`
        """

        return PaginatedList(
            GradingStandard,
            self._requester,
            "GET",
            "accounts/%s/grading_standards" % (self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_group_categories(self, **kwargs):
        """
        List group categories for a context.

        :calls: `GET /api/v1/accounts/:account_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupCategory`
        """
        from canvasapi.group import GroupCategory

        return PaginatedList(
            GroupCategory,
            self._requester,
            "GET",
            "accounts/{}/group_categories".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_groups(self, **kwargs):
        """
        Return a list of active groups for the specified account.

        :calls: `GET /api/v1/accounts/:account_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.group.Group`
        """
        from canvasapi.group import Group

        return PaginatedList(
            Group,
            self._requester,
            "GET",
            "accounts/{}/groups".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_index_of_reports(self, report_type, **kwargs):
        """
        Retrieve all reports that have been run for the account of a specific type.

        :calls: `GET /api/v1/accounts/:account_id/reports/:report \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index>`_

        :param report_type: The type of report.
        :type report_type: str
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.AccountReport`
        """
        return PaginatedList(
            AccountReport,
            self._requester,
            "GET",
            "accounts/{}/reports/{}".format(self.id, report_type),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_migration_systems(self, **kwargs):
        """
        Return a list of migration systems.

        :calls: `GET /api/v1/accounts/:account_id/content_migrations/migrators \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_migration.Migrator`
        """
        from canvasapi.content_migration import Migrator

        return PaginatedList(
            Migrator,
            self._requester,
            "GET",
            "accounts/{}/content_migrations/migrators".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_outcome_group(self, group, **kwargs):
        """
        Returns the details of the Outcome Group with the given id.

        :calls: `GET /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :param group: The outcome group object or ID to return.
        :type group: :class:`canvasapi.outcome.OutcomeGroup` or int

        :returns: An outcome group object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        outcome_group_id = obj_or_id(group, "outcome group", (OutcomeGroup,))
        response = self._requester.request(
            "GET",
            "accounts/{}/outcome_groups/{}".format(self.id, outcome_group_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return OutcomeGroup(self._requester, response.json())

    def get_outcome_groups_in_context(self, **kwargs):
        """
        Get all outcome groups for context - BETA

        :calls: `GET /api/v1/accounts/:account_id/outcome_groups \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index>`_

        :returns: Paginated List of OutcomesGroups in the context.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeGroups`
        """
        from canvasapi.outcome import OutcomeGroup

        return PaginatedList(
            OutcomeGroup,
            self._requester,
            "GET",
            "accounts/{}/outcome_groups".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_outcome_import_status(self, outcome_import, **kwargs):
        """
        Get the status of an already created Outcome import.
        Pass 'latest' for the outcome import id for the latest import.

        :calls: `GET /api/v1/accounts/:account_id/outcome_imports/:id \
        <https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.show>`_

        :param outcome_import: The outcome import object or ID to get the status of.
        :type outcome_import: :class:`canvasapi.outcome_import.OutcomeImport`,
            int, or string: "latest"

        :rtype: :class:`canvasapi.outcome_import.OutcomeImport`
        """
        if outcome_import == "latest":
            outcome_import_id = "latest"
        else:
            outcome_import_id = obj_or_id(
                outcome_import, "outcome_import", (OutcomeImport,)
            )

        response = self._requester.request(
            "GET",
            "accounts/{}/outcome_imports/{}".format(self.id, outcome_import_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return OutcomeImport(self._requester, response_json)

    def get_report(self, report_type, report_id, **kwargs):
        """
        Return a report which corresponds to the given report type and ID.

        :calls: `GET /api/v1/accounts/:account_id/reports/:report/:id \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.show>`_

        :param report_type: The type of the report which is being looked up.
        :type report_type: `string`

        :param report_id: The id for the report which is being looked up.
        :type report_id: `int`

        :rtype: :class:`canvasapi.account.AccountReport`
        """
        response = self._requester.request(
            "GET",
            "accounts/{}/reports/{}/{}".format(self.id, report_type, report_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return AccountReport(self._requester, response_json)

    def get_reports(self, **kwargs):
        """
        Return a list of reports for the current context.

        :calls: `GET /api/v1/accounts/:account_id/reports \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.available_reports>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.AccountReport`
        """
        return PaginatedList(
            AccountReport,
            self._requester,
            "GET",
            "accounts/{}/reports".format(self.id),
            {"account_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_role(self, role, **kwargs):
        """
        Retrieve a role by ID.

        :calls: `GET /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show>`_

        :param role: The object or ID of the role.
        :type role: :class:`canvasapi.account.Role` or int

        :rtype: :class:`canvasapi.account.Role`
        """
        role_id = obj_or_id(role, "role", (Role,))

        response = self._requester.request(
            "GET",
            "accounts/{}/roles/{}".format(self.id, role_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Role(self._requester, response.json())

    def get_roles(self, **kwargs):
        """
        List the roles available to an account.

        :calls: `GET /api/v1/accounts/:account_id/roles \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.Role`
        """

        return PaginatedList(
            Role,
            self._requester,
            "GET",
            "accounts/{}/roles".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_root_outcome_group(self, **kwargs):
        """
        Redirect to root outcome group for context

        :calls: `GET /api/v1/accounts/:account_id/root_outcome_group \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect>`_

        :returns: The OutcomeGroup of the context.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        response = self._requester.request(
            "GET",
            "accounts/{}/root_outcome_group".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return OutcomeGroup(self._requester, response.json())

    def get_rubric(self, rubric_id, **kwargs):
        """
        Get a single rubric, based on rubric id.

        :calls: `GET /api/v1/accounts/:account_id/rubrics/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show>`_

        :param rubric_id: The ID of the rubric.
        :type rubric_id: int
        :rtype: :class:`canvasapi.rubric.Rubric`
        """
        response = self._requester.request(
            "GET",
            "accounts/%s/rubrics/%s" % (self.id, rubric_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Rubric(self._requester, response.json())

    def get_rubrics(self, **kwargs):
        """
        Get the paginated list of active rubrics for the current account.

        :calls: `GET /api/v1/accounts/:account_id/rubrics \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.rubric.Rubric`
        """
        return PaginatedList(
            Rubric,
            self._requester,
            "GET",
            "accounts/%s/rubrics" % (self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_scopes(self, **kwargs):
        """
        Retrieve a paginated list of scopes.

        :calls: `GET /api/v1/accounts/:account_id/scopes \
        <https://canvas.instructure.com/doc/api/api_token_scopes.html#method.scopes_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.scope.Scope`
        """
        from canvasapi.scope import Scope

        return PaginatedList(
            Scope,
            self._requester,
            "GET",
            "accounts/{}/scopes".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_single_grading_standard(self, grading_standard_id, **kwargs):
        """
        Get a single grading standard from the account.

        :calls: `GET /api/v1/accounts/:account_id/grading_standards/:grading_standard_id \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show>`_

        :param grading_standard_id: The grading standard id
        :type grading_standard_id: int
        :rtype: :class:`canvasapi.grading_standards.GradingStandard`
        """

        response = self._requester.request(
            "GET",
            "accounts/%s/grading_standards/%d" % (self.id, grading_standard_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return GradingStandard(self._requester, response.json())

    def get_sis_import(self, sis_import, **kwargs):
        """
        Retrieve information on an individual SIS import from this account.

        :calls: `GET /api/v1/accounts/:account_id/sis_imports/:id \
        <https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.show>`_

        :param sis_import: The object or ID of the sis_import to retrieve.
        :type sis_import: int, str or :class:`canvasapi.sis_import.SisImport`

        :rtype: :class:`canvasapi.sis_import.SisImport`
        """
        sis_import_id = obj_or_id(sis_import, "sis_import", (SisImport,))

        response = self._requester.request(
            "GET",
            "accounts/{}/sis_imports/{}".format(self.id, sis_import_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"account_id": self.id})

        return SisImport(self._requester, response_json)

    def get_sis_imports(self, **kwargs):
        """
        Get the paginated list of SIS imports for the current account.

        :calls: `GET /api/v1/accounts/:account_id/sis_imports \
        <https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.sis_import.SisImport`
        """

        return PaginatedList(
            SisImport,
            self._requester,
            "GET",
            "accounts/{}/sis_imports".format(self.id),
            {"account_id": self.id},
            _root="sis_imports",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_sis_imports_running(self, **kwargs):
        """
        Get the paginated list of running SIS imports for the current account.

        :calls: `GET /api/v1/accounts/:account_id/sis_imports/importing \
        <https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.importing>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList`
            of :class:`canvasapi.sis_import.SisImport`
        """

        return PaginatedList(
            SisImport,
            self._requester,
            "GET",
            "accounts/{}/sis_imports/importing".format(self.id),
            {"account_id": self.id},
            _root="sis_imports",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_subaccounts(self, recursive=False, **kwargs):
        """
        List accounts that are sub-accounts of the given account.

        :calls: `GET /api/v1/accounts/:account_id/sub_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts>`_

        :param recursive: If true, the entire account tree underneath this account will \
        be returned. If false, only direct sub-accounts of this  account will be returned.
        :type recursive: bool
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.Account`
        """
        kwargs["recursive"] = recursive
        return PaginatedList(
            Account,
            self._requester,
            "GET",
            "accounts/{}/sub_accounts".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_user_logins(self, **kwargs):
        """
        Given a user ID, return that user's logins for the given account.

        :calls: `GET /api/v1/accounts/:account_id/logins \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.login.Login`
        """
        from canvasapi.login import Login

        return PaginatedList(
            Login,
            self._requester,
            "GET",
            "accounts/{}/logins".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_user_notifications(self, user, **kwargs):
        """
        Return a list of all global notifications in the account for
        this user. Any notifications that have been closed by the user
        will not be returned.

        :calls: `GET /api/v1/accounts/:account_id/users/:user_id/account_notifications \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_index>`_

        :param user: The user object or ID to retrieve notifications for.
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.AccountNotification`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        return PaginatedList(
            AccountNotification,
            self._requester,
            "GET",
            "accounts/{}/users/{}/account_notifications".format(self.id, user_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_users(self, **kwargs):
        """
        Retrieve a list of users associated with this account.

        :calls: `GET /api/v1/accounts/:account_id/users \
        <https://canvas.instructure.com/doc/api/users.html#method.users.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        return PaginatedList(
            User,
            self._requester,
            "GET",
            "accounts/{}/users".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def import_outcome(self, attachment, **kwargs):
        """
        Import outcome into canvas.

        :calls: `POST /api/v1/accounts/:account_id/outcome_imports \
        <https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.create>`_

        :param attachment: A file handler or path of the file to import.
        :type attachment: file or str

        :rtype: :class:`canvasapi.outcome_import.OutcomeImport`
        """

        attachment, is_path = file_or_path(attachment)

        try:
            response = self._requester.request(
                "POST",
                "accounts/{}/outcome_imports".format(self.id),
                file={"attachment": attachment},
                _kwargs=combine_kwargs(**kwargs),
            )

            response_json = response.json()
            response_json.update({"account_id": self.id})

            return OutcomeImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    def show_account_auth_settings(self, **kwargs):
        """
        Return the current state of each account level setting

        :calls: `GET /api/v1/accounts/:account_id/sso_settings \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show_sso_settings>`_

        :rtype: :class:`canvasapi.account.SSOSettings`
        """

        response = self._requester.request(
            "GET",
            "accounts/{}/sso_settings".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return SSOSettings(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update an existing account.

        :calls: `PUT /api/v1/accounts/:id \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update>`_

        :returns: True if the account was updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            "PUT", "accounts/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if "name" in response.json():
            super(Account, self).set_attributes(response.json())
            return True
        else:
            return False

    def update_account_auth_settings(self, **kwargs):
        """
        Return the current state of account level after updated

        :calls: `PUT /api/v1/accounts/:account_id/sso_settings \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update_sso_settings>`_

        :rtype: :class:`canvasapi.account.SSOSettings`
        """

        response = self._requester.request(
            "PUT",
            "accounts/{}/sso_settings".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return SSOSettings(self._requester, response.json())

    def update_role(self, role, **kwargs):
        """
        Update permissions for an existing role.

        :calls: `PUT /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.update>`_

        :param role: The object or ID of the role.
        :type role: :class:`canvasapi.account.Role` or int

        :rtype: :class:`canvasapi.account.Role`
        """
        role_id = obj_or_id(role, "role", (Role,))

        response = self._requester.request(
            "PUT",
            "accounts/{}/roles/{}".format(self.id, role_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Role(self._requester, response.json())


class AccountNotification(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.subject, self.id)

    def update_global_notification(self, account_notification, **kwargs):
        """
        Updates a global notification.

        :calls: `PUT /api/v1/accounts/:account_id/account_notifications/:id \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.update>`_

        :param account_notification: The notification to update with.
        :type account_notification: dict

        :rtype: :class:`canvasapi.account.AccountNotification`
        """
        required_key_list = ["subject", "message", "start_at", "end_at"]
        required_keys_present = all(
            x in account_notification for x in required_key_list
        )

        if isinstance(account_notification, dict) and required_keys_present:
            kwargs["account_notification"] = account_notification
        else:
            raise RequiredFieldMissing(
                (
                    "account_notification must be a dictionary with keys "
                    "'subject', 'message', 'start_at', and 'end_at'."
                )
            )

        response = self._requester.request(
            "PUT",
            "accounts/{}/account_notifications/{}".format(self.account_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return AccountNotification(self._requester, response.json())


class AccountReport(CanvasObject):
    def __str__(self):
        try:
            return "{} ({})".format(self.report, self.id)
        except AttributeError:
            # Print params if not a report instance
            return "{} ({})".format(self.report, self.parameters)

    def delete_report(self, **kwargs):
        """
        Delete this report.

        :calls: `DELETE /api/v1/accounts/:account_id/reports/:report/:id \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.destroy>`_

        :rtype: :class:`canvasapi.account.AccountReport`
        """
        response = self._requester.request(
            "DELETE",
            "accounts/{}/reports/{}/{}".format(self.account_id, self.report, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return AccountReport(self._requester, response.json())


class Role(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.label, self.base_role_type)


class SSOSettings(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.login_handle_name, self.change_password_url)


class Admin(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{} {} ({})".format(self.user["name"], self.user["id"], self.id)
