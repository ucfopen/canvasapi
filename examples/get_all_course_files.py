# Import the Canvas class
import os
import pathlib
import pdfkit

import requests
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://auburn.instructure.com"
# Canvas API key. Replace this with a file with your own key in it.
API_KEY = open(".canvas.txt").read().strip()

# Create a download directory, dl, to place all content in.
if not os.path.exists('dl'):
    os.mkdir('dl')

os.chdir('dl')


def download_files(my_obj, destination_folder_name='./'):
    for folder_name in my_obj.get_folders():
        os.mkdir(os.path.join(destination_folder_name, folder_name.name))
        for filename in folder_name.get_files():
            print("Downloading", filename)
            filename.download(location=os.path.join(destination_folder_name, folder_name.name, filename.filename))


def download_assignments_and_submissions(my_course, my_user_id='1064433'):
    print("Getting assignment submissions for", my_course.name)
    for assignment_info in my_course.get_assignments():
        assignment_folder_name = assignment_info.name.replace(' ', '_')
        dir_path = os.path.join('Assignments', assignment_folder_name)
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
        # Download Assignment Details
        print(assignment_info.description)
        if assignment_info.description:
            pdfkit.from_string(assignment_info.description, os.path.join(dir_path, str(assignment_info.name) + '.pdf'))
        try:
            for attachment in assignment_info.get_submission(my_user_id).attachments:
                with open(os.path.join(dir_path, attachment['filename']),
                          'wb') as fh:
                    print("Downloading", attachment['url'])
                    r = requests.get(attachment['url'])
                    if r.status_code == 200:
                        file_data = r.content
                        fh.write(file_data)
                    else:
                        print("Failed to download!")

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    # Get my own user identifier in Canvas to pull personal submissions.
    user_id = canvas.get_current_user().id

    # The course ID can be found in the URL on the course page on Canvas or by running canvas.get_courses()
    # course_id = '344017' # Mobile Robots Fall 2012
    course_id = '1115873'  # Mobile Robots Summer 2018
    course = canvas.get_course(course_id)

    course_folder_name = course.name.replace(' ', '_')
    pathlib.Path(course_folder_name).mkdir(parents=True, exist_ok=True)
    os.chdir(course_folder_name)
    download_assignments_and_submissions(course)
    download_files(course)
