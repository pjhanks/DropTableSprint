from django.test import TestCase

import TAScheduler.classes.Users
from TAScheduler.models import MyUser


class positiveTests(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp.save()
    def test_changeAll(self):
        TAScheduler.classes.Users.UserClass.changeInfo("1","Fry","123 park", "fred5@uwm.edu", "17000000000","1235")
        Check=MyUser.objects.filter(IDNumber="1")
        Check=Check[0]
        self.assertEqual(Check.address,"123 park")
    def test_ChangeSome(self):
        TAScheduler.classes.Users.UserClass.changeInfo("1","Fred", None, "fred5@uwm.edu", "17000000000","")
        Check = MyUser.objects.filter(IDNumber="1")
        Check = Check[0]
        self.assertEqual(Check.name, "Fred")
        self.assertEqual(Check.address, "123 park")
        self.assertEqual(Check.password, "1235")

class negativeTests(TestCase):
    def setUp(self):
        temp = MyUser(IDNumber="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Instructor",
                      password="1234")
        temp.save()

    def test_tooManyArguments(self):
        with self.assertRaises(TypeError, msg="Should not accept that many fields"):
            TAScheduler.classes.Users.UserClass.changeInfo("1","Fred", "None", "fred5@uwm.edu", "17000000000","1234", "error")

    def test_tooFewArguments(self):
        with self.assertRaises(TypeError, msg="Should not accept that few fields"):
            TAScheduler.classes.Users.UserClass.changeInfo("1","Fred", "None", "fred5@uwm.edu", "17000000000")

    def test_nonExistingUser(self):
        with self.assertRaises(RuntimeError, msg="Should not accept invalid ID"):
            TAScheduler.classes.Users.UserClass.changeInfo("3","Fred", "None", "fred5@uwm.edu", "17000000000","1234")
