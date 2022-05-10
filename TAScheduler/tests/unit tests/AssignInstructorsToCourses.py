from django.test import TestCase
from TAScheduler.classes import Courses
from TAScheduler.models import MyUser, Course


class positiveTests(TestCase):
    def setUp(self):
        self.myuser = MyUser.objects.create(IDNumber="1",
                                            name="Fred",
                                            address="123 park place",
                                            email="fred@uwm.edu",
                                            phoneNumber="18000000000",
                                            role="Instructor",
                                            password="1234")
        self.myuser.save()

        self.admin = MyUser.objects.create(IDNumber="2",
                                           name="Fred",
                                           address="123 park place",
                                           email="fred@uwm.edu",
                                           phoneNumber="18000000000",
                                           role="Supervisor",
                                           password="1234")
        self.admin.save()

        self.courses = Course.objects.create(courseCode="1",
                                             courseNumber="3")

        self.courses.save()

        self.courses = Course.objects.create(courseCode="2",
                      instructorID=self.myuser,
                      courseNumber="3")
        self.courses.save()

    def test_NonetoSome(self):
        Courses.CoursesClass.assignInstructor(self, "1", "1")
        checkCourse = Course.objects.get(courseCode="1")
        self.assertEqual(checkCourse.instructorID.IDNumber, "1")

    def testSomeToSome(self):
        Courses.CoursesClass.assignInstructor(self, "2", "2")
        checkCourse = Course.objects.get(courseCode="2")
        self.assertEqual(checkCourse.instructorID.IDNumber, "2")


class negativeTests(TestCase):

    def setUp(self):
        self.myuser = MyUser.objects.create(IDNumber="1",
                                            name="Fred",
                                            address="123 park place",
                                            email="fred@uwm.edu",
                                            phoneNumber="18000000000",
                                            role="Instructor",
                                            password="1234")
        self.myuser.save()

        self.admin = MyUser.objects.create(IDNumber="2",
                                           name="Fred",
                                           address="123 park place",
                                           email="fred@uwm.edu",
                                           phoneNumber="18000000000",
                                           role="Supervisor",
                                           password="1234")
        self.admin.save()

        self.courses = Course.objects.create(courseCode="1",
                                             courseNumber="3")

        self.courses.save()

        self.courses = Course.objects.create(courseCode="2",
                                             instructorID=self.myuser,
                                             courseNumber="3")
        self.courses.save()

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
