PyCanvas Deploy Procedures
==========================

Pre-Flight Checklist
--------------------

- On branch `master` and up-to-date
- All tests pass
- 100% coverage
- `CHANGELOG` is accurate

Packaging
---------

Update version number in `setup.py`.

Run `python setup.py sdist`. This should create a file in the `dist` directory called something like `pycanvas-0.0.0.tar.gz`.

Generate Documentation
----------------------

In the `docs` directory, run `make clean html`.

**TODO:** how to publish documentation.

Deploy
------

Commit the new files and the changes to `setup.py` and push.

Create a merge request from `master` to `stable`, and merge.

Tag the merge commit with the version number: `git tag -a v0.0.0  -m "Release version 0.0.0" abc1234`

Push the tag: `git push origin v0.0.0`
