from TAScheduler.models import Course, MyUser


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

    def unassignInstructor(self, CourseCode):
        if CourseCode is None:
            raise Exception("does not accept full Primary keys")
        check = Course.objects.filter(courseCode=CourseCode)
        if check.count() <= 0:
            raise Exception("Database does not contain course with that ID")
        else:
            temp = Course.objects.get(courseCode=CourseCode)
            if temp.instructorID is None:
                raise Exception("Instructor is already not assigned to Course")
            temp.instructorID = None
            temp.save()
