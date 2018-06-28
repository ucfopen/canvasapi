# Import the Canvas class
from canvasapi import Canvas, upload
from pprint import pprint
# Canvas API URL
API_URL = "https://auburn.instructure.com"
# Canvas API key
API_KEY = open("/Users/kreitzem/iCloud/code/organize/api-keys/canvas.txt").read().strip()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course_id = 1113938
course = canvas.get_course(course_id)
fh = open('/Users/kreitzem/Library/Mobile Documents/com~apple~CloudDocs/code/github/School/Teaching/Analog Electronics/homework problems/HW10v2simpleGenCEamp.pdf')

hw_folder = [x for x in course.get_folders() if x.id == 5816809][0]
hw_folder.upload(fh)


