import django

django.setup()
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DropTableSprint.settings')
import unittest
from django.test import TestCase
from TAScheduler.classes.Courses import CoursesClass
from TAScheduler.models import Course, MyUser

class testPositive(TestCase):
    def setUp(self):
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

    def test_removeFromCourse(self):
        CoursesClass.unassignInstructor(self, "479")
        things = Course.objects.get(courseCode="479")
        self.assertEqual(things.instructorID, None)


class testNegative(TestCase):
    def setUp(self):
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
                       role="TA",
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

    def test_NoInstructorFound(self):
        # testNegative.setUp(self)
        with self.assertRaises(Exception, msg="No Instructor to remove"):
            CoursesClass.unassignInstructor(self, "351")

    def testNotEnoughElements(self):
        # testNegative.setUp(self)
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            CoursesClass.unassignInstructor("479")

    def testTooManyElements(self):
        # testNegative.setUp(self)
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            CoursesClass.unassignInstructor(self, "479", "error")
