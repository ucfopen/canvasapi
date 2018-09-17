CanvasAPI Deploy Procedures
===========================

Pre-Flight Checklist
--------------------

- On branch `develop` and up-to-date
- All tests pass
- 100% coverage
- No linter errors
- `CHANGELOG` is accurate

Packaging
---------

Update version number in `__init__.py`.

Run `python setup.py sdist`. This should create a file in the `dist` directory called something like `canvasapi-0.0.0.tar.gz`.

Generate Documentation
----------------------

Documentation should now be automatically pushed to readthedocs.

Deploy
------

Commit the new files and the changes to `__init__.py` and push.

Create a merge request from `develop` to `master`, and merge.

Tag the merge commit with the version number: `git tag -s v0.0.0  -m "Release version 0.0.0" abc1234`

Push the tag: `git push upstream v0.0.0`

Run `twine upload dist/canvasapi-0.0.0.tar.gz` to upload to PyPI.

Create release on GitHub for the new tag. Use the text from the changelog for content.
