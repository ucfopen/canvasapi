# Contributing to CanvasAPI

Thanks for your interest in contributing!

Below you'll find guidelines for contributing that will keep our codebase clean and happy. 

## Table of Contents

* [How can I contribute?](#how-can-i-contribute)
    * [Bug reports](#bug-reports)
    * [Resolving issues](#resolving-issues)
    * [Making your first contribution](#making-your-first-contribution)
        * [Setting up the environment](#setting-up-the-environment)
        * [Writing tests](#writing-tests)
            * [API Coverage Tests](#api-coverage-tests)
            * [Engine tests](#engine-tests)
        * [Running tests / coverage reports](#running-tests-coverage-reports)
* [Code style guidelines](#code-style-guidelines)
    * [Foolish consistency](#foolish-consistency)
    * [Method docstrings](#method-docstrings)
        * [Descriptions](#descriptions)
        * [Links to related API endpoints](#links-to-related-api-endpoints)
        * [Parameters](#parameters)
        * [Returns](#returns)
        * [Docstring examples](#docstring-examples)

## How can I contribute?

### Bug Reports

Bug reports are awesome. Writing quality bug reports helps us identify issues and solve them even faster. You can submit bug reports directly to our [issue tracker](https://github.com/ucfopen/canvasapi/issues).

Here are a few things worth mentioning when making a report:

* What **version** of CanvasAPI are you running? (Use `pip show canvasapi` -- we try to build frequently so "latest" isn't always accurate.)
* What steps can be taken to **reproduce the issue**?
* **Detail matters.** Try not to be too be verbose, but generally the more information, the better!

### Resolving issues

We welcome pull requests for bug fixes and new features! Feel free to browse our open, unassigned issues and assign yourself to them. You can also filter by labels:

* [simple](https://github.com/ucfopen/canvasapi/issues?q=sort%3Aid_desc-desc+is%3Aopen+label%3Asimple) -- easier issues to start working on; great for getting familiar with the codebase.
* [api coverage](https://github.com/ucfopen/canvasapi/issues?q=sort%3Aid_desc-desc+is%3Aopen+label%3Aapi-coverage) -- covering new endpoints or updating existing ones.
* [internal](https://github.com/ucfopen/canvasapi/issues?q=sort%3Aid_desc-desc+is%3Aopen+label%3Ainternal) -- updates to the engine to improve performance.
* [major](https://github.com/ucfopen/canvasapi/issues?q=sort%3Aid_desc-desc+is%3Aopen+label%3Amajor) -- difficult or major changes or additions that require familiarity with the library.
* [bug](https://github.com/ucfopen/canvasapi/issues?q=sort%3Aid_desc-desc+is%3Aopen+label%3Abug) -- happy little code accidents.

Once you've found an issue you're interested in tackling, take a look at our [first contribution tutorial](#making-your-first-contribution) for information on our pull request policy.

### Making your first contribution

#### Setting up the environment

Now that you've selected an issue to work on, you'll need to set up an environment for writing code. We'll assume you already have pip, virtualenv, and git installed and are using a terminal. If not, please set those up before continuing.

1. Clone our repository by executing `git clone git@github.com:ucfopen/canvasapi.git`
2. Pull the latest commit from the **master** branch: `git pull origin master` 
3. Create a new branch with the format **issue/[issue_number]-[issue-title]**: `git checkout -b issue/1-test-issue-for-documentation`
4. Set up a new virtual environment ( `virtualenv env` ) and activate it (`source env/bin/activate`)
5. Install the required dependencies with `pip install -r dev_requirements.txt`

From here, you can go about working on your issue you normally would. Please make sure to adhere to our [style guidelines for both code and docstrings](#code-style-guidelines). Once you're satisfied with the result, it's time to write a unit test for it.

#### Writing tests

Tests are a critical part of building applications, and we [pity the fool who doesn't write them](https://blog.codinghorror.com/i-pity-the-fool-who-doesnt-write-unit-tests/). Unit tests help us monitor the health of the code checked into the repository and they provide a nice overview at the progress we make. Due to the size and nature of the library, it's unrealistic for us to manually test each component. Because of this, we require pull requests to A) have tests associated with the changes being made and B) pass those and all other tests.

You'll notice our tests live in the creatively named `tests` directory. Within that directory, you'll see several files in the form `test_[class].py` and another directory named `fixtures`. Depending on the scope of the issue you're solving, you'll be writing two different kinds of tests.

##### API Coverage Tests

We use the [requests-mock](https://pypi.python.org/pypi/requests-mock) library to simulate API responses. Those mock responses live inside the `fixtures` directory in JSON files. Each file's name describes the endpoints that are contained within. For example, course endpoints live in `course.json`. These fixtures are loaded on demand in a given test. Let's look at `test_get_user` in `test_course.py` as an example:

```python
# get_user()
def test_get_user(self, m):
    register_uris({'course': ['get_user']}, m)

    user = self.course.get_user(1)

    self.assertIsInstance(user, User)
    self.assertTrue(hasattr(user, 'name'))
```

Breakdown:

```python
# get_user()
```

It is common to have multiple tests for a single method. All related tests should be grouped together under a single comment with the name of the method being tested.

---

```python
def test_get_user(self, m):
```

This is a standard Python `unittest` test method with one addition: the `m` variable is passed to all methods with names starting with `test`. `m` is a Mocker object that can be used to override the routing of HTTP requests.

---

```python
register_uris({'course': ['get_user']}, m)
```

The `register_uris` function tells a mocker object which fixtures to load. It takes in two arguments: a dictionary describing which fixtures to load, and a mocker object.  The dictionary keys represent which file the desired fixtures are located in. The values are lists containing each desired fixture from that particular file. The example above will register the `get_user` fixture in `course.json`.

Example Fixture:

```json
"get_user": {
    "method": "GET",
    "endpoint": "courses/1/users/1",
    "data": {
        "id": 1,
        "name": "John Doe"
    },
    "status_code": 200
},
```

When this fixture is loaded, all `GET` requests to a url matching `courses/1/users/1` will return a status code of 200 and the provided user data for John Doe.

---

```python
user = self.course.get_user(1)

self.assertIsInstance(user, User)
self.assertTrue(hasattr(user, 'name'))
```
The rest is basic unit testing. Call the function to be tested, and assert various outcomes. If necessary, multiple tests can written for a single method. All related tests should appear together under the same comment, as described earlier.

---

It is common to need certain object(s) for multiple tests. For example, most methods in `test_course.py` require a `Course` object. In this case, save a course to the class in `self.course` for later use.

Do this in the `setUp` class method:
```python
with requests_mock.Mocker() as m:
    requires = {
        'course': ['get_by_id', 'get_page'],
        'quiz': ['get_by_id'],
        'user': ['get_by_id']
    }
    register_uris(requires, m)

    self.course = self.canvas.get_course(1)
    self.page = self.course.get_page('my-url')
    self.quiz = self.course.get_quiz(1)
    self.user = self.canvas.get_user(1)
```

Since `setUp` is not a test method, it does not automatically get passed a Mocker object `m`. To use the mocker, all relevant code needs to be inside a `with` statement:

```python
with requests_mock.Mocker() as m:
```

##### Engine tests

Not all of CanvasAPI relies on networking. While these pieces are few and far between, we still need to verify that they're performing correctly. Writing tests for engine-level code is just as important as user-facing code and is a bit easier. You'll just need to follow the same process as you would for API tests, minus the fixtures.

#### Running tests / coverage reports

Once you've written test case(s) for your issue, you'll need to run the test to verify that your changes are passing and haven't interfered with any other part of the library.

You'll do this by running `coverage run -m unittest discover` from the main `canvasapi` directory. If your tests pass, you're ready to run a coverage report!

Coverage reports tell us how much of our code is actually being tested. As of right now, we're happily maintaining 100% code coverage (🎉!) and our goal is to keep it there. Ensure you've covered your changes entirely by running `coverage report`. Your output should look something like this:

```
Name                             Stmts   Miss  Cover
----------------------------------------------------
canvasapi/__init__.py                3      0   100%
canvasapi/account.py               166      0   100%
canvasapi/appointment_group.py      17      0   100%
canvasapi/assignment.py             24      0   100%
[...]
canvasapi/upload.py                 29      0   100%
canvasapi/user.py                  101      0   100%
canvasapi/util.py                   29      0   100%
----------------------------------------------------
TOTAL                             1586      0   100%
```

Certain statements can be omitted from the coverage report by adding `# pragma: no cover` but this should be used conservatively. If your tests pass and your coverage is at 100%, you're ready to [submit a pull request](https://github.com/ucfopen/canvasapi/pulls)!

Be sure to include the issue number in the title with a pound sign in front of it (#123) so we know which issue the code is addressing. Point the branch at `develop` and then submit it for review.


## Code Style Guidelines

We try to adhere to Python's [PEP 8](https://www.python.org/dev/peps/pep-0008/) specification as much as possible. In short, that means:

* We use four spaces for indentation.
* Lines should be around 80 characters long, but up to 99 is allowed. Once you get into the 85+ territory, consider breaking your code into separate lines.

We use `pycodestyle` and `pyflakes` for linting:

```
pycodestyle canvasapi tests
```

```
pyflakes canvasapi tests
```

### Foolish consistency

> A foolish consistency is the hobgoblin of little minds. -- Ralph Waldo Emerson

An important tenet of PEP8 is to not get hung up on PEP8. While we try to be as PEP8 compliant as possible, maintaining the consistency of the project is more important than modifying an existing style choice.

Below you'll find several established styles that'll help you along the way.

### Method docstrings
Method docstrings should include a description, a link to the related API endpoint (if available), parameter name, parameter description, and parameter type, return description (if available), and return type. They should be included in the following order:

#### Descriptions
A description should be a concise, *action* statement (use "*write* a good docstring" over "*writes* a good docstring") that describes the method. Generally, the official API documentation's description is usable (make sure it's an **action statement** though). Special functionality should be documented. 

#### Links to related API endpoints
A link to a related API endpoint is denoted with `:calls:`. CanvasAPI uses Sphinx to automatically generate documentation, so we can provide a link to an API endpoint with the reStructuredText syntax:

```
:calls: `THE TEXT OF THE HYPERLINK \ 
    <https://the.url/to/use/>`_
```

Hyperlink text should match the text underneath the endpoint in the official Canvas API documentation. Generally, that looks like this:

```
:calls: `HTTP_METHOD /api/v1/endpoint/:variable
```

**Note**: It's okay to go over 80 characters for the URL, it can't be helped. Use a backslash to split the hyperlink text from the actual URL to limit line length.

#### Parameters
Parameters should be listed in the order that they appear in the method prototype. They should take on the following form:
```
:param PARAMETER_NAME: PARAMETER_DESCRIPTION.
:type PARAMETER_NAME: PYTHON_TYPE
```

#### Returns
**Return description** should be listed first, if available. This should be included to clarify a returned value, for example:

```python
def uncheck_box(box_id):
    """
    Uncheck the box with the given ID.

    :returns: True if the box was successfully unchecked, False otherwise.
    :rtype: bool
    """
```

In most cases, the return value is easy to infer based on the type and the description given in the docstring. `:returns:` is only necessary to clarify ambiguous cases.

**Return type** should always be included when a value is returned. If it's not a primitive type (`int`, `str`, `bool`, `list`, etc.) a fully-qualified class name should be included:

```
:rtype: :class:`canvasapi.user.User`
```

In the event a PaginatedList is returned:

```
:rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.user.User`
```

#### Docstring Examples
Here are some real world examples of how docstrings should be formatted:

```python
def get_account(self, account_id):
    """
    Retrieve information on an individual account.

    :calls: `GET /api/v1/accounts/:id \
    <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show>`_

    :param account_id: The ID of the account to retrieve.
    :type account_id: int
    :rtype: :class:`canvasapi.account.Account`
    """
```

```python
def get_accounts(self, **kwargs):
    """
    List accounts that the current user can view or manage.

    Typically, students and teachers will get an empty list in
    response. Only account admins can view the accounts that they
    are in.

    :calls: `GET /api/v1/accounts \
    <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.index>`_

    :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.account.Account`
    """
```

```python
def clear_course_nicknames(self):
    """
    Remove all stored course nicknames.

    :calls: `DELETE /api/v1/users/self/course_nicknames \
    <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

    :returns: True if the nicknames were cleared, False otherwise.
    :rtype: bool
    """
```
