import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.authentication_event import AuthenticationEvent
from canvasapi.avatar import Avatar
from canvasapi.calendar_event import CalendarEvent
from canvasapi.communication_channel import CommunicationChannel
from canvasapi.content_export import ContentExport
from canvasapi.content_migration import ContentMigration, Migrator
from canvasapi.course import Course
from canvasapi.enrollment import Enrollment
from canvasapi.eportfolio import EPortfolio
from canvasapi.feature import Feature, FeatureFlag
from canvasapi.file import File
from canvasapi.folder import Folder
from canvasapi.grade_change_log import GradeChangeEvent
from canvasapi.license import License
from canvasapi.login import Login
from canvasapi.page_view import PageView
from canvasapi.paginated_list import PaginatedList
from canvasapi.pairing_code import PairingCode
from canvasapi.usage_rights import UsageRights
from canvasapi.user import User
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestUser(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"user": ["get_by_id"]}, m)

            self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.user)
        self.assertIsInstance(string, str)

    # get_profile()
    def test_get_profile(self, m):
        register_uris({"user": ["profile"]}, m)

        profile = self.user.get_profile()

        self.assertIsInstance(profile, dict)
        self.assertIn("name", profile)

    # get_page_views()
    def test_get_page_views(self, m):
        register_uris({"user": ["page_views", "page_views_p2"]}, m)

        page_views = self.user.get_page_views()
        page_view_list = [view for view in page_views]

        self.assertEqual(len(page_view_list), 4)
        self.assertIsInstance(page_view_list[0], PageView)

    # get_courses()
    def test_get_courses(self, m):
        register_uris({"user": ["courses", "courses_p2"]}, m)

        courses = self.user.get_courses()
        course_list = [course for course in courses]

        self.assertEqual(len(course_list), 4)
        self.assertIsInstance(course_list[0], Course)

    # get_grade_change_events_for_student()
    def test_get_grade_change_events_for_student(self, m):
        register_uris({"user": ["get_grade_change_events_for_student"]}, m)

        response = self.user.get_grade_change_events_for_student()

        self.assertIsInstance(response, PaginatedList)
        self.assertEqual(len([event for event in response]), 2)

        for event in response:
            self.assertEqual(event.links["course"], self.user.id)
            self.assertIsInstance(event, GradeChangeEvent)
            self.assertEqual(event.event_type, "grade_change")

    # get_grade_change_events_for_grader()
    def test_get_grade_change_events_for_grader(self, m):
        register_uris({"user": ["get_grade_change_events_for_grader"]}, m)

        response = self.user.get_grade_change_events_for_grader()

        self.assertIsInstance(response, PaginatedList)
        self.assertEqual(len([event for event in response]), 2)

        for event in response:
            self.assertEqual(event.links["course"], self.user.id)
            self.assertIsInstance(event, GradeChangeEvent)
            self.assertEqual(event.event_type, "grade_change")

    # get_missing_submissions()
    def test_get_missing_submissions(self, m):
        register_uris({"user": ["missing_sub", "missing_sub_p2"]}, m)

        missing_assigments = self.user.get_missing_submissions()
        assignment_list = [assignment for assignment in missing_assigments]

        self.assertEqual(len(assignment_list), 4)
        self.assertIsInstance(assignment_list[0], Assignment)

    # update_settings()
    def test_update_settings(self, m):
        register_uris({"user": ["update_settings"]}, m)

        settings = self.user.update_settings(manual_mark_as_read=True)

        self.assertIsInstance(settings, dict)
        self.assertIn("manual_mark_as_read", settings)
        self.assertTrue(settings["manual_mark_as_read"])

    # get_color()
    def test_get_color(self, m):
        register_uris({"user": ["color"]}, m)

        color = self.user.get_color("course_1")

        self.assertIsInstance(color, dict)
        self.assertIn("hexcode", color)
        self.assertEqual(color["hexcode"], "#abc123")

    # get_colors()
    def test_get_colors(self, m):
        register_uris({"user": ["colors"]}, m)

        colors = self.user.get_colors()

        self.assertIsInstance(colors, dict)
        self.assertIn("custom_colors", colors)
        self.assertIsInstance(colors["custom_colors"], dict)

    # update_color()
    def test_update_color(self, m):
        register_uris({"user": ["color_update"]}, m)

        new_hexcode = "#f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        self.assertIsInstance(color, dict)
        self.assertIn("hexcode", color)
        self.assertEqual(color["hexcode"], new_hexcode)

    def test_update_color_no_hashtag(self, m):
        register_uris({"user": ["color_update"]}, m)

        new_hexcode = "f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        self.assertIsInstance(color, dict)
        self.assertIn("hexcode", color)
        self.assertEqual(color["hexcode"], "#" + new_hexcode)

    # edit()
    def test_edit(self, m):
        register_uris({"user": ["edit"]}, m)

        new_name = "New User Name"
        self.user.edit(user={"name": new_name})

        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, "name"))
        self.assertEqual(self.user.name, new_name)

    # merge_into()
    def test_merge_into_id(self, m):
        register_uris({"user": ["merge"]}, m)

        self.user.merge_into(2)

        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, "name"))
        self.assertEqual(self.user.name, "John Smith")

    def test_merge_into_user(self, m):
        register_uris({"user": ["get_by_id_2", "merge"]}, m)

        other_user = self.canvas.get_user(2)
        self.user.merge_into(other_user)

        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, "name"))
        self.assertEqual(self.user.name, "John Smith")

    # get_avatars()
    def test_get_avatars(self, m):
        register_uris({"user": ["avatars", "avatars_p2"]}, m)

        avatars = self.user.get_avatars()
        avatar_list = [avatar for avatar in avatars]

        self.assertEqual(len(avatar_list), 4)
        self.assertIsInstance(avatar_list[0], Avatar)

    # get_assignments()
    def test_user_get_assignments(self, m):
        register_uris(
            {
                "course": ["get_by_id"],
                "user": ["get_user_assignments", "get_user_assignments2"],
            },
            m,
        )

        assignments_by_id = self.user.get_assignments(1)
        assignment_list = [assignment for assignment in assignments_by_id]
        self.assertIsInstance(assignments_by_id[0], Assignment)
        self.assertEqual(len(assignment_list), 4)

        course_obj = self.canvas.get_course(1)
        assignments_by_obj = self.user.get_assignments(course_obj)
        assignment_list = [assignment for assignment in assignments_by_obj]
        self.assertIsInstance(assignments_by_obj[0], Assignment)
        self.assertEqual(len(assignment_list), 4)

    # get_enrollments()
    def test_get_enrollments(self, m):
        register_uris({"user": ["list_enrollments", "list_enrollments_2"]}, m)

        enrollments = self.user.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    # upload()
    def test_upload(self, m):
        register_uris({"user": ["upload", "upload_final"]}, m)

        filename = "testfile_user_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.user.upload(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)

    # get_calendar_events_for_user()
    def test_get_calendar_events_for_user(self, m):
        register_uris({"user": ["list_calendar_events_for_user"]}, m)

        cal_events = self.user.get_calendar_events_for_user()
        cal_event_list = [cal_event for cal_event in cal_events]
        self.assertEqual(len(cal_event_list), 2)
        self.assertIsInstance(cal_event_list[0], CalendarEvent)

    # get_communication_channels()
    def test_get_communication_channels(self, m):
        register_uris({"user": ["list_comm_channels", "list_comm_channels2"]}, m)

        comm_channels = self.user.get_communication_channels()
        channel_list = [channel for channel in comm_channels]
        self.assertEqual(len(channel_list), 4)
        self.assertIsInstance(channel_list[0], CommunicationChannel)

    # create_communication_channel()
    def test_create_communication_channels(self, m):
        register_uris({"user": ["create_comm_channel"]}, m)

        channel = {"type": "email", "address": "username@example.org"}
        new_channel = self.user.create_communication_channel(
            communication_channel=channel
        )

        self.assertIsInstance(new_channel, CommunicationChannel)

    # get_eportfolios()
    def test_get_eportfolios(self, m):
        register_uris({"user": ["get_eportfolios"]}, m)

        eportfolios = self.user.get_eportfolios()
        eportfolio_list = [portfolio for portfolio in eportfolios]
        self.assertIsInstance(eportfolios, PaginatedList)
        self.assertIsInstance(eportfolios[0], EPortfolio)
        self.assertEqual(len(eportfolio_list), 2)
        self.assertEqual(eportfolios[0].name, "ePortfolio 1")

    def test_get_eportfolios_with_deleted(self, m):
        register_uris({"user": ["get_eportfolios_include_deleted"]}, m)

        eportfolios = self.user.get_eportfolios()
        eportfolio_list = [portfolio for portfolio in eportfolios]
        self.assertIsInstance(eportfolios, PaginatedList)
        self.assertIsInstance(eportfolios[0], EPortfolio)
        self.assertEqual(len(eportfolio_list), 3)
        self.assertEqual(eportfolios[2].name, "ePortfolio 3")
        self.assertEqual(eportfolios[2].workflow_state, "deleted")

    def test_moderate_user_eportfolios(self, m):
        register_uris({"user": ["moderate_user_eportfolios"]}, m)

        spam_eportfolios = self.user.moderate_all_eportfolios(
            spam_status="marked_as_spam"
        )
        eportfolio_list = [portfolio for portfolio in spam_eportfolios]
        self.assertIsInstance(spam_eportfolios, PaginatedList)
        self.assertIsInstance(spam_eportfolios[0], EPortfolio)
        self.assertEqual(len(eportfolio_list), 2)
        self.assertEqual(spam_eportfolios[0].spam_status, "marked_as_spam")

    # get_files()
    def test_get_files(self, m):
        register_uris({"user": ["get_user_files", "get_user_files2"]}, m)

        files = self.user.get_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)

    # get_file()
    def test_get_file(self, m):
        register_uris({"user": ["get_file"]}, m)

        file_by_id = self.user.get_file(1)
        self.assertIsInstance(file_by_id, File)
        self.assertEqual(file_by_id.display_name, "User_File.docx")
        self.assertEqual(file_by_id.size, 1024)

        file_by_obj = self.user.get_file(file_by_id)
        self.assertIsInstance(file_by_obj, File)
        self.assertEqual(file_by_obj.display_name, "User_File.docx")
        self.assertEqual(file_by_obj.size, 1024)

    # get_file_quota()
    def test_get_file_quota(self, m):
        register_uris({"user": ["get_file_quota"]}, m)

        file_quota = self.user.get_file_quota()
        self.assertIsInstance(file_quota, dict)
        self.assertEqual(file_quota["quota"], 889234510)
        self.assertEqual(file_quota["quota_used"], 476231098)

    # get_folder()
    def test_get_folder(self, m):
        register_uris({"user": ["get_folder"]}, m)

        folder_by_id = self.user.get_folder(1)
        self.assertEqual(folder_by_id.name, "Folder 1")
        self.assertIsInstance(folder_by_id, Folder)

        folder_by_obj = self.user.get_folder(folder_by_id)
        self.assertEqual(folder_by_obj.name, "Folder 1")
        self.assertIsInstance(folder_by_obj, Folder)

    # get_folders()
    def test_get_folders(self, m):
        register_uris({"user": ["list_folders"]}, m)

        folders = self.user.get_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({"user": ["create_folder"]}, m)

        name_str = "Test String"
        response = self.user.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)

    # get_user_logins()
    def test_get_user_logins(self, m):
        requires = {"user": ["list_user_logins", "list_user_logins_2"]}
        register_uris(requires, m)

        response = self.user.get_user_logins()
        login_list = [login for login in response]

        self.assertIsInstance(login_list[0], Login)
        self.assertEqual(len(login_list), 2)

    # get_observees()
    def test_get_observees(self, m):
        requires = {"user": ["list_observees", "list_observees_2"]}
        register_uris(requires, m)

        response = self.user.get_observees()
        observees_list = [observees for observees in response]

        self.assertIsInstance(observees_list[0], User)
        self.assertEqual(len(observees_list), 4)

    def test_get_observers(self, m):
        requires = {"user": ["list_observers", "list_observers"]}
        register_uris(requires, m)

        response = self.user.get_observers()
        observers_list = [observers for observers in response]

        self.assertIsInstance(observers_list[0], User)
        self.assertEqual(len(observers_list), 2)

    # add_observee_with_credentials()
    def test_add_observee_with_credentials(self, m):
        register_uris({"user": ["add_observee_with_credentials"]}, m)

        response = self.user.add_observee_with_credentials()

        self.assertIsInstance(response, User)

    # show_observee()
    def test_show_observee(self, m):
        register_uris({"user": ["show_observee"]}, m)

        response = self.user.show_observee(6)

        self.assertIsInstance(response, User)

    # add_observee()
    def test_add_observee(self, m):
        register_uris({"user": ["add_observee"]}, m)

        response = self.user.add_observee(7)

        self.assertIsInstance(response, User)

    # remove_observee()
    def test_remove_observee(self, m):
        register_uris({"user": ["remove_observee"]}, m)

        response = self.user.remove_observee(8)

        self.assertIsInstance(response, User)

    # create_content_migration
    def test_create_content_migration(self, m):
        register_uris({"user": ["create_content_migration"]}, m)

        content_migration = self.user.create_content_migration("dummy_importer")

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    def test_create_content_migration_migrator(self, m):
        register_uris(
            {"user": ["create_content_migration", "get_migration_systems_multiple"]}, m
        )

        migrators = self.user.get_migration_systems()
        content_migration = self.user.create_content_migration(migrators[0])

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    def test_create_content_migration_bad_migration_type(self, m):
        register_uris({"user": ["create_content_migration"]}, m)

        with self.assertRaises(TypeError):
            self.user.create_content_migration(1)

    # get_content_migration
    def test_get_content_migration(self, m):
        register_uris({"user": ["get_content_migration_single"]}, m)

        content_migration = self.user.get_content_migration(1)

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    # get_content_migrations
    def test_get_content_migrations(self, m):
        register_uris({"user": ["get_content_migration_multiple"]}, m)

        content_migrations = self.user.get_content_migrations()

        self.assertEqual(len(list(content_migrations)), 2)

        self.assertIsInstance(content_migrations[0], ContentMigration)
        self.assertEqual(content_migrations[0].id, 1)
        self.assertEqual(content_migrations[0].migration_type, "dummy_importer")
        self.assertIsInstance(content_migrations[1], ContentMigration)
        self.assertEqual(content_migrations[1].id, 2)
        self.assertEqual(content_migrations[1].migration_type, "dummy_importer")

    # get_migration_systems
    def test_get_migration_systems(self, m):
        register_uris({"user": ["get_migration_systems_multiple"]}, m)

        migration_systems = self.user.get_migration_systems()

        self.assertEqual(len(list(migration_systems)), 2)

        self.assertIsInstance(migration_systems[0], Migrator)
        self.assertEqual(migration_systems[0].type, "dummy_importer")
        self.assertEqual(migration_systems[0].requires_file_upload, True)
        self.assertEqual(migration_systems[0].name, "Dummy Importer 01")
        self.assertIsInstance(migration_systems[1], Migrator)
        self.assertEqual(migration_systems[1].type, "dummy_importer_02")
        self.assertEqual(migration_systems[1].requires_file_upload, False)
        self.assertEqual(migration_systems[1].name, "Dummy Importer 02")

    # get_content_exports()
    def test_list_content_exports(self, m):
        register_uris({"user": ["multiple_content_exports"]}, m)

        content_exports = self.user.get_content_exports()
        content_export_list = [content_export for content_export in content_exports]

        self.assertEqual(len(content_export_list), 2)
        self.assertEqual(content_export_list[0].id, 2)
        self.assertEqual(content_export_list[1].export_type, "b")
        self.assertIsInstance(content_export_list[0], ContentExport)

    # get_content_export()
    def test_show_content_export(self, m):
        register_uris({"user": ["single_content_export"]}, m)

        content_export = self.user.get_content_export(11)

        self.assertTrue(hasattr(content_export, "export_type"))
        self.assertIsInstance(content_export, ContentExport)

    # export_content()
    def test_export_content(self, m):
        register_uris({"user": ["export_content"]}, m)

        content_export = self.user.export_content("d")

        self.assertIsInstance(content_export, ContentExport)
        self.assertTrue(hasattr(content_export, "export_type"))

    # get_features()
    def test_get_features(self, m):
        register_uris({"user": ["get_features"]}, m)

        features = self.user.get_features()

        self.assertIsInstance(features, PaginatedList)
        self.assertIsInstance(features[0], Feature)

    # get_enabled_features()
    def test_get_enabled_features(self, m):
        register_uris({"user": ["get_enabled_features"]}, m)

        features = self.user.get_enabled_features()

        self.assertIsInstance(features, list)
        self.assertIsInstance(features[0], str)

    # get_feature_flag()
    def test_get_feature_flag(self, m):
        register_uris({"user": ["get_features", "get_feature_flag"]}, m)

        feature = self.user.get_features()[0]

        feature_flag = self.user.get_feature_flag(feature)

        self.assertIsInstance(feature_flag, FeatureFlag)
        self.assertEqual(feature_flag.feature, "high_contrast")

    # get_authentication_events()
    def test_get_authentication_events(self, m):
        register_uris({"user": ["get_authentication_events"]}, m)

        authentication_event = self.user.get_authentication_events()
        event_list = [event for event in authentication_event]

        self.assertEqual(len(event_list), 2)

        self.assertIsInstance(event_list[0], AuthenticationEvent)
        self.assertEqual(event_list[0].event_type, "login")
        self.assertEqual(event_list[0].pseudonym_id, 9478)

        self.assertIsInstance(event_list[1], AuthenticationEvent)
        self.assertEqual(event_list[1].created_at, "2012-07-20T15:00:00-06:00")
        self.assertEqual(event_list[1].event_type, "logout")

    # set_usage_rights()
    def test_set_usage_rights(self, m):
        register_uris({"user": ["set_usage_rights"]}, m)

        usage_rights = self.user.set_usage_rights(
            file_ids=[1, 2],
            usage_rights={"use_justification": "fair_use", "license": "private"},
        )

        self.assertIsInstance(usage_rights, UsageRights)
        self.assertEqual(usage_rights.use_justification, "fair_use")
        self.assertEqual(usage_rights.message, "2 files updated")
        self.assertEqual(usage_rights.license, "private")
        self.assertEqual(usage_rights.file_ids, [1, 2])

    # remove_usage_rights()
    def test_remove_usage_rights(self, m):
        register_uris({"user": ["remove_usage_rights"]}, m)

        retval = self.user.remove_usage_rights(file_ids=[1, 2])

        self.assertIsInstance(retval, dict)
        self.assertIn("message", retval)
        self.assertEqual(retval["file_ids"], [1, 2])
        self.assertEqual(retval["message"], "2 files updated")

    # get_licenses()
    def test_get_licenses(self, m):
        register_uris({"user": ["get_licenses"]}, m)

        licenses = self.user.get_licenses()
        self.assertIsInstance(licenses, PaginatedList)
        licenses = list(licenses)

        for lic in licenses:
            self.assertIsInstance(lic, License)
            self.assertTrue(hasattr(lic, "id"))
            self.assertTrue(hasattr(lic, "name"))
            self.assertTrue(hasattr(lic, "url"))

        self.assertEqual(2, len(licenses))

    # resolve_path()
    def test_resolve_path(self, m):
        register_uris({"user": ["resolve_path"]}, m)

        full_path = "Folder_Level_1/Folder_Level_2/Folder_Level_3"
        folders = self.user.resolve_path(full_path)
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 4)
        self.assertIsInstance(folder_list[0], Folder)

        folder_names = ("my_files/" + full_path).split("/")
        for folder_name, folder in zip(folder_names, folders):
            self.assertEqual(folder_name, folder.name)

    # resolve_path() with null input
    def test_resolve_path_null(self, m):
        register_uris({"user": ["resolve_path_null"]}, m)

        # test with null input
        root_folder = self.user.resolve_path()
        root_folder_list = [folder for folder in root_folder]
        self.assertEqual(len(root_folder_list), 1)
        self.assertIsInstance(root_folder_list[0], Folder)
        self.assertEqual("my_files", root_folder_list[0].name)

    # create_pairing_code()
    def test_create_pairing_code(self, m):
        register_uris({"user": ["observer_pairing_codes"]}, m)

        pairing_code = self.user.create_pairing_code()
        self.assertIsInstance(pairing_code, PairingCode)
        self.assertEqual("abc123", pairing_code.code)

    # terminate_sessions()
    def test_terminate_sessions(self, m):
        register_uris({"user": ["terminate_sessions"]}, m)
        resp = self.user.terminate_sessions()
        self.assertEqual(resp, "ok")


@requests_mock.Mocker()
class TestUserDisplay(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": [
                        "get_by_id",
                        "get_assignment_by_id",
                        "list_gradeable_students",
                    ]
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)
            self.userDisplays = self.assignment.get_gradeable_students()
            self.userDisplayList = [ud for ud in self.userDisplays]
            self.userDisplay = self.userDisplayList[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.userDisplay)
        self.assertIsInstance(string, str)
