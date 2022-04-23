import unittest
import Users
from django.test import TestCase
from .models import MyUser


class testPositive(TestCase):
    userList = None

    def setUp(self):
        temp = MyUser(ID="1",
                      name="Fred",
                      address="123 park place",
                      email="fred@uwm.edu",
                      phoneNumber="18000000000",
                      role="Administrator")
        temp.save
        temp = MyUser(ID="2",
                      name="Alex",
                      address="124 park place",
                      email="alex@uwm.edu",
                      phoneNumber="18000000001",
                      role="TA")
        temp.save
        #fill test database with the things in thingList

    def test_addUser(self):
        #add Something.addUser("user info");
        
        Users.createUser("3", "James", "125 park place", "alex@uwm.edu", "18000000002","Instructor")
        things = list(map(str, MyUser.objects.filter(name="James")))
        self.assertIn("3",things,"Item was not added to list")

    def test_intPhone(self):
      
      #non string
      Users.createUser("3", "James", "125 park place", "alex@uwm.edu", 18000000002,"Instructor")
      things = list(map(str, MyUser.objects.filter(name="James")))
      self.assertIn("3",things,"Item was improperly added to list")

    def test_badID(self):
      #same ids
      Users.createUser("2", "James", "125 park place", "alex@uwm.edu", "18000000002","Instructor")
      things = list(map(str, MyUser.objects.filter(name="James")))
      self.assertIn("2",things,"Item was improperly added to list")
      
    def test_toManyFields(Self):
      Users.createUser("2", "James", "125 park place", "alex@uwm.edu", "18000000002","Instructor","error")


    def test_toLittleFields(Self):
      Users.createUser("2", "James", "alex@uwm.edu", "18000000002","Instructor")
