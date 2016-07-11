# Contributing to PyCanvas

Thanks for your interest in contributing!

Below you'll find guidelines for contributing that will keep our codebase clean and happy. 

## Table of Contents

* [How can I contribute?](#how-can-i-contribute)
	* [Bug reports](#bug-reports)
	* [Resolving issues](#resolving-issues)
* [Making your first contribution](#making-your-first-contribution)
	* [Setting up the environment](#setting-up-the-environment)
	* [Writing tests](#writing-tests)
	* [Running tests / coverage reports](#running-tests-coverage-reports)
* [Code style guidelines](#code-style-guidelines)
	* [Foolish consistency](#foolish-consistency)
	* [Method docstrings](#method-docstrings)
		* [Docstring examples](#docstring-examples)

## How can I contribute?

### Bug Reports

#### Reporting bugs
Bug reports are awesome. Writing quality bug reports helps us identify issues and solve them even faster. You can submit bug reports directly to our [issue tracker](https://***REMOVED***/pycanvas/issues).

Here are a few things worth mentioning when making a report:

* What **version** of PyCanvas are you running? (Use `pip list` -- we try to build frequently so "latest" isn't always accurate.)
* What steps can be taken to **reproduce the issue**?
* **Detail matters.** Try not to be too be verbose, but generally the more information, the better!

### Resolving issues
We welcome pull requests for bug fixes and new features! Feel free to browse our open, unassigned issues and assign yourself to them. You can also filter by labels:

* [simple](https://***REMOVED***/pycanvas/issues?scope=all&sort=id_desc&state=opened&utf8=%E2%9C%93&label_name%5B%5D=simple) -- easier issues to start working on; great for getting familiar with the codebase.
* [api coverage](https://***REMOVED***/pycanvas/issues?scope=all&sort=id_desc&state=opened&utf8=%E2%9C%93&label_name%5B%5D=api+coverage) -- covering new endpoints or updating existing ones.
* [internal](https://***REMOVED***/pycanvas/issues?scope=all&sort=id_desc&state=opened&utf8=%E2%9C%93&label_name%5B%5D=internal) -- updates to the engine to improve performance.
* [major](https://***REMOVED***/pycanvas/issues?scope=all&sort=id_desc&state=opened&utf8=%E2%9C%93&label_name%5B%5D=major) -- difficult or major changes or additions that require familiarity with the library.


Once you've found an issue you're interested in tackling, take a look at our [first contribution tutorial](#making-your-first-contribution) for information on our pull request policy.

### Making your first contribution

#### Setting up the environment

Now that you've selected an issue to work on, you'll need to set up an environment for writing code. We'll assume you already have pip, virtualenv, and git installed and are using a terminal. If not, please set those up before continuing.

1. Clone our repository by executing `git clone git@***REMOVED***/pycanvas.git`
2. Pull the latest commit from the **master** branch: `git pull origin master` 
3. Create a new branch with the format **issue/[issue_number]-[issue-title]**: `git branch -b issue/1-test-issue-for-documentation`
4. Set up a new virtual environment ( `virtualenv env` ) and activate it (`source env/bin/activate`)
5. Install the required dependencies with `pip install -r dev_requirements.txt`

From here, you can go about working on your issue you normally would. Please make sure to adhere to our [style guidelines for both code and docstrings](#code-style-guidelines). Once you're satisfied with the result, it's time to write a unit test for it.

#### Writing tests

Tests are a critical part of building applications, and we [pity the fool who doesn't write them](https://blog.codinghorror.com/i-pity-the-fool-who-doesnt-write-unit-tests/). Unit tests help us monitor the health of the code checked into the repository and they provide a nice overview at the progress we make. Due to the size and nature of the library, it's unrealistic for us to manually test each component. Because of this, we require pull requests to A) have tests associated with the changes being made and B) pass those and all other tests.

You'll notice our tests live in the creatively named `tests` directory. Within that directory, you'll see several files in the form `test_[class].py` and another directory named `fixtures`. Depending on the scope of the issue you're solving, you'll be writing two different kinds of tests.

##### API coverage tests

We use the [requests-mock](https://pypi.python.org/pypi/requests-mock) library to simulate API responses, and those mock responses live inside the `fixtures` directory in JSON files. Each file's name describes the endpoints that are contained within (course endpoints live in `course.json`, for example). Those fixtures are loaded by name within a test Python file. Let's look at `test_course.py`:

```
  @classmethod
   def setUpClass(self):
       requires = {
           'course': [
               'create', 'create_assignment', 'deactivate_enrollment',
               'enroll_user', 'get_all_assignments', 'get_all_assignments2',
               'get_assignment_by_id'
           ],
           'external_tool': ['get_by_id_course'],
           'quiz': ['get_by_id'],
           'user': ['get_by_id']
       }
       
	    adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)
```

This file tests several different endpoints, all of which are included in a `requires` dict and then loaded by the `register_uris()` function in `tests.util`. The keys in the dictionary are the file names of the JSON files (without the extension) and the values are lists with elements that match the related keys in the JSON file.
Once they're loaded with `register_uris()`, any attempt to access a URL that matches will return the local fixture rather than trying to access a remote server.

Let's look at the first required fixture, `course create_quiz`:

```
"create": {
	"method": "POST",
	"endpoint": "courses/1/quizzes",
	"data": {
		"id": 1,
		"title": "Newer Title"
	},
	"status_code": 200
}
```

While we're at it, let's pull out the code in the library for creating a quiz:

```
def create_quiz(self, title, **kwargs):
	from quiz import Quiz
	response = self._requester.request(
	    'POST',
	    'courses/%s/quizzes' % (self.id),
	    **combine_kwargs(**kwargs)
	)
```

This code sends a POST request to the URL `courses/:course_id/quizzes`. With that information, we know that our fixture needs to contain `"method": "POST"` and `"endpoint": "courses/1/quizzes"`. You may be wondering where the ID (`courses/1`) came from. In our setUpClass method in `test_course.py`, we define a few starting objects to work with:

```
self.course = self.canvas.get_course(1)
self.quiz = self.course.get_quiz(1)
self.user = self.canvas.get_user(1)
```

For consistency, it's easiest to call give your fixture objects an ID of 1 unless you need a second object.

In the actual test, we use the `create_quiz()` method of `Course` to create a quiz with some data:

```
# create_quiz()
def test_create_quiz(self):
	title = 'Newer Title'
	new_quiz = self.course.create_quiz(self.course.id, quiz={'title': title})

	assert isinstance(new_quiz, Quiz)
	assert hasattr(new_quiz, 'title')
	assert new_quiz.title == title
	assert hasattr(new_quiz, 'course_id')
	assert new_quiz.course_id == self.course.id
```

Take a look at the existing tests to get a feel for the process. Once you've written a few, it should be second nature.

##### Engine tests

Not all of PyCanvas relies on networking. While these pieces are few and far between, we still need to verify that they're performing correctly. Writing tests for engine-level code is just as important as user-facing code and is a bit easier. You'll just need to follow the same process as you would for API tests, minus the fixtures.

#### Running tests / coverage reports

Once you've written test case(s) for your issue, you'll need to run the test to verify that your changes are passing and haven't interfered with any other part of the library.

You'll do this by running `coverage run -m unittest discover` from the main `pycanvas` directory. If your tests pass, you're ready to run a coverage report!

Coverage reports tell us how much of our code is actually being tested. As of right now, we're happily maintaining 100% code coverage (🎉!) and our goal is to keep it there. Ensure you've covered your changes entirely by running `coverage report`. Your output should look something like this:

```
Name                         Stmts   Miss  Cover
------------------------------------------------
pycanvas/__init__.py            14      0   100%
pycanvas/account.py             83      0   100%
pycanvas/assignment.py          11      0   100%
pycanvas/avatar.py               2      0   100%
pycanvas/canvas.py              60      0   100%
pycanvas/canvas_object.py       20      0   100%
pycanvas/course.py             126      0   100%
pycanvas/enrollment.py           2      0   100%
pycanvas/exceptions.py          10      0   100%
pycanvas/external_tool.py       33      0   100%
pycanvas/module.py              62      0   100%
pycanvas/page_view.py            4      0   100%
pycanvas/paginated_list.py      66      0   100%
pycanvas/quiz.py                15      0   100%
pycanvas/requester.py           42      0   100%
pycanvas/section.py              9      0   100%
pycanvas/user.py                48      0   100%
pycanvas/util.py                22      0   100%
------------------------------------------------
TOTAL                          629      0   100%
```

Certain statements can be omitted from the coverage report by adding `# pragma: no cover` but this should be used conservatively. If your tests pass and your coverage is at 100%, you're ready to [submit a pull request](https://***REMOVED***/pycanvas/merge_requests)! 

Be sure to include the issue number in the title with a pound sign in front of it (#123) so we know which issue the code is addressing. Point the branch at master and then submit it for review.


## Code Style Guidelines

We try to adhere to Python's [PEP 8](https://www.python.org/dev/peps/pep-0008/) specification as much as possible. In short, that means:

* We use four spaces for indentation.
* All Python files end with an empty new line.
* Two spaces before a class declaration, one space before a function declaration.
* Lines should be around 80 characters long. Once you get into the 85+ territory, consider breaking your code into separate lines.

It's a good idea to set up a Python linter for your text editor to point out errors.

### Foolish consistency

> A foolish consistency is the hobgoblin of little minds. -- Ralph Waldo Emerson

An important tenet of PEP8 is to not get hung up on PEP8. While we try to be as PEP8 compliant as possible, maintaining the consistency of the project is more important than modifying an existing style choice.

Below you'll find several established styles that'll help you along the way.

### Method docstrings
Method docstrings should include a description, a link to the related API endpoint (if available), parameter name, parameter description, and parameter type, return description (if available), and return type. They should be included in the following order:

#### Descriptions
A description should be a concise, *action* statement (use "*write* a good docstring" over "*writes* a good docstring") that describes the method. Generally, the official API documentation's description is usable (make sure it's an **action statement** though). Special functionality should be documented. 

#### Links to related API endpoints
A link to a related API endpoint is denoted with `:calls:`. PyCanvas uses Sphinx to automatically generate documentation, so we can provide a link to an API endpoint with the reStructuredText syntax:

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

```
def uncheck_box(box_id):
	"""
	Uncheck the box with the given ID.
	
	:returns: True if the box was successfully unchecked, False otherwise.
	:rtype: bool
	"""
```

In most cases, the return value is easy to infer based on the type and the description given in the docstring. Only use `:returns:` to clarify ambiguous cases (usually relating to boolean returns).

**Return type** should always be included when a value is returned. If it's not a primitive type (int, str, bool, list, etc.) a fully-qualified class name should be included:

```
:rtype: :class:`pycanvas.user.User`
```

In the event a PaginatedList is returned:

```
:rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
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
        :rtype: :class:`pycanvas.account.Account`
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

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.Account`
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
