import django
django.setup()
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DropTableSprint.settings')
import unittest
from django.test import TestCase
from TAScheduler.classes.Instructors import InstructorsClass
from TAScheduler.models import MyUser


class testPositive(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Bob",
                      address="879 place",
                      email="bob@uwm.edu",
                      phoneNumber="182354231",
                      role="Instructor",
                      password="123")
        temp.save()

    def test_addInstructor(self):
        InstructorsClass.createUser("2", "Tom", "462 place", "tom@uwm.edu", "18272345012", "Instructor", "124")
        things = MyUser.objects.get(IDNUMBER="2")
        self.assertIn("2", things.IDNumber, "Item was not added to list")

class testNegative(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Bob",
                      address="879 place",
                      email="bob@uwm.edu",
                      phoneNumber="182354231",
                      role="Instructor",
                      password="123")
        temp.save()

    def test_badID(self):
        # same ids
        with self.assertRaises(Exception, msg="There is already a user with that ID"):
            InstructorsClass.createInstructor(self,"1", "James", "125 park place", "alex@uwm.edu", "18000000002", "Instructor", "123")
        #things = list(map(str, MyUser.objects.filter(name="James")))
        #self.assertIn("2", things, "Item was improperly added to list")

    def test_toManyFields(self):
        # too many fields
        with self.assertRaises(Exception, msg="Should not accept that many fields"):
            InstructorsClass.createInstructor(self,"1", "Bob", "879 place", "bob@uwm.edu", "182354231", "Instructor", "error",
                                 "123")

    def test_toLittleFields(self):
        # too few fields
        with self.assertRaises(Exception, msg="Should not accept that few fields"):
            InstructorsClass.createInstructor(self,"1", "Bob", "bob@uwm.edu", "182354231", "Instructor", "123")

    def test_intPhone(self):
        # non string
        with self.assertRaises(Exception, msg="You must pass a str value!"):
            InstructorsClass.createInstructor(self, "1", "Bob", "879 place", "bob@uwm.edu", 182354231, "Instructor", "123")
        #things = list(map(str, MyUser.objects.filter(name="James")))
        #self.assertIn("3", things, "Item was improperly added to list")