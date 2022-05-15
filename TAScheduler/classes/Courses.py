from TAScheduler.models import Course, MyUser, ClassTAAssignments


class CoursesClass():
    def createCourse(self, CourseCode, instructorID, CourseNumber):
        if (CourseCode is None):
            raise Exception("does not accept null Primary keys")
        check = Course.objects.filter(courseCode=CourseCode)
        checkInstructor = MyUser.objects.filter(IDNumber=instructorID)
        if (checkInstructor.count()) == 0:
            raise Exception("No such instructor")
        if check.count() > 0:
            raise Exception("Database already contains a course with that ID")
        else:
            x = MyUser.objects.get(IDNumber=instructorID)
            temp = Course(courseCode=CourseCode, instructorID=x, courseNumber=CourseNumber)
            temp.save()

    def createCourseNoInstructor(self, CourseCode, CourseNumber):
        if (CourseCode is None):
            raise Exception("does not accept null Primary keys")
        check = Course.objects.filter(courseCode=CourseCode)
        if check.count() > 0:
            raise Exception("Database already contains am course with that ID")
        else:
            temp = Course(courseCode=CourseCode, instructorID=None, courseNumber=CourseNumber)
            temp.save()

    def assignInstructor(self, CourseCode, InstructorID):
        toUpdate = Course.objects.get(courseCode=CourseCode)
        toUpdate.instructorID = MyUser.objects.get(IDNumber=InstructorID)
        toUpdate.save()


    def removeInstructor(self, CourseCode):
        toUpdate = Course.objects.get(courseCode=CourseCode)
        #toUpdate.instructorID = MyUser.objects.get(IDNumber=InstructorID)
        toUpdate.instructorID = None
        toUpdate.save()

    def assignTA(self, CourseCode, TAcode):
        courseCode = Course.objects.get(courseCode=CourseCode)
        taCode = MyUser.objects.get(IDNumber=TAcode)
        check = ClassTAAssignments.objects.filter(courseCode=courseCode, TAcode=taCode)
        if check.count()>0:
            raise RuntimeError("That TA is already assigned to that course!")
        else:

            id = ClassTAAssignments.objects.filter(courseCode=CourseCode).count()

            temp = ClassTAAssignments(AssignmentsID=id,courseCode=courseCode, TAcode=taCode)
            temp.save()

    def removeTA(self, CourseCode, TAcode):
        courseCode = Course.objects.get(courseCode=CourseCode)
        try:
            toUpdate = ClassTAAssignments.objects.get(courseCode=courseCode)
        except Exception:
            print("No ClassTAAssignment Object exists")

        if toUpdate.TAcode.IDNumber != TAcode:
            raise RuntimeError("That TA isn't assigned to that course!")
        else:
            toUpdate.delete()
