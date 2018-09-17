# Import the Canvas class
from canvasapi import Canvas, upload
from pprint import pprint
# Canvas API URL
API_URL = "https://auburn.instructure.com"
# Canvas API key
API_KEY = open(".canvas.txt").read().strip()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course_id = 1113938 # Analog Electronics
course = canvas.get_course(course_id)
fh = open('HW10v2simpleGenCEamp.pdf')
target_folder_id = 5816809
hw_folder = [x for x in course.get_folders() if x.id == target_folder_id][0]
print(dir(hw_folder))
hw_folder.upload(fh)


