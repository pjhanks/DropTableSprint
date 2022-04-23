from .models import MyUser, TA, Course, Sections, ClassTAAssignments
class Users():
  
  def createUser(self, IDnumber, name, address, email, phoneNumber, role, password):
    check = list(map(str, MyUser.objects.filter(ID=IDnumber)))
    if len(check)==0:
      raise Exception("Database already contains someone with that ID")
    else:
      temp = MyUser(IDnumber, name, address, email, phoneNumber, role, password)
      temp.save()

  def createTA(self, TACode, TAID):
    check = list(map(str, TA.objects.filter(ID=TACode)))
    if len(check)==0:
      raise Exception("Database already contains a TA with that ID")
    elif type(TACode) != str or type(TAID) != str:
      raise Exception("A non-string value was passed in createTA!")
    else:
      temp = TA(TACode)
      temp.save()

  def createCourse(self, courseCode, instructorID, TAs, courseNumber):
    check = list(map(str, Course.objects.filter(ID=courseCode)))
    if len(check)==0:
      raise Exception("Database already contains a course with that ID")
    elif type(courseCode) != str or type(instructorID) != str or type(TAs != str) or type(courseNumber) != str:
      raise Exception("A non-string value was passed in createCourse!")
    else:
      temp = Course(courseCode, instructorID, TAs, courseNumber)
      temp.save()

  def createSections(self, sectionCode, parentCode, TA):
    check = list(map(str, Sections.objects.filter(ID=sectionCode)))
    if len(check)==0:
      raise Exception("Database already contains a section with that ID")
    else:
      temp = Sections(sectionCode, parentCode, TA)
      temp.save()

  def createClassTAAssignments(self, AssignmentsID, courseCode, TAID):
    check = list(map(str, Sections.objects.filter(ID=AssignmentsID)))
    if len(check) == 0:
      raise Exception("Database already contains a classTAAssignment with that ID")
    else:
      temp = Sections(AssignmentsID, courseCode, TAID)
      temp.save()
