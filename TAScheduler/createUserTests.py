import django
import unittest
from django.test import TestCase
from TAScheduler.Users import UserClass
from TAScheduler.models import MyUser


class testPositive(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Administrator",
                      password="123")
        temp.save
        temp.save()
        temp = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        temp.save
        temp.save()

    def test_addUser(self):
        # add Something.addUser("user info");
        UserClass.createUser(self, "3", "James", "125 park place", "alex@uwm.edu", "18000000002", "Instructor", "123")
        things = MyUser.objects.get(name="James")
        self.assertIn("3", things.IDNumber, "Item was not added to list")

    def test_intPhone(self):
        # non string
        UserClass.createUser(self, "3", "James", "125 park place", "alex@uwm.edu", 18000000002, "Instructor", "123")
        things = list(map(str, MyUser.objects.filter(name="James")))
        self.assertIn("3", things, "Item was improperly added to list")


class testNegative(TestCase):
    def setup(self):
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Administrator",
                      password="123")
        temp.save
        temp.save()
        temp = MyUser(IDNumber="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA",
                      password="123")
        temp.save
        temp.save()

    def test_badID(self):
        # same ids
        UserClass.createUser(self,"2", "James", "125 park place", "alex@uwm.edu", "18000000002", "Instructor", "123")
        things = list(map(str, MyUser.objects.filter(name="James")))
        self.assertIn("2", things, "Item was improperly added to list")

    def test_toManyFields(self):
        # too many fields
        with self.assertRaises(ValueError, msg="Should not accept that many fields"):
            UserClass.createUser(self,"2", "Alex", "125 park place", "alex@uwm.edu", "18000000002", "Instructor", "error",
                                 "123")

    def test_toLittleFields(self):
        # too few fields
        with self.assertRaises(ValueError, msg="Should not accept that few fields"):
            UserClass.createUser(self,"2", "Alex", "alex@uwm.edu", "18000000002", "Instructor", "123")