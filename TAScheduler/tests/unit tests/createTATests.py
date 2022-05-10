import unittest
import Users
from django.test import TestCase
from TAScheduler.models import TA


class testTA(TestCase):
    TAList = None

    def setUp(self):
        temp = TA(ID="1",
                  TAID="7")
        temp.save()

        temp = TA(ID="2",
                  TAID="11")
        temp.save()


    def test_addTA(self):
        # add Something.addTA("TAcode");

        Users.createTA("3", "8")
        things = list(map(str, TA.objects.filter(TAID="8")))
        self.assertIn("3", things, "TA was not added to list")

    def test_intID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createTA must be strings!"):
            Users.createTA(3, "8")

    def test_floatID(self):
        # non string
        with self.assertRaises(TypeError, msg="The values passed to createTA must be strings!"):
            Users.createTA(3.0, "8")

    def test_badID(self):
        # same ids
        Users.createTA("2", "42")
        things = list(map(str, TA.objects.filter(name="2")))
        self.assertIn("2", things, "TA was improperly added to list")

    def test_toManyFields(self):
        with self.assertRaises(TypeError, msg="Too many arguments passed for createTA!"):
            Users.createTA("3", "7", "park place")

    def test_toLittleFields(self):
        with self.assertRaises(TypeError, msg="Not enough arguments passed for createTA!"):
            Users.createTA("3")
