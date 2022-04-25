from .models import Course, MyUser


class CoursesClass():

    def createCourse(self, CourseCode, instructorID, CourseNumber):
        if (CourseCode is None):
            raise Exception("does not accept null Primary keys")
        check = list(map(str, Course.objects.filter(courseCode=CourseCode)))
        checkInstructor = MyUser.objects.filter(IDNumber=instructorID)
        if (checkInstructor.count()) == 0:
            raise Exception("No such parent course")
        if len(check) > 0:
            raise Exception("Database already contains am course with that ID")
        else:
            x = MyUser.objects.get(IDNumber=instructorID)
            temp = Course(courseCode=CourseCode, instructorID=x, courseNumber=CourseNumber)
            temp.save()

    def createCourse2(self, CourseCode, CourseNumber):
        if (CourseCode is None):
            raise Exception("does not accept null Primary keys")
        check = list(map(str, Course.objects.filter(courseCode=CourseCode)))
        if len(check) > 0:
            raise Exception("Database already contains am course with that ID")
        else:
            temp = Course(courseCode=CourseCode, instructorID=None, courseNumber=CourseNumber)
            temp.save()
