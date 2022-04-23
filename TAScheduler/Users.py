from .models import MyUser, TA, Course, Sections, ClassTAAssignments
class Users():
  
  def createUser(self, IDnumber, name, address, email, phoneNumber, role, password):
    check = list(map(str, MyUser.objects.filter(ID=IDnumber)))
    if len(check)==0:
      raise Exception("Database already contains someone with that ID")
    else:
      temp = MyUser(IDnumber, name, address, email, phoneNumber, role, password)
      temp.save()

  def createTA(self, TACode):
    check = list(map(str, TA.objects.filter(ID=TACode)))
    if len(check)==0:
      raise Exception("Database already contains a TA with that ID")
    else:
      temp = TA(TACode)
      temp.save()

  def createCourse(self, courseCode, instructorID, TAs, courseNumber):
    check = list(map(str, Course.objects.filter(ID=courseCode)))
    if len(check)==0:
      raise Exception("Database already contains a course with that ID")
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
