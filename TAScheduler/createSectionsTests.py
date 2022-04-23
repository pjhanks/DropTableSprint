import unittest
import Users
from django.test import TestCase
from .models import Sections


class testSection(TestCase):
    SectionList = None

    def setUp(self):
        temp = Sections(ID="1",
                      parentCode="7",
                      TA="39")
        temp.save()

        temp = Course(ID="2",
                      parentCode="8",
                      TA="32")
        temp.save()

    def test_addSection(self):
        # add Something.addSection("sectionCode");
        Users.createSection("3", "9", "44")
        things = list(map(str, Sections.objects.filter(parentCode="9")))
        self.assertIn("3", things, "Section was not added to list")

    def test_intID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createSection must be strings!"):
            Users.createSection(3, "9", "44")

    def test_floatID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createCourse must be strings!"):
            Users.createSection(3.0, "9", "44")

    def test_badID(self):
        # same ids
        Users.createSection("2", "9", "42")
        things = list(map(str, Sections.objects.filter(name="2")))
        self.assertIn("2", things, "Section was improperly added to list")

    def test_toManyFields(self):
        with self.assertRaises(TypeError, msg="Too many arguments passed for createSection!"):
            Users.createSection("3", "9", "44", "oops extra argument")

    def test_toLittleFields(self):
        with self.assertRaises(TypeError, msg="Not enough arguments passed for createSection!"):
            Users.createSection("3")
