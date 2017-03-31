# canvasapi
canvasapi is a Python package that allows for simple access to the Instructure Canvas API.

## Installation
`pip install canvasapi`

## Getting Started
The first thing to do is open a connection with Canvas. You will need to provide the URL for the API endpoint of your Canvas instance as well as a valid API key.
```python
from canvasapi import Canvas

api_url = "https://example.com/api/v1/"  # URL of API for your Canvas instance
api_key = "p@$$w0rd"  # Your API key

canvas = Canvas(api_url, api_key)
```

You can now use `canvas` to begin making API calls. Here are some examples:
```python
course = canvas.get_course('1111111')
```

```python
user = canvas.get_user('5555555')
print user.name
```

Some calls will return a `PaginatedList` object instead of a single object.
```python
users = course.get_users()
print users
```

```python
<PaginatedList of type User>
```

This `PaginatedList` object is iterable. However, it doesn't contain any data until called. Calls to the API are made as-needed and results are stored in the object. You can use it like this:

```python
for user in users:
    print user.name
```

You can also use indices:

```python
print users[2].name
```

And even slices!

```python
for user in users[2:]:
	print user.name
```

**Warning**: Presently, there is no way to determine the exact number of records Canvas might return without brute forcing through all the API calls. This means that `PaginatedList` is not aware of it's own length and negative indicies and slices (`users[-1]`, `users[-1:]`, etc.) are not possible at this time.
