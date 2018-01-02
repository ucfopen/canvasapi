# Change Log

## [Unreleased]

### New Endpoint Coverage

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
- Added a requester cache that rememebers the last 5 requests to Canvas. It can be accessed as the attribute `_cache` of the `requester object`. (e.g. `course._requester._cache`)
- Files can now be downloaded directly from the `File` object in one of two ways: (Thanks, [@DanBrink91](https://github.com/DanBrink91))
    1. `get_contents` will directly return the contents of the file. (e.g. `file.get_contents()`)
    2. `download` will download the file and save it to the provided path. (e.g. `file.download('example.txt')`)
- Lots of formatting fixes and spelling corrections.

### Deprecation Warning

Including `/api/v1/` at the end of the API URL passed to a new `Canvas` object is now deprecated. Users should now only pass the root URL into the `Canvas` object (e.g. `"https://example.com/api/v1/"` should now be `"https://example.com"`).

For now, users including `/api/v1/` will see a `DeprecationWarning`, but things will otherwise operate normally. We will remove the ability to continue using `/api/v1/` in a future release.

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

[Unreleased]: https://github.com/ucfopen/canvasapi/compare/v0.7.0...develop
[0.7.0]: https://github.com/ucfopen/canvasapi/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/ucfopen/canvasapi/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/ucfopen/canvasapi/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/ucfopen/canvasapi/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/ucfopen/canvasapi/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/ucfopen/canvasapi/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ucfopen/canvasapi/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/ucfopen/canvasapi/compare/v0.1.1...v0.1.2
