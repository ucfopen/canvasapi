# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://auburn.instructure.com"
# Canvas API key
API_KEY = open("/Users/kreitzem/iCloud/code/organize/api-keys/canvas.txt").read().strip()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

course_id = 1113938
course = canvas.get_course(course_id)


# See assignment groups and what their codes are. Modify code to update with specific group you need to put
# assignments in.
assignment_infos = [x for x in course.get_assignments()]
for assignment_info in assignment_infos:
    print assignment_info


