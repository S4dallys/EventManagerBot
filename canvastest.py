from canvasapi import Canvas
from replit import db

canvas = Canvas("https://dlsu.instructure.com/",
                db["canvas_tokens"]["Sand#0392"])

user = canvas.get_current_user()

courses = user.get_courses(enrollment_state="active")

course = courses[2]

hws = user.get_assignments(course)

hw = course.get_assignment(hws[0], include=['can_submit', 'submission'])

# print(hw.submission)
print(course.name)
print(hw.name)
print(hw.can_submit)
print(hw.submission)
