import unittest
import Users
from django.test import TestCase
from TAScheduler.models import ClassTAAssignments


class testClassTAAssignments(TestCase):
    ClassTAList = None

    def setUp(self):
        temp = ClassTAAssignments(ID="1",
                      courseCode="7",
                      TAcode="39")
        temp.save()

        temp = ClassTAAssignments(ID="2",
                      courseCode="8",
                      TAcode="32")
        temp.save()

    def test_addClassTA(self):
        # add Something.addClassTA("AssignmentsID");
        Users.createClassTAAssignments("3", "9", "44")
        things = list(map(str, ClassTAAssignments.objects.filter(courseCode="9")))
        self.assertIn("3", things, "Class TA Assignment was not added to list")

    def test_intID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createClassTAAssignments must be strings!"):
            Users.createClassTAAssignments(3, "9", "44")

    def test_floatID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createClassTAAssignments must be strings!"):
            Users.createClassTAAssignments(3.0, "9", "44")

    def test_badID(self):
        # same ids
        Users.createClassTAAssignments("2", "9", "42")
        things = list(map(str, ClassTAAssignments.objects.filter(name="2")))
        self.assertIn("2", things, "Class TA Assignment was improperly added to list")

    def test_toManyFields(self):
        with self.assertRaises(TypeError, msg="Too many arguments passed for createClassTAAssignments!"):
            Users.createClassTAAssignments("3", "9", "44", "oops extra argument")

    def test_toLittleFields(self):
        with self.assertRaises(TypeError, msg="Not enough arguments passed for createClassTAAssignments!"):
            Users.createClassTAAssignments("3")
