CanvasAPI Deploy Procedures
===========================

Pre-Flight Checklist
--------------------

- On branch `develop` and up-to-date
- All tests pass
- 100% coverage
- No linter errors
- `CHANGELOG` is accurate

Generate Documentation
----------------------

Documentation should now be automatically pushed to readthedocs.

Deploy
------

Update version number in `__init__.py`.

Commit the the changes to `__init__.py` and push.

Create a merge request from `develop` to `master`, and merge.

Tag the merge commit with the version number: `git tag -s v0.0.0  -m "Release version 0.0.0" abc1234`

Push the tag: `git push upstream v0.0.0`

GitHub Actions should automatically deploy the tagged code to PyPI.

Create release on GitHub for the new tag. Use the text from the changelog for content.
