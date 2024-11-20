# Change Log

## [Unreleased]

### Backstage

- Updated deploy Action to use more modern processes.

## [3.3.0] - 2023-08-27

### General

- Added documentation for PaginatedList
- Rework requester URLs to accommodate graphql and new quizzes endpoints (Thanks, [@bennettscience](https://github.com/bennettscience))

### Bugfixes

- Fixed PaginatedList not respecting new quizzes endpoints (Thanks, [@jonespm](https://github.com/jonespm))

### Backstage

- Updated codecov action

## [3.2.0] - 2023-05-25

### New Endpoint Coverage

- New Quizzes
- Delete Page in Groups (Thanks, [@Caitlin-Fabian](https://github.com/Caitlin-Fabian))

### General

- Added support for pagination with metadata when headers are missing (Thanks, [@bennettscience](https://github.com/bennettscience))
- Added support for Python 3.11

### Bugfixes

- Fixed an issue where `Course.create_discussion_topic` wouldn't accept attachment files.

## [3.1.0] - 2023-04-21

### New Endpoint Coverage

- Account Calendars (Thanks, [@dmols](https://github.com/dmols))
  - List available account calendars
  - Get a single account calendar
  - Update a calendar's visibility
  - Update many calendars' visibility
  - List all account calendars
- Enrollments (Thanks, [@svanderwulp](https://github.com/svanderwulp))
  - Accept Course Invitation
  - Reject Course Invitation
- File (Thanks, [@bennettscience](https://github.com/bennettscience))
  - Update File
- JWTs (Thanks [@dmols](https://github.com/dmols))
  - Create JWTs
  - Refresh JWTs
- Moderation Grading (Moderation Set)
  - List students selected for moderation
  - Select students for moderation
- Query Course Events (Thanks, [@dmols](https://github.com/dmols))
  - Query by course
  - Query by account
- Rubrics (Thanks, [@bennettscience](https://github.com/bennettscience))
  - Create, Update, and Delete Rubric Assessments
  - Create a Rubric Association
- Users
  - Terminate all user sessions (Thanks, [@lucas-salas](https://github.com/lucas-salas))

### General

- Updated Codecov action to v3

### Bugfixes

- Fixed an issue where kwargs were not passed along to Canvas in `Course.get_module()`. (Thanks, [@bennettscience](https://github.com/bennettscience))
- Fixed an issue where not all functions allowed arbitrary keyword arguments. Added a test to detect and prevent this for the future.
- Fixed an issue with `Course.get_enabled_features()` where it would throw an error trying to paginate. It now returns a list of strings directly. (Thanks, [@bennettscience](https://github.com/bennettscience))
- Added missing docs for `AssignmentOverride`. (Thanks, [@lafent](https://github.com/lafent))
- Fixed a typo in `Canvas.create_calendar_event()` where an error message improperly listed the missing key as 'context_codes' instead of 'context_code'. (Thanks, [@dmols](https://github.com/dmols) and [@mikesuhan](https://github.com/mikesuhan))

## [3.0.0] - 2022-09-21

### New Endpoint Coverage

- Delete a Rubric (Thanks, [@ggarfink](https://github.com/ggarfink))
- Grade Change Log for Assignments, Courses, and Users (Thanks, [@matthewf-ucsd](https://github.com/matthewf-ucsd))
- Content Migrations: List items for selective import (Thanks, [@matthewf-ucsd](https://github.com/matthewf-ucsd))
- List observers of a User (Thanks, [@bennettscience](https://github.com/bennettscience))
- ePortfolio endpoints (Thanks, [@Birdmaaan4](https://github.com/Birdmaaan4) and [@bennettscience](https://github.com/bennettscience))
- Delete an Admin from an Account (Thanks, [@shaneros](https://github.com/shaneros))

### General

- Added support for Python 3.10
- Smart DateTimes now support any ISO 8601 format, including time offsets. (Thanks, [@kailukaitisBrendan](https://github.com/kailukaitisBrendan))

### Bugfixes

- Fixed an issue where kwargs were not passed along to Canvas in `User.get_profile()`. (Thanks, [@breed](https://github.com/breed))

### Breaking Changes

- Dropped support for Python 3.6
- Update `QuizSubmission.get_submission_events` to return a `PaginatedList`. (Thanks, [@stevenbell](https://github.com/stevenbell))
- Update `Course.get_course_level_student_summary_data` to return a `PaginatedList` of `CourseStudentSummary` items instead of a dictionary. (Thanks, [@craigdsthompson](https://github.com/craigdsthompson))
- Update `Course.get_outcome_results` to return a `PaginatedList` of `OutcomeResult` items instead of a dictionary. (Thanks, [@bennettscience](https://github.com/bennettscience))
- Remove unnecessary `id` parameter from `delete`, `reorder_question_group`, and `update` methods in `QuizGroup` class. (Thanks, [@kailukaitisBrendan](https://github.com/kailukaitisBrendan))
- Update `Submission` to return attachments as `File` objects instead of dictionaries. (Thanks, [@laitingsheng](https://github.com/laitingsheng))

## [2.2.0] - 2021-03-25

### New Endpoint Coverage

- Enroll a user in a section (Thanks, [@damianfs](https://github.com/damianfs))
- File quota for courses, groups, and users (Thanks, [@deundrewilliams](https://github.com/deundrewilliams))
- Provisional Grades (Thanks, [@zenith110](https://github.com/zenith110))

### General

- Added support for Python 3.9
- Added `RateLimitExceeded` exception to distinguish between being rate limited and being otherwise forbidden from accesing a resource. It is a subclass of the `Forbidden` exception.
- File uploads now accept path-like objects (Thanks, [@theunkn0wn1](https://github.com/theunkn0wn1))
- Add list of CanvasAPI Projects to README (Thanks, [@deundrewilliams](https://github.com/deundrewilliams))
- PyPI Package Description now uses README (Thanks, [@bennettscience](https://github.com/bennettscience))
- Replaced Travis CI with GitHub Actions

### Bugfixes

- Fixed an issue where `Canvas.create_poll()` did not work due to an incorrect parameter.
- Canvas.get_todo_items() now correctly returns a `PaginatedList` of `Todo` items (Thanks, [@bennettscience](https://github.com/bennettscience))
- Fixed an issue where `Favorite.remove()` did not handle parameters properly. (Thanks, [@deundrewilliams](https://github.com/deundrewilliams))

## [2.1.0] - 2020-12-04

### New Endpoint Coverage

- Course TODO items (Thanks, [@onomou](https://github.com/onomou))
- Create observer pairing code (Thanks, [@bennettscience](https://github.com/bennettscience))

### General

- Added missing documentation for the get_current_user method and clarifications to the `CurrentUser` class. (Thanks, [@Xx-Ashutosh-xX](https://github.com/Xx-Ashutosh-xX))
- `Canvas.get_announcement` now has a required parameter `context_codes`, which accepts a list of course IDs or `Course` objects.
- Updated contributing guide
- Added missing documentation for the "Smart DateTimes" feature
- Added basic troubleshooting guide to documentation

### Bugfixes

- Fixed an issue where an `Announcement` object sometimes didn't have an associated course ID. (Thanks, [@bennettscience](https://github.com/bennettscience))
- Fixed an issue where an encoding problem could lead to file downloads hanging indefinitely. (Thanks, [@blepabyte](https://github.com/blepabyte))

### Deprecation Warnings

- The `enrollment_type` argument on `Course.enroll_user` is now deprecated. Pass this information to `enrollment[type]` as a keyword argument instead. e.g. `enroll_user(enrollment={'type': 'StudentEnrollment'})`

## [2.0.0] - 2020-08-14

### General

- Added support for arbitrary keyword arguments across the entire library

### New Endpoint Coverage

- Custom Gradebook Columns (Thanks,[@aileenpongnon](https://github.com/aileenpongnon))
- Files
  - Resolve Path (Thanks,[@dsavransky](https://github.com/dsavransky))

### Bugfixes

- Fixed an issue where `Quiz.get_quiz_group` incorrectly set `course_id` to the quiz ID. (Thanks,[@hcolclou](https://github.com/hcolclou))
- Fixed an issue where `Course.create_external_tool` didn't accept `client_id` (LTI 1.3 support).
- Fixed an issue where `Module.create_module_item` didn't (Thanks,[@aileenpongnon](https://github.com/aileenpongnon) and [@onomou](https://github.com/onomou))
- Fixed an issue where `Page.revert_to_revision` would incorrectly always set `group_id` to the page ID. Now correctly sets `group_id` or `course_id` appropriately.

### Breaking Changes

- `Course.create_external_tool` no longer supports positional arguments for its required parameters. Use keyword arguments instead.

## [1.0.0] - 2020-07-09

### General

- Added support for Python 3.8
- Dropped support for Python 3.4, 3.5, and 2.7
- Removed all previously deprecated methods and attributes.
- Upgraded Ubuntu version for Travis (Thanks,[@jonespm](https://github.com/jonespm))
- Set up automatic deployments to PyPI via Travis
- Set up nightly build

## [0.16.1] - 2020-07-06

### Bugfixes

- Fixed an issue where the user-provided API_URL/base_url wasn't run through cleanup.

### Deprecation Warnings

- Using `/api/v1/` in the API_URL has been deprecated since v0.8.0 and legacy support will be removed in the next release. Ensure your provided url doesn't contain `api/v1/`. See deprecation warning in changelog for v0.8.0.
- :warning: **_This is the final release with support for Python 3.5_** :warning:

## [0.16.0] - 2020-06-26

### New Endpoint Coverage

- Enrollment Terms
  - Get a Single Enrollment Term (Thanks, [@lcamacho](https://github.com/lcamacho))
- Files
  - Resolve Path for Course (Thanks,[@dsavransky](https://github.com/dsavransky))
- GraphQL (Thanks,[@jonespm](https://github.com/jonespm))
- Late Policy (Thanks, [@kennygperez](https://github.com/kennygperez))
- Quiz Assignment Overrides (Thanks, [@kennygperez](https://github.com/kennygperez))
- Quiz Statistics (Thanks, [@andrew-gardener](https://github.com/andrew-gardener))

### General

- Updated README to use updated parameters for getting a user's courses by enrollment state (Thanks,[@Vishvak365](https://github.com/Vishvak365))

### Deprecation Warnings

- :warning: **_This is the final release with support for Python 2.7_** :warning:
  - [Python 2.7 is end-of-life as of January 2020](https://www.python.org/doc/sunset-python-2/)
  - Future releases of CanvasAPI will _NOT_ support any version of Python 2
- :warning: **_This is the final release with support for Python 3.4_** :warning:
  - [Python 3.4 is end-of-life as of March 2019](https://www.python.org/downloads/release/python-3410/)
  - Future releases of CanvasAPI will _NOT_ support Python 3.4 or below
- This is the final deprecation warning for all methods marked as deprecated in this changelog or in our documentation. They will be removed in the next release.

### Bugfixes

- Fixed an issue where `Quiz.get_submission()` ignored data added from using the `include` kwarg. (Thanks,[@Mike-Nahmias](https://github.com/Mike-Nahmias))
- Fixed the broken `__str__` method on the `ChangeRecord` class (Thanks,[@Mike-Nahmias](https://github.com/Mike-Nahmias))
- Fixed an issue where printing an `AccountReport` would fail due to not having an ID (Thanks,[@Mike-Nahmias](https://github.com/Mike-Nahmias))
- Fixed an issue where `"report_type"` was passed improperly (Thanks,[@brucespang](https://github.com/brucespang))
- Fixed some new `flake8` issues (Thanks,[@dsavransky](https://github.com/dsavransky) and [@jonespm](https://github.com/jonespm))
- Fixed an incorrect docstring for `Course.create_page()` (Thanks,[@dsavransky](https://github.com/dsavransky))
- Fixed an issue where extra whitespace in the user-supplied canvas URL would break `PaginatedList` (Thanks,[@amorqiu](https://github.com/amorqiu))

## [0.15.0] - 2019-11-19

### New Endpoint Coverage

- Assignment Extensions (Thanks, [@ljoks](https://github.com/ljoks))
- AssignmentGroup (Thanks, [@ctcuff](https://github.com/ctcuff))
  - List Assignments
- Authentications Log (Thanks, [@weining-li](https://github.com/weining-li))
- Brand Configs (Thanks, [@bennettscience](https://github.com/bennettscience))
- Comm Messages (Thanks, [@ljoks](https://github.com/ljoks))
- File Usage Rights (Thanks, [@atarisafari](https://github.com/atarisafari) and [@joonro](https://github.com/joonro))
- Gradebook History (Thanks, [@gdijkhoffz](https://github.com/gdijkhoffz))
- Quiz Reports (Thanks, [@atarisafari](https://github.com/atarisafari)
- Quiz Submission Events (Thanks, [@Goff-Davis](https://github.com/Goff-Davis))
- Quiz Submission User List (Thanks, [@gdijkhoffz](https://github.com/gdijkhoffz))
- Rubric Associations (Thanks, [@weining-li](https://github.com/weining-li))

### General

- Throw `IndexError` when using negative indexes on `PaginatedList` objects (Thanks, [@UniversalSuperBox](https://github.com/UniversalSuperBox))
- `Assignment.overrides` now returns a list of `AssignmentOverride` objects.

### Deprecation Warnings

- `CanvasObject.attributes` is now deprecated and will be removed in a future version.
- `CanvasObject.to_json()` is now deprecated and will be removed in a future version. To view the original attributes sent by Canvas, enable logs from the requests library.

### Bugfixes

- Fixed an issue where `util.clean_headers()` would throw a `ValueError` if a user accidentally included a space in their API token. (Thanks, [@keeeeeegan](https://github.com/keeeeeegan))
- Fixed an issue where `QuizSubmission` objects sometimes wouldn't have a course_id, making some methods unusable. (Thanks, [@bennettscience](https://github.com/bennettscience))
- Fixed an issue where `get_user()` did not accept arbitrary keyword arguments (Thanks, [@eriktews](https://github.com/eriktews))
- Fixed an issue where an import was triggering a `DeprecationWarning` (Thanks, [@Screeeech](https://github.com/Screeeech))
- Fixed an issue where a GroupedSubmission wasn't saving the `submissions` attribute properly

## [0.14.0] - 2019-08-20

### New Endpoint Coverage

- API Token scopes (Thanks, [@jrsilveti](https://github.com/jrsilveti))
  - List scopes
- Account Notifications (Thanks, [@jrsilveti](https://github.com/jrsilveti))
  - Show a global notification
  - Update a global notification
- Account Reports (Thanks, [@jrsilveti](https://github.com/jrsilveti))
  - Start a report
  - Status of a report
  - Delete a report
- Collaborations (Thanks, [@jrsilveti](https://github.com/jrsilveti))
  - List collaborations
  - List members of a collaboration
- Feature Flags (Thanks, [@cat0698](https://github.com/cat0698))
  - List features
  - List enabled features
  - Get feature flag
  - Set feature flag
  - Remove feature flag
- Rubric (Thanks, [@cat0698](https://github.com/cat0698))
  - Create a single rubric

### General

- Removed overzealous global enabling of `DeprecationWarning`. (Thanks, [@Screeeech](https://github.com/Screeeech))
  - _Note:_ `DeprecationWarnings` are disabled by default, so you may need to run your code with `python -Wd` to see them.

## [0.13.0] - 2019-07-08

### New Endpoint Coverage

- Content Exports (Thanks, [@weining-li](https://github.com/weining-li))
- ePub Exports (Thanks, [@jrsilveti](https://github.com/jrsilveti))
- Favorites (Thanks, [@atarisafari](https://github.com/atarisafari))
- Grading Periods (Thanks, [@jrsilveti](https://github.com/jrsilveti))
- Outcome Import (Thanks, [@jrsilveti](https://github.com/jrsilveti))
- Peer Reviews (Thanks, [@vutoan1245](https://github.com/vutoan1245))
- Planner (Thanks, [@weining-li](https://github.com/weining-li))
  - Planner
  - Planner Notes
  - Planner Overrides
- Polls (Thanks, [@Goff-Davis](https://github.com/Goff-Davis))
  - Poll
  - PollChoice
  - PollSession
  - PollSubmission
- Quiz Submission Questions (Thanks, [@bradfordlynch](https://github.com/bradfordlynch))

### General

- Added [documentation for Debugging](https://canvasapi.readthedocs.io/en/latest/debugging.html)
- Added request and response logging to `Requester.request`
- Added [documentation for Exceptions](https://canvasapi.readthedocs.io/en/latest/exceptions.html)
- Added generic error handling for unhandled 4XX+ HTTP errors
- Added [Code of Conduct](https://github.com/ucfopen/canvasapi/blob/develop/CODE_OF_CONDUCT.md)
- Added support for PATCH methods (Thanks, [@us91](https://github.com/us91))
- Added a warning when using a blank `CANVAS_URL` (Thanks, [@gdijkhoffz](https://github.com/gdijkhoffz))
- Added Issue and Pull Request Templates
- Added CODEOWNERS file

### Deprecation Warnings

- `Quiz.get_all_quiz_submissions` is now deprecated. Use `Quiz.get_submissions` instead.

### Bugfixes

- Fixed an issue where creating an external tool did not properly send parameters to Canvas. (Thanks, [@altgilbers](https://github.com/altgilbers))
- Fixed an issue where getting Quiz Submissions would only return up to the first 10 results (Thanks,[@Mike-Nahmias](https://github.com/Mike-Nahmias))
- Fixed an issue where unhandled 4XX and 5XX HTTP errors would cause a JSONDecodeError
- Removed a limitation where the parameter `grouped` being passed to `get_multiple_submissions` would be ignored. These methods now return a `GroupedSubmission` object containing multiple `Submission` objects, instead of ignoring. (Thanks, [@bennettscience](https://github.com/bennettscience))

## [0.12.0] - 2019-04-03

### New Endpoint Coverage

- Assignment Overrides
- Quiz Submissions (Thanks, [@wallacetyler](https://github.com/wallacetyler))
- Blueprints (Thanks, [@gdijkhoffz](https://github.com/gdijkhoffz))
- Create an Admin (Thanks, [@altgilbers](https://github.com/altgilbers))
- SIS Imports (Thanks, [@nottheswimmer](https://github.com/nottheswimmer))
- Create and Delete Communication Channels (Thanks, [@matthewf-ucsd](https://github.com/matthewf-ucsd))

### General

- Added support for HTTP response 409 (Thanks, [@wallacetyler](https://github.com/wallacetyler))

### Bugfixes

- Fixed an issue where `Section.edit()` didn't accept keyword arguments (Thanks, [@wjw27](https://github.com/wjw27))

## [0.11.0] - 2018-09-17

### New Endpoint Coverage

- Get all quiz submissions (Thanks, [@petarGitNik](https://github.com/petarGitNik))
- Upload a file to a submission (Thanks, [@MarkLalor](https://github.com/MarkLalor))
- Upload a file to a folder (Thanks, [@elec3647](https://github.com/elec3647))
- Get Admins in an account (Thanks, [@kensler](https://github.com/kensler))

### General

- Added support for Python 3.7
- Added a warning when using HTTP for the base url instead of HTTPS. This should help prevent some confusing behavior that Canvas exhibits when making HTTP requests to an HTTPS-enabled instance.
- Added more detailed [documentation for passing complex parameters as keyword arguments](https://canvasapi.readthedocs.io/en/latest/keyword-args.html).

### Bugfixes

- Fixed an issue where `Outcome.get_subgroups()` didn't have sufficient context to call other methods.
- Fixed improper passing of keyword arguments when editing a Module (Thanks, [@phaustin](https://github.com/phaustin))

## [0.10.0] - 2018-06-01

### New Endpoint Coverage

- Content Migrations (Thanks, [@qwertynerd97](https://github.com/qwertynerd97))
- Copy a File (Thanks, [@qwertynerd97](https://github.com/qwertynerd97))
- Course Quiz Extensions
- List Announcements (Thanks, [@rmanbaird](https://github.com/rmanbaird))
- Grade/Comment on Multiple Submissions (Thanks, [@rmanbaird](https://github.com/rmanbaird))
- Quiz Extensions

### General

- Lots of docstring fixes. (Thanks, [@rmanbaird](https://github.com/rmanbaird))

### Deprecation Warnings

- All methods starting with `list_` have been deprecated. Each has been replaced with a corresponding method starting with `get_`. For example, `Course.list_groups()` is now `Course.get_groups()`. The `list_` methods will be removed in a future release. (Thanks [@qwertynerd97](https://github.com/qwertynerd97) for doing the bulk of the grunt work.)
- `Course.update_tab()` is now deprecated. Use `Tab.update()` instead.

### Bugfixes

- Fixed a bug where taking a slice of a `PaginatedList` where the `start` was larger than the list caused an infinite loop.
- Fixed a typo that prevented `Assignment.submit()` from working properly. (Thanks, [@Tobiaqs](https://github.com/Tobiaqs))

## [0.9.0] - 2018-03-01

### New Endpoint Coverage

- Quiz Questions

### General

- Added example usage for several common endpoints to our documentation.
- Updated `PaginatedList` to allow specification of the root element to build the list from when given an atypical JSON response (see [#146](https://github.com/ucfopen/canvasapi/issues/146)). (thanks [@dfwarden](https://github.com/dfwarden))
- Improved keyword argument support for `course.get_section()` (thanks [@andrew-gardener](https://github.com/andrew-gardener))
- When uploading a file to a submission with `Submission.upload_comment()`, it will automatically attached to a new comment.

### Deprecation Warnings

- :warning: **_Dropped support for Python 3.3_** :warning:
  - [Python 3.3 is end-of-life as of September 2017](https://www.python.org/dev/peps/pep-0398/#lifespan)
  - Should continue to function in 3.3, but compatibility cannot be guaranteed going forward.
- Several methods in the `Course` and `Section` classes relating to assignments and submissions have been deprecated.
  - Comparable methods have been implemented in the `Assignment` and `Submission` classes, as appropriate.
  - The deprecated methods now include a warning in the documentation with reference to the replacement. Additionally, the deprecated methods will raise a `DeprecationWarning`.
  - These methods will be removed in a future release.
- `Course.list_sections()` has been deprecated. Use `Course.get_sections()` instead.

### Bugfixes

- Fixed an issue where booleans would be capitalized when sent to Canvas, causing Canvas to misinterpret them and set default values.
- Fixed an issue where unexpected JSON responses from Canvas would cause `PaginatedList` objects to fail.

## [0.8.2] - 2018-01-24

### Bugfixes

- Fixed an issue where editing and deleting user logins would use incorrect IDs.

## [0.8.1] - 2018-01-23

### General

- Fixed several incorrect and missing docstrings

### Bugfixes

- Fixed an issue where Canvas returning `while(1);` at the beginning of a response to uploading a file prevented uploads from completing.
- Fixed an issue where a trailing slash in the provided BASE_URL would cause `PaginatedList` objects to fail.
- Fixed an issue where combine_kwargs was transposing empty brackets and keys when a dictionary had a list as a value.

## [0.8.0] - 2018-01-04

### New Endpoint Coverage

- Account
  - Delete a sub account
- Grading Standards (Thanks, [@JonGuilbe](https://github.com/JonGuilbe))
- Notification Preferences (Thanks, [@a-goetz](https://github.com/a-goetz))
  - Update a preference
  - Update preferences by category
  - Update multiple preferences
- Outcomes (Thanks, [@a-goetz](https://github.com/a-goetz))
- Quiz Question Groups (Thanks, [@JonGuilbe](https://github.com/JonGuilbe))
- Rubric (Thanks, [@sigurdurb](https://github.com/sigurdurb))

### General

- Added support for other iterables as parameter values. (Thanks, [@liblit](https://github.com/liblit))
- For many endpoints that accept an "object id", either a CanvasAPI Object or integer ID can now be passed. (Thanks, [@a-goetz](https://github.com/a-goetz))
- Added a requester cache that remembers the last 5 requests to Canvas. It can be accessed as the attribute `_cache` of the `requester object`. (e.g. `course._requester._cache`)
- Files can now be downloaded directly from the `File` object in one of two ways: (Thanks, [@DanBrink91](https://github.com/DanBrink91))
  1. `get_contents` will directly return the contents of the file. (e.g. `file.get_contents()`)
  2. `download` will download the file and save it to the provided path. (e.g. `file.download('example.txt')`)
- Moved several methods exclusive to the API Key owner's user from the `User` class to a new class called `CurrentUser`. There is a new method in the `Canvas` class called `get_current_user` to access this object. (e.g. `canvas.get_current_user()`) (Thanks, [@DanBrink91](https://github.com/DanBrink91))

### Bugfixes

- Fixed a bug where creating conversations wouldn't work until the user iterated over the response.
- Lots of formatting fixes and spelling corrections.

### Deprecation Warning

Including `/api/v1/` at the end of the API URL passed to a new `Canvas` object is now deprecated. Users should now only pass the root URL into the `Canvas` object (e.g. `"https://example.com/api/v1/"` should now be `"https://example.com"`).

For now, users including `/api/v1/` will see a `DeprecationWarning`, but things will otherwise operate normally. The ability to continue using `/api/v1/` will be removed in a future release.

## [0.7.0] - 2017-10-04

Thanks to all the contributors who helped with this release: [@stephenwoosley](https://github.com/stephenwoosley), [@jackrsteiner](https://github.com/jackrsteiner), and [@allygator](https://github.com/allygator). You guys are awesome!

Huge thanks to [@liblit](https://github.com/liblit) for lots of issues, suggestions, and pull requests. Couldn't have done all this without you!

### New Endpoint Coverage

- Upload file to a Submission Comment (`Submission.upload_comment()`)

### General

- Switched to `flake8` instead of just `pyflakes` and `pycodestyle`.
- Added markdown linter and fixed related issues.
- `DateTime` "Smart Objects" are now timezone aware.
- Keyword arguments now support lists and tuples. Can be nested in other lists and/or inside dictionaries. See issue [#55](https://github.com/ucfopen/canvasapi/issues/55) for details.
- `DateTime` objects passed as params now auto-format to ISO 8601 strings.
- Added table of contents to README.
- Updated "Getting Started" page in Documentation to match README.

### Bugfixes

- Fixed an issue where editing a page would report a missing ID.
- Fixed an issue where kwargs weren't passed along in `Course.get_pages()`.
- Fixed an issue where `Course.list_multiple_submissions()` would always set grouped to `True`. It now correctly always sets grouped to `False` by removing the param.
- Fixed several issues relating to `DiscussionTopic` methods returning incorrect types.
- Fixed an issue where reordering pinned topics had no valid values for the order param.

## [0.6.0] - 2017-08-15

### General

- Added support for SIS IDs to get accounts, courses, groups and sections. (Thanks for the suggestion, [@sigurdurb](https://github.com/sigurdurb)!)

## [0.5.1] - 2017-08-02

### General

- Moved documentation to [Read the Docs](http://canvasapi.readthedocs.io).

### Bugfixes

- Fixed an issue where kwargs in Python 2.7 wouldn't be properly formatted when converted to get parameters.

## [0.5.0] - 2017-07-10

### New Endpoint Coverage

- Files (Get file from Canvas, Course, Group, or User)

### General

- Added support for Python 3.3, 3.4, 3.5, and 3.6 while maintaining 2.7 compatibility.

### Bugfixes

- Fixed an issue where non-ASCII characters in CanvasObject data would throw UnicodeEncodeError exceptions.

## [0.4.0] - 2017-06-16

### New Endpoint Coverage

- Analytics
- Announcement External Feeds
- Authentication Providers
- Communications Channels
- Files
- Logins
- Notification Preferences
- Submissions
- Search
- Tabs
- User Observees

### General

- Set up TravisCI and Coveralls.
- Added Badges to README.
- Updated CONTRIBUTING.md to more accurately reflect our dev process.

## [0.3.0] - 2017-03-30

### New Endpoint Coverage

- Appointment Groups
- Assignment Groups
- Bookmarks
- Calendar Events
- Discussions
- External Tools

### General

- Updated CHANGELOG.md format
- Created AUTHORS.md
- Added LICENSE
- Added `pycodestyle` and `pyflakes` requirements
- Added setup.cfg with `pycodestyle` max-line-length definition
- Moved .coveragerc settings to setup.cfg
- Changed `assert` statements to use the assertion methods built into unittest.

## [0.2.0] - 2017-01-04

### New Endpoint Coverage

- Groups
- Roles
- Page Revisions
- Sections
- Conversations

### General

- Standardized `__str__` methods. They now (generally) follow the convention of the value of the single most relevant field followed by an ID in parentheses.
- Reworked how `requests_mock` is used in test suite.
- Nested dictionaries are now allowed as kwargs
- Split 401 into two exceptions: `InvalidAccessToken` if `'WWW-Authenticate'` header is present. Otherwise, `Unauthorized`.

### Bugfixes

- Moved some incorrectly placed enrollment methods to the Enrollment class.
- Corrected `Process` class to `Progress`
- Minor text fixes.

## [0.1.2] - 2016-07-22

### New Endpoint Coverage

- Getting a Group
- Uploading a file to a Course or User
- Several Page related endpoints

### General

- Added contribution guide
- Added Docker container for testing (e.g. with Jenkins)
- Split requirements files into three:
  - dev_requirements.txt
  - tests_requirements.txt
  - requirements.txt

### Bugfixes

- Added some missing parameters
- Fixed some incorrectly defined parameters
- Fixed an issue where tests would fail due to an improperly configured requires block

[Unreleased]: https://github.com/ucfopen/canvasapi/compare/v3.3.0...develop
[3.3.0]: https://github.com/ucfopen/canvasapi/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/ucfopen/canvasapi/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/ucfopen/canvasapi/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/ucfopen/canvasapi/compare/v2.2.0...v3.0.0
[2.2.0]: https://github.com/ucfopen/canvasapi/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/ucfopen/canvasapi/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/ucfopen/canvasapi/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/ucfopen/canvasapi/compare/v0.16.1...v1.0.0
[0.16.1]: https://github.com/ucfopen/canvasapi/compare/v0.16.0...v0.16.1
[0.16.0]: https://github.com/ucfopen/canvasapi/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/ucfopen/canvasapi/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/ucfopen/canvasapi/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/ucfopen/canvasapi/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/ucfopen/canvasapi/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/ucfopen/canvasapi/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/ucfopen/canvasapi/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/ucfopen/canvasapi/compare/v0.8.2...v0.9.0
[0.8.2]: https://github.com/ucfopen/canvasapi/compare/v0.8.1...v0.8.2
[0.8.1]: https://github.com/ucfopen/canvasapi/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/ucfopen/canvasapi/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/ucfopen/canvasapi/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/ucfopen/canvasapi/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/ucfopen/canvasapi/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/ucfopen/canvasapi/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/ucfopen/canvasapi/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/ucfopen/canvasapi/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ucfopen/canvasapi/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/ucfopen/canvasapi/compare/v0.1.1...v0.1.2
