import unittest

import TAScheduler.classes.Courses
from TAScheduler.classes import Users
from django.test import TestCase
from TAScheduler.models import ClassTAAssignments, Course, MyUser


class testClassTAAssignments(TestCase):
    ClassTAList = None

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

        course8 = Course(courseCode="8",
                      instructorID=temp1,
                      courseNumber="101")
        temp.save()
        course7 = Course(courseCode="7",
                      instructorID=temp2,
                      courseNumber="315")
        course7.save()

        ta39 = MyUser(IDNumber="39",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="TA",
                      password="1234")
        ta39.save()

        ta32 = MyUser(IDNumber="32",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="TA",
                      password="1234")
        ta32.save()



        temp = ClassTAAssignments(AssignmentsID="1",
                      courseCode=course7,
                      TAcode=ta39)
        temp.save()

        temp = ClassTAAssignments(AssignmentsID="2",
                      courseCode=course8,
                      TAcode=ta32)
        temp.save()

    def test_addClassTA(self):
        # add Something.addClassTA("AssignmentsID");
        TAScheduler.classes.Courses.CoursesClass.assignTA(self,"9","39")
        things = ClassTAAssignments.objects.filter(courseCode="9")
        self.assertIn("3", things[0], "Class TA Assignment was not added to list")

    def test_intID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createClassTAAssignments must be strings!"):
            Users.UserClass.createClassTAAssignments(3, "9", "44")

    def test_floatID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createClassTAAssignments must be strings!"):
            Users.UserClass.createClassTAAssignments(3.0, "9", "44")

    def test_badID(self):
        # same ids
        Users.UserClass.createClassTAAssignments("2", "9", "42")
        things = list(map(str, ClassTAAssignments.objects.filter(name="2")))
        self.assertIn("2", things, "Class TA Assignment was improperly added to list")

    def test_toManyFields(self):
        with self.assertRaises(TypeError, msg="Too many arguments passed for createClassTAAssignments!"):
            Users.UserClass.createClassTAAssignments("3", "9", "44", "oops extra argument")

    def test_toLittleFields(self):
        with self.assertRaises(TypeError, msg="Not enough arguments passed for createClassTAAssignments!"):
            Users.UserClass.createClassTAAssignments("3")
