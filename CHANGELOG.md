PyCanvas Changelog
==================

Version 0.2
-----------

**New Endpoint Coverage**

- Groups
- Roles
- Page Revisions
- Sections
- Conversations

**General**

- Standardized `__str__` methods. They now (generally) follow the convention of the value of the single most relevant field followed by an ID in parentheses.
- Reworked how `requests_mock` is used in test suite.
- Nested dictionaries are now allowed as kwargs
- Split 401 into two exceptions: `InvalidAccessToken` if `'WWW-Authenticate'` header is present. Otherwise, `Unauthorized`.


**Bugfixes**

- Moved some incorrectly placed enrollment methods to the Enrollment class.
- Corrected `Process` class to `Progress`
- Minor text fixes.

Version 0.1.2
-------------

**New Endpoint Coverage**

- Getting a Group
- Uploading a file to a Course or User
- Several Page related endpoints

**General**

- Added contribution guide
- Added Docker container for testing (e.g. with Jenkins)
- Split requirements files into three:
    - dev_requirements.txt
    - tests_requirements.txt
    - requirements.txt

**Bugfixes**

- Added some missing parameters
- Fixed some incorrectly defined parameters
- Fixed an issue where tests would fail due to an improperly configured requires block
