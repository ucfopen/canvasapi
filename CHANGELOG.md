# Change Log

## [Unreleased]

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
    - *Note:* `DeprecationWarnings` are disabled by default, so you may need to run your code with `python -Wd` to see them.

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

[Unreleased]: https://github.com/ucfopen/canvasapi/compare/v0.14.0...develop
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
