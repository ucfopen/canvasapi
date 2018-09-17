# Import the Canvas class
import csv
from pprint import pprint
from canvasapi import Canvas

# Canvas API URL for your school:
API_URL = "https://auburn.instructure.com"

# Canvas API key
API_KEY = open(".canvas.txt").read().strip()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Specify the course ID for the course you wish to work on.
course_id = 1113938

# Assignment Group ID
assignment_group_id = 1401937 # Reading

# Create course object
course = canvas.get_course(course_id)

# In this example, I am going to iterate through a spreadsheet and create reading assignments. In this spreadsheet,
# the first column is a number and the second column contains the page numbers students have to read. Please see the
# official canvas api documentation for all the fields in an assignment that you can set.

for row in csv.reader(open('reading_assignments.tsv').readlines(), delimiter='\t'):
    pprint(row)
    reading_num = row[0]
    pages = row[1]
    description = """Please read the following pages in your textbook: %s""" % pages
    assignment = {
        "name": "Reading Assignment %s" % reading_num,
        # The next three items are left commented out. I usually set those when creating homeworks or other types of
        # assignments
        # "submission_types": "online_upload",
        # "allowed_extensions": ["pdf"],
        # "points_possible": 100,
        "points_possible": 0,
        "description": description,
        "assignment_group_id": assignment_group_id,  # Reading Assignments Group
        "published": False  # Set to True if you're confident things will work, else your students will see your
        # mess-up.
        }
    my_assignment = course.create_assignment(assignment)



