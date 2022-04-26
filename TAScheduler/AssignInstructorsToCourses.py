from django.test import TestCase
from TAScheduler import Courses
from TAScheduler.models import MyUser,Course

class positiveTests(TestCase):
    def setup(self):
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp.save()
        temp = MyUser(IDNumber="2",
                      name="John",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp.save()
        temp = Course(courseCode="1",
                      instructorID=None,
                      courseNumber="3")
        temp.save()
        temp = Course(courseCode="2",
                      instructorID="1",
                      courseNumber="3")
        temp.save()
    def test_NonetoSome(self):
        Courses.assignInstructor("1","1")
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual(checkCourse.instructorID, "1")
    def testSomeToSome(self):
        Courses.assignInstructor("2", "2")
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual(checkCourse.instructorID, "2")

class negativeTests(TestCase):
    def setup(self):
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp.save()
        temp = MyUser(IDNumber="2",
                      name="John",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="TA",
                      password="1234")
        temp.save()
        temp = Course(courseCode="1",
                      instructorID=None,
                      courseNumber="3")
        temp.save()
        temp = Course(courseCode="2",
                      instructorID="1",
                      courseNumber="3")
        temp.save()
    def testNotInstructor(self):
        Courses.assignInstructor("2", "2")
        checkCourse = Course.objects.get(courseCode="1")
        self.assertNotEqual(checkCourse.instructorID, "2")
    def testNotEnoughElements(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            Courses.assignInstructor("2")
    def testTooManyElements(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
         Courses.assignInstructor("2", "2", "error")