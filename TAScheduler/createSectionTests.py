import django
django.setup()
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DropTableSprint.settings')
import unittest
from django.test import TestCase
from TAScheduler.Sections import SectionsClass
from TAScheduler.models import Course, MyUser, Sections


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

    def test_addSection(self):
        SectionsClass.createSection(self, "202", "351")
        things = Sections.objects.get(parentCode="351")
        self.assertIn("202", things.sectionCode, "Section was not successfully added")

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

    def test_noSectionCode(self):
        #passes null primary key
        with self.assertRaises(Exception, msg="You can't pass a null Primary key!"):
            SectionsClass.createSection(self, None, "456")

    def test_tooManyFields(self):
        # too many fields
        with self.assertRaises(Exception, msg="Should not accept that many fields"):
            SectionsClass.createSection(self, "102", "304", "506")

    def test_tooLittleFields(self):
        # too few fields
        with self.assertRaises(Exception, msg="Should not accept that few fields"):
            SectionsClass.createSection(self, "105")

    def test_noParentCourse(self):
        with self.assertRaises(Exception, msg="No course exists with that parent code!"):
            SectionsClass.createSection(self, "111", "7000")

    def test_sectionAlreadyExists(self):
        SectionsClass.createSection(self, "202", "351")
        with self.assertRaises(Exception, msg="The course already has a section with that ID"):
            SectionsClass.createSection(self, "202", "351")