import django
django.setup()
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DropTableSprint.settings')
import unittest
from django.test import TestCase
from TAScheduler.Courses import CoursesClass
from TAScheduler.models import Course, MyUser


class testPositive(TestCase):
    def setUp(self):
        temp1 = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Supervisor",
                      password="123")
        temp1.save()
        temp2 = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        temp2.save()
        temp = MyUser(IDNumber="3",
                      name="Bob",
                      address="879 place",
                      email="bob@uwm.edu",
                      phoneNumber="182354231",
                      role="Instructor",
                      password="123")
        temp.save()

        temp = Course(courseCode="351",
                      instructorID=temp1,
                      courseNumber="101")
        temp.save()
        temp = Course(courseCode="479",
                      instructorID=temp2,
                      courseNumber="315")
        temp.save()

    def test_addCourse(self):
        CoursesClass.createCourse(self, "217", "3", "444")
        things = Course.objects.get(courseCode="217")
        self.assertIn("217", things.courseCode, "Course was not successfully added")

    def test_addCourseNoInstructor(self):
        CoursesClass.createCourse2(self, "222", "444")
        things = Course.objects.get(courseCode="222")
        self.assertIn("222", things.courseCode, "Course was not successfully added")

class testNegative(TestCase):
    def setUp(self):
        temp1 = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Supervisor",
                      password="123")
        temp1.save()
        temp2 = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        temp2.save()
        temp = MyUser(IDNumber="3",
                      name="Bob",
                      address="879 place",
                      email="bob@uwm.edu",
                      phoneNumber="182354231",
                      role="Instructor",
                      password="123")
        temp.save()

        temp = Course(courseCode="351",
                      instructorID=temp1,
                      courseNumber="101")
        temp.save()
        temp = Course(courseCode="479",
                      instructorID=temp2,
                      courseNumber="315")
        temp.save()

    def test_noCourseCode(self):
        #passes null primary key
        with self.assertRaises(Exception, msg="You can't pass a null Primary key!"):
            CoursesClass.createCourse(self, None, "3", "456")

    def test_tooManyFields(self):
        # too many fields
        with self.assertRaises(Exception, msg="Should not accept that many fields"):
            CoursesClass.createCourse(self, "102", "3", "111", "222")

    def test_tooLittleFields(self):
        # too few fields
        x = MyUser.objects.get(IDNumber="3")
        with self.assertRaises(Exception, msg="Should not accept that few fields"):
            CoursesClass.createCourse(self, "105", "3")

    def test_noCourseCode_noInstructor(self):
        #passes null primary key
        with self.assertRaises(Exception, msg="You can't pass a null Primary key!"):
            CoursesClass.createCourse2(self, None, "456")

    def test_tooManyFields_noInstructor(self):
        # too many fields
        with self.assertRaises(Exception, msg="Should not accept that many fields"):
            CoursesClass.createCourse2(self, "102", "111", "222")

    def test_tooLittleFields_noInstructor(self):
        # too few fields
        with self.assertRaises(Exception, msg="Should not accept that few fields"):
            CoursesClass.createCourse(self, "105")