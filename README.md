# PyCanvas
PyCanvas is a Python package that allows for simple access to the Instructure Canvas API.

## Installation
(TODO)

## Getting Started
The first thing to do is open a connection with Canvas. You will need to provide the URL for the API endpoint of your Canvas instance as well as a valid API key.
```python
from pycanvas import Canvas

api_url = "https://example.com/api/v1/"  # URL of API for your Canvas instance
api_key = "p@$$w0rd g0e$ here"  # Your API key

canvas = Canvas(api_url, api_key)
```

You can now use `canvas` to begin making API calls. Here are some examples:

```python
course = canvas.get_course('1111111')
```

```python
user = canvas.get_user('5555555')
page_views = user.page_views()
```