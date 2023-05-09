from canvasapi import Canvas, exceptions


# current term id
TERM_ID = 233

# user class
class Student:

  def __init__(self, token):
    self.canvas = Canvas(
  "https://dlsu.instructure.com/",
  token)
    self.user = self.canvas.get_current_user()

    courses = self.user.get_courses()

    # get all courses within term
    courseList = []
    for course in courses:
      try:
        if (course.enrollment_term_id == TERM_ID):
          courseList.append(course)
      except:
        pass

    self.courses = courseList

  def __str__(self):
    return f"This is a user class for {self.user.name}!"

  def details(self):
    return {
      'name': self.user.name,
      'total courses': len(self.courses),
      'courses': [c.course_code for c in self.courses],
      'cur_term': TERM_ID,
    }

  def get_assignments(self, course):
    assignments = self.user.get_assignments(course)
    return [a for a in assignments]
