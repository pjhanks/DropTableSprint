from django.test import TestCase
from TAScheduler.classes import Courses
from TAScheduler.models import MyUser, Course


class positiveTests(TestCase):
    def setup(self):
        temp1 = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp1.save()
        temp2 = MyUser(IDNumber="2",
                      name="John",
                      address="123 park place",
                      email="john@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp2.save()
        temp = Course(courseCode="351",
                      instructorID=None,
                      courseNumber="101")
        temp.save()
        temp = Course(courseCode="479",
                      instructorID=temp2,
                      courseNumber="315")
        temp.save()

    def test_NonetoSome(self):
        Courses.CoursesClass.assignInstructor(self, "351", "1")
        checkCourse = Course.objects.get(courseCode="351")
        self.assertEqual(checkCourse.instructorID, "1")

    def testSomeToSome(self):
        Courses.CoursesClass.assignInstructor(self, "2", "2")
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual(checkCourse.instructorID, "2")


class negativeTests(TestCase):
    def setup(self):
        temp1 = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp1.save()
        temp2 = MyUser(IDNumber="2",
                      name="John",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp2.save()
        temp = Course(courseCode="351",
                      instructorID=None,
                      courseNumber="101")
        temp.save()
        temp = Course(courseCode="479",
                      instructorID=temp2,
                      courseNumber="315")
        temp.save()

    def testNotInstructor(self):
        Courses.CoursesClass.assignInstructor(self, "2", "2")
        checkCourse = Course.objects.get(courseCode="1")
        self.assertNotEqual(checkCourse.instructorID, "2")

    def testNotEnoughElements(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            Courses.CoursesClass.assignInstructor("2")

    def testTooManyElements(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            Courses.CoursesClass.assignInstructor(self, "2", "2", "error")
