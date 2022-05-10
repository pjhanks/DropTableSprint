import unittest
import Users
from django.test import TestCase
from .models import Course


class testCourse(TestCase):
    CourseList = None

    def setUp(self):
        temp = Course(ID="1",
                      instructorID="7",
                      TAs="39",
                      courseNumber="101")
        temp.save()

        temp = Course(ID="2",
                      instructorID="8",
                      TAs="32",
                      courseNumber="345")
        temp.save()


    def test_addCourse(self):
        # add Something.addCourse("courseCode");
        Users.createCourse("3", "9", "44", "212")
        things = list(map(str, Course.objects.filter(instructor="9")))
        self.assertIn("3", things, "Course was not added to list")

    def test_intID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createCourse must be strings!"):
            Users.createCourse(3, "9", "44", "212")

    def test_floatID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createCourse must be strings!"):
            Users.createCourse(3.0, "9", "44", "212")

    def test_badID(self):
        # same ids
        Users.createCousre("2", "9", "42", "313")
        things = list(map(str, Course.objects.filter(name="2")))
        self.assertIn("2", things, "Course was improperly added to list")

    def test_toManyFields(self):
        with self.assertRaises(TypeError, msg="Too many arguments passed for createCourse!"):
            Users.createCourse("3", "9", "44", "212", "oops extra argument")

    def test_toLittleFields(self):
        with self.assertRaises(TypeError, msg="Not enough arguments passed for createCourse!"):
            Users.createCourse("3")
