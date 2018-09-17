# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://auburn.instructure.com"

# Canvas API key
API_KEY = open(".canvas.txt").read().strip()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

course_id = 1113938
course = canvas.get_course(course_id)


# See assignment groups and what their codes are. Modify code to update with specific group you need to put
# assignments in.
assignment_group_names = [x for x in course.get_assignment_groups()]
for assignment_group in assignment_group_names:
    print(assignment_group)


