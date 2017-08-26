# Change Log

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

[0.6.0]: https://github.com/ucfopen/canvasapi/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/ucfopen/canvasapi/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/ucfopen/canvasapi/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/ucfopen/canvasapi/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/ucfopen/canvasapi/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ucfopen/canvasapi/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/ucfopen/canvasapi/compare/v0.1.1...v0.1.2
