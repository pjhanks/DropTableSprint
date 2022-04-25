from .models import Course, MyUser


class CoursesClass():

    def createCourseTeacher(self, CourseCode, instructorID, CourseNumber):
        if (CourseCode is None):
            raise Exception("does not accept null Primary keys")
        check = list(map(str, Course.objects.filter(courseCode=CourseCode)))
        checkInstructor = list(map(str, MyUser.objects.filter(ID=instructorID)))
        if len(checkInstructor) > 0:
            raise Exception("No such parent course")
        if len(check) > 0:
            raise Exception("Database already contains am course with that ID")
        else:
            temp = Course(CourseCode, instructorID, CourseNumber)
            temp.save()

    def createCourse(self, CourseCode, CourseNumber):
        if (CourseCode is None):
            raise Exception("does not accept null Primary keys")
        check = list(map(str, Course.objects.filter(courseCode=CourseCode)))
        if len(check) > 0:
            raise Exception("Database already contains am course with that ID")
        else:
            temp = Course(CourseCode, None, CourseNumber)
            temp.save()
    def assignInstructor(self, CourseCode, InstructorID):
        toUpdate = Course.objects.get(courseCode=CourseCode)
        toUpdate.instructorID=InstructorID
        toUpdate.save()