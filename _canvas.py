# from setup import Student
from dateutil import parser
import datetime as dt
import pytz
import re

# create timezone obj
tz = pytz.timezone("Hongkong")


# get range using dt
def getRange(range):
  return (dt.datetime.today().astimezone(tz),
          dt.datetime.today().astimezone(tz) + dt.timedelta(int(range)))


# iso string -> readable dt object
def getReadableDate(date):
  try:
    d = parser.isoparse(date).astimezone(tz)
    return dt.datetime.strftime(d, "%m/%d/%y, %-H:%M")
  except:
    return None


# id -> html link for courses
def getCourseLink(courseId):
  return "https://dlsu.instructure.com/courses/{link}".format(link=courseId)


# get assignment in range
def getAssignments(user, courseCode, dateRange):
  courses = [c for c in user.courses if courseCode.upper() in c.name.upper()]

  if len(courses) == 0:
    raise NameError

  validAssignments = {"course": courses[0], "hws": [], "hws_no_due": []}

  for hw in user.get_assignments(courses[0]):
    try:
      _dateRange = getRange(dateRange)
      date = parser.isoparse(hw.due_at).astimezone(tz)
      if _dateRange[0] <= date <= _dateRange[1]:
        validAssignments["hws"].append(hw)
    except:
      validAssignments["hws_no_due"].append(hw)

  if not len(validAssignments["hws"]) and not len(
      validAssignments["hws_no_due"]):
    return None

  def sortByDue(hw):
    return hw.due_at

  validAssignments["hws"].sort(key=sortByDue)

  return validAssignments


# return string form of assignments
def printAssignments(user, courseCode, dateRange, dated):
  try:
    assignments = getAssignments(user, courseCode, dateRange)
  except NameError:
    return 0

  if assignments == None:
    return None

  if dated != "-U":
    assignments["hws_no_due"] = []
    if len(assignments["hws"]) == 0:
      return None
    

  returnList = [
    f"---------\n**Course: {assignments['course'].course_code} **",
    f"({getCourseLink(assignments['course'].id)})\n"
  ]
  for hw in assignments["hws"]:
    hwString = [
      f"**{hw.name}**", f"Due: {getReadableDate(hw.due_at)}",
      f"Lock: {getReadableDate(hw.lock_at)}", f"Link: {hw.html_url}\n"
    ]
    for s in hwString:
      returnList.append(s)

  for hw in assignments["hws_no_due"]:
    hwString = [
      f"**{hw.name}**", "Due: Undated", f"Link: {hw.html_url}\n"
    ]
    for s in hwString:
      returnList.append(s)

  return "\n".join(returnList)

def getAssignmentDetailed(user, courseCode, hw):
  try:
    hws = getAssignments(user, courseCode, None)
  except NameError:
    return "Failed. Course not found."

  if hws == None:
    return "Could not find assignment."

  for _hw in hws["hws_no_due"]:
    if hw.upper() in _hw.name.upper():
      if getReadableDate(_hw.due_at) == None or parser.isoparse(
          _hw.due_at).astimezone(tz) >= dt.datetime.today().astimezone(tz):
        try:
          desc = _hw.description
          pattern = re.compile('<.*?>')
          result = re.sub(pattern, '', desc)
          result = re.sub("&nbsp;", '', result)
        except TypeError:
          result = "Assignment locked. Cannot view description."

        if result == "":
          result = "No description."

        return "\n".join([
          f"**{_hw.name}**", f"Link: {_hw.html_url}",
          f"Course: {hws['course'].course_code}", f"Submission types: {', '.join(_hw.submission_types)}", f"Description: {result}"
        ])

  return "Assignment not found :("
